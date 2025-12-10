import json
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from member.models import Member, Individual
from stats.stats import (
    get_stats1, get_stats2, get_stats3, get_stats4, get_stats5,
    get_stats6, get_stats7, get_stats8, get_stats9,
    get_risk_analysis,get_age_group 
)


def stats_home(request):
    # 1. 로그인 체크
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    # 2. 회원 객체
    member = get_object_or_404(Member, member_id=member_id)

    member_industries = member.industries.all()
    individual_list = (
        Individual.objects
        .filter(member_industry__in=member_industries)
        .select_related('member_industry')
        .order_by('-i_accident_date', '-accident_id')
    )

    # 4. 나이 계산
    today = date.today()
    birth = member.m_birth_date
    age = today.year - birth.year - (
        (today.month, today.day) < (birth.month, birth.day)
    )

    #나이대 계산 
    age_group = get_age_group(age) 

    # 5. 선택된 산재(사고) 결정
    selected_individual = None
    industry = None

    if individual_list.exists():
        selected_accident_id = request.GET.get('accident_id')

        if selected_accident_id:
            selected_individual = (
                individual_list
                .filter(accident_id=selected_accident_id)
                .first()
            )
            if selected_individual is None:
                selected_individual = individual_list.first()
        else:
            selected_individual = individual_list.first()

        industry = selected_individual.member_industry
    else:
        # 산재가 없으면 통계 없이 렌더
        return render(request, "stats/stats.html", {
            "member": member,
            "industry": None,
            "age": age,
            "age_group": age_group,
            "individual_list": individual_list,
            "selected_individual": None,
            "summary1": None,
            "summary2": None,
            "summary3": None,
            "summary4": None,
            "summary5": None,
            "summary6_json": "null",
            "summary7_json": "null",
            "summary8_json": "null",
            "summary9_json": "null",
            "risk_analysis": None,
        })

    # 6. 업종명 추출
    industry_name1 = industry.i_industry_type2
    industry_name2 = industry.i_industry_type1
    industry_name3 = industry.i_industry_type1
    industry_name4 = industry.i_industry_type2
    industry_name5 = industry.i_industry_type2
    industry_name6 = industry.i_industry_type2
    industry_name7 = industry.i_industry_type2
    industry_name8 = industry.i_industry_type2
    industry_name9 = industry.i_industry_type2

    # 7. 통계 계산
    summary1 = get_stats1(industry_name1)
    summary2 = get_stats2(industry_name2)
    summary3 = get_stats3(industry_name3)
    summary4 = get_stats4(industry_name4)
    summary5 = get_stats5(industry_name5)
    summary6 = get_stats6(industry_name6)
    summary7 = get_stats7(industry_name7)
    summary8 = get_stats8(industry_name8)
    summary9 = get_stats9(industry_name9)

    # 8. 종합 위험도 분석 
    risk_analysis = get_risk_analysis(
        industry_name=industry.i_industry_type2,
        age=age,
        gender=member.m_sex
    )

    # 9. JS에서 사용할 데이터는 JSON 직렬화
    summary6_json = json.dumps(summary6, ensure_ascii=False)
    summary7_json = json.dumps(summary7, ensure_ascii=False)
    summary8_json = json.dumps(summary8, ensure_ascii=False)
    summary9_json = json.dumps(summary9, ensure_ascii=False)

    # 10. 템플릿 렌더링
    return render(request, "stats/stats.html", {
        "member": member,
        "industry": industry,
        "age": age,
        "age_group": age_group,
        "individual_list": individual_list,
        "selected_individual": selected_individual,
        "summary1": summary1,
        "summary2": summary2,
        "summary3": summary3,
        "summary4": summary4,
        "summary5": summary5,
        "summary6_json": summary6_json,
        "summary7_json": summary7_json,
        "summary8_json": summary8_json,
        "summary9_json": summary9_json,
        "risk_analysis": risk_analysis,  
    })