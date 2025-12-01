from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 주변 산재 검색
# @login_required(login_url="/login/")
def search(request):
    return render(request, "search.html")

