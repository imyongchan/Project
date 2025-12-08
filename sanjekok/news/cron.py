from .crawler.run import run_news_crawl

def news_crawl_job():
    print("[CRON] 자동 크롤링 시작")
    run_news_crawl()
    print("[CRON] 자동 크롤링 종료")
