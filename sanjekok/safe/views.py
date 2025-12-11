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
    try:    # 크롤링 실행 
        crawl_safe()   
        messages.success(request, f"크롤링 완료!")
    except Exception as e:
        messages.error(request, f"크롤링 중 오류 발생: {e}")

    return redirect("Safe:safe_main") # 크롤링 후 뉴스 리스트로 이동


# 2) 사용자용: 자료목록 검색/필터, 자료목록

def safe_list(request):
    qs = Safe.objects.all()

    # -------------------------------
    # 검색
    # -------------------------------
    q = request.GET.get("q")
    if q:
        qs = qs.filter(s_title__icontains=q)

    # -------------------------------
    # 자료형태 필터
    # -------------------------------
    material_type = request.GET.get("type")

    # 대표 자료형태 값들 (기타 제외)
    MAIN_TYPES = ["OPS", "동영상", "책자", "PPT"]

    if material_type in MAIN_TYPES:
        qs = qs.filter(s_type=material_type)

    elif material_type == "기타":
        # 기타 = 대표 4개 유형이 아닌 모든 자료
        qs = qs.exclude(s_type__in=MAIN_TYPES) | qs.filter(s_type__isnull=True) | qs.filter(s_type="")

    # -------------------------------
    # 정렬
    # -------------------------------
    order = request.GET.get("order", "latest")

    if order == "latest":
        qs = qs.order_by("-s_created_at")
    elif order == "old":
        qs = qs.order_by("s_created_at")
    elif order == "view":
        qs = qs.order_by("-s_view_count")

    # -------------------------------
    # 페이지네이션
    # -------------------------------
    from django.core.paginator import Paginator
    paginator = Paginator(qs, 12)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, "safe/safe_list.html", {
        "page_obj": page_obj,
        "q": q,
        "order": order,
        "material_type": material_type,
    })


    
