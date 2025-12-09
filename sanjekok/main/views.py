import requests
from django.shortcuts import render
from django.conf import settings
from news.models import News

def main(request):
    api_key = settings.KOSIS_API_KEY
    req_url = "https://kosis.kr/openapi/Param/statisticsParameterData.do?"

    by_age = "&itmId=16118AAD6+&objL1=ALL&objL2=ALL&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N003"
    by_gender = "&itmId=16118AAD6+&objL1=ALL&objL2=ALL&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N002"
    by_industry = "&itmId=16118AAD6_15118AI8AA+16118AAD6_15118AI8AB+16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+16118AAD6_15118AI8ACAB+16118AAD6_15118AI8ACAD+&objL1=ALL&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&orgId=118&tblId=DT_11806_N000"
    
    url_age = f"{req_url}method=getList&apiKey={api_key}{by_age}"
    url_gender = f"{req_url}method=getList&apiKey={api_key}{by_gender}"
    url_industry = f"{req_url}method=getList&apiKey={api_key}{by_industry}"

    # 연령별
    data_age = requests.get(url_age).json()

    for item in data_age:
        if item.get("C1_NM") != "총계":
            continue  # 총계가 아니면 건너뛰기

        result = float(item["DT"])
    
    # 업무별

    # 성별
    for item in data_age:
        if item.get("C1_NM") != "총계":
            continue  # 총계가 아니면 건너뛰기

        result = float(item["DT"])

    #뉴스 
    news = News.objects.order_by('-n_created_at')[:3]

    context = {
        'list' : news
    }

    return render(request, "main.html", context)