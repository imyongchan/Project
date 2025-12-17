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
from django.urls import reverse

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

    paginator = Paginator(members, 8)   # 페이지당 리뷰 5개
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # ===== 10페이지 단위 계산 =====
    page_group_size = 10
    current_page = page_obj.number

    start_page = ((current_page - 1) // page_group_size) * page_group_size + 1
    end_page = start_page + page_group_size - 1

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    page_range = range(start_page, end_page + 1)

    # 🔥 다음 / 이전 그룹 페이지 계산
    prev_group_page = start_page - 1 if start_page > 1 else None
    next_group_page = end_page + 1 if end_page < paginator.num_pages else None

    # ===== 쿼리스트링 유지 =====
    querydict = request.GET.copy()
    querydict.pop("page", None)
    query_string = querydict.urlencode()

    context = {
        'page_obj': page_obj,
        'query_string': query_string,
        'page_range': page_range,
        "prev_group_page": prev_group_page,
        "next_group_page": next_group_page,
    }
    return render(request, 'manager_member.html', context)

def delete(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)
    member.m_status = 99  # 탈퇴 상태로 변경
    member.save()
    return redirect('Manager:member')

def review(request):

    filter_by = request.GET.get("filter_by")
    keyword = request.GET.get("keyword", "").strip()

    # ❗ 필터 미선택 + 검색어 입력
    if keyword and not filter_by:
        url = reverse('Manager:review')
        return redirect(f"{url}?error=need_filter")

    reviews = Review.objects.all().order_by('-id')

    if filter_by == "hospital" and keyword:
        reviews = reviews.filter(
            hospital__h_hospital_name__icontains=keyword
        )

    if filter_by == "member" and keyword:
        reviews = reviews.filter(
            member__m_username__icontains=keyword
        )

    # =============================
    # 페이징
    # =============================
    paginator = Paginator(reviews, 10)   # 페이지당 리뷰 5개
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # ===== 10페이지 단위 계산 =====
    page_group_size = 10
    current_page = page_obj.number

    start_page = ((current_page - 1) // page_group_size) * page_group_size + 1
    end_page = start_page + page_group_size - 1

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    page_range = range(start_page, end_page + 1)

    # 🔥 다음 / 이전 그룹 페이지 계산
    prev_group_page = start_page - 1 if start_page > 1 else None
    next_group_page = end_page + 1 if end_page < paginator.num_pages else None

    # ===== 쿼리스트링 유지 =====
    querydict = request.GET.copy()
    querydict.pop("page", None)
    query_string = querydict.urlencode()

    context = {
        'page_obj': page_obj,
        'r_list': page_obj,       # 기존 템플릿 호환
        'page_range': page_range,
        'query_string': query_string,
        "prev_group_page": prev_group_page,
        "next_group_page": next_group_page,
    }

    return render(request, 'manager_review.html', context)

def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('Manager:review')

def stats(request):
    total_individual = Individual.objects.all()

    industry1 = request.GET.get("industry1")
    industry2 = request.GET.get("industry2")
    injury = request.GET.get("injury")
    disease = request.GET.get("disease")
    raw_date = request.GET.get("accident_date", "")

    accident_date = raw_date.replace("-", "").strip()

    if industry1:
        total_individual = total_individual.filter(
            member_industry__i_industry_type1=industry1
        )

    if industry2:
        total_individual = total_individual.filter(
            member_industry__i_industry_type2=industry2
        )

    if injury:
        total_individual = total_individual.filter(i_injury=injury)

    if disease:
        total_individual = total_individual.filter(i_disease_type=disease)

    if accident_date.isdigit():
        if len(accident_date) == 4:
            start_date = date(int(accident_date), 1, 1)
            end_date = date(int(accident_date) + 1, 1, 1)

        elif len(accident_date) == 6:
            year = int(accident_date[:4])
            month = int(accident_date[4:6])
            start_date = date(year, month, 1)
            end_date = date(year + (month // 12), (month % 12) + 1, 1)

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

        if start_date and end_date:
            total_individual = total_individual.filter(
                i_accident_date__gte=start_date,
                i_accident_date__lt=end_date
            )

    # =============================
    # 페이징
    # =============================
    paginator = Paginator(total_individual, 8)  # 페이지당 데이터 5개
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # ===== 10페이지 단위 페이징 계산 =====
    page_group_size = 10
    current_page = page_obj.number

    start_page = ((current_page - 1) // page_group_size) * page_group_size + 1
    end_page = start_page + page_group_size - 1

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    page_range = range(start_page, end_page + 1)

    # 🔥 다음 / 이전 그룹 페이지 계산
    prev_group_page = start_page - 1 if start_page > 1 else None
    next_group_page = end_page + 1 if end_page < paginator.num_pages else None

    # ===== 쿼리스트링 유지 =====
    querydict = request.GET.copy()
    querydict.pop("page", None)
    query_string = querydict.urlencode()

    return render(
        request,
        "manager_stats.html",
        {
            "page_obj": page_obj,
            "page_range": page_range,   # 🔥 추가
            "query_string": query_string,
            "prev_group_page": prev_group_page,
            "next_group_page": next_group_page,
        }
    )

def logout(request):
    request.session.flush()  # 세션 완전 삭제
    messages.success(request, "로그아웃되었습니다.")
    return redirect('Manager:login')

def detail(request, id):
    review = get_object_or_404(Review, pk=id)

    context = {
        'review': review
    }

    return render(request, 'manager_detail.html', context)