from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse

import math
import requests
from pyproj import Transformer

from member.models import Member, Individual, Member_industry

SAFEMAP_HOSPITAL_URL = "https://www.safemap.go.kr/openapi2/IF_0025"
KAKAO_GEOCODE_URL = "https://dapi.kakao.com/v2/local/search/address.json"
TRANSFORMER = Transformer.from_crs("EPSG:5179", "EPSG:4326", always_xy=True)


def haversine_km(lat1, lng1, lat2, lng2):
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
    member_id = request.session.get("member_id")
    if not member_id:
        return None

    try:
        return Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        return None


def get_latest_accident_address(member: Member):
    industries = member.industries.all()
    accident = (
        Individual.objects
        .filter(member_industry__in=industries)
        .order_by("-i_accident_date", "-accident_id")
        .first()
    )
    if accident:
        return accident.i_address
    return None


def _fetch_all_items():
    params = {
        "serviceKey": settings.SAFEMAP_KEY,
        "pageNo": 1,
        "numOfRows": 10000,
        "returnType": "json",
    }
    resp = requests.get(SAFEMAP_HOSPITAL_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    body = data.get("body")
    if body is None and "response" in data:
        body = data["response"].get("body")

    if body is None:
        items = data.get("items") or data.get("item") or []
    else:
        items = body.get("items") or body.get("item") or []

    if isinstance(items, dict):
        items = [items]

    return items


def _extract_lat_lng(item):
    lat = None
    lng = None

    for lat_key in ("latitude", "LAT", "lat", "Lat"):
        if lat_key in item:
            try:
                lat = float(item[lat_key])
                break
            except (TypeError, ValueError):
                pass

    for lng_key in ("longitude", "LNG", "lng", "Lng", "lon"):
        if lng_key in item:
            try:
                lng = float(item[lng_key])
                break
            except (TypeError, ValueError):
                pass

    if lat is not None and lng is not None:
        return lat, lng

    try:
        x = float(item.get("x") or item.get("X"))
        y = float(item.get("y") or item.get("Y"))
        lng, lat = TRANSFORMER.transform(x, y)
        return lat, lng
    except (TypeError, ValueError):
        return None, None


def hospital_search(request):
    member = get_current_member(request)

    home_lat = home_lng = None
    work_lat = work_lng = None
    acc_lat = acc_lng = None

    if member:
        home_lat, home_lng = geocode_address(member.m_address)
        work_lat, work_lng = geocode_address(member.m_jaddress)

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
    전국 산재 병원 전체(IF_0025)에서
    집/근무지/사고지역 기준 가장 가까운 병원 Top10만 반환.
    - Top10 후보는 항상 거리(distance_km) 기준으로 먼저 자른 뒤
      sort 파라미터(distance/rating/review)에 따라 Top10 안에서만 정렬.
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
        return JsonResponse({"error": f"SAFEMAP 병원 API 호출 실패: {e}"}, status=500)

    hospitals = []
    for it in items:
        lat, lng = _extract_lat_lng(it)
        if lat is None or lng is None:
            continue

        distance = haversine_km(base_lat, base_lng, lat, lng)

        objt_id = str(
            it.get("objt_id")
            or it.get("OBJT_ID")
            or it.get("hosp_id")
            or it.get("HOSP_ID")
            or ""
        )

        name = (
            it.get("fclty_nm")
            or it.get("FCLTY_NM")
            or it.get("hname")
            or it.get("HNAME")
            or it.get("yadmNm")
            or it.get("YADM_NM")
        )

        address = (
            it.get("adres")
            or it.get("ADRES")
            or it.get("addr")
            or it.get("ADDR")
        )

        road_address = (
            it.get("rn_adres")
            or it.get("RN_ADRES")
            or it.get("road_addr")
            or it.get("ROAD_ADDR")
        )

        tel = (
            it.get("telno")
            or it.get("TELNO")
            or it.get("tel")
            or it.get("TEL")
        )

        # 실제 평점/리뷰 데이터가 없으면 0으로 기본값
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
        })

    # 1단계: 전국 기준으로 "거리순" 정렬 후 Top10 추출
    hospitals.sort(key=lambda h: h["distance_km"])
    top10 = hospitals[:10]

    # 2단계: 그 Top10 안에서만 정렬 옵션 적용
    if sort == "rating":
        top10.sort(key=lambda h: (-h["rating"], h["distance_km"]))
    elif sort == "review":
        top10.sort(key=lambda h: (-h["review_count"], h["distance_km"]))
    # sort == distance 인 경우에는 이미 거리순이라 추가 정렬 불필요

    return JsonResponse({"hospitals": top10})


def hospital_detail(request, objt_id: str):
    try:
        items = _fetch_all_items()
    except Exception as e:
        raise Http404(f"SAFEMAP 병원 API 호출 실패: {e}")

    target = None
    for it in items:
        cur_id = str(
            it.get("objt_id")
            or it.get("OBJT_ID")
            or it.get("hosp_id")
            or it.get("HOSP_ID")
            or ""
        )
        if cur_id == objt_id:
            target = it
            break

    if not target:
        raise Http404("해당 병원을 찾을 수 없습니다.")

    lat, lng = _extract_lat_lng(target)
    if lat is None or lng is None:
        raise Http404("병원 좌표 정보를 찾을 수 없습니다.")

    name = (
        target.get("fclty_nm")
        or target.get("FCLTY_NM")
        or target.get("hname")
        or target.get("HNAME")
        or target.get("yadmNm")
        or target.get("YADM_NM")
    )

    address = (
        target.get("adres")
        or target.get("ADRES")
        or target.get("addr")
        or target.get("ADDR")
    )

    road_address = (
        target.get("rn_adres")
        or target.get("RN_ADRES")
        or target.get("road_addr")
        or target.get("ROAD_ADDR")
    )

    tel = (
        target.get("telno")
        or target.get("TELNO")
        or target.get("tel")
        or target.get("TEL")
    )

    context = {
        "KAKAO_KEY": settings.KAKAO_KEY,
        "objt_id": objt_id,
        "name": name,
        "address": address,
        "road_address": road_address,
        "tel": tel,
        "lat": lat,
        "lng": lng,
    }
    return render(request, "hospital/hospital_detail.html", context)
