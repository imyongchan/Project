from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from member.models import Member, Individual
from reviews.models import Review
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta

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
    # 전체 회원수
    member_count = Member.objects.filter(m_status=1).count()


    # 오늘 신규 가입
    today = timezone.localdate()  # 오늘 날짜
    days_ago = today - timedelta(days=6) # 최근 6일 상태

    new_members_today = Member.objects.filter(
        m_created_at=today
    ).count()

	# 전체 산재 수
    total_individual = Individual.objects.count()

    #  전체 리뷰수

    review_count = Review.objects.count()

    days = []
    counts = []

    for i in range(6, -1, -1):  # 6일 전 ~ 오늘
        day = today - timedelta(days=i)
        days.append(day.strftime("%m-%d"))
        
        # 해당 날짜 가입자 수 세기
        count = Member.objects.filter(m_created_at__date=day).exclude(m_status=0).count()
        counts.append(count)


    context = {
        'member_count': member_count,
        'new_members_today': new_members_today,
        'review_count' : review_count,
        'total_individual' : total_individual,
        'days': days,
        'counts': counts,
    }

    return render(request, 'manager_dash.html', context)
