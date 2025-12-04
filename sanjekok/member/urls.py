from django.urls import path
from . import views

app_name = 'Member'

urlpatterns = [
    path('registerf/', views.registerf, name='registerf'),  # 회원가입
    path('registers/', views.registers, name='registers'),  # 회원가입 두번쨰
    path('login/', views.login, name='login'),  # 로그인
    path('check-username/', views.check_username, name='check_username'), # 아이디 중복 확인
]
