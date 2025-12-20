# run.py (SERVER)
import time
from .fetch import fetch_html
from .parse import parse_list_page, parse_detail_page
from .save import save_news
from datetime import datetime, timedelta

def crawl_news():
    print(f"\n===== 🟠 뉴스 크롤링 시작 (이미지 제외) 🟠 =====")

    one_year_ago = datetime.now() - timedelta(days=365)
    page = 1

    while True:
        print(f"\n▶ 목록 페이지 {page} 수집 중...")

        try:
            list_url = (
                f"http://sanjaenews.co.kr/news/list.php?"
                f"&mcode=m641vf2&vg=&page={page}"
            )
            list_soup = fetch_html(list_url)
            articles = parse_list_page(list_soup)

            if not articles:
                print("🌐 기사 없음 → 종료")
                break

        except Exception as e:
            print("❌ 목록 수집 실패:", e)
            break

        for art in articles:
            try:
                detail_soup = fetch_html(art["link"])
                detail = parse_detail_page(
                    detail_soup,
                    art.get("created_at_raw")
                )

                published_at = detail.get("published_at")
                if published_at and published_at < one_year_ago:
                    print("⏹ 1년 이전 기사 → 종료")
                    return

                art["writer"] = detail.get("writer")

                # ✅ 이미지 다운로드 안 함
                # 원본 이미지 URL 그대로 저장
                art["img_url"] = art.get("img_url")

                save_news(art)

            except Exception as e:
                print(f"❌ 상세 실패: {art['link']}", e)

            time.sleep(0.3)

        page += 1
        time.sleep(0.5)

    print("✅ 뉴스 텍스트 크롤링 완료")
