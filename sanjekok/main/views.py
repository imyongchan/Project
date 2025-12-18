import requests
from django.shortcuts import render
from django.conf import settings
from news.models import News
from django.shortcuts import render
from datetime import datetime, date
import locale
import calendar
import random

SAFETY_QUOTES = [
    "오늘의 안전이 내일의 일상을 지킵니다",
    "작은 부주의가 큰 사고가 됩니다",
    "안전은 선택이 아니라 기본입니다",
    "익숙함이 가장 위험합니다",
    "오늘도 무사고, 그것이 최고의 성과입니다",
    "당신의 안전이 가족의 행복입니다",
    "안전에는 베테랑이 없습니다",
    "안전은 끝이 아니라 시작입니다",
    "찾았다 위험! 보인다 안전!",
    "작업 전 안전점검은 생명을 지키는 습관입니다",
    "내 일을 위한 위험성 평가는 나를 위한 준비입니다",
    "오늘의 안전, 내일의 행복",
]
def get_today_safety_quote():
    seed = date.today().toordinal()
    random.seed(seed)
    return random.choice(SAFETY_QUOTES)

def main(request):
    api_key = settings.KOSIS_API_KEY
    req_url = "https://kosis.kr/openapi/Param/statisticsParameterData.do?"


    by_age = "&itmId=16118AAD6+&objL1=ALL&objL2=ALL&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N003"
    by_gender = "&itmId=16118AAD6+&objL1=ALL&objL2=ALL&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N002"
    by_industry = "&itmId=16118AAD6_15118AI8AA+16118AAD6_15118AI8AB+16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+16118AAD6_15118AI8ACAB+16118AAD6_15118AI8ACAD+&objL1=ALL&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N000"
   
    url_age = f"{req_url}method=getList&apiKey={api_key}{by_age}"
    url_gender = f"{req_url}method=getList&apiKey={api_key}{by_gender}"
    url_industry = f"{req_url}method=getList&apiKey={api_key}{by_industry}"


    # ===== 1) 연령별 =====
    data_age = requests.get(url_age).json()


    # 연령대별 합계 초기화
    age_total = {}


    for item in data_age:
        industry = item["C1_NM"]      # 산업명
        age_group = item["C2_NM"]     # 연령대
        year = int(item["PRD_DE"])    # 연도
        value = int(float(item["DT"]))  # 값


        # 총계 산업 제외, 2021~2023년만
        if industry == "총계" or year < 2021 or year > 2023:
            continue


        if age_group != "50~54세" and age_group != "55~59세" and age_group != "60세 이상":
            continue


        if age_group not in age_total:
            age_total[age_group] = 0


        age_total[age_group] += value




    # ===== 2) 산업별 =====
    data_industry = requests.get(url_industry).json()


    industry_total = {}


    for item in data_industry:
        industry = item["C1_NM"]   # 제조업, 건설업 등
        kind = item["ITM_NM"]
        value = int(float(item["DT"]))


        if industry not in ("광업", "제조업", "건설업", "어업", "농업"):
            continue


        # 재해자수만
        if kind != "재해자수":
            continue


        if industry not in industry_total:
            industry_total[industry] = 0


        industry_total[industry] += value  # 여기서 바로 더함








    # ===== 3) 성별 =====
    data_gender = requests.get(url_gender).json()


        # 결과 구조 초기화
    gender_total = {"남자": 0, "여자": 0}


    for item in data_gender:
        c1 = item["C1_NM"]  # 총계
        c2 = item["C2_NM"]  # 남자/여자
        value = int(float(item["DT"]))


        # 총계 + 성별만
        if c1 == "총계" and c2 in ["남자", "여자"]:
            gender_total[c2] += value


   
    #시계
    now = datetime.now()  


    #뉴스
    news = News.objects.order_by('-n_created_at')[:8]


    # 캘린더


    now = datetime.now()
    year = now.year
    month = now.month


    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]


    fixed_holidays = {
        (1, 1): "신정",
        (3, 1): "삼일절",
        (5, 5): "어린이날",
        (6, 6): "현충일",
        (8, 15): "광복절",
        (10, 3): "개천절",
        (10, 9): "한글날",
        (12, 25): "성탄절",
    }


    holidays = {}
    for (m, d), name in fixed_holidays.items():
        if m == month:
            holidays[d] = name


    calendar_with_holidays = []


    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                week_data.append({
                    "day": day,
                    "holiday": holidays.get(day)
                })
        calendar_with_holidays.append(week_data)

    # 오늘의 안전글귀
    today_quote = get_today_safety_quote()
    
    context = {
        "gender_total": gender_total,
        "age_total": age_total,
        "industry_total": industry_total,
        'list' : news,
        "now": now,
        "year": year,
        "month_name": month_name,
        "calendar": calendar_with_holidays,
        "today_quote": today_quote,   # ✅ 추가
    }


    return render(request, "main.html", context)


def service(request):
    return render(request, "intro_service.html")


def tech(request):
    return render(request, "intro_tech.html")
