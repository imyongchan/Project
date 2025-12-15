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
        reg_dt = item.get("contsRegYmd")
   
        # 자료고유번호
        seq = item.get("medSeq") 
        
        # 조회수 
        views = item.get("totHitSum")   
        
        # 내용
        note = item.get("medNote") 
        
        # 동영상 url
        video_url = item.get("ytbUrlAddr")     
        
        # 공공누리
        publisher = item.get("medGonggongnuriNm")           
            

        # 키워드 문자열 → 리스트
        keywords_raw = item.get("medKeyword")  # 예: "사다리,이동식 사다리,작업수칙"
        keywords = []
        if keywords_raw:
            keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    
    
        # 언어 판별
        lang_raw = item.get("langCrtrNtnltyNm")

        if lang_raw is None or lang_raw == "공통언어":
            language = "한국어"            # 한국어 자료
        else:
            language = "외국어"       # 외국어 자료
            
       
       
        # ---------------------------------------------------

        results.append({
            "title": title,     # 제목
            "img": img_url,     # 썸네일 이미지 url
            "type": content_type,   # 자료형태   
            "content": note,    # 자료내용
            "reg_dt": reg_dt,     # 자료 작성일
            "views": views,   # 조회수
            "seq": seq,         # 링크에 덭붙일 자료고유번호
            "language": language,  # 안전자료언어
            "video_url": video_url, # 동영상자료 시 동영상 url
            "publisher": publisher, # 공공누리
            "tags": keywords,  # 키워드(들) 
        })

    return results
