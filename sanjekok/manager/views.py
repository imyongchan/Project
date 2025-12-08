from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from member.models import Member, Individual
from reviews.models import Review
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

def login(request):
    if request.method == "GET":
        return render(request, "manager_login.html")

    elif request.method == "POST":
        m_username = request.POST.get("username")
        m_password = request.POST.get("password")

        member = Member.objects.filter(m_username=m_username).first()

        if (not member) or (not check_password(m_password, member.m_password)) or (member.m_status != 0):
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "manager_login.html")


        request.session['member_id'] = int(member.member_id)
        request.session['member_username'] = member.m_username

        request.session['manager_login'] = True

        messages.success(request, f"{member.m_name}님 환영합니다!")
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

def member(request):
    members = Member.objects.filter(m_status=1).order_by('-member_id')

    paginator = Paginator(members, 5)   # ▶ 한 페이지에 5개씩
    page_number = request.GET.get('page')  # ▶ URL에서 page 값 받기
    page_obj = paginator.get_page(page_number)  # ▶ 페이지 객체 생성

    context = {
        'page_obj': page_obj
    }
    return render(request, 'manager_member.html', context)

def delete(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)
    member.m_status = 0  # 탈퇴 상태로 변경
    member.save()
    return redirect('manager_member.html')

def review(request):

    hospital = request.GET.get('hospital', '')
    member = request.GET.get('member', '')

    reviews = Review.objects.all().order_by('-id')

    # 병원 필터
    if hospital:
        reviews = reviews.filter(hospital_id__name__icontains=hospital)

    # 작성자 필터
    if member:
        reviews = reviews.filter(member_id__m_username__icontains=member)

    paginator = Paginator(reviews, 5)   # ▶ 한 페이지에 5개씩
    page_number = request.GET.get('page')  # ▶ URL에서 page 값 받기
    page_obj = paginator.get_page(page_number)  # ▶ 페이지 객체 생성

    context = {
        'page_obj': page_obj,
        'r_list': reviews
    } 

    return  render(request, 'manager_review.html', context)

def stats(request):

    total_individual = Individual.objects.all()

    paginator = Paginator(total_individual, 5)   # ▶ 한 페이지에 5개씩
    page_number = request.GET.get('page')  # ▶ URL에서 page 값 받기
    page_obj = paginator.get_page(page_number)  # ▶ 페이지 객체 생성

    context = {
        'page_obj': page_obj
    }

    return render(request, 'manager_stats.html', context)

def logout(request):
    request.session.flush()  # 세션 완전 삭제
    messages.success(request, "로그아웃되었습니다.")
    return render(request, 'manager_logout.html')