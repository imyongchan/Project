# safe/crawler/run.py

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
    print("\n=============== 안전자료 전체 크롤링 시작 ===============\n")

    for shpCd in TYPE_CODES:
        print(f"\n===== 🟠 자료형태 [{shpCd or '기타'}] 크롤링 시작 🟠 =====")

        try:
            for page in range(1, 3):  # 페이지 1~2까지 테스트(임시)
                print(f" 페이지 {page} 요청 중...")

                # 1) API 요청
                try:
                    data = fetch_page(shpCd=shpCd, page=page)
                except Exception as e:
                    print(f" ❌ fetch 실패: {e}")
                    break

                # 2) 파싱
                items = parse_list(data, shpCd)

                # 3) 페이지 종료 감지
                if not items:
                    print(" 더 이상 데이터 없음 → 다음 자료형태로 이동")
                    break

                # 4) 저장
                save_items(items)

        except Exception as e:
            print(f" ❌ [{shpCd or '기타'}] 크롤링 중 오류 발생: {e}")
            continue

        print(f"===== 🌐 자료형태 [{shpCd or '기타'}] 완료 =====")



    print("\n======= 안전자료 전체 크롤링 종료 =======")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 크롤링 종료 시간: {end_time}\n")
