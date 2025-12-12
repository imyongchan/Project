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

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Safe

def safe_list(request):

    # 0) 전체 자료 불러오기
    materials = Safe.objects.all()

    # -----------------------------------------
    # 1) 제목 검색
    # -----------------------------------------
    search_keyword = request.GET.get("q", "")
    if search_keyword:
        materials = materials.filter(s_title__icontains=search_keyword)

    # -----------------------------------------
    # 2) 자료유형(type) - 체크박스 다중 선택
    # -----------------------------------------
    selected_types = request.GET.getlist("type")  # ['OPS','책자','기타']
    BASE_TYPES = ["OPS", "동영상", "책자", "PPT"]

    if selected_types:

        filtered_materials = []  # 조건에 맞는 자료만 담는 리스트

        for item in materials:
            item_type = item.s_type

            # 2-1) 기본 유형이 선택된 경우
            if item_type in selected_types:
                filtered_materials.append(item)
                continue

            # 2-2) 기타가 선택된 경우
            if "기타" in selected_types:
                if item_type not in BASE_TYPES:  # 대표 4개에 속하지 않으면 기타
                    filtered_materials.append(item)
                    continue

        # 기존 QuerySet을 파이썬 list로 줄였기 때문에 다시 id 목록으로 필터링
        material_ids = [m.id for m in filtered_materials]
        materials = Safe.objects.filter(id__in=material_ids)

    # -----------------------------------------
    # 3) 언어 필터 (radio 1개 선택)
    # -----------------------------------------
    selected_language = request.GET.get("lang", "")  # '', 한국어, 외국어

    if selected_language == "한국어":
        materials = materials.filter(s_language="한국어")

    elif selected_language == "외국어":
        materials = materials.exclude(s_language="한국어")

    # -----------------------------------------
    # 4) 정렬
    # -----------------------------------------
    selected_order = request.GET.get("order", "latest")

    if selected_order == "latest":
        materials = materials.order_by("-s_created_at")
    elif selected_order == "old":
        materials = materials.order_by("s_created_at")
    elif selected_order == "view":
        materials = materials.order_by("-s_view_count")

    # -----------------------------------------
    # 5) 페이지네이션
    # -----------------------------------------
    paginator = Paginator(materials, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # -----------------------------------------
    # 템플릿 렌더링
    # -----------------------------------------
    return render(request, "safe/safe_list.html", {
        "page_obj": page_obj,
        "search_keyword": search_keyword,
        "selected_types": selected_types,
        "selected_language": selected_language,
        "selected_order": selected_order,
    })



    
