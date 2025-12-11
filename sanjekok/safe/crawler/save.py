# safe/crawler/save.py
from datetime import datetime
from safe.models import Safe, Tag, SafeTag


def convert_date(date_raw):
    """
    문자열 날짜를 datetime.date로 변환 (YYYYMMDD 또는 YYYY-MM-DD 대응)
    """
    if not date_raw:
        return None

    try:
        # YYYYMMDD
        if len(date_raw) == 8:
            return datetime.strptime(date_raw, "%Y-%m-%d").date()

    except:
        return None

    return None

# 상세페이지 링크 생성용 Base URL
BASE_DETAIL_URL = ("https://portal.kosha.or.kr/archive/cent-archive/master-arch/master-list1/master-detail1?medSeq=")

def save_items(items):
    """
    parse_list() 결과(items 리스트)를 Safe/Tag DB에 저장.
    """
    for item in items:
        
        # 1) 파싱된 데이터 꺼내기
        title = item["title"]
        img = item["img"]
        type_name = item["type"]
        contents = item["content"]
        created_at = convert_date(item["created_at"])

        hit = item["hit"] or 0
        seq = item["seq"]
        link = BASE_DETAIL_URL + str(seq)  # 

        language = item["language"]
        video_url = item["video_url"]
        publisher = item["publisher"] or 'KOSHA'
        tag_list = item["tags"]     # 리스트 형태로 들어있음


        # 2) Safe 테이블에 저장
        safe, created = Safe.objects.update_or_create(
            s_title=title,
            defaults={
                "s_type": type_name,
                "s_image_url": img,
                "s_contents": contents,
                "s_created_at": created_at,
                "s_view_count": hit,
                "s_link": link,
                "s_language": language,
                "s_publisher": publisher,
                "s_video_url": video_url,
            }
        )


        # 3) Tag 생성 및 SafeTag 연결
        for tag_name in tag_list:
            tag_name = tag_name.strip()
            if not tag_name:
                continue

            tag, _ = Tag.objects.get_or_create(st_tag=tag_name)
            SafeTag.objects.get_or_create(safe=safe, tag=tag)
