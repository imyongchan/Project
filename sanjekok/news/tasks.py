# news/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .crawler.run import crawl_news

scheduler = None  # 전역 스케줄러

def start_scheduler():
    global scheduler

    # 개발환경에서만 실행
    if not settings.DEBUG:
        return

    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(crawl_news, 'interval', minutes=1)

        print("🔄 APScheduler: 시작합니다...")
        scheduler.start()
