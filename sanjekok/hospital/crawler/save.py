# hospital/crawler/save.py
#
# 파싱된 병원 데이터를 t_hospital 테이블에 저장
# - 이름/주소 하나라도 비어 있는 건 parse 단계에서 이미 제외됨
# - 여기서는 중복 체크 없이 무조건 create() 만 호출

from typing import List, Dict
from hospital.models import Hospital


def save_hospitals(hospitals: List[Dict]) -> int:
    """
    파싱된 병원 dict 리스트를 DB에 저장.
    - 이름/주소가 없는 건 parse 단계에서 이미 제외됨
    - 여기서는 중복 여부를 따지지 않고 모두 CREATE
    """
    count = 0

    for data in hospitals:
        name = (data.get("h_hospital_name") or "").strip()
        addr = (data.get("h_address") or "").strip()

        # 안전망: 혹시라도 비어 있으면 다시 한 번 걸러줌
        if not name or not addr:
            continue

        phone = (data.get("h_phone_number") or "").strip()[:11]

        Hospital.objects.create(
            h_hospital_name=name,
            h_address=addr,
            h_phone_number=phone,
            h_hospital_type=(data.get("h_hospital_type") or "").strip(),
            h_rc=(data.get("h_rc") or "").strip(),
            h_rc_info=(data.get("h_rc_info") or "").strip(),
            h_tr=(data.get("h_tr") or "").strip(),
            h_ei=(data.get("h_ei") or "").strip(),
        )
        count += 1

    return count
