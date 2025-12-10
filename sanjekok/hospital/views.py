from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse

import math
import requests
from pyproj import Transformer

from member.models import Member, Individual  # app 이름에 맞게 조정

# SAFEMAP 산재지정의료기관 API
SAFEMAP_HOSPITAL_URL = "http://www.safemap.go.kr/openApiService/data/getInlcmdlcnstData.do"
# 카카오 로컬 API (주소 → 좌표 변환)
KAKAO_GEOCODE_URL = "https://dapi.kakao.com/v2/local/search/address.json"

# TM(EPSG:5179) → WGS84(경위도)
TRANSFORMER = Transformer.from_crs("EPSG:5179", "EPSG:4326", always_xy=True)


def haversine_km(lat1, lng1, lat2, lng2):
    """두 좌표 사이 거리(km) 계산"""
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def geocode_address(address: str):
    """
    카카오 로컬 API를 사용하여 주소를 (lat, lng)로 변환.
    실패 시 (None, None) 반환.
    """
    if not address:
        return None, None

    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}
    params = {"query": address}

    try:
        resp = requests.get(KAKAO_GEOCODE_URL, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        docs = resp.json().get("documents", [])
        if not docs:
            return None, None

        first = docs[0]
        lng = float(first["x"])
        lat = float(first["y"])
        return lat, lng
    except Exception:
        return None, None


def get_current_member(request):
    """
    현재 로그인한 사용자의 Member 레코드 반환.
    m_username == auth.User.username 라고 가정.
    """
    if not request.user.is_authenticated:
        return None

    try:
        return Member.objects.get(m_username=request.user.username)
    except Member.DoesNotExist:
        return None


def get_latest_accident_address(member: Member):
    """
    해당 회원의 가장 최근 사고지역 주소(Individual.i_address) 반환.
    없으면 None.
    """
    accident = (
        Individual.objects
        .filter(member_industry__member=member)
        .order_by("-i_accident_date", "-accident_id")
        .first()
    )
    if accident:
        return accident.i_address
    return None


def _fetch_all_items():
    """
    SAFEMAP 산재지정의료기관 API 호출 → item 리스트 반환
    """
    params = {
        "serviceKey": settings.SAFEMAP_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "type": "json",
    }
    resp = requests.get(SAFEMAP_HOSPITAL_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("body", {}).get("items", {}).get("item", [])
    if isinstance(items, dict):
        items = [items]
    return items


def hospital_search(request):
    """
    산재지정의료기관 리스트 페이지.
    Member 의 집/근무지 주소와 Individual 의 최근 사고지역 주소를
    좌표로 변환하여 템플릿에 넘겨준다.
    """
    member = get_current_member(request)

    home_lat = home_lng = None
    work_lat = work_lng = None
    acc_lat = acc_lng = None

    if member:
        # 집, 근무지
        home_lat, home_lng = geocode_address(member.m_address)
        work_lat, work_lng = geocode_address(member.m_jaddress)

        # 최근 사고지역
        accident_addr = get_latest_accident_address(member)
        acc_lat, acc_lng = geocode_address(accident_addr)

    ctx = {
        "HOME_LAT": home_lat,
        "HOME_LNG": home_lng,
        "WORK_LAT": work_lat,
        "WORK_LNG": work_lng,
        "ACC_LAT": acc_lat,
        "ACC_LNG": acc_lng,
    }
    return render(request, "hospital/hospital.html", ctx)


def hospital_api(request):
    """
    /hospital/api/?lat=..&lng=..&sort=distance|rating|review
    기준 좌표에서 가까운 산재지정의료기관 Top10 반환(JSON)
    """
    try:
        base_lat = float(request.GET.get("lat"))
        base_lng = float(request.GET.get("lng"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "lat, lng 파라미터가 필요합니다."}, status=400)

    sort = request.GET.get("sort", "distance")

    try:
        items = _fetch_all_items()
    except Exception as e:
        return JsonResponse({"error": f"SAFEMAP API 호출 실패: {e}"}, status=500)

    hospitals = []
    for it in items:
        try:
            x = float(it.get("x") or it.get("X"))
            y = float(it.get("y") or it.get("Y"))
        except (TypeError, ValueError):
            continue

        # TM → WGS84
        lng, lat = TRANSFORMER.transform(x, y)
        distance = haversine_km(base_lat, base_lng, lat, lng)

        objt_id = str(it.get("objt_id") or it.get("OBJT_ID") or "")
        name = it.get("fclty_nm") or it.get("FCLTY_NM")
        address = it.get("adres") or it.get("ADRES")
        road_address = it.get("rn_adres") or it.get("RN_ADRES")
        tel = it.get("telno") or it.get("TELNO")

        # 실제 평점/리뷰 데이터를 쓰고 싶으면 여기서 교체
        rating = float(it.get("rating", 0.0))
        review_count = int(it.get("review_count", 0))

        hospitals.append({
            "id": objt_id,
            "name": name,
            "address": address,
            "road_address": road_address,
            "tel": tel,
            "lat": lat,
            "lng": lng,
            "distance_km": round(distance, 2),
            "rating": rating,
            "review_count": review_count,
            "detail_url": reverse("hospital_detail", args=[objt_id]),
            "external_url": f"https://www.comwel.or.kr/comwel/medi/orsc.jsp?objtId={objt_id}",
        })

    if sort == "rating":
        hospitals.sort(key=lambda h: (-h["rating"], h["distance_km"]))
    elif sort == "review":
        hospitals.sort(key=lambda h: (-h["review_count"], h["distance_km"]))
    else:
        hospitals.sort(key=lambda h: h["distance_km"])

    return JsonResponse({"hospitals": hospitals[:10]})


def hospital_detail(request, objt_id: str):
    """
    /hospital/detail/<objt_id>/
    단일 병원 상세 페이지 (카카오 지도 포함)
    """
    try:
        items = _fetch_all_items()
    except Exception as e:
        raise Http404(f"SAFEMAP API 호출 실패: {e}")

    target = None
    for it in items:
        cur_id = str(it.get("objt_id") or it.get("OBJT_ID") or "")
        if cur_id == objt_id:
            target = it
            break

    if not target:
        raise Http404("해당 병원을 찾을 수 없습니다.")

    x = float(target.get("x") or target.get("X"))
    y = float(target.get("y") or target.get("Y"))
    lng, lat = TRANSFORMER.transform(x, y)

    context = {
        "KAKAO_KEY": settings.KAKAO_KEY,
        "objt_id": objt_id,
        "name": target.get("fclty_nm") or target.get("FCLTY_NM"),
        "address": target.get("adres") or target.get("ADRES"),
        "road_address": target.get("rn_adres") or target.get("RN_ADRES"),
        "tel": target.get("telno") or target.get("TELNO"),
        "lat": lat,
        "lng": lng,
        "external_url": f"https://www.comwel.or.kr/comwel/medi/orsc.jsp?objtId={objt_id}",
    }
    return render(request, "hospital/hospital_detail.html", context)
