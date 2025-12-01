from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 주변 산재 검색
@login_required(login_url="/login/")
def search_accident(request):
    return render(request, "search_accident.html")


# 주변 병원 검색
@login_required(login_url="/login/")
def search_hospital(request):
    return render(request, "search_hospital.html")


# 병원 상세 페이지
@login_required(login_url="/login/")
def hospital_detail(request, hospital_id):
    context = {
        "hospital_id": hospital_id,   # 템플릿에서 id 사용 가능
    }
    return render(request, "hospital_detail.html", context)
