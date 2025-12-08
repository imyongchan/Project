from django.shortcuts import render
from django.conf import settings
from member.models import Member, Individual
from django.http import JsonResponse
import requests
import traceback
from math import radians, sin, cos, sqrt, atan2


# 위 경도 거리 계산
def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

# 주소 검색
def search_page(request):

    user = request.user if request.user.is_authenticated else None

    home_address = ""
    work_address = ""
    accidents = []

    if user:
        try:
            member = Member.objects.get(member_id=user.member_id)
            home_address = member.m_address
            work_address = member.m_jaddress

            # 사고지역 가져오기
            accidents = Individual.objects.filter(member_industry__member=member)

        except Member.DoesNotExist:
            pass

    return render(request, "search/search.html", {
        "home_address": home_address,
        "work_address": work_address,
        "accidents": accidents,
        "KAKAO_JS_KEY": settings.KAKAO_JS_KEY,
    })


# 주소 좌표 변환
def geocode_api(request):
    query = request.GET.get("query")
    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}

    try:
        resp = requests.get(
            "https://dapi.kakao.com/v2/local/search/address.json",
            params={"query": query},
            headers=headers
        )
        return JsonResponse(resp.json())
    except Exception as e:
        print("GEOCODE ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


# 주변 산재 검색
def incidents_api(request):
    try:
        center_lat = float(request.GET.get("lat"))
        center_lng = float(request.GET.get("lng"))
        radius_km = 5  # ← 요청에 따라 반경 고정 5km

        # SAFEMAP API 호출
        safemap = requests.get(
            "https://www.safemap.go.kr/openapi2/IF_0060",
            params={
                "serviceKey": settings.SAFEMAP_API_KEY,
                "pageNo": 1,
                "numOfRows": 200,
                "returnType": "json"
            },
            timeout=10
        ).json()

        items = safemap.get("body", {}).get("items", {}).get("item", [])
        results = []

        # 카카오 REST 키 설정
        headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}

        for it in items:
            address = it.get("locplc")
            if not address:
                continue

            # locplc → 위경도 변환
            geo = requests.get(
                "https://dapi.kakao.com/v2/local/search/address.json",
                params={"query": address},
                headers=headers
            ).json()

            docs = geo.get("documents", [])
            if not docs:
                continue

            item_lat = float(docs[0]["y"])
            item_lng = float(docs[0]["x"])

            # 중심점과 거리 계산
            dist = haversine(center_lat, center_lng, item_lat, item_lng)

            # 5km 이내만 포함
            if dist <= radius_km:
                results.append({
                    "lat": item_lat,
                    "lng": item_lng,
                    "area": it.get("area_nm"),
                    "location": address,
                    "count": it.get("dsps_co"),
                    "year": it.get("syd_year"),
                    "org_nm": it.get("org_nm"),
                    "distance": round(dist, 2)
                })

        return JsonResponse({
            "totalCount": len(results),
            "items": results
        })

    except Exception as e:
        print("INCIDENT ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
