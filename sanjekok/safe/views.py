from django.shortcuts import render, redirect
from django.contrib import messages

from .crawler.run import crawl_safe
from .models import Safe

from .decorators import login_required

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
    return render(request, "safe/safe_main.html")
    
