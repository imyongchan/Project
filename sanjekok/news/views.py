from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import News
from .crawler.run import crawl_news   # ← 크롤링 모듈만 가져오기


# -----------------------------
# 1) 관리자용: 수동 크롤링 실행
# -----------------------------
def crawl_news_view(request):
    """
    관리자용 크롤링 실행
    /news/crawl/ 로 접근했을 때 JSON, XML 등 모두 크롤링하도록 호출
    """
    try:
        created_count = crawl_news()   # 크롤링 실행 → 몇 개 저장됐는지 반환하게 구현 권장
        messages.success(request, f"크롤링 완료! {created_count}개의 뉴스가 업데이트되었습니다.")
    except Exception as e:
        messages.error(request, f"크롤링 중 오류 발생: {e}")

    return redirect("News:news_list")


# -----------------------------
# 2) 사용자용 뉴스 리스트 (페이지네이션)
# -----------------------------
def news_list(request):
    posts = News.objects.all().order_by('-id')  # 최신순

    WRITE_PAGES = 5     # 페이지 블록 개수
    PER_PAGE = 10       # 한 페이지당 게시물 개수

    # page 값 (없으면 1)
    page = int(request.GET.get("page", 1))

    paginator = Paginator(posts, PER_PAGE)
    page_obj = paginator.get_page(page)

    # 페이지네이션 계산
    start_page = ((page_obj.number - 1) // WRITE_PAGES) * WRITE_PAGES + 1
    end_page = min(start_page + WRITE_PAGES - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    context = {
        "list": page_obj,
        "write_pages": WRITE_PAGES,
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range,
    }

    return render(request, 'news/news_list.html', context)
