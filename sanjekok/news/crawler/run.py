# news/crawler/run.py

import time
import traceback
from .fetch import fetch_html
from .parse import parse_list_page, parse_detail_page
from .save import save_news

def crawl_news():
    """
    뉴스 전체 크롤링 (1~5페이지)
    fetch → parse → detail fetch → detail parse → save
    """

    for page in range(1, 6):
        print(f"📄 {page} 페이지 수집 중...")

        try:
            list_url = (
                "http://sanjaenews.co.kr/news/list.php?"
                "&mcode=m641vf2&vg=photo&page=" + str(page)
            )

            # 1) 목록 HTML 수집
            list_soup = fetch_html(list_url)

            # 2) 목록 파싱
            articles = parse_list_page(list_soup)
            if not articles:
                print("  👉 더 이상 항목 없음. 종료.")
                break

        except Exception as e:
            print("❌ 목록 페이지 수집 실패:", e)
            traceback.print_exc()
            continue

        # 상세페이지 처리
        for art in articles:
            try:
                detail_soup = fetch_html(art["link"])
                detail = parse_detail_page(detail_soup)
                art["writer"] = detail["writer"]

                save_news(art)

            except Exception as e:
                print(f"❌ 상세페이지 실패: {art.get('link')}")
                traceback.print_exc()
                continue

            time.sleep(0.15)

    print("전체 크롤링 완료")
