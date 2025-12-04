from django.urls import path
from . import views

app_name = 'Member'

urlpatterns = [
    path('registerf/', views.registerf, name='registerf'),  # 회원가입
    path('registers/', views.registers, name='registers'),  # 회원가입 두번쨰
    path('login/', views.login, name='login'),  # 로그인
    path('check-username/', views.check_username, name='check_username'), # 아이디 중복 확인
    path('complete/', views.complete, name='complete'),  # 회원가입 완료

    path('mypage/', views.mypage, name='mypage'),  # 마이페이지
    path('mypage/profile/', views.mypage_profile, name='mypage_profile'),  # 마이페이지 - 프로필 수정

    path('mypage/individual-list/', views.mypage_individual_list, name='mypage_individual_list'),  # 마이페이지 - 산재 관리
]
