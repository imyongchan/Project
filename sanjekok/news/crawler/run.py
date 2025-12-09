import time
from .fetch import fetch_html
from .parse import parse_list_page, parse_detail_page
from .save import save_news
import traceback

def crawl_news():
    """
    뉴스 전체 크롤링 (1~5페이지)(임시)
    fetch → parse → detail fetch → detail parse → save
    """
    print(f"🧡 크롤링 시작")
    for page in range(1, 2):

        try:
            list_url = f"http://sanjaenews.co.kr/news/list.php?&mcode=m641vf2&vg=&page={page}"

            # 1) 목록 HTML 수집
            list_soup = fetch_html(list_url)

            # 2) 목록 파싱
            articles = parse_list_page(list_soup) 
            if not articles:    # articles = 각 기사 정보(dict) 가 담긴 list
                print("더 이상 항목 없음. 종료.")
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
                art["writer"] = detail["writer"]  # writer 키 값 새로 추가

                save_news(art) # DB 저장

            except Exception as e:
                print(f"❌ 상세페이지 실패: {art.get('link')}", e)
                continue

            time.sleep(0.15)

    print("🌐 전체 크롤링 완료")
    
    from datetime import datetime
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 크롤링 종료 시간: {end_time}")
