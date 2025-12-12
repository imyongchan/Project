from django.urls import path
from . import views

app_name = "Search"

urlpatterns = [
    path('', views.search_page, name='search_page'),
    path('geocode/', views.geocode_api, name='geocode_api'),   # 주소검색/
    path('incidents/', views.incidents_api, name='incidents_api'), # 산업재해수
]
