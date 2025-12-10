from django.urls import path
from . import views

app_name = 'Member'

urlpatterns = [
    path('registerf/', views.registerf, name='registerf'),  # 회원가입
    path('registers/', views.registers, name='registers'),  # 회원가입 두번쨰
    path('login/', views.login, name='login'),  # 로그인
    path('kakao/login/', views.kakao_login, name='kakao_login'),  # 카카오 로그인
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),  # 카카오 로그인 콜백
    path('check-username/', views.check_username, name='check_username'), # 아이디 중복 확인
    path('complete/', views.complete, name='complete'),  # 회원가입 완료
    path('logout/', views.logout, name='logout'),  # 로그아웃

    path('mypage/', views.mypage, name='mypage'),  # 마이페이지 - 비밀번호 확인
    path('mypage_profile/', views.mypage_profile, name='mypage_profile'),  # 마이페이지
    path('mypage/profile-modify/', views.mypage_profile_modify, name='mypage_profile_modify'),  # 마이페이지 - 프로필 수정

    path('mypage/individual-list/', views.mypage_individual_list, name='mypage_individual_list'),  # 마이페이지 - 산재 관리
    path('mypage/individual/add/', views.mypage_individual_add, name='mypage_individual_add'),  # 마이페이지 - 산재 추가
    path('mypage/individual/delete/<int:individual_id>/', views.mypage_individual_delete, name='mypage_individual_delete'), # 마이페이지 - 산재 삭제
    path('mypage/individual/bulk-delete/', views.mypage_individual_bulk_delete, name='mypage_individual_bulk_delete'), # 마이페이지 - 산재 다중 삭제
    path('mypage/password-change/', views.mypage_password_change, name='mypage_password_change'),  # 마이페이지 - 비밀번호 변경
    path('mypage/withdrawal/', views.mypage_withdrawal, name='mypage_withdrawal'),  # 마이페이지 - 회원 탈퇴

]
