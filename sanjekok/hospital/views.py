# hospital/views.py

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

import math
from urllib.parse import urlencode

import re
import requests
from django.db.models import Avg, Count

from member.models import Member, Individual
from .models import Hospital  # t_hospital 테이블과 연결된 모델
from reviews.models import Review


# 카카오 주소 검색 API (병원 상세 페이지에서만 사용)
KAKAO_GEOCODE_URL = "https://dapi.kakao.com/v2/local/search/address.json"


# 병원 좌표 캐시 (서버 프로세스가 살아 있는 동안만 유지)
HOSPITAL_COORD_CACHE: dict[int, tuple[float | None, float | None]] = {}


def get_hospital_coords(hospital: Hospital):
    """
    병원별 좌표를 캐싱해서, 같은 병원에 대해 여러 번 카카오 API를 호출하지 않도록 함.
    """
    hid = hospital.id
    if hid in HOSPITAL_COORD_CACHE:
        return HOSPITAL_COORD_CACHE[hid]

    lat, lng = geocode_address(hospital.h_address or "")
    HOSPITAL_COORD_CACHE[hid] = (lat, lng)
    return lat, lng


def geocode_address(address: str):
    """
    카카오 주소 검색 API를 이용해 주소 → (lat, lng) 변환

    지저분한 주소 예:
      - '대전 중구 계백로 1727 (오류동)'
      - '인천광역시 서구 새오개로111번안길 32 2,3층'
      - '경기 화성시 향남읍 발안양감로 187 4,5층 (센트럴프라자)'
      - '경북 안동시 서후면 광평리 211-2'

    처리 전략:
      1) 괄호 안(동/빌딩명 등) 제거
      2) 쉼표(,)를 공백으로 바꾸고
         - '호', '층' 이 들어간 토큰(101호, 3층, 4,5층 등)은 제거
      3) 정리된 문자열로 여러 쿼리를 만들어 순서대로 시도
         - 첫 숫자까지 자른 형태 (도로명 + 건물번호)           → 최우선
         - '시/도/특별시/광역시' 이후만 남긴 형태
         - 전체 cleaned 문자열
         - 괄호 제거 전 main
         - 마지막으로 원본 raw
      4) 숫자에 '-' 가 들어가면(211-2) 지번 앞부분(211)도 추가 시도
    """
    if not address:
        return None, None

    # 0. 공백 정리
    raw = " ".join((address or "").split()).strip()

    # 1. 괄호 앞 부분만 사용
    main = raw.split("(")[0].strip()   # 예: '대전 중구 계백로 1727', '... 187 4,5층'

    # 2. 쉼표를 공백으로 바꾸고, '호' / '층' 들어간 토큰 제거
    tokens = main.replace(",", " ").split()
    cleaned_tokens = []
    for t in tokens:
        if ("호" in t) or ("층" in t):
            # 301호, 3층, 4,5층 등은 지오코딩에 거의 필요 없음
            continue
        cleaned_tokens.append(t.strip())

    cleaned_tokens = [t for t in cleaned_tokens if t]
    cleaned = " ".join(cleaned_tokens)

    queries: list[str] = []

    # 도우미: 리스트에 중복 없이 추가
    def add_query(q: str):
        q = q.strip()
        if q and q not in queries:
            queries.append(q)

    # 숫자 토큰 위치 찾기 (건물번호 후보)
    tokens2 = cleaned.split() if cleaned else []
    num_idxs = [
        i for i, t in enumerate(tokens2)
        if re.fullmatch(r"\d+(?:-\d+)?", t or "")
    ]

    # 3-1. 첫 숫자까지 자른 형태 (도로명 + 건물번호)
    if num_idxs:
        first_num_idx = num_idxs[0]
        trimmed = " ".join(tokens2[: first_num_idx + 1]).strip()
        if trimmed:
            add_query(trimmed)

        # 만약 숫자가 '211-2' 처럼 생겼다면 '211' 도 한 번 더 시도
        num_token = tokens2[first_num_idx]
        if "-" in num_token:
            left = num_token.split("-")[0]
            trimmed_left = " ".join(tokens2[: first_num_idx] + [left])
            add_query(trimmed_left)

    # 3-2. 마지막 시/도/특별시/광역시 이후만 남긴 형태
    if tokens2:
        city_idxs = [
            i for i, t in enumerate(tokens2)
            if ("시" in t or "도" in t or "특별시" in t or "광역시" in t)
        ]
        if city_idxs:
            j = city_idxs[-1]
            city_query_full = " ".join(tokens2[j:]).strip()  # 예: '화성시 향남읍 발안양감로 187'
            add_query(city_query_full)

            # 시/도 이후 + 첫 숫자까지
            if num_idxs and num_idxs[0] >= j:
                city_num = " ".join(tokens2[j: num_idxs[0] + 1])
                add_query(city_num)

    # 3-3. cleaned 전체
    if cleaned:
        add_query(cleaned)

    # 3-4. 괄호 제거 전 main
    if main:
        add_query(main)

    # 3-5. 원본 전체
    add_query(raw)

    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}

    for q in queries:
        try:
            resp = requests.get(
                KAKAO_GEOCODE_URL,
                headers=headers,
                params={"query": q},
                timeout=3,   # 타임아웃 살짝 줄임
            )
            resp.raise_for_status()
            docs = resp.json().get("documents", [])
            if not docs:
                print(f"[geocode_address] no docs for query={q!r} from address={address!r}")
                continue

            first = docs[0]
            lng = float(first["x"])
            lat = float(first["y"])
            # 성공한 쿼리 로그 (원하면 지워도 됨)
            print(f"[geocode_address] OK query={q!r} -> ({lat}, {lng})")
            return lat, lng
        except Exception as e:
            print(f"[geocode_address] error for query={q!r}, address={address!r}: {e}")

    # 모든 후보 실패 시
    print(f"[geocode_address] NO RESULT for address={address!r}")
    return None, None


