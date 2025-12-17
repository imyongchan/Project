from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from member.models import Member, Individual
import requests
import traceback
from math import radians, sin, cos, sqrt, atan2, exp, atan, pi
from django.shortcuts import redirect
from django.contrib import messages


# 위·경도 거리 계산 (단위: km) 
def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # 지구 반지름(km)
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


# (구버전 SAFEMAP 호환 함수 - 현재 DB 기반 산재에서는 사용하지 않음)
def mercator_to_wgs84(x, y):
    R = 6378137.0  # 지구 반지름 (m)
    lon_rad = x / R
    lat_rad = 2 * atan(exp(y / R)) - pi / 2
    return lat_rad * 180.0 / pi, lon_rad * 180.0 / pi  # (lat, lon)


# 검색 페이지
def search_page(request):
    home_address = ""
    work_address = ""
    accidents = []

    member_id = request.session.get("member_id")
    
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')
    

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            home_address = member.m_address or ""
            work_address = member.m_jaddress or ""
            member_industries = member.industries.all()
            accidents = (
                Individual.objects
                .filter(member_industry__in=member_industries)
                .order_by("-i_accident_date")
            )
        except Member.DoesNotExist:
            pass

    return render(request, "search/search.html", {
        "home_address": home_address,
        "work_address": work_address,
        "accidents": accidents,
        "KAKAO_JS_KEY": settings.KAKAO_JS_KEY,

        # ✅ 추가: JS 캐시 깨기용 버전(값은 아무 문자열이어도 됨)
        "JS_VERSION": "v4",
    })

# 단일 주소 좌표 변환 API (집/근무지/드롭다운 이동용으로 유지)
def geocode_api(request):
    query = request.GET.get("query")
    if not query:
        return JsonResponse({"error": "query 파라미터가 필요합니다."}, status=400)

    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}

    try:
        resp = requests.get(
            "https://dapi.kakao.com/v2/local/search/address.json",
            params={"query": query},
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return JsonResponse(resp.json())
    except Exception as e:
        print("GEOCODE ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


def _parse_float(name: str, value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} 값이 올바르지 않습니다.")


# 주변/화면 내 산재 검색 (DB: t_individual 기반)
def incidents_api(request):
    """
    프론트에서 지도 bounds(남서/북동)를 보내면,
    그 화면 안에 보이는 산재만 반환하여 totalCount도 '보이는 만큼'만 집계됩니다.

    Query:
      - swLat, swLng, neLat, neLng  (권장)
      - (구버전 호환) lat, lng, radius(km)
    """
    member_id = request.session.get("member_id")

    swLat = request.GET.get("swLat")
    swLng = request.GET.get("swLng")
    neLat = request.GET.get("neLat")
    neLng = request.GET.get("neLng")

    qs = (
        Individual.objects
        .select_related("member_industry", "member_industry__member")
        .exclude(i_lat__isnull=True)
        .exclude(i_lng__isnull=True)
    )

    # ✅ 1) bounds 기반(권장): 화면에 보이는 만큼만 반환
    if swLat is not None and swLng is not None and neLat is not None and neLng is not None:
        try:
            sw_lat = _parse_float("swLat", swLat)
            sw_lng = _parse_float("swLng", swLng)
            ne_lat = _parse_float("neLat", neLat)
            ne_lng = _parse_float("neLng", neLng)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # 남/북, 서/동 정렬 보정
        low_lat, high_lat = (sw_lat, ne_lat) if sw_lat <= ne_lat else (ne_lat, sw_lat)
        low_lng, high_lng = (sw_lng, ne_lng) if sw_lng <= ne_lng else (ne_lng, sw_lng)

        qs = qs.filter(i_lat__gte=low_lat, i_lat__lte=high_lat, i_lng__gte=low_lng, i_lng__lte=high_lng)

    # ✅ 2) (구버전 호환) 중심+반경
    else:
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        radius_param = request.GET.get("radius")  # km

        if lat is None or lng is None:
            return JsonResponse({"error": "swLat,swLng,neLat,neLng 또는 lat,lng 파라미터가 필요합니다."}, status=400)

        try:
            center_lat = _parse_float("lat", lat)
            center_lng = _parse_float("lng", lng)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        try:
            radius_km = float(radius_param) if radius_param is not None else 5.0
        except ValueError:
            radius_km = 5.0

        # 1차: 대략적인 bbox 필터로 DB 부담 감소
        lat_delta = radius_km / 111.0
        lng_delta = radius_km / (111.0 * max(cos(radians(center_lat)), 0.1))
        qs = qs.filter(
            i_lat__gte=center_lat - lat_delta,
            i_lat__lte=center_lat + lat_delta,
            i_lng__gte=center_lng - lng_delta,
            i_lng__lte=center_lng + lng_delta,
        )

        # 2차: haversine 정확 거리 필터
        filtered = []
        for it in qs:
            dist = haversine(center_lat, center_lng, float(it.i_lat), float(it.i_lng))
            if dist <= radius_km:
                filtered.append(it)
        qs = filtered

    # 결과 구성
    items = []
    if isinstance(qs, list):
        iterable = qs
        total_count = len(qs)
    else:
        iterable = qs.order_by("-i_accident_date", "-accident_id")
        total_count = iterable.count()

    for it in iterable:
        ind = it.member_industry
        mem = ind.member if ind else None

        items.append({
            "accident_id": it.accident_id,
            "lat": float(it.i_lat),
            "lng": float(it.i_lng),
            "is_mine": (member_id is not None and mem is not None and int(member_id) == int(mem.member_id)),
            "i_accident_date": it.i_accident_date.isoformat() if it.i_accident_date else None,
            "i_injury": it.i_injury,
            "i_disease_type": it.i_disease_type,
            "i_address": it.i_address,
            "i_industry_type1": getattr(ind, "i_industry_type1", None),
            "i_industry_type2": getattr(ind, "i_industry_type2", None),
        })

    return JsonResponse({
        "totalCount": total_count,
        "items": items,
    })
