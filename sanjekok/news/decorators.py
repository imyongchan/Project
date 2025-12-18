from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from member.models import Member

def crawl_admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        # 1️⃣ 관리자 로그인 여부
        if not request.session.get("manager_login"):
            messages.error(request, "관리자 로그인이 필요합니다.")
            return redirect("Manager:login")

        # 2️⃣ 세션 member 확인
        member_id = request.session.get("member_id")
        if not member_id:
            messages.error(request, "세션이 만료되었습니다.")
            return redirect("Manager:login")

        # 3️⃣ admin 계정 확인
        try:
            member = Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            messages.error(request, "유효하지 않은 계정입니다.")
            return redirect("Manager:login")

        if member.m_username != "admin":
            messages.error(request, "크롤링 권한이 없습니다.")
            return redirect("Main:main")

        return function(request, *args, **kwargs)

    return wrap