def calc_distance_km(lat1, lng1, lat2, lng2):
    """
    두 좌표(위도/경도) 사이 거리를 km 단위로 계산 (하버사인 공식)
    """
    if None in (lat1, lng1, lat2, lng2):
        return None

    R = 6371.0  # 지구 반지름 (km)

    rlat1 = math.radians(lat1)
    rlng1 = math.radians(lng1)
    rlat2 = math.radians(lat2)
    rlng2 = math.radians(lng2)

    dlat = rlat2 - rlat1
    dlng = rlng2 - rlng1

    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


# 기준 주소(집/근무지/사고지역) 좌표 캐시
BASE_COORD_CACHE: dict[str, tuple[float | None, float | None]] = {}


def get_base_coords(base_addr: str):
    """
    기준 주소 문자열을 지오코딩 + 캐싱
    """
    if not base_addr:
        return None, None

    key = base_addr.strip()
    if key in BASE_COORD_CACHE:
        return BASE_COORD_CACHE[key]

    lat, lng = geocode_address(key)
    BASE_COORD_CACHE[key] = (lat, lng)
    return lat, lng


def _address_rank(base_addr: str, target_addr: str) -> int:
    """
    문자열 주소 기준으로 '가까움' 등급을 계산.
    0: 같은 시/도 + 같은 구/군 + 같은 읍/면/동
    1: 같은 시/도 + 같은 구/군
    2: 같은 시/도만 같음
    3: 나머지
    """
    if not base_addr or not target_addr:
        return 3

    parts = base_addr.split()
    si = parts[0] if len(parts) >= 1 else ""
    gungu = parts[1] if len(parts) >= 2 else ""
    dong = parts[2] if len(parts) >= 3 else ""

    rank = 3

    if si and si in target_addr:
        rank = 2
        if gungu and gungu in target_addr:
            rank = 1
            if dong and dong in target_addr:
                rank = 0

    return rank


def hospital_search(request):
    """
    병원 검색 화면
    - 세션의 member_id 로 Member 조회
    - 집/근무지/사고목록(여러 건)을 템플릿에 내려보냄
    """
    home_address = ""
    work_address = ""
    accidents_ctx = []   # [{id, title(i_title), address}, ...]

    member_id = request.session.get("member_id")

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)

            # 집 / 근무지 주소
            home_address = member.m_address or ""
            work_address = member.m_jaddress or ""

            # 회원이 속한 업종들의 모든 사고 (최신순)
            industries = member.industries.all()
            accidents = (
                Individual.objects
                .filter(member_industry__in=industries)
                .order_by("-i_accident_date", "-accident_id")
            )

            for acc in accidents:
                accidents_ctx.append({
                    "id": acc.accident_id,
                    "title": acc.i_title,        # 산재제목 필드 그대로 사용
                    "address": acc.i_address or "",
                })

        except Member.DoesNotExist:
            pass

    ctx = {
        "home_address": home_address,
        "work_address": work_address,
        "accidents": accidents_ctx,
    }
    return render(request, "hospital/hospital.html", ctx)


