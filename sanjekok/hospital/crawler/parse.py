# hospital/crawler/parse.py
#
# SAFEMAP IF_0025 JSON → Hospital 모델용 dict 리스트로 변환

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

    주소는:
      - 지번주소(adres/ADRES)가 있으면 우선 사용
      - 없으면 도로명주소(rn_adres/RN_ADRES)를 사용

    이름이나 주소가 하나라도 없으면 해당 레코드는 버린다.
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

        # 지번주소
        jibun_addr = (
            it.get("adres")
            or it.get("ADRES")
            or ""
        )

        # 도로명주소
        road_addr = (
            it.get("rn_adres")
            or it.get("RN_ADRES")
            or ""
        )

        # 지번주소 우선, 없으면 도로명주소
        address = (jibun_addr or road_addr).strip()

        # 전화번호
        phone = (
            it.get("telno")
            or it.get("TELNO")
            or it.get("tel")
            or it.get("TEL")
            or ""
        )

        # 종별 (병원/의원/상급종합병원 등)
        hosp_type = (
            it.get("fclty_ty")
            or it.get("FCLTY_TY")
            or it.get("hosp_ty")
            or it.get("HOSP_TY")
            or ""
        )

        # 부가기능 / 재활인증 / 진폐요양 / 진료제한 / 평가연도 등
        rc = (
            it.get("coniosis")
            or it.get("CONIOSIS")
            or it.get("rc")
            or it.get("RC")
            or ""
        )

        rc_info = (
            it.get("rm_cd")
            or it.get("RM_CD")
            or it.get("rc_info")
            or it.get("RC_INFO")
            or ""
        )

        tr = (it.get("tr") or it.get("TR") or "")
        ei = (it.get("ei") or it.get("EI") or "")

        # 이름이나 주소 둘 중 하나라도 없으면 버림
        if not name or not address:
            continue

        results.append(
            {
                "h_hospital_name": name.strip(),
                "h_address": address,  # 이미 strip 적용
                "h_phone_number": phone.strip(),
                "h_hospital_type": hosp_type.strip(),
                "h_rc": rc.strip() if isinstance(rc, str) else rc,
                "h_rc_info": rc_info.strip() if isinstance(rc_info, str) else rc_info,
                "h_tr": tr.strip() if isinstance(tr, str) else tr,
                "h_ei": ei.strip() if isinstance(ei, str) else ei,
            }
        )

    return results
