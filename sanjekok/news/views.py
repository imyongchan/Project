from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import News
from .crawler import crawl_news

def crawl_news_view(request):
    crawl_news()    # crawler.py 실행
    return redirect("News:news_list")

def news_list(request):
    posts = News.objects.all().order_by('-id')  # 최신 기사순 ...
    write_pages = 5    # 페이징 블록에 들어갈 페이지개수  (사용자가 못 바꿈)
    per_page = 10      # 한페이지당 표시할 기사 개수 (사용자가 못 바꿈)
    page = int(request.GET.get("page", 1))

    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page)

    start_page = ((page_obj.number - 1) // write_pages) * write_pages + 1
    end_page = start_page + write_pages - 1

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages  # 총 페이지수 넘지 않게
        
    page_range = range(start_page, end_page + 1)

    context = {
        "news": page_obj,
        "write_pages": write_pages,
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range,
    }
    
    return render(request, 'news/news_list.html', context)