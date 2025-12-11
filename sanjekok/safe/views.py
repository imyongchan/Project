from django.shortcuts import render, redirect
from django.contrib import messages

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
def safe_main(request):
    qs = Safe.objects.all().order_by('-id')

    # 언어 필터
    lang = request.GET.get("lang")
    if lang == "한국어":
        qs = qs.filter(s_language="한국어")
    elif lang == "외국어":
        qs = qs.filter(s_language="외국어")

    # 자료형태 필터
    type = request.GET.get("type")
    if type:
        qs = qs.filter(s_type=type)

    # 제목 검색
    q = request.GET.get("q")
    if q:
        qs = qs.filter(s_title__icontains=q)

    return render(request, "safe/safe_list.html", {
        "list": qs,
    })

    
