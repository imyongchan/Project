import pandas as pd
import requests
from django.conf import settings

API_KEY = settings.KOSIS_API_KEY

# 업종별 재해자수, 재해율, 사망자수, 사망만인율
def get_stats1(industry_name1):
    
    json_URL = (
        f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+16118AAD6_15118AI8ACAB+16118AAD6_15118AI8ACAD+&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAC+15118AI7ABAC00+15118AI7ABAC000+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+15118AI7ABAE+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+15118AI7ABAH00+15118AI7ABAJ+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAZ00+15118AI7ABAX+15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7ACAA00+15118AI7AD+15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+15118AI7AJAB+15118AI7AJAC+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+15118AI7ACAA01+15118AI7ACAA02+15118AI7ACAA03+15118AI7AJAJ+15118AI7AJAD+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=NM+ITM_NM+PRD_DE+LST_CHN_DE+&orgId=118&tblId=DT_11806_N000"
    )

    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    # 업종으로 필터 
    df_industry = df[df["C1_NM"] == industry_name1]


    pivot = (
                df_industry.pivot_table(
                    index="PRD_DE",        
                    columns="ITM_NM",      # 재해자수 / 사망자수 / 재해율 / 사망만인율
                    values="DT",
                    aggfunc="sum"
                ))

    pivot = pivot.sort_index()

    years = pivot.index.to_list()   # [2021, 2022, 2023] 
    y1, y2, y3 = years[-1], years[-2], years[-3]   #y1=2023, y2=2022, y3=2021

    rows = []

    #최근 1년 : y1만 사용
    sub = pivot.loc[[y1]]
    rows.append({
            "기간": "최근 1년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": sub["재해율"].mean().round(2),
            "사망자수": int(sub["사망자수"].sum()),
            "사망만인율": sub["사망만인율"].mean().round(2),
    })

    #최근 2년 : y2,y1만 사용
    sub = pivot.loc[[y2,y1]]
    rows.append({
            "기간": "2년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": sub["재해율"].mean().round(2),
            "사망자수": int(sub["사망자수"].sum()),
            "사망만인율": sub["사망만인율"].mean().round(2),
    })

    #최근 3년 : y3,y2,y1만 사용
    sub = pivot.loc[[y3,y2,y1]]
    rows.append({
            "기간": "3년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": sub["재해율"].mean().round(2),
            "사망자수":int(sub["사망자수"].sum()),
            "사망만인율": sub["사망만인율"].mean().round(2),
    })

    summary = pd.DataFrame(rows).set_index("기간")
    summary1 = summary.to_dict("records")
    return summary1 
    # [{기간: ..., 재해자수: ..., 재해율: ..., 사망자수: ..., 사망만인율: ...}, ...]




