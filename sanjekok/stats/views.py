from django.shortcuts import render
from datetime import date
from member.models import Member
from stats.stats import get_stats1,get_stats2,get_stats3


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
    industry_name1 = industry.i_industry_type2
    industry_name2 = industry.i_industry_type1
    industry_name3 = industry.i_industry_type1


    summary1 = get_stats1(industry_name1)
    summary2 = get_stats2(industry_name2)
    summary3 = get_stats3(industry_name3)

    return render(request, "stats.html", {
        "member": member,
        "industry": industry,
        "age": age,
        "individual_list": individual_list,
        "summary1": summary1,
        "summary2": summary2,
        "summary3": summary3,
    })
