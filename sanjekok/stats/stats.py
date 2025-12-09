import pandas as pd

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
        top10 = filtered_row.head(10)

        top10_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top10.items():
            top10_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
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
        top10 = filtered_row.head(10)

        top10_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top10.items():
            top10_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
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
        top10 = filtered_row.head(10)

        top10_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top10.items():
            top10_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
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
        top10 = filtered_row.head(10)

        top10_list = []
        filtered_rank_series = filtered_row.rank(ascending=False, method="min")

        for name, cnt in top10.items():
            top10_list.append({
                "rank": int(filtered_rank_series[name]),
                "name": name,
                "count": int(cnt),
            })

        rank_series = numeric_row.rank(ascending=False, method="min")
        rank_map = {name: int(r) for name, r in rank_series.items()}

        result[period] = {
            "top10": top10_list,
            "rank_map": rank_map,
        }

    return result