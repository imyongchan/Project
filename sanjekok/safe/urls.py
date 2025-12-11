from django.urls import path
from . import views

app_name = 'Safe'

urlpatterns = [
    path('', views.safe_main, name='safe_main'),
    path('crawl/', views.crawl_safe_view, name='crawl_safe')
]
