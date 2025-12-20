import pandas as pd
import math
from .models import (
    Stats1, Stats2, Stats3, Stats4, Stats5,
    Stats6, Stats7, Stats8, Stats9,
)



# 업종별 재해자수, 재해율, 사망자수, 사망만인율
def get_stats1(industry_name1):
    # DB에서 해당 업종 데이터만 가져오기
    qs = Stats1.objects.filter(c1_nm=industry_name1)

    if not qs.exists():
        return []

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "itm_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",         # 연도
            columns="itm_nm",       # 재해자수 / 사망자수 / 재해율 / 사망만인율
            values="dt",
            aggfunc="sum",
        )
        .sort_index()
    )

    years = sorted(pivot.index.to_list())  # 예: [2021, 2022, 2023]
    rows = []

    # 최근 1년
    if len(years) >= 1:
        y1 = years[-1]
        sub = pivot.loc[[y1]]
        rows.append({
            "기간": "최근 1년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": float(sub["재해율"].mean().round(2)),
            "사망자수": int(sub["사망자수"].sum()),
            "사망만인율": float(sub["사망만인율"].mean().round(2)),
        })

    # 최근 2년
    if len(years) >= 2:
        y1, y2 = years[-1], years[-2]
        sub = pivot.loc[[y2, y1]]
        rows.append({
            "기간": "2년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": float(sub["재해율"].mean().round(2)),
            "사망자수": int(sub["사망자수"].sum()),
            "사망만인율": float(sub["사망만인율"].mean().round(2)),
        })

    # 최근 3년
    if len(years) >= 3:
        y1, y2, y3 = years[-1], years[-2], years[-3]
        sub = pivot.loc[[y3, y2, y1]]
        rows.append({
            "기간": "3년",
            "재해자수": int(sub["재해자수"].sum()),
            "재해율": float(sub["재해율"].mean().round(2)),
            "사망자수": int(sub["사망자수"].sum()),
            "사망만인율": float(sub["사망만인율"].mean().round(2)),
        })

    summary1 = pd.DataFrame(rows).set_index("기간")
    return summary1.to_dict("records")



