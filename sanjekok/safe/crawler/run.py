# safe/crawler/run.py
import time
from .fetch import fetch_page
from .parse import parse_list
from .save import save_items
from datetime import datetime

TYPE_CODES = [
    "12",  # OPS
    "02",  # 동영상
    "01",  # 책자
    "07",  # PPT
    ""     # 기타
]


def crawl_safe():
    print("\n===== 안전자료 전체 크롤링 시작 =====\n")

    for shpCd in TYPE_CODES:
        print(f"\n===== 🟠 자료형태 [{shpCd or '기타'}] 시작 🟠 =====")

        page = 1

        while True:
            print(f" ▶ 페이지 {page} 요청 중...")

            try:
                data = fetch_page(shpCd=shpCd, page=page)
            except Exception as e:
                print(f" ❌ fetch 실패: {e}")
                break

            items = parse_list(data, shpCd)

            # 종료 조건
            if not items:
                print(" 🌐 더 이상 데이터 없음 → 다음 자료형태로 이동")
                break

            save_items(items)

            page += 1
            time.sleep(0.3)  # ⭐ API 배려

        print(f"===== 🌐 자료형태 [{shpCd or '기타'}] 완료 =====")

    from datetime import datetime
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n===== 안전자료 전체 크롤링 종료 =====")
    print(f"🕒 종료 시간: {end_time}\n")
