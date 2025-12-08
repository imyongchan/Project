from django.shortcuts import render
from django.conf import settings
from member.models import Member, Individual
from django.http import JsonResponse
import requests
import traceback
from math import radians, sin, cos, sqrt, atan2


# 위·경도 거리 계산 (단위: km)
def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # 지구 반지름(km)
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


# 검색 페이지
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

            # 산재 목록
            accidents = Individual.objects.filter(member_industry__member=member)

        except Member.DoesNotExist:
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
    try:
        center_lat = request.GET.get("lat")
        center_lng = request.GET.get("lng")
        if center_lat is None or center_lng is None:
            return JsonResponse({"error": "lat, lng 파라미터가 필요합니다."}, status=400)

        center_lat = float(center_lat)
        center_lng = float(center_lng)
        radius_km = 5  # 반경 5km

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

        items = safemap.get("body", {}).get("items", {}).get("item", []) or []

        results = []
        headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"}

        for it in items:
            address = it.get("locplc")
            if not address:
                continue

            # 위·경도 변환
            try:
                geo_resp = requests.get(
                    "https://dapi.kakao.com/v2/local/search/address.json",
                    params={"query": address},
                    headers=headers,
                    timeout=5,
                )
                geo_resp.raise_for_status()
                geo = geo_resp.json()
            except Exception as e:
                print("KAKAO GEOCODE ERROR:", e, "주소:", address)
                continue

            docs = geo.get("documents", [])
            if not docs:
                continue

            try:
                item_lat = float(docs[0]["y"])
                item_lng = float(docs[0]["x"])
            except (KeyError, ValueError):
                continue

            # 중심점과 거리 계산
            dist = haversine(center_lat, center_lng, item_lat, item_lng)

            # 반경 이내만 포함
            if dist <= radius_km:
                results.append({
                    "lat": item_lat,
                    "lng": item_lng,
                    "area": it.get("area_nm"),
                    "location": address,
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

    except Exception as e:
        print("INCIDENT ERROR:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
