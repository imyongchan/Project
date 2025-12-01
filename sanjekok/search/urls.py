from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    # 주변 산재 검색
    path("search/", views.search),
]
