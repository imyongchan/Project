from django.urls import path
from . import views

app_name = 'Safe'

urlpatterns = [
    path('', views.safe_list, name='safe_list'),
    path("detail/<int:pk>/", views.safe_detail, name="safe_detail"),
    path('crawl/', views.crawl_safe_view, name='crawl_safe')
]
