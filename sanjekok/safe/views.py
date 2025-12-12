from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .decorators import login_required

from .crawler.run import crawl_safe
from .models import Safe

# 1) 관리자용: 수동 크롤링 실행

def crawl_safe_view(request):
    """
    /safe/crawl/ 로 접근했을 때 크롤링 실행
    """
    try:     
        crawl_safe()   # 크롤링 실행
        messages.success(request, f"크롤링 완료!")
    except Exception as e:
        messages.error(request, f"크롤링 중 오류 발생: {e}")

    return redirect("Safe:safe_list") # 크롤링 후 뉴스 리스트로 이동


# 2) 사용자용: 자료목록 검색/필터, 자료목록(검색결과)

def safe_list(request):

    materials = Safe.objects.all()

    # 검색어
    search_keyword = request.GET.get("q", "")
    if search_keyword:
        materials = materials.filter(s_title__icontains=search_keyword)

    # 자료유형
    selected_types = request.GET.getlist("type")
    BASE_TYPES = ["OPS", "동영상", "책자", "PPT"]

    if selected_types == ["전체"] or not selected_types:
        pass  # 전체 조회
    else:
        filtered = []
        for item in materials:
            t = item.s_type

            if t in selected_types:
                filtered.append(item)
                continue

            if "기타" in selected_types and t not in BASE_TYPES:
                filtered.append(item)
                continue

        materials = Safe.objects.filter(id__in=[m.id for m in filtered])

    # 언어
    selected_language = request.GET.get("lang", "")
    if selected_language == "한국어":
        materials = materials.filter(s_language="한국어")
    elif selected_language == "외국어":
        materials = materials.exclude(s_language="한국어")

    # 정렬
    selected_order = request.GET.get("order", "latest")
    if selected_order == "latest":
        materials = materials.order_by("-s_created_at")
    elif selected_order == "old":
        materials = materials.order_by("s_created_at")
    elif selected_order == "view":
        materials = materials.order_by("-s_view_count")

    # 페이지네이션
    paginator = Paginator(materials, 12)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, "safe/safe_list.html", {
        "page_obj": page_obj,
        "search_keyword": search_keyword,
        "selected_types": selected_types,
        "selected_language": selected_language,
        "selected_order": selected_order,
    })






    
