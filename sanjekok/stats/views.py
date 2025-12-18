import json
from datetime import date
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages

from member.models import Member, Individual
from stats.stats import (
    get_stats1, get_stats2, get_stats3, get_stats4, get_stats5,
    get_stats6, get_stats7, get_stats8, get_stats9,
    get_risk_analysis,get_age_group
)


INDUSTRY_TYPE2_TO_TYPE1 = {
    # 광업
    "석탄광업 및 채석업": "광업",
    "석회석·금속·비금속광업 및 기타광업": "광업",

    # 제조업
    "식료품제조업": "제조업",
    "섬유 및 섬유제품 제조업": "제조업",
    "목재 및 종이제품 제조업": "제조업",
    "출판·인쇄·제본업":"제조업",
    "화학 및 고무제품 제조업": "제조업",
    "의약품·화장품·연탄·석유제품제조업": "제조업",
    "기계기구·금속·비금속광물제품제조업": "제조업",
    "금속제련업": "제조업",
    "전기기계기구·정밀기구·전자제품제조업": "제조업",
    "선박건조 및 수리업": "제조업",
    "수제품 및 기타제품 제조업": "제조업",

    # 전기가스
    "전기·가스·증기 및 수도사업": "전기·가스·증기 및 수도사업",

    # 건설
    "건설업": "건설업",

    # 운수창고
    "철도·항공·창고·운수관련서비스업": "운수·창고 및 통신업",
    "육상 및 수상운수업": "운수·창고 및 통신업",
    "통신업": "운수·창고 및 통신업",

    # 기타
    "임업": "기타",
    "어업": "기타",
    "농업": "기타",
    "금융 및 보험업": "기타",
    "시설관리및사업지원서비스업": "기타",
    "해외파견자": "기타",
    "전문·보건·교육·여가관련서비스업": "기타",
    "도소매·음식·숙박업": "기타",
    "부동산업 및 임대업": "기타",
    "국가 및 지방자치단체의 사업": "기타",
    "주한미군": "기타",
    "기타의 각종사업": "기타",
}



def stats_home(request):
    # 1. 로그인 체크
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = Member.objects.filter(pk=member_id).first()
    if not member:
        request.session.flush()  # 세션 꼬인거/DB 비어있는거 정리
        messages.error(request, "회원 정보가 없습니다. 다시 로그인해주세요.")
        return redirect("Member:login")

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

    show_detail = bool(request.GET.get('accident_id'))

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

    industry_type2 = industry.i_industry_type2
    
    industry_type1_from_map = INDUSTRY_TYPE2_TO_TYPE1.get(industry_type2, None)

    # 6. 업종명 추출
    industry_name1 = industry.i_industry_type2 # 재해율, 사망자율
    industry_name2 = industry_type1_from_map# 성별 재해
    industry_name3 = industry_type1_from_map # 성별 사망재해
    industry_name4 = industry.i_industry_type2 # 연령대 재해
    industry_name5 = industry.i_industry_type2 # 연령대 사망
    industry_name6 = industry.i_industry_type2 # 발생형태
    industry_name7 = industry.i_industry_type2 # 발생형태 사망
    industry_name8 = industry.i_industry_type2 # 질병형태
    industry_name9 = industry.i_industry_type2 # 질병형태 사망 

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

    def convert_np(obj):
        if isinstance(obj, list):
            return [convert_np(v) for v in obj]
        elif isinstance(obj, dict):
            return {k: convert_np(v) for k, v in obj.items()}
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        else:
            return obj

    risk_analysis_1y = get_risk_analysis(
        industry_name=industry.i_industry_type2,
        age=age,
        gender=member.m_sex,
        years=1,
        member_name=member.m_name
    )
    risk_analysis_2y = get_risk_analysis(
        industry_name=industry.i_industry_type2,
        age=age,
        gender=member.m_sex,
        years=2,
        member_name=member.m_name
    )
    risk_analysis_3y = get_risk_analysis(
        industry_name=industry.i_industry_type2,
        age=age,
        gender=member.m_sex,
        years=3,
        member_name=member.m_name
    )

    risk_analysis_json = {
        "1": convert_np(risk_analysis_1y),
        "2": convert_np(risk_analysis_2y),
        "3": convert_np(risk_analysis_3y),
    }
   

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
        "risk_analysis_json": json.dumps(risk_analysis_json, ensure_ascii=False),
        "show_detail": show_detail,
    })