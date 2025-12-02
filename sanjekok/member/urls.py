from django.urls import path
from . import views

app_name = 'Member'

urlpatterns = [
    path('register/', views.register, name='register'),  # 회원가입
]
