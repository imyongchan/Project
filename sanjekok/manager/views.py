from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from member.models import Member
from django.contrib.auth.hashers import make_password, check_password

def login(request):
    if request.method == "GET":
        return render(request, "manager_login.html")

    elif request.method == "POST":
        m_username = request.POST.get("username")
        m_password = request.POST.get("password")

        member = Member.objects.filter(m_username=m_username).first()

        if not member or not check_password(m_password, member.m_password) and member.m_status!=0:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "manager_login.html")

        request.session['member_id'] = int(member.member_id)
        request.session['member_username'] = member.m_username

        messages.success(request, f"{member.m_username}님 환영합니다!")
    return render(request, "manager_main.html")

def main(request):
    
    return render(request, 'manager_main.html')

def dash(request):
    return render(request, 'manager_dash.html')
