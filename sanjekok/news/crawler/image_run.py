# image_run.py (LOCAL ONLY)
import time
from news.models import News
from .save import download_news_image

def crawl_news_images(limit=30):
    """
    DB에 저장된 뉴스 이미지 다운로드
    """
    print("\n===== 🟢 뉴스 이미지 다운로드 시작 =====")

    qs = News.objects.filter(
        n_image_url__startswith="http"
    ).order_by("-n_created_at")[:limit]

    for idx, news in enumerate(qs, start=1):
        print(f"🖼 이미지 {idx} 다운로드 중...")

        local_path = download_news_image(
            news.n_image_url,
            f"news_{news.id}.png"
        )

        news.n_image_url = local_path
        news.save(update_fields=["n_image_url"])

        time.sleep(0.5)

    print("✅ 이미지 다운로드 완료")