# 업종별 성별 재해
def get_stats2(industry_name2):
    qs = Stats2.objects.filter(c1_nm=industry_name2)

    if not qs.exists():
        return []

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",    # 남자 / 여자
            values="dt",
            aggfunc="sum",
        )
        .sort_index()
    )

    # 전체, 비율 계산
    pivot["전체"] = pivot.get("남자", 0) + pivot.get("여자", 0)
    pivot["남자비율"] = (pivot.get("남자", 0) / pivot["전체"] * 100).round(2)
    pivot["여자비율"] = (pivot.get("여자", 0) / pivot["전체"] * 100).round(2)

    years = sorted(pivot.index.to_list())
    rows = []

    if len(years) >= 1:
        y1 = years[-1]
        sub = pivot.loc[[y1]]
        rows.append({
            "기간": "최근 1년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    if len(years) >= 2:
        y1, y2 = years[-1], years[-2]
        sub = pivot.loc[[y2, y1]]
        rows.append({
            "기간": "2년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    if len(years) >= 3:
        y1, y2, y3 = years[-1], years[-2], years[-3]
        sub = pivot.loc[[y3, y2, y1]]
        rows.append({
            "기간": "3년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    summary2 = pd.DataFrame(rows).set_index("기간")
    return summary2.to_dict("records")


def get_stats3(industry_name3):
    qs = Stats3.objects.filter(c1_nm=industry_name3)


    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",
            values="dt",
            aggfunc="sum",
        )
        .sort_index()
    )

    pivot["전체"] = pivot.get("남자", 0) + pivot.get("여자", 0)
    pivot["남자비율"] = (pivot.get("남자", 0) / pivot["전체"] * 100).round(2)
    pivot["여자비율"] = (pivot.get("여자", 0) / pivot["전체"] * 100).round(2)

    years = sorted(pivot.index.to_list())
    rows = []

    if len(years) >= 1:
        y1 = years[-1]
        sub = pivot.loc[[y1]]
        rows.append({
            "기간": "최근 1년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    if len(years) >= 2:
        y1, y2 = years[-1], years[-2]
        sub = pivot.loc[[y2, y1]]
        rows.append({
            "기간": "2년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    if len(years) >= 3:
        y1, y2, y3 = years[-1], years[-2], years[-3]
        sub = pivot.loc[[y3, y2, y1]]
        rows.append({
            "기간": "3년",
            "남자": int(sub["남자"].sum()),
            "여자": int(sub["여자"].sum()),
            "전체": int(sub["전체"].sum()),
            "남자비율": float(sub["남자비율"].mean().round(2)),
            "여자비율": float(sub["여자비율"].mean().round(2)),
        })

    summary3 = pd.DataFrame(rows).set_index("기간")
    return summary3.to_dict("records")


# 연령별 재해현황 
def get_stats4(industry_name4):
    qs = Stats4.objects.filter(c1_nm=industry_name4)

    if not qs.exists():
        return []

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",   
            values="dt",
            aggfunc="sum",
        )
        .sort_index()
    )

    # '분류불능' 있으면 제거
    pivot = pivot.drop(columns=["분류불능"], errors="ignore")

    age_pivot = pd.DataFrame(index=pivot.index)

    age_pivot["18세 미만"] = pivot.get("18세 미만", 0)
    age_pivot["20대"] = pivot.get("18~24세", 0) + pivot.get("25~29세", 0)
    age_pivot["30대"] = pivot.get("30~34세", 0) + pivot.get("35~39세", 0)
    age_pivot["40대"] = pivot.get("40~44세", 0) + pivot.get("45~49세", 0)
    age_pivot["50대"] = pivot.get("50~54세", 0) + pivot.get("55~59세", 0)
    age_pivot["60대 이상"] = pivot.get("60세 이상", 0)

    pivot = age_pivot.sort_index()
    years = sorted(pivot.index.to_list())
    rows = []

    if len(years) >= 1:
        y1 = years[-1]
        sub = pivot.loc[[y1]]
        rows.append({
            "기간": "최근 1년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    if len(years) >= 2:
        y1, y2 = years[-1], years[-2]
        sub = pivot.loc[[y2, y1]]
        rows.append({
            "기간": "2년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    if len(years) >= 3:
        y1, y2, y3 = years[-1], years[-2], years[-3]
        sub = pivot.loc[[y3, y2, y1]]
        rows.append({
            "기간": "3년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    summary4 = pd.DataFrame(rows).set_index("기간")
    return summary4.to_dict("records")


# 연령별 사망 재해현황 
def get_stats5(industry_name5):
    qs = Stats5.objects.filter(c1_nm=industry_name5)

    if not qs.exists():
        return []

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",
            values="dt",
            aggfunc="sum",
        )
        .sort_index()
    )

    age_pivot = pd.DataFrame(index=pivot.index)

    age_pivot["18세 미만"] = pivot.get("18세 미만", 0)
    age_pivot["20대"] = pivot.get("18~24세", 0) + pivot.get("25~29세", 0)
    age_pivot["30대"] = pivot.get("30~34세", 0) + pivot.get("35~39세", 0)
    age_pivot["40대"] = pivot.get("40~44세", 0) + pivot.get("45~49세", 0)
    age_pivot["50대"] = pivot.get("50~54세", 0) + pivot.get("55~59세", 0)
    age_pivot["60대 이상"] = pivot.get("60세 이상", 0)

    pivot = age_pivot.sort_index()
    years = sorted(pivot.index.to_list())
    rows = []

    if len(years) >= 1:
        y1 = years[-1]
        sub = pivot.loc[[y1]]
        rows.append({
            "기간": "최근 1년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    if len(years) >= 2:
        y1, y2 = years[-1], years[-2]
        sub = pivot.loc[[y2, y1]]
        rows.append({
            "기간": "2년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    if len(years) >= 3:
        y1, y2, y3 = years[-1], years[-2], years[-3]
        sub = pivot.loc[[y3, y2, y1]]
        rows.append({
            "기간": "3년",
            "18세미만": int(sub["18세 미만"].sum()),
            "20대": int(sub["20대"].sum()),
            "30대": int(sub["30대"].sum()),
            "40대": int(sub["40대"].sum()),
            "50대": int(sub["50대"].sum()),
            "60대이상": int(sub["60대 이상"].sum()),
        })

    summary5 = pd.DataFrame(rows).set_index("기간")
    return summary5.to_dict("records")


# 발생형태별  
def get_stats6(industry_name6):
    qs = Stats6.objects.filter(c1_nm=industry_name6)

    if not qs.exists():
        return {}

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",    # 발생형태명
            values="dt",
            aggfunc="sum",
        )
        .fillna(0)
        .sort_index()
    )

    years = sorted(pivot.index.to_list())
    rows = []

    def add_row(n_years: int, label: str):
        if len(years) < 1:
            return
        use_years = years[-n_years:] if len(years) >= n_years else years
        sub = pivot.loc[use_years]
        s = sub.sum(axis=0)
        s["기간"] = label
        rows.append(s)

    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    if not rows:
        return {}

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        # 기간 컬럼 제거 후, 0보다 큰 것만 상위 7개
        numeric_row = row.drop(labels=[], errors="ignore")
        filtered_row = numeric_row[numeric_row > 0].sort_values(ascending=False)
        top7 = filtered_row.head(7)

        top7_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top7.items():
            top7_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top7": top7_list,
            "rank_map": rank_map,
        }

    return result
            

# 발생형태 사망별  
def get_stats7(industry_name7):
    qs = Stats7.objects.filter(c1_nm=industry_name7)

    if not qs.exists():
        return {}

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )

    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",
            values="dt",
            aggfunc="sum",
        )
        .fillna(0)
        .sort_index()
    )

    years = sorted(pivot.index.to_list())
    rows = []

    def add_row(n_years: int, label: str):
        if len(years) < 1:
            return
        use_years = years[-n_years:] if len(years) >= n_years else years
        sub = pivot.loc[use_years]
        s = sub.sum(axis=0)
        s["기간"] = label
        rows.append(s)

    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    if not rows:
        return {}

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        numeric_row = row.drop(labels=[], errors="ignore")
        filtered_row = numeric_row[numeric_row > 0].sort_values(ascending=False)
        top7 = filtered_row.head(7)

        top7_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top7.items():
            top7_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top7": top7_list,
            "rank_map": rank_map,
        }

    return result




# 질병 유형별  
def get_stats8(industry_name8):
    qs = Stats8.objects.filter(c1_nm=industry_name8)

    if not qs.exists():
        return {}

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )
    df = df[~df["c2_nm"].isin(["직업병", "작업관련성 질병"])]
    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",    # 질병 유형명
            values="dt",
            aggfunc="sum",
        )
        .fillna(0)
        .sort_index()
    )

    years = sorted(pivot.index.to_list())
    rows = []

    def add_row(n_years: int, label: str):
        if len(years) < 1:
            return
        use_years = years[-n_years:] if len(years) >= n_years else years
        sub = pivot.loc[use_years]
        s = sub.sum(axis=0)
        s["기간"] = label
        rows.append(s)

    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    if not rows:
        return {}

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        numeric_row = row.drop(labels=[], errors="ignore")
        filtered_row = numeric_row[numeric_row > 0].sort_values(ascending=False)
        top7 = filtered_row.head(7)

        top7_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top7.items():
            top7_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top7": top7_list,
            "rank_map": rank_map,
        }

    return result
            
# 질병 사망유형별  
def get_stats9(industry_name9):
    qs = Stats9.objects.filter(c1_nm=industry_name9)

    if not qs.exists():
        return {}

    df = pd.DataFrame.from_records(
        qs.values("prd_de", "c2_nm", "dt")
    )
    df = df[~df["c2_nm"].isin(["직업병", "작업관련성 질병"])]
    pivot = (
        df.pivot_table(
            index="prd_de",
            columns="c2_nm",
            values="dt",
            aggfunc="sum",
        )
        .fillna(0)
        .sort_index()
    )

    years = sorted(pivot.index.to_list())
    rows = []

    def add_row(n_years: int, label: str):
        if len(years) < 1:
            return
        use_years = years[-n_years:] if len(years) >= n_years else years
        sub = pivot.loc[use_years]
        s = sub.sum(axis=0)
        s["기간"] = label
        rows.append(s)

    add_row(1, "최근 1년")
    add_row(2, "2년")
    add_row(3, "3년")

    if not rows:
        return {}

    summary = pd.DataFrame(rows).set_index("기간")
    result = {}

    for period, row in summary.iterrows():
        numeric_row = row.drop(labels=[], errors="ignore")
        filtered_row = numeric_row[numeric_row > 0].sort_values(ascending=False)
        top7 = filtered_row.head(7)

        top7_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top7.items():
            top7_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top7": top7_list,
            "rank_map": rank_map,
        }

    return result

#종합 위험도 분석 
#----------------------------------------------------------------------------------
def get_age_group(age):
    """나이를 연령대 그룹으로 변환"""
    if age < 18:
        return "18세미만"
    elif 18 <= age < 30:
        return "20대"
    elif 30 <= age < 40:
        return "30대"
    elif 40 <= age < 50:
        return "40대"
    elif 50 <= age < 60:
        return "50대"
    else:
        return "60대이상"


def _calculate_gender_weight(industry_name, gender, years):
    qs2 = Stats2.objects.filter(c1_nm=industry_name)
    
    if not qs2.exists():
        return 0.5
    
    df2 = pd.DataFrame.from_records(qs2.values("prd_de", "c2_nm", "dt"))
    
    year_list = sorted(df2["prd_de"].unique())
    recent_years = year_list[-years:] if len(year_list) >= years else year_list
    df2 = df2[df2["prd_de"].isin(recent_years)]
    
    pivot2 = df2.pivot_table(
        index="prd_de",
        columns="c2_nm",
        values="dt",
        aggfunc="sum"
    ).fillna(0)
    
    total_male = pivot2.get("남자", pd.Series([0])).sum()
    total_female = pivot2.get("여자", pd.Series([0])).sum()
    total = total_male + total_female
    
    if total == 0:
        return 0.5
    
    return total_male / total if gender == "남자" else total_female / total


def _calculate_age_weight(industry_name, age_group, years):
    qs4 = Stats4.objects.filter(c1_nm=industry_name)
    
    if not qs4.exists():
        return 1.0 / 6
    
    df4 = pd.DataFrame.from_records(qs4.values("prd_de", "c2_nm", "dt"))
    
    year_list = sorted(df4["prd_de"].unique())
    recent_years = year_list[-years:] if len(year_list) >= years else year_list
    df4 = df4[df4["prd_de"].isin(recent_years)]
    
    pivot4 = df4.pivot_table(
        index="prd_de",
        columns="c2_nm",
        values="dt",
        aggfunc="sum"
    ).fillna(0)
    
    pivot4 = pivot4.drop(columns=["분류불능"], errors="ignore")
    
    age_data = pd.DataFrame(index=pivot4.index)
    age_data["18세미만"] = pivot4.get("18세 미만", 0)
    age_data["20대"] = pivot4.get("18~24세", 0) + pivot4.get("25~29세", 0)
    age_data["30대"] = pivot4.get("30~34세", 0) + pivot4.get("35~39세", 0)
    age_data["40대"] = pivot4.get("40~44세", 0) + pivot4.get("45~49세", 0)
    age_data["50대"] = pivot4.get("50~54세", 0) + pivot4.get("55~59세", 0)
    age_data["60대이상"] = pivot4.get("60세 이상", 0)
    
    totals = age_data.sum(axis=0)
    total_sum = totals.sum()
    
    if total_sum == 0:
        return 1.0 / 6
    
    return totals.get(age_group, 0) / total_sum



def _get_weighted_top5(industry_name, model_list, weight, years):
    combined_series = pd.Series(dtype=float)
    
    for model in model_list:
        qs = model.objects.filter(c1_nm=industry_name)
        if not qs.exists():
            continue
        
        df = pd.DataFrame.from_records(qs.values("prd_de", "c2_nm", "dt"))
        # Stats8 또는 Stats9인 경우 '직업병'과 '작업관련성 질병' 제외
        if model.__name__ in ['Stats8', 'Stats9']:
            df = df[~df["c2_nm"].isin(["직업병", "작업관련성 질병"])]

        
        year_list = sorted(df["prd_de"].unique())
        recent_years = year_list[-years:] if len(year_list) >= years else year_list
        df = df[df["prd_de"].isin(recent_years)]
        
        pivot = df.pivot_table(
            index="prd_de",
            columns="c2_nm",
            values="dt",
            aggfunc="sum"
        ).fillna(0)
        
        totals = pivot.sum(axis=0)
        combined_series = totals if combined_series.empty else combined_series.add(totals, fill_value=0)
    
    if combined_series.empty:
        return []
    
    weighted_series = combined_series * weight
    filtered = weighted_series[weighted_series > 0].sort_values(ascending=False)
    
    if filtered.empty:
        return []
    
    top5 = filtered.head(5)
    total_weighted = filtered.sum()
    
    top5_list = []
    for rank, (name, weighted_count) in enumerate(top5.items(), start=1):
        percentage = (weighted_count / total_weighted * 100) if total_weighted > 0 else 0
        top5_list.append({
            "rank": rank,
            "name": name,
            "count": int(weighted_count),
            "percentage": round(percentage, 1)
        })
    
    return top5_list


def get_risk_analysis(industry_name, age, gender, years=3, member_name=None):

    age_group = get_age_group(age)
    
    # ===== 1. 기본 통계 데이터 가져오기 =====
    stats1 = get_stats1(industry_name)
    
    # 데이터가 없는 경우 기본값 반환
    if not stats1:
        return {
            "period": f"{years}년",
            "age_group": age_group,
            "gender": gender,
            "industry": industry_name,
            "injury_top5": [],
            "disease_top5": [],
            "has_data": False,
            "gender_weight_pct": 50.0,
            "age_weight_pct": 16.7,
            "message":  f"{member_name}님현재 조건에서충분한 통계 데이터가 없습니다.",
            # 종합 위험도 점수
            "total_score": 0,
            "risk_level": "데이터 없음",
            "color": "gray",
            "breakdown": {
                "base_score": 0,
                "personal_score": 0,
                "severity_score": 0
            },
        }
    
    # 해당 기간 데이터 추출
    recent = next((s for s in stats1 if s.get("기간") == f"{years}년"), stats1[0])
    
    # ===== 2. 성별/연령대 가중치 계산 =====
    gender_weight = _calculate_gender_weight(industry_name, gender, years)
    age_weight = _calculate_age_weight(industry_name, age_group, years)
    
    # 전체 가중치 (성별 * 연령대)
    total_weight = gender_weight * age_weight
    
    # ===== 3. 발생형태별 위험 분석 (TOP 5) =====
    injury_top5 = _get_weighted_top5(
        industry_name, 
        [Stats6, Stats7],  # 일반 재해 + 사망 재해
        total_weight,
        years
    )
    
    # ===== 4. 질병형태별 위험 분석 (TOP 5) =====
    disease_top5 = _get_weighted_top5(
        industry_name,
        [Stats8, Stats9],  # 일반 질병 + 사망 질병
        total_weight,
        years
    )
    
    has_data = len(injury_top5) > 0 or len(disease_top5) > 0
    
    # ===== 5. 기본 위험도 점수 계산 (40점) =====
    accident_rate = recent.get("재해율", 0)
    death_rate = recent.get("사망만인율", 0)

    accident_score = min(math.sqrt(accident_rate) * 10, 14)
    death_rate_score = min(math.log1p(death_rate) * 9, 26)

    base_score = accident_score + death_rate_score
    
    # ===== 6. 개인화 위험도 점수 계산 (최대 40점) =====
    injury_risk = sum(item.get("percentage", 0) for item in injury_top5[:3]) / 100 * 20
    disease_risk = sum(item.get("percentage", 0) for item in disease_top5[:3]) / 100 * 20

    weight_factor = (gender_weight * 0.2) + (age_weight * 0.8)
    raw_personal_score = (injury_risk + disease_risk) * weight_factor

    personal_score = min(raw_personal_score, 40)
    
    # ===== 7. 중증도 점수 계산 (20점) =====
    total_accidents = recent.get("재해자수", 0)
    total_deaths = recent.get("사망자수", 0)
    severity_ratio = (total_deaths / total_accidents * 100) if total_accidents > 0 else 0
    severity_score = min(severity_ratio * 2, 20)
    
    # ===== 8. 종합 점수 계산 =====
    total_score = base_score + personal_score + severity_score
    

    # ===== 9. 위험도 등급 분류 =====
    if total_score >= 85:
        risk_level = "매우 높음"
        color = "red"
    elif total_score >= 65:
        risk_level = "높음"
        color = "orange"
    elif total_score >= 50:  # > 에서 >= 로 변경
        risk_level = "보통"
        color = "yellow"
    elif total_score >= 25:  # > 에서 >= 로 변경
        risk_level = "낮음"
        color = "green"
    else:
        risk_level = "매우낮음"
        color = "white"

    explanation = build_risk_explanation(
    base_score= base_score,
    personal_score = personal_score,
    severity_score= severity_score,
    accident_rate=accident_rate,
    death_rate=death_rate,
    gender_weight_pct=gender_weight * 100,
    age_weight_pct=age_weight * 100,
    severity_ratio=severity_ratio,
)    
    
    # ===== 10. 결과 반환 =====
    result = {
        # 기존 get_risk_analysis 반환값
        "period": f"{years}년",
        "age_group": age_group,
        "gender": gender,
        "industry": industry_name,
        "injury_top5": injury_top5,
        "disease_top5": disease_top5,
        "has_data": has_data,
        "gender_weight_pct": round(gender_weight * 100, 1),
        "age_weight_pct": round(age_weight * 100, 1),
        "message":  f"{member_name}님과 같은 조건({industry_name}, {age_group}, {gender})에서 최근 {years}년간 가장 많이 발생한 재해 유형입니다.",
        
        # 종합 위험도 점수 (새로 추가)
        "total_score": round(total_score, 0),
        "risk_level": risk_level,
        "color": color,
        "explanation": explanation,
        "breakdown": {
            "base_score": round(base_score, 1),
            "personal_score": round(personal_score, 1),
            "severity_score": round(severity_score, 1)
        },

    }
    
    return result

def build_risk_explanation(
    base_score,
    personal_score,
    severity_score,
    accident_rate=None,
    death_rate=None,
    gender_weight_pct=None,
    age_weight_pct=None,
    severity_ratio=None,
):
    explanation = []

    # =========================
    # 1) 기본 위험도(0~40) 설명
    # =========================
    if base_score >= 32:
        msg = (
            f"기본 위험도 점수는 {base_score:.1f}/40으로 매우 높은 구간입니다. "
            "즉, 업종 자체의 재해 발생 빈도와 치명 사고 위험이 모두 높은 편이라 "
            "개인 조건과 무관하게 기본적으로 위험도가 크게 반영됩니다."
        )
    elif base_score >= 24:
        msg = (
            f"기본 위험도 점수는 {base_score:.1f}/40으로 높은 구간입니다. "
            "업종 자체에서 사고가 자주 발생하거나, 발생 시 치명도로 이어질 가능성이 있어 "
            "안전수칙·보호구 착용 같은 기본 안전 관리가 특히 중요합니다."
        )
    elif base_score >= 14:
        msg = (
            f"기본 위험도 점수는 {base_score:.1f}/40으로 보통 구간입니다. "
            "업종 자체의 위험 신호가 일부 존재하지만, 작업 환경과 안전관리 수준에 따라 "
            "체감 위험이 달라질 수 있는 수준입니다."
        )
    else:
        msg = (
            f"기본 위험도 점수는 {base_score:.1f}/40으로 낮은 구간입니다. "
            "통계상 업종 자체의 사고 빈도와 치명 사고 위험이 상대적으로 크지 않은 편입니다."
        )

    # 보조 근거(있으면 추가)
    if accident_rate is not None and death_rate is not None:
        msg += f" (참고: 재해율 {accident_rate:.2f}%, 사망만인율 {death_rate:.2f}‰)"
    explanation.append(msg)

    # =========================
    # 2) 개인화 위험도(0~40) 설명
    # =========================
    if personal_score >= 32:
        msg = (
            f"개인화 위험도 점수는 {personal_score:.1f}/40으로 매우 높은 구간입니다. "
            "회원님의 연령대/성별에서 많이 발생하는 재해·질병 패턴이 "
            "해당 업종의 주요 위험 요인과 강하게 겹친다는 의미입니다. "
            "즉 ‘업종 위험’이 ‘개인 조건’에서 더 증폭되는 케이스입니다."
        )
    elif personal_score >= 24:
        msg = (
            f"개인화 위험도 점수는 {personal_score:.1f}/40으로 높은 구간입니다. "
            "회원님의 조건(연령대/성별)이 업종의 주요 재해·질병 분포와 일부 겹쳐 "
            "개인적으로 주의해야 할 포인트가 뚜렷하게 존재합니다."
        )
    elif personal_score >= 14:
        msg = (
            f"개인화 위험도 점수는 {personal_score:.1f}/40으로 보통 구간입니다. "
            "업종의 주요 위험 요소와 회원님의 조건이 부분적으로만 겹치며, "
            "작업 형태/직무에 따라 위험도가 달라질 수 있습니다."
        )
    else:
        msg = (
            f"개인화 위험도 점수는 {personal_score:.1f}/40으로 낮은 구간입니다. "
            "회원님의 조건이 업종 내에서 상대적으로 높은 위험 패턴과 크게 겹치지 않아 "
            "개인 조건에 의한 위험 증폭은 크지 않은 편입니다."
        )

    # 가중치 근거(있으면 추가)
    if gender_weight_pct is not None and age_weight_pct is not None:
        msg += f" (참고: 성별 {gender_weight_pct:.1f}%, 연령 {age_weight_pct:.1f}%)"
    explanation.append(msg)

    # =========================
    # 3) 중증도(0~20) 설명
    # =========================
    if severity_score >= 16:
        msg = (
            f"중증도 점수는 {severity_score:.1f}/20으로 매우 높은 구간입니다. "
            "사고가 한 번 발생했을 때 사망으로 이어질 가능성이 높다는 의미로, "
            "‘사고 빈도’보다 ‘사고 결과의 심각도’가 위험도를 크게 끌어올립니다."
        )
    elif severity_score >= 10:
        msg = (
            f"중증도 점수는 {severity_score:.1f}/20으로 높은 구간입니다. "
            "재해 대비 사망 비율이 무시하기 어려운 수준이라, "
            "위험 작업 공정에서는 추가적인 보호장비/안전 프로세스가 필요합니다."
        )
    elif severity_score >= 4:
        msg = (
            f"중증도 점수는 {severity_score:.1f}/20으로 보통 구간입니다. "
            "사망 사고가 발생하긴 하지만, 전체 재해 대비 비중은 제한적입니다. "
            "다만 특정 작업 상황에서 중대사고가 발생할 수 있어 예방 조치가 중요합니다."
        )
    else:
        msg = (
            f"중증도 점수는 {severity_score:.1f}/20으로 낮은 구간입니다. "
            "통계상 사망으로 이어지는 비율이 낮아, 사고가 발생해도 "
            "치명도 측면의 위험은 상대적으로 작습니다."
        )

    if severity_ratio is not None:
        msg += f" (참고: 재해 대비 사망비율 {severity_ratio:.1f}%)"
    explanation.append(msg)

    return explanation