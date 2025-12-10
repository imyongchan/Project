# hospital/crawler/parse.py
#
# SAFEMAP IF_0025 JSON → Hospital 모델용 dict 리스트로 변환
# h_address 에는 무조건 rn_adres(또는 RN_ADRES) 값만 넣는다.

from typing import List, Dict


def _extract_items(raw_json: dict):
    """
    응답 JSON에서 item 배열만 꺼내기.
    (response.body.items.item / body.items / items 등 여러 형태를 처리)
    """
    if not raw_json:
        return []

    # 1) body 찾기 (response.body 또는 최상단 body)
    body = raw_json.get("body")
    if body is None and "response" in raw_json:
        body = raw_json["response"].get("body")

    # 2) body 내부나 최상단에서 items / item 추출
    if body is None:
        items = raw_json.get("items") or raw_json.get("item") or []
    else:
        items = body.get("items") or body.get("item") or []

    # 3) items = {"item":[...]} 형태 처리
    if isinstance(items, dict) and "item" in items:
        items = items["item"]

    # 4) item 이 dict 한 개만 오는 경우
    if isinstance(items, dict):
        items = [items]

    return items


def parse_hospitals(raw_json: dict) -> List[Dict]:
    """
    SAFEMAP 산재지정병원 API JSON → Hospital 테이블에 넣을 dict 리스트로 변환

    - h_hospital_name : fclty_nm 계열
    - h_address       : rn_adres / RN_ADRES (도로명주소)만 사용
    - 이름이나 rn_adres 둘 중 하나라도 없으면 해당 레코드는 버린다.
    - h_rc, h_rc_info 는 쓰지 않으므로 항상 빈 문자열로 둔다.
    """
    items = _extract_items(raw_json)
    results: List[Dict] = []

    for it in items:
        # 의료기관명(시설명)
        name = (
            it.get("fclty_nm")
            or it.get("FCLTY_NM")
            or it.get("area_nm")
            or it.get("AREA_NM")
            or it.get("org_nm")
            or it.get("ORG_NM")
            or it.get("yadmNm")
            or it.get("YADM_NM")
            or ""
        )
        name = name.strip() if isinstance(name, str) else ""

        # 도로명주소: rn_adres / RN_ADRES 만 사용
        road_addr = (
            it.get("rn_adres")
            or it.get("RN_ADRES")
            or ""
        )
        address = road_addr.strip() if isinstance(road_addr, str) else ""

        # 전화번호
        phone = (
            it.get("telno")
            or it.get("TELNO")
            or it.get("tel")
            or it.get("TEL")
            or ""
        )
        phone = phone.strip() if isinstance(phone, str) else ""

        # 종별 (병원/의원/상급종합병원 등)
        hosp_type = (
            it.get("fclty_ty")
            or it.get("FCLTY_TY")
            or it.get("hosp_ty")
            or it.get("HOSP_TY")
            or ""
        )
        hosp_type = hosp_type.strip() if isinstance(hosp_type, str) else ""

        # 이름이나 주소 둘 중 하나라도 없으면 버림
        if not name or not address:
            continue

        results.append(
            {
                "h_hospital_name": name,
                "h_address": address,           # rn_adres 그대로 들어감
                "h_phone_number": phone,
                "h_hospital_type": hosp_type,
                "h_rc": "",                     # 사용 안 함
                "h_rc_info": "",                # 사용 안 함
                "h_tr": "",                     # 필요 시 나중에 사용
                "h_ei": "",
            }
        )

    return results
