import time
from .fetch import fetch_html
from .parse import parse_list_page, parse_detail_page
from .save import save_news

def crawl_news():
    """
    뉴스 전체 크롤링
    """
    print(f"\n===== 🟠 뉴스 크롤링 시작 🟠 =====")

    page = 1

    while True:
        print(f"\n▶ 목록 페이지 {page} 수집 중...")

        try:
            list_url = f"http://sanjaenews.co.kr/news/list.php?&mcode=m641vf2&vg=&page={page}"

            # 1) 목록 HTML 수집
            list_soup = fetch_html(list_url)

            # 2) 목록 파싱
            articles = parse_list_page(list_soup)

            # 종료 조건
            if not articles:
                print("🌐 더 이상 기사 없음 → 크롤링 종료")
                break

        except Exception as e:
            print("❌ 목록 페이지 수집 실패:", e)
            break   

        # 상세페이지 처리
        for art in articles:
            try:
                detail_soup = fetch_html(art["link"])
                detail = parse_detail_page(detail_soup)

                art["writer"] = detail.get("writer")
                save_news(art)

            except Exception as e:
                print(f"❌ 상세페이지 실패: {art.get('link')}", e)
                continue

            time.sleep(0.2)  

        page += 1
        time.sleep(0.5)      # ⭐ 페이지 단위 휴식

    from datetime import datetime
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n====== 뉴스 전체 크롤링 완료 =====")
    print(f"🕒 종료 시간: {end_time}")