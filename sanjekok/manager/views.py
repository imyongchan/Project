from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from member.models import Member, Individual
from reviews.models import Review
from hospital.models import Hospital
from django.contrib.auth.hashers import check_password
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models.functions import Cast
from django.db.models import CharField

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
    today = date.today()
    days_ago = today - timedelta(days=6)

    new_members_today = Member.objects.filter(
        m_created_at__date=today
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
    return redirect('Manager:member')

def review(request):

    filter_by = request.GET.get("filter_by")
    keyword = request.GET.get("keyword", "")

    reviews = Review.objects.all().order_by('-id')

    if filter_by == "hospital" and keyword:
        reviews = reviews.filter(hospital__h_hospital_name__icontains=keyword)

    if filter_by == "member" and keyword:
        reviews = reviews.filter(member__m_username__icontains=keyword)

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'r_list': page_obj,
    }
    return render(request, 'manager_review.html', context)

def stats(request):
    
    total_individual = Individual.objects.all()

    industry1 = request.GET.get("industry1")
    industry2 = request.GET.get("industry2")
    injury = request.GET.get("injury")
    disease = request.GET.get("disease")
    raw_date = request.GET.get("accident_date", "")

    # -------- 날짜 정규화 --------
    accident_date = raw_date.replace("-", "").strip()

    # 필터들
    if industry1:
        total_individual = total_individual.filter(member_industry__i_industry_type1=industry1)

    if industry2:
        total_individual = total_individual.filter(member_industry__i_industry_type2=industry2)

    if injury:
        total_individual = total_individual.filter(i_injury=injury)

    if disease:
        total_individual = total_individual.filter(i_disease_type=disease)

    # -------- 날짜 처리 --------
    if accident_date.isdigit():

        # YYYY (연도)
        if len(accident_date) == 4:
            year = int(accident_date)
            start_date = date(year, 1, 1)
            end_date = date(year + 1, 1, 1)

        # YYYYMM (년월)
        elif len(accident_date) == 6:
            year = int(accident_date[:4])
            month = int(accident_date[4:6])

            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)

        # YYYYMMDD (년월일)
        elif len(accident_date) == 8:
            try:
                start_date = date(
                    int(accident_date[:4]),
                    int(accident_date[4:6]),
                    int(accident_date[6:8])
                )
                end_date = start_date + timedelta(days=1)
            except:
                start_date = end_date = None
        else:
            start_date = end_date = None

        # 실제 필터 적용
        if start_date and end_date:
            total_individual = total_individual.filter(
                i_accident_date__gte=start_date,
                i_accident_date__lt=end_date
            )

    # -------- 페이징 --------
    paginator = Paginator(total_individual, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "manager_stats.html", {"page_obj": page_obj})


def logout(request):
    request.session.flush()  # 세션 완전 삭제
    messages.success(request, "로그아웃되었습니다.")
    return render(request, 'manager_logout.html')