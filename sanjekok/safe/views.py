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


# 2) 사용자용: 로그인 필요. 회원only

@login_required
def safe_list(request):
    qs = Safe.objects.all()

    # 검색
    q = request.GET.get("q")
    if q:
        qs = qs.filter(s_title__icontains=q)


    # 정렬: latest, old, view
    order = request.GET.get("order", "latest")

    if order == "latest":
        qs = qs.order_by("-s_created_at")
    elif order == "old":
        qs = qs.order_by("s_created_at")
    elif order == "view":
        qs = qs.order_by("-s_view_count")

    # -------------------------------
    # 페이지네이션 — 12개씩
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "safe/safe_list.html", {
        "page_obj": page_obj,
        "order": order,
        "q": q,
    })

    
