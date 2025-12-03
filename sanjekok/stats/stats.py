# stats/stats.py
import pandas as pd
import requests
from django.conf import settings


def get_industry_accident_stats(industry_name):
    API_KEY = settings.KOSIS_API_KEY

    json_URL = (
        "https://kosis.kr/openapi/Param/statisticsParameterData.do"
        f"?method=getList&apiKey={API_KEY}"
        "&itmId=16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+"
        "16118AAD6_15118AI8ACAB+16118AAD6_15118AI8ACAD+"
        "&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+"
        "15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+"
        "15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAC+15118AI7ABAC00+"
        "15118AI7ABAC000+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+"
        "15118AI7ABAE+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+"
        "15118AI7ABAH00+15118AI7ABAJ+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+"
        "15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+"
        "15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+"
        "15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+"
        "15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+"
        "15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAZ00+15118AI7ABAX+"
        "15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7ACAA00+15118AI7AD+"
        "15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+"
        "15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+"
        "15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+"
        "15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+"
        "15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+"
        "15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+"
        "15118AI7AJAB+15118AI7AJAC+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+"
        "15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+"
        "15118AI7ACAA01+15118AI7ACAA02+15118AI7ACAA03+15118AI7AJAJ+15118AI7AJAD+"
        "&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8="
        "&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023"
        "&outputFields=NM+ITM_NM+PRD_DE+LST_CHN_DE+&orgId=118&tblId=DT_11806_N000"
    )

    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    # 업종으로 필터 (여기서 industry_name이 C1_NM과 정확히 일치해야 데이터가 나옴)
    df_industry = df[df["C1_NM"] == industry_name]

    
    pivot = (
        df_industry
        .pivot_table(
            index="PRD_DE",
            columns="ITM_NM",
            values="DT",
            aggfunc="sum",  
        )
    )

    # 필요한 컬럼만 / 없으면 0으로 채우기
    cols = ["재해자수", "재해율", "사망자수", "사망만인율"]
    pivot = pivot.reindex(columns=cols, fill_value=0).reset_index()

    # year 컬럼 이름 맞추기
    pivot = pivot.rename(columns={"PRD_DE": "year"})

    # [{year: ..., 재해자수: ..., 재해율: ..., 사망자수: ..., 사망만인율: ...}, ...]
    stats_by_year = pivot.to_dict("records")
    return stats_by_year
