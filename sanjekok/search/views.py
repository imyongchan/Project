import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

def search_page(request):
    return render(request, "search.html")

def place_search(request):
    keyword = request.GET.get("q", "")
    if not keyword:
        return JsonResponse({"results": []})

    # SAFEMAP or Kakao Key 선택: 안전한 방식 유지
    kakao_key = settings.KAKAO_KEY

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {kakao_key}"}
    params = {"query": keyword}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    results = []
    for item in data.get("documents", []):
        results.append({
            "place_name": item.get("place_name"),
            "address": item.get("road_address_name") or item.get("address_name"),
            "lat": item.get("y"),
            "lng": item.get("x")
        })

    return JsonResponse({"results": results})
