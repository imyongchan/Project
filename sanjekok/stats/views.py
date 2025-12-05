import json
from django.shortcuts import render
from datetime import date
from member.models import Member
from stats.stats import (
    get_stats1, get_stats2, get_stats3, get_stats4, get_stats5, get_stats6,get_stats7,get_stats8,
    get_stats9

)

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
