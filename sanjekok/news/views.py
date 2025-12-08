from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import News
from .crawler.run import crawl_news   # ← 크롤링 모듈만 가져오기


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



# 2) 뉴스목록: 페이지네이션

def news_list(request):
    posts = News.objects.all().order_by('id')  # 최신순

    WRITE_PAGES = 5     # 페이지 블록 개수
    PER_PAGE = 10       # 한 페이지당 게시물 개수

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

    context = {
        "list": page_obj,
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range,
    }

    return render(request, 'news/news_list.html', context)
