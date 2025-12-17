# news/views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from .models import News
from .crawler.run import crawl_news   # ← 크롤링 모듈만 가져오기

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
# 1) 관리자용: 수동 크롤링 실행
def crawl_news_view(request):
    """
    /news/crawl/ 로 접근했을 때 크롤링 실행
    """
    try:    # 크롤링 실행 
        crawl_news()   
        messages.success(request, f"크롤링 완료!")
    except Exception as e:
        messages.error(request, f"크롤링 중 오류 발생: {e}")

    return redirect("News:news_list") # 크롤링 후 뉴스 리스트로 이동



# 2) 사용자용: 뉴스목록

def news_list(request):
    posts = News.objects.all().order_by('-n_created_at') # 기사작성일 순 
    # id로 하면 새로운뉴스 insert될때 뒤에 붙는데 그게 앞에 안나옴

    WRITE_PAGES = 5     # 페이지 블록 개수
    PER_PAGE = 10       # 한 페이지당 게시물 개수

     # -----------------------
    # 1) 필터 파라미터 수집
    # -----------------------
    q = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "all")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # -----------------------
    # 2) 기본 QS + 필터 적용
    #    (템플릿이 쓰는 필드명 기준)
    # -----------------------
    qs = News.objects.all().order_by("-n_created_at")

    if q:
        if search_type == "title":
            qs = qs.filter(n_title__icontains=q)
        elif search_type == "content":
            qs = qs.filter(n_contents__icontains=q)
        elif search_type == "author":
            qs = qs.filter(n_writer__icontains=q)
        else:  # all (default)
            qs = qs.filter(
                Q(n_title__icontains=q) |
                Q(n_contents__icontains=q)
            )

    # 작성일 범위 (n_created_at 기준)
    if start_date:
        qs = qs.filter(n_created_at__gte=start_date)
    if end_date:
        qs = qs.filter(n_created_at__lte=end_date)
        
    # -----------------------
    # 3) 페이지네이션
    # ----------------------- 
    
    # page 값 (없으면 1)
    page = request.GET.get("page")
    
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    paginator = Paginator(posts, PER_PAGE)
    page_obj = paginator.get_page(page)

    # 페이지네이션 범위 계산
    start_page = ((page_obj.number - 1) // WRITE_PAGES) * WRITE_PAGES + 1
    end_page = min(start_page + WRITE_PAGES - 1, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    
    # -----------------------
    # 4) 페이지 이동 시 필터 유지용 쿼리스트링
    # -----------------------
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    query_params = params.urlencode()
    
    context = {
        "list": page_obj,
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range,
        
        # 필터 상태 유지(템플릿에서 그대로 사용)
        "search_keyword": q,
        "search_type": search_type,
        "start_date": start_date,
        "end_date": end_date,
        
        # 페이지네이션 링크용
        "query_params": query_params,
    }

    return render(request, 'news/news_list.html', context)
