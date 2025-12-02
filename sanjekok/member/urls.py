from django.urls import path
from . import views

app_name = 'Member'

urlpatterns = [
    path('registerf/', views.registerf, name='registerf'),  # 회원가입
    path('registers/', views.registers, name='registers'),  # 회원가입 두번쨰
    path('login/', views.login, name='login'),  # 로그인
]