def hospital_api(request):
    """
    기준 주소(addr)와 t_hospital의 h_address 를 이용해
    근처 병원 Top10을 반환.

    - sort=distance : 실제 거리(km) 기준 오름차순
                      (단, 지오코딩은 '문자열 상 가까워 보이는 병원 상위 10개'에만 수행)
    - sort=rating   : 평점 내림차순 (현재는 0.0 placeholder)
    - sort=review   : 리뷰 수 내림차순 (현재는 0 placeholder)
    """
    base_addr = (request.GET.get("addr") or "").strip()  # 집/근무지/사고지역 중 선택된 주소
    sort = request.GET.get("sort", "distance")

    # 기준 주소를 1번만 지오코딩(+캐시)
    base_lat = base_lng = None
    if base_addr:
        base_lat, base_lng = get_base_coords(base_addr)

    # 1단계: 모든 병원에 대해 문자열 주소 랭크 계산 (빠른 연산)
    raw_items = []
    for h in Hospital.objects.all():
        addr = h.h_address or ""
        addr_rank = _address_rank(base_addr, addr)

        raw_items.append({
            "hospital": h,
            "addr": addr,
            "addr_rank": addr_rank,
            # 나중에 채울 필드들
            "distance_km": None,
            "rating": 0.0,
            "review_count": 0,
        })

    # 문자열 기준으로 '가까워 보이는 순' 정렬
    raw_items.sort(key=lambda x: (x["addr_rank"], x["addr"]))
    CANDIDATE_COUNT = 10
    candidates = raw_items[:CANDIDATE_COUNT]

    # 2단계: 후보 병원들에 대해서만 실제 거리 계산 (지오코딩 + 하버사인)
    if sort == "distance" and base_lat is not None and base_lng is not None:
        for item in candidates:
            h = item["hospital"]
            addr = item["addr"]
            if not addr:
                continue

            h_lat, h_lng = get_hospital_coords(h)  # 병원 좌표 캐시 사용
            if h_lat is not None and h_lng is not None:
                d = calc_distance_km(base_lat, base_lng, h_lat, h_lng)
                if d is not None:
                    item["distance_km"] = round(d, 1)

        # 실제 거리 기준 오름차순 정렬 (거리 없으면 맨 뒤)
        def dist_key(item):
            d = item["distance_km"]
            return d if d is not None else 1e9

        candidates.sort(key=dist_key)

    else:
        # 거리순이 아니면 문자열 기준으로만 정렬
        # (추후 rating, review 구현 시 이쪽에 로직 추가)
        candidates.sort(key=lambda x: (x["addr_rank"], x["addr"]))

    # 3단계: 화면에 보여줄 Top10만 추출
    top10 = candidates[:10]

    # 4단계: JSON 응답용 데이터 구성
    result = []
    for item in top10:
        h = item["hospital"]
        addr = item["addr"]

        # 상세 페이지 링크에 기준 주소(base_addr)를 같이 붙인다.
        detail_url = reverse("hospital_detail", args=[h.id])
        if base_addr:
            detail_url = f"{detail_url}?{urlencode({'base_addr': base_addr})}"

        result.append({
            "id": h.id,
            "name": h.h_hospital_name,
            "address": addr,
            "road_address": addr,
            "tel": h.h_phone_number,
            "distance_km": item["distance_km"],  # 실제 거리 (없으면 None)
            "detail_url": detail_url,
        })

    return JsonResponse({"hospitals": result})


def hospital_detail(request, hospital_id: int):
    """
    단일 병원 상세 정보
    - 병원 주소를 지오코딩해서 지도 표시용 lat/lng 전달
      (get_hospital_coords로 캐시 사용)
    - 기준 위치(base_addr)와의 거리(km), 리뷰 평균/개수도 함께 계산
      (기준 주소도 get_base_coords로 캐시 사용)
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)

    # 병원 좌표: 캐시 사용
    lat, lng = get_hospital_coords(hospital)

    # 1) 기준 주소(base_addr) 지오코딩
    #    /hospital/detail/<id>/?base_addr=서울특별시 ... 형태로 넘어온다.
    base_addr = (request.GET.get("base_addr") or "").strip()
    base_lat = base_lng = None
    if base_addr:
        base_lat, base_lng = get_base_coords(base_addr)

    distance_km = None
    if base_lat is not None and base_lng is not None and lat is not None and lng is not None:
        d = calc_distance_km(base_lat, base_lng, lat, lng)
        if d is not None:
            distance_km = round(d, 1)  # 소수점 1자리까지

    # 2) 리뷰 평균 / 개수 집계
    agg = (
        Review.objects
        .filter(hospital=hospital)
        .aggregate(avg_rating=Avg("r_rating"), review_count=Count("id"))
    )
    avg_rating_raw = agg["avg_rating"] or 0
    review_count = agg["review_count"] or 0

    avg_rating = f"{avg_rating_raw:.1f}"  # 예: "4.3"

    context = {
        "KAKAO_KEY": settings.KAKAO_JS_KEY,
        "hospital_id": hospital.id,
        "name": hospital.h_hospital_name,
        "address": hospital.h_address,
        "road_address": hospital.h_address,
        "tel": hospital.h_phone_number,
        "lat": lat,
        "lng": lng,

        # 상단 우측에 쓸 값들
        "distance_km": distance_km,  # 예: 0.8 (실패 시 None)
        "avg_rating": avg_rating,    # 리뷰 평균 (없으면 0.0)
        "review_count": review_count,
    }
    return render(request, "hospital/hospital_detail.html", context)


@require_GET
def hospital_geocode(request):
    """
    필요하다면 사용할 수 있는 지오코딩 API (현재 목록에서는 사용하지 않음).
    """
    query = request.GET.get("query")
    if not query:
        return JsonResponse({"documents": []})

    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}
    params = {"query": query}

    try:
        resp = requests.get(
            KAKAO_GEOCODE_URL, headers=headers, params=params, timeout=5
        )
        resp.raise_for_status()
        return JsonResponse(resp.json())
    except requests.RequestException as e:
        return JsonResponse({"documents": [], "error": str(e)}, status=500)