# 업종별 성별 재해
def get_stats2(industry_name2):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AB+15118AI7AC+15118AI7AC00+15118AI7AD+15118AI7AE+15118AI7AJ+&objL2=11101SSB21+11101SSB22+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N002")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name2]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))

    pivot['전체']=pivot['남자']+pivot['여자']
    pivot["남자비율"] = (pivot["남자"] / pivot["전체"] * 100).round(2)
    pivot["여자비율"] = (pivot["여자"] / pivot["전체"] * 100).round(2)

    pivot = pivot.sort_index()

    years = pivot.index.to_list()   # [2021, 2022, 2023] 
    y1, y2, y3 = years[-1], years[-2], years[-3]   #y1=2023, y2=2022, y3=2021

    rows = []

    # 1) 최근 1년 : y1만 사용
    sub = pivot.loc[[y1]]
    rows.append({
        "기간": "최근 1년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),   
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 2) 최근 2년 : y1 + y2
    sub = pivot.loc[[y2, y1]]
    rows.append({
        "기간": "2년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),  
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 3) 최근 3년 : y1 + y2 + y3
    sub = pivot.loc[[y3, y2, y1]]
    rows.append({
        "기간": "3년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 원하는 형태의 새 테이블 생성
    summary = pd.DataFrame(rows).set_index("기간")
    summary2 = summary.to_dict("records")
    return summary2 
    # [{기간: 남자,여자,전체,남자비율,여자비율}]


    # 업종별 성별 사망 재해
def get_stats3(industry_name3):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AB+15118AI7AC+15118AI7AC01+15118AI7AD+15118AI7AE+15118AI7AJ+&objL2=11101SSB21+11101SSB22+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N014")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name3]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))

    pivot['전체']=pivot['남자']+pivot['여자']
    pivot["남자비율"] = (pivot["남자"] / pivot["전체"] * 100).round(2)
    pivot["여자비율"] = (pivot["여자"] / pivot["전체"] * 100).round(2)

    pivot = pivot.sort_index()

    years = pivot.index.to_list()   # [2021, 2022, 2023] 
    y1, y2, y3 = years[-1], years[-2], years[-3]   #y1=2023, y2=2022, y3=2021

    rows = []

    # 1) 최근 1년 : y1만 사용
    sub = pivot.loc[[y1]]
    rows.append({
        "기간": "최근 1년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),   
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 2) 최근 2년 : y1 + y2
    sub = pivot.loc[[y2, y1]]
    rows.append({
        "기간": "2년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),  
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 3) 최근 3년 : y1 + y2 + y3
    sub = pivot.loc[[y3, y2, y1]]
    rows.append({
        "기간": "3년",
        "남자": int(sub["남자"].sum()),
        "여자": int(sub["여자"].sum()),
        "전체": int(sub["전체"].sum()),
        "남자비율": sub["남자비율"].mean().round(2),
        "여자비율": sub["여자비율"].mean().round(2),
    })

    # 원하는 형태의 새 테이블 생성
    summary = pd.DataFrame(rows).set_index("기간")
    summary3 = summary.to_dict("records")
    return summary3
    # [{기간: 남자,여자,전체,남자비율,여자비율}]


# 연령별 재해현황 
def get_stats4(industry_name4):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAC+15118AI7AC00+15118AI7AC000+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+15118AI7ABAE+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+15118AI7ABAH00+15118AI7ABAJ+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAZ00+15118AI7ABAX+15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7AC01+15118AI7AD+15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+15118AI7AJAB+15118AI7AJAC+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+15118AI7AC02+15118AI7AC03+15118AI7AC030+15118AI7AJAJ+15118AI7AJAD+&objL2=15118AC1AM+15118AC1AN+15118AC1AO+15118AC1AP+15118AC1AQ+15118AC1AR+15118AC1AT+15118AC1AF+15118AC1AG+15118AC1AH+15118AC1AI+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N003")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name4]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))
    
    pivot=pivot.drop('분류불능',axis=1)
    age_pivot = pd.DataFrame(index=pivot.index)

    age_pivot["18세 미만"] = pivot.get("18세 미만", 0)
    age_pivot["20대"] = (
        pivot.get("18~24세", 0) +
        pivot.get("25~29세", 0)
    )
    age_pivot["30대"] = (
        pivot.get("30~34세", 0) +
        pivot.get("35~39세", 0)
    )
    age_pivot["40대"] = (
        pivot.get("40~44세", 0) +
        pivot.get("45~49세", 0)
    )
    age_pivot["50대"] = (
        pivot.get("50~54세", 0) +
        pivot.get("55~59세", 0)
    )
    age_pivot["60대 이상"] = pivot.get("60세 이상", 0)

    age_pivot

    pivot = age_pivot.sort_index()

    years = pivot.index.to_list()   # [2021, 2022, 2023] 
    y1, y2, y3 = years[-1], years[-2], years[-3]   #y1=2023, y2=2022, y3=2021

    rows = []

    # 1) 최근 1년 : y1만 사용
    sub = pivot.loc[[y1]]
    rows.append({
        "기간": "최근 1년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 2) 최근 2년 : y1 + y2
    sub = pivot.loc[[y2,y1]]
    rows.append({
        "기간": "2년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 3) 최근 3년 : y1 + y2 + y3
    sub = pivot.loc[[y3,y2,y1]]
    rows.append({
        "기간": "3년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 원하는 형태의 새 테이블 생성
    summary = pd.DataFrame(rows).set_index("기간")
    summary4 = summary.to_dict("records")
    return summary4
    # [{기간: 18세 미만,10대,20대,30대,40대,50대,60대 이상}]


# 연령별 사망 재해현황 
def get_stats5(industry_name5):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAC+15118AI7AC00+15118AI7AC000+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+15118AI7ABAE+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+15118AI7ABAH00+15118AI7ABAJ+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAZ00+15118AI7ABAX+15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7AC01+15118AI7AD+15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+15118AI7AJAB+15118AI7AJAC+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+15118AI7AC02+15118AI7AC03+15118AI7AC030+15118AI7AJAJ+15118AI7AJAD+&objL2=15118AC1AM+15118AC1AN+15118AC1AO+15118AC1AP+15118AC1AQ+15118AC1AR+15118AC1AT+15118AC1AF+15118AC1AG+15118AC1AH+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N015")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name5]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))
    
    age_pivot = pd.DataFrame(index=pivot.index)

    age_pivot["18세 미만"] = pivot.get("18세 미만", 0)
    age_pivot["20대"] = (
        pivot.get("18~24세", 0) +
        pivot.get("25~29세", 0)
    )
    age_pivot["30대"] = (
        pivot.get("30~34세", 0) +
        pivot.get("35~39세", 0)
    )
    age_pivot["40대"] = (
        pivot.get("40~44세", 0) +
        pivot.get("45~49세", 0)
    )
    age_pivot["50대"] = (
        pivot.get("50~54세", 0) +
        pivot.get("55~59세", 0)
    )
    age_pivot["60대 이상"] = pivot.get("60세 이상", 0)

    age_pivot

    pivot = age_pivot.sort_index()

    years = pivot.index.to_list()   # [2021, 2022, 2023] 
    y1, y2, y3 = years[-1], years[-2], years[-3]   #y1=2023, y2=2022, y3=2021

    rows = []

    # 1) 최근 1년 : y1만 사용
    sub = pivot.loc[[y1]]
    rows.append({
        "기간": "최근 1년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 2) 최근 2년 : y1 + y2
    sub = pivot.loc[[y2,y1]]
    rows.append({
        "기간": "2년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 3) 최근 3년 : y1 + y2 + y3
    sub = pivot.loc[[y3,y2,y1]]
    rows.append({
        "기간": "3년",
        "18세미만": sub["18세 미만"].sum(),
        "20대": sub["20대"].sum(),
        "30대": sub["30대"].sum(),
        "40대": sub["40대"].sum(),
        "50대": sub["50대"].sum(),
        "60대이상": sub["60대 이상"].sum(),

    })

    # 원하는 형태의 새 테이블 생성
    summary = pd.DataFrame(rows).set_index("기간")
    summary5 = summary.to_dict("records")
    return summary5
    # [{기간: 18세 미만,10대,20대,30대,40대,50대,60대 이상}]


# 발생형태별  
def get_stats6(industry_name6):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAB0+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+15118AI7ABAH00+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAJ+15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7AD+15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+15118AI7AJAB+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+15118AI7AJAI00+15118AI7AJAI01+15118AI7AJAI010+15118AI7AJAJ+15118AI7AJAD+&objL2=15118AJ401+15118AJ402+15118AJ403+15118AJ404+15118AJ405+15118AJ406+15118AJ407+15118AJ408+15118AJ409+15118AJ410+15118AJ411+15118AJ412+15118AJ413+15118AJ414+15118AJ415+15118AJ416+15118AJ417+15118AJ418+15118AJ422+15118AJ423+15118AJ419+15118AJ420+15118AJ421+15118AJ424+15118AJ425+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N011")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name6]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))
    
    pivot = pivot.fillna(0).sort_index()
    years = pivot.index.to_list()   # 예: ['2021', '2022', '2023']

    rows = []

    def add_row(n_years: int, label: str):
            use_years = years[-n_years:]       # 마지막 n_years개 연도
            sub = pivot.loc[use_years]
            s = sub.sum(axis=0)                # 발생형태별 합계
            s["기간"] = label
            rows.append(s)

        
    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        sorted_row = row.sort_values(ascending=False)

        top10 = sorted_row.head(10)

        top10_list = []
        for rank, (name, cnt) in enumerate(top10.items(), start=1):
            top10_list.append({
                "rank": rank,
                "name": name,
                "count": int(cnt),
            })

        rank_series = row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
            "rank_map": rank_map,
        }

    return result
            

# 발생형태 사망별  
def get_stats7(industry_name7):
    json_URL = (f"https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}&itmId=16118AAD6+&objL1=15118AI7AA+15118AI7AAAF+15118AI7AAAG+15118AI7AAAA+15118AI7AAAB+15118AI7AAAC+15118AI7AAAD+15118AI7AAAE+15118AI7AB+15118AI7ABAA+15118AI7ABAn+15118AI7ABAo+15118AI7ABAoo+15118AI7ABAB+15118AI7ABAB0+15118AI7ABAp+15118AI7ABAp0+15118AI7ABAD+15118AI7ABAD0+15118AI7ABAF+15118AI7ABAF0+15118AI7ABAH+15118AI7ABAH0+15118AI7ABAH00+15118AI7ABAG+15118AI7ABAq+15118AI7ABAq0+15118AI7ABAK+15118AI7ABAK0+15118AI7ABAM+15118AI7ABAr+15118AI7ABAr0+15118AI7ABAr00+15118AI7ABAr000+15118AI7ABAL+15118AI7ABAN+15118AI7ABAO+15118AI7ABAP+15118AI7ABAQ+15118AI7ABAQ0+15118AI7ABAQ00+15118AI7ABAR+15118AI7ABAS+15118AI7ABAT+15118AI7ABAT0+15118AI7ABAU+15118AI7ABAV+15118AI7ABAV0+15118AI7ABAY+15118AI7ABAZ+15118AI7ABAJ+15118AI7ABAs+15118AI7AC+15118AI7ACAA+15118AI7AD+15118AI7ADAB+15118AI7AE+15118AI7AEAA+15118AI7AEAA0+15118AI7AEAA00+15118AI7AEAN+15118AI7AEAN0+15118AI7AEAB+15118AI7AEAC+15118AI7AEAF+15118AI7AEAH+15118AI7AEAI+15118AI7AEAI0+15118AI7AEAJ+15118AI7AEAK+15118AI7AEAM+15118AI7AF+15118AI7AFAA+15118AI7AG+15118AI7AGAC+15118AI7AGAA+15118AI7AGAB+15118AI7AH+15118AI7AHAA+15118AI7AK+15118AI7AKAA+15118AI7AJ+15118AI7AJAA+15118AI7AJAA0+15118AI7AJAA00+15118AI7AJAB+15118AI7AJAL+15118AI7AJAE+15118AI7AJAE0+15118AI7AJAF+15118AI7AJAG+15118AI7AJAH+15118AI7AJAH0+15118AI7AJAI+15118AI7AJAI00+15118AI7AJAI01+15118AI7AJAI010+15118AI7AJAJ+15118AI7AJAD+&objL2=15118AJ401+15118AJ402+15118AJ403+15118AJ404+15118AJ405+15118AJ406+15118AJ407+15118AJ408+15118AJ409+15118AJ410+15118AJ411+15118AJ412+15118AJ413+15118AJ414+15118AJ415+15118AJ416+15118AJ417+15118AJ418+15118AJ422+15118AJ423+15118AJ419+15118AJ420+15118AJ421+15118AJ424+15118AJ425+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2021&endPrdDe=2023&outputFields=OBJ_NM+NM+ITM_NM+PRD_DE+&orgId=118&tblId=DT_11806_N022")
    
    response = requests.get(json_URL)
    data = response.json()

    df = pd.json_normalize(data)
    df["DT"] = df["DT"].astype(float)

    df_industry = df[df["C1_NM"] == industry_name7]

    pivot = (
        df_industry .pivot_table(
            index="PRD_DE",        
            columns="C2_NM",    
            values="DT",
            aggfunc="sum"
        ))
    
    pivot = pivot.fillna(0).sort_index()
    years = pivot.index.to_list()   # 예: ['2021', '2022', '2023']

    rows = []

    def add_row(n_years: int, label: str):
            use_years = years[-n_years:]       # 마지막 n_years개 연도
            sub = pivot.loc[use_years]
            s = sub.sum(axis=0)                # 발생형태별 합계
            s["기간"] = label
            rows.append(s)

        
    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        sorted_row = row.sort_values(ascending=False)

        top10 = sorted_row.head(10)

        top10_list = []
        for rank, (name, cnt) in enumerate(top10.items(), start=1):
            top10_list.append({
                "rank": rank,
                "name": name,
                "count": int(cnt),
            })

        rank_series = row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
            "rank_map": rank_map,
        }

    return result
            
