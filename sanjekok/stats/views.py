import json
from django.shortcuts import render
from datetime import date
from member.models import Member, Individual

from stats.stats import (
    get_stats1, get_stats2, get_stats3, get_stats4, get_stats5,
    get_stats6, get_stats7, get_stats8, get_stats9
)

def stats_home(request):
    # 연습용: member_id=4인 회원 하나 가져오기
    member = Member.objects.filter(member_id=4).first()
    if member is None:
        # 해당 회원이 없으면 로그인 페이지나 에러페이지로
        return render(request, "main/login.html", {"member": None})

    #  회원의 업종 관계에서 첫 번째 업종 가져오기
    industry = member.industries.first()
    if industry is None:
        # 업종이 아직 등록 안 된 경우
        today = date.today()
        birth = member.m_birth_date
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        return render(request, "stats/stats.html", {
            "member": member,
            "industry": None,
            "age": age,
            "individual_list": [],
            "summary1": None,
            "summary2": None,
            "summary3": None,
            "summary4": None,
            "summary5": None,
            "summary6_json": "null",
            "summary7_json": "null",
            "summary8_json": "null",
            "summary9_json": "null",
        })

    # 나이 계산
    today = date.today()
    birth = member.m_birth_date
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    # 해당 회원의 산재 리스트 (개인 산재 기록)
    individual_list = Individual.objects.filter(member_industry__member=member)

  
    industry_name1 = industry.i_industry_type2
    industry_name2 = industry.i_industry_type1
    industry_name3 = industry.i_industry_type1
    industry_name4 = industry.i_industry_type2
    industry_name5 = industry.i_industry_type2
    industry_name6 = industry.i_industry_type2
    industry_name7 = industry.i_industry_type2
    industry_name8 = industry.i_industry_type2
    industry_name9 = industry.i_industry_type2

    summary1 = get_stats1(industry_name1)
    summary2 = get_stats2(industry_name2)
    summary3 = get_stats3(industry_name3)
    summary4 = get_stats4(industry_name4)
    summary5 = get_stats5(industry_name5)
    summary6 = get_stats6(industry_name6)
    summary7 = get_stats7(industry_name7)
    summary8 = get_stats8(industry_name8)
    summary9 = get_stats9(industry_name9)

    summary6_json = json.dumps(summary6, ensure_ascii=False)
    summary7_json = json.dumps(summary7, ensure_ascii=False)
    summary8_json = json.dumps(summary8, ensure_ascii=False)
    summary9_json = json.dumps(summary9, ensure_ascii=False)

    return render(request, "stats/stats.html", {
        "member": member,
        "industry": industry,
        "age": age,
        "individual_list": individual_list,
        "summary1": summary1,
        "summary2": summary2,
        "summary3": summary3,
        "summary4": summary4,
        "summary5": summary5,
        "summary6_json": summary6_json,
        "summary7_json": summary7_json,
        "summary8_json": summary8_json,
        "summary9_json": summary9_json,
    })
