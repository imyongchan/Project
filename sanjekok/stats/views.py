from django.shortcuts import render
from datetime import date
from member.models import Member
from stats.stats import get_industry_accident_stats



def stats_home(request):
    member = Member.objects.first()
    industry = member.industries.first()

    # 업종명
    industry_name = industry.i_industry_type2

    # KOSIS API 업종별 재해자수 가져오기
    stats_by_year = get_industry_accident_stats(industry_name)

  
    # 나이 계산
    today = date.today()
    birth = member.m_birth_date
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    # ✔ 해당 회원의 산재 리스트 가져오기
    individual_list = member.individuals.all()

    
    
    return render(request, "stats.html", {
        "member": member,
        "industry": industry,
        "age": age,
        "individual_list": individual_list,
        "stats_by_year": stats_by_year,

    })
