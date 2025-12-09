import requests
import pandas as pd
from datetime import datetime

from django.core.management.base import BaseCommand
from stats.models import Stats1


API_KEY = 'N2MzYzJlN2ZiNjM1OGRiODJkYmIxYzkxYTY2Zjg1ODI='


def parse_date(value):
    """LST_CHN_DE 문자열을 python date로 변환"""
    s = str(value)
    return datetime.strptime(s, "%Y-%m-%d").date()


def build_url():
    base = (
        "https://kosis.kr/openapi/Param/statisticsParameterData.do"
        "?method=getList"
        f"&apiKey={API_KEY}"
        "&itmId=16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+16118AAD6_15118AI8ACAB+"
        "16118AAD6_15118AI8ACAD+"
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
        "&format=json&jsonVD=Y"
        "&prdSe=Y&startPrdDe=2021&endPrdDe=2023"
        "&outputFields=NM+ITM_NM+PRD_DE+LST_CHN_DE+"
        "&orgId=118&tblId=DT_11806_N000"
    )
    return base


class Command(BaseCommand):
    help = "KOSIS API에서 업종별 재해 통계(Stats1)를 가져와 t_stats1 테이블에 저장합니다."

    def handle(self, *args, **options):
        url = build_url()
        self.stdout.write(f"요청 URL: {url[:120]}...")  # 너무 길어서 앞부분만 출력

        # 1) API 호출
        res = requests.get(url)
        res.raise_for_status()

        data = res.json()
        self.stdout.write(f"응답 건수: {len(data)}")

        df = pd.DataFrame(data)

        # 2) Stats1 객체 리스트 생성
        objs = []

        for row in df.itertuples(index=False):
            raw_dt = row.DT
            dt_value = 0.0 if raw_dt in (None, "", ".") else float(raw_dt)

            lst_chn = parse_date(row.LST_CHN_DE)

            obj = Stats1(
                dt=dt_value,
                prd_de=int(row.PRD_DE),
                lst_chn_de=lst_chn,
                c1_nm=str(row.C1_NM),
                itm_nm=str(row.ITM_NM),
            )
            objs.append(obj)

        # 3) bulk_create 로 한 번에 저장
        Stats1.objects.bulk_create(objs, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"t_stats1 저장 완료! 총 {len(objs)}건"))