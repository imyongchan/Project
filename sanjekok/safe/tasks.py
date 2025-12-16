from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .crawler.run import crawl_safe

scheduler = None  # 전역 스케줄러 (중복 실행 방지)

def start_scheduler():
    global scheduler

    # 운영환경(배포)에서는 실행 금지
    if not settings.DEBUG:
        print("🚫 DEBUG=False → APScheduler 실행 안 함 (safe)")
        return

    # 중복 실행 방지
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            crawl_safe,
            'interval',
            hours=24   # 안전자료는 보통 뉴스보다 덜 자주
        )
        scheduler.start()
        print("🔄 APScheduler(safe): 시작합니다...")
    else:
        print("이미 실행 중인 safe 스케줄러 있음")

def stop_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None
        print("🛑 APScheduler(safe): 종료했습니다...")
