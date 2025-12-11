# safe/crawler/run.py
from .fetch import fetch_page
from .parse import parse_list
from .save import save_items

# 자료형태 코드 목록
TYPE_CODES = [
    "12",  # OPS
    "02",  # 동영상
    "01",  # 책자
    "07",  # PPT
    ""     # 기타
]


def crawl_safe():
    """
    안전자료 전체 크롤링:
    - shpCd(자료형태 코드)별
    - page(1~N)별 반복 수집
    """
    for shpCd in TYPE_CODES:
        print(f"\n===== 자료형태 {shpCd or '기타'} 크롤링 시작 =====")

        for page in range(1, 3):  # 우선 1~2페이지만 테스트
            print(f"  - 페이지 {page} 요청 중...")

            data = fetch_page(shpCd=shpCd, page=page)
            items = parse_list(data, shpCd)
            save_items(items)

        print(f"===== 자료형태 {shpCd or '기타'} 완료 =====\n")
