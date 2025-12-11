# safe/crawler/parse.py

def parse_list(data, shpCd):
    """
    KOSHA API 응답(JSON)에서 안전자료 목록을 뽑아
    Safe/Tag 저장용 dict 리스트로 변환.
    """
    items = data.get("payload", {}).get("list", [])
    results = []

    for item in items:
        title = item.get("medName")

        # 썸네일 이미지
        img_url = item.get("medThumbnailPath")
        if img_url and img_url.startswith("/"):
            img_url = "https://portal.kosha.or.kr" + img_url

        # 자료형태(사람이 읽는 값, 예: PPT, 동영상 등)
        content_type = item.get("contsFbctnShpNm")

        # 자료 등록일자
        reg_dt = item.get("constRegYmd")

        # 키워드 문자열 → 리스트
        keywords_raw = item.get("medKeyword")  # 예: "사다리,이동식 사다리,작업수칙"
        keywords = []
        if keywords_raw:
            keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

        results.append({
            "title": title,
            "type": content_type,
            "img": img_url,
            "date": reg_dt,
            "keywords": keywords,
        })

    return results
