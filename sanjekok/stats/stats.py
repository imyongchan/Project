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
            columns="c2_nm",   # '18세 미만', '18~24세', ...
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
        # 기간 컬럼 제거 후, 0보다 큰 것만 상위 10개
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
    
    # ===== 6. 개인화 위험도 점수 계산 (40점) =====
    # 발생형태 위험도 (상위 3개 비율 합산)
    injury_risk = sum(item.get("percentage", 0) for item in injury_top5[:3]) / 100 * 20
    
    # 질병 위험도 (상위 3개 비율 합산)
    disease_risk = sum(item.get("percentage", 0) for item in disease_top5[:3]) / 100 * 20
    
    # 개인화 점수 = (발생형태 + 질병) × (성별 가중치 + 연령 가중치)
    personal_score = (injury_risk + disease_risk) * (gender_weight + age_weight)
    
    # ===== 7. 중증도 점수 계산 (20점) =====
    total_accidents = recent.get("재해자수", 0)
    total_deaths = recent.get("사망자수", 0)
    severity_ratio = (total_deaths / total_accidents * 100) if total_accidents > 0 else 0
    severity_score = min(severity_ratio * 2, 20)
    
    # ===== 8. 종합 점수 계산 =====
    total_score = base_score + personal_score + severity_score
    
    # ===== 9. 위험도 등급 분류 =====
    if total_score >= 70:
        risk_level = "매우 높음"
        color = "red"
    elif total_score >= 50:
        risk_level = "높음"
        color = "orange"
    elif total_score >= 30:
        risk_level = "보통"
        color = "yellow"
    else:
        risk_level = "낮음"
        color = "green"

    explanation = build_risk_explanation(
    accident_rate=accident_rate,
    death_rate=death_rate,
    severity_ratio=severity_ratio,
    personal_score=personal_score,
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
    accident_rate,
    death_rate,
    severity_ratio,
    personal_score,
):
    explanation = []

    # 1️⃣ 재해 발생 빈도
    if accident_rate >= 1.5:
        explanation.append(
            "이 업종은 사고가 비교적 자주 발생하는 편으로, "
            "일상적인 작업 중에도 재해에 노출될 가능성이 있습니다."
        )
    elif accident_rate >= 1.0:
        explanation.append(
            "이 업종의 사고 발생 수준은 평균보다 약간 높은 편으로, "
            "작업 시 기본적인 안전 관리가 특히 중요합니다."
        )
    else:
        explanation.append(
            "이 업종은 사고 발생 빈도가 낮은 편으로, "
            "다른 업종에 비해 일상적인 재해 위험은 크지 않은 것으로 보입니다."
        )

    # 2️⃣ 사망 위험
    if death_rate >= 1.0:
        explanation.append(
            "사고가 발생할 경우 중대 사고로 이어질 가능성이 높은 업종입니다. "
            "작은 사고라도 생명에 위협이 될 수 있어 각별한 주의가 필요합니다."
        )
    elif death_rate > 0:
        explanation.append(
            "드물지만 치명적인 사고 사례가 발생한 업종으로, "
            "위험 상황에서는 사고의 결과가 심각해질 수 있습니다."
        )

    # 3️⃣ 중증도
    if severity_ratio >= 5:
        explanation.append(
            "전체 사고 중 사망으로 이어지는 비율이 높은 편으로, "
            "사고가 발생하면 중증 사고로 이어질 가능성이 큽니다."
        )
    elif severity_ratio > 0:
        explanation.append(
            "사고는 발생하지만 대부분은 경미한 사고에 그치는 경향이 있어, "
            "중증 사고 위험은 상대적으로 낮은 편입니다."
        )

    # 4️⃣ 개인화 위험
    if personal_score >= 30:
        explanation.append(
            "회원님의 성별과 연령대에서 자주 발생하는 사고 유형이 "
            "해당 업종의 주요 재해 유형과 겹쳐 개인적인 위험도가 높게 나타났습니다."
        )
    elif personal_score >= 15:
        explanation.append(
            "회원님의 조건이 업종의 주요 위험 요소와 일부 겹쳐 "
            "개인적인 주의가 필요한 수준으로 평가되었습니다."
        )



    return explanation