from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if 'member_id' not in request.session:
            messages.error(request, "로그인이 필요합니다.")
            return redirect('Member:login')
        return function(request, *args, **kwargs)
    return wrap

def mypage_auth_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        # 1. 로그인 확인 (login_required와 동일)
        if 'member_id' not in request.session:
            messages.error(request, "로그인이 필요합니다.")
            return redirect('Member:login')

        # 2. 소셜 로그인 사용자는 비밀번호 확인 절차 면제
        if request.session.get('member_provider') != 'local':
            return function(request, *args, **kwargs)

        # 3. 마이페이지 인증 여부 확인
        if not request.session.get('mypage_authorized'):
            messages.info(request, "마이페이지 기능에 접근하려면 비밀번호를 다시 확인해야 합니다.")
            # 원래 가려던 URL을 세션에 저장
            request.session['next_url'] = request.path
            return redirect('Member:mypage_check')
            
        return function(request, *args, **kwargs)
    return wrap
