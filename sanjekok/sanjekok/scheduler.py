import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

from news.crawler.run import crawl_news
from safe.crawler.run import crawl_safe

scheduler = None


def start_scheduler():
    global scheduler

    # runserver 자동 리로드 중복 실행 방지
    if os.environ.get("RUN_MAIN") != "true":
        return

    # 운영 환경에서는 APScheduler 비활성화
    if not settings.DEBUG:
        print("🚫 DEBUG=False → APScheduler OFF")
        return

    if scheduler is None:
        scheduler = BackgroundScheduler(timezone="Asia/Seoul")

        # 뉴스: 하루 2번 (09:00, 21:00)
        scheduler.add_job(
            crawl_news,
            trigger=CronTrigger(hour="9,21", minute=0),
            id="news_crawler",
            replace_existing=True,
        )

        # 안전자료: 하루 1번 (03:30)
        scheduler.add_job(
            crawl_safe,
            trigger=CronTrigger(hour=3, minute=30),
            id="safe_crawler",
            replace_existing=True,
        )

        scheduler.start()
        print("🔄 APScheduler 시작 (뉴스 2회 / 안전자료 1회)")
