from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    # 주변 산재 검색
    path("accident/", views.search_accident, name="search_accident"),

    # 주변 병원 검색
    path("hospital/", views.search_hospital, name="search_hospital"),

    # 병원 상세 페이지
    path("hospital/<int:hospital_id>/", views.hospital_detail, name="hospital_detail"),
]
