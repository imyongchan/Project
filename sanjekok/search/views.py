from django.shortcuts import render
from django.conf import settings
from member.models import Member, Individual
from django.http import JsonResponse
import requests
import traceback
from math import radians, sin, cos, sqrt, atan2, exp, atan, pi  # ← 추가: exp, atan, pi


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


# SAFEMAP x,y(웹 메르카토, EPSG:3857 가정) → WGS84(lat, lng) 변환
def mercator_to_wgs84(x, y):
    """
    SAFEMAP IF_0060 응답의 x, y 값을 위도/경도(도 단위)로 변환.
    x, y 가 Web Mercator(EPSG:3857) 기준이라고 보고 변환합니다.
    """
    R = 6378137.0  # 지구 반지름 (m)
    lon_rad = x / R
    lat_rad = 2 * atan(exp(y / R)) - pi / 2
    return lat_rad * 180.0 / pi, lon_rad * 180.0 / pi  # (lat, lon)


# 검색 페이지
def search_page(request):
    home_address = ""
    work_address = ""
    accidents = []

    # member/views.py 의 login 에서 세션에 저장한 값 사용
    member_id = request.session.get("member_id")

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)

            # 집 / 근무지 주소
            home_address = member.m_address or ""
            work_address = member.m_jaddress or ""

            # 이 회원이 가진 업종(related_name='industries' 가정)
            member_industries = member.industries.all()

            # 해당 업종에 속한 산재(사고지역 리스트)
            accidents = (
                Individual.objects
                .filter(member_industry__in=member_industries)
                .order_by("-i_accident_date")
            )
        except Member.DoesNotExist:
            # 회원 정보가 없으면 기본값(빈 값) 유지
            pass

    return render(request, "search/search.html", {
        "home_address": home_address,
        "work_address": work_address,
        "accidents": accidents,
        "KAKAO_JS_KEY": settings.KAKAO_JS_KEY,
    })


# 단일 주소 좌표 변환 API
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


# 주변 산재 검색
def incidents_api(request):
    # 중심 좌표 파라미터
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    radius_param = request.GET.get("radius")  # 선택(없으면 기본 5km)

    if lat is None or lng is None:
        return JsonResponse({"error": "lat, lng 파라미터가 필요합니다."}, status=400)

    try:
        center_lat = float(lat)
        center_lng = float(lng)
    except ValueError:
        return JsonResponse({"error": "lat, lng 값이 올바르지 않습니다."}, status=400)

    try:
        radius_km = float(radius_param) if radius_param is not None else 5.0
    except ValueError:
        radius_km = 5.0  # 잘못된 값이 들어오면 기본 5km

    # SAFEMAP API 호출
    try:
        safemap_resp = requests.get(
            "https://www.safemap.go.kr/openapi2/IF_0060",
            params={
                "serviceKey": settings.SAFEMAP_KEY,
                "pageNo": 1,
                "numOfRows": 200,
                "returnType": "json",
            },
            timeout=10,
        )
        safemap_resp.raise_for_status()
        safemap = safemap_resp.json()
    except Exception as e:
        print("SAFEMAP ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"error": "SAFEMAP API 호출 실패"}, status=502)

    # 응답 파싱
    items = safemap.get("body", {}).get("items", {}).get("item", [])

    # item 이 단일 객체(dict)로 오는 경우를 위해 처리
    if not items:
        items = []
    elif not isinstance(items, list):
        items = [items]

    results = []

    for it in items:
        # SAFEMAP 의 좌표값
        x = it.get("x")
        y = it.get("y")
        if x is None or y is None:
            continue

        try:
            x = float(x)
            y = float(y)
        except (TypeError, ValueError):
            continue

        # x, y → 위도/경도(도 단위) 변환
        item_lat, item_lng = mercator_to_wgs84(x, y)

        # 중심점과 거리 계산
        dist = haversine(center_lat, center_lng, item_lat, item_lng)

        # 반경 이내만 포함
        if dist <= radius_km:
            results.append({
                "lat": item_lat,
                "lng": item_lng,
                "area": it.get("area_nm"),
                "location": it.get("locplc"),   # 소재지(주소)
                "count": it.get("dsps_co"),
                "year": it.get("syd_year"),
                "org_nm": it.get("org_nm"),
                "distance": round(dist, 2),
            })

    # 거리 순으로 정렬(가까운 순)
    results.sort(key=lambda x: x["distance"])

    return JsonResponse({
        "totalCount": len(results),
        "items": results,
    })
