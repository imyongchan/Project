from django.shortcuts import render
from django.conf import settings

def search(request):
    return render(request, "search.html", {
        "KAKAO_KEY": settings.KAKAO_KEY
    })
