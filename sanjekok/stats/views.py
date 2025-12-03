from django.shortcuts import render
from datetime import date
from member.models import Member
from stats.stats import get_industry_accident_stats


def stats_home(request):
    member = Member.objects.first()
    industry = member.industries.first()

    # 나이 계산
    today = date.today()
    birth = member.m_birth_date
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    # 해당 회원의 산재 리스트
    individual_list = member.individuals.all()

    # stats.py의 피벗테이블 딕셔너리
    # [{year: ..., 재해자수: ..., 재해율: ..., 사망자수: ..., 사망만인율: ...}, ...]
    industry_name = industry.i_industry_type2

    # 업종별 연도/지표 데이터
    stats_by_year = get_industry_accident_stats(industry_name)

    return render(request, "stats.html", {
        "member": member,
        "industry": industry,
        "age": age,
        "individual_list": individual_list,
        "stats_by_year": stats_by_year,
    })
