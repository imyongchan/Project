# safe/crawler/save.py
from datetime import datetime
from safe.models import Safe, Tag, SafeTag


def convert_date(date_raw):
    """문자열 날짜(constRegYmd / YYYY-MM-DD...)를 Date로 변환."""
    if not date_raw:
        return None

    try:
        # "20251210" ← 다 이런 형태
        if len(date_raw) == 8:
            return datetime.strptime(date_raw, "%Y-%m-%d").date()
    except Exception:
        return None

    return None


def save_items(items):
    """
    1) Safe 저장
    2) Tag(키워드) 저장
    3) SafeTag 연결
    """
    for item in items:
        title = item["title"]
        img = item["img"]
        type_name = item["type"]          # 자료형태 이름 (PPT/영상/책자 등)
        keywords = item["keywords"]       # 리스트
        date = convert_date(item["date"])

        # 1) Safe 저장
        safe, created = Safe.objects.update_or_create(
            s_title=title,
            defaults={
                "s_type": type_name or "",      # None 방지
                "s_image_url": img or "",
                "s_created_at": date,
                "s_publisher": "KOSHA",
                "s_link": "",                   # 나중에 상세 링크 크롤링 시 업데이트
            }
        )

        # 2) 키워드 → Tag / SafeTag
        for kw in keywords:
            tag, _ = Tag.objects.get_or_create(st_tag=kw)
            SafeTag.objects.get_or_create(safe=safe, tag=tag)
