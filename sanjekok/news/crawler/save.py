# DB 저장

from news.models import News
from datetime import datetime
from django.utils import timezone

import os
import requests
from django.conf import settings

NEWS_IMG_DIR = os.path.join(settings.BASE_DIR, "static/img/news")
DEFAULT_IMG = "img/news/default.png"

def download_news_image(img_url, filename):
    if not img_url:
        return DEFAULT_IMG

    try:
        r = requests.get(
            img_url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        
        # ⭐ 여기 한 줄 추가
        if int(r.headers.get("Content-Length", 0)) > 500_000:
            return DEFAULT_IMG

        content_type = r.headers.get("Content-Type", "")
        if r.status_code == 200 and content_type.startswith("image/"):
            os.makedirs(NEWS_IMG_DIR, exist_ok=True)
            file_path = os.path.join(NEWS_IMG_DIR, filename)

            with open(file_path, "wb") as f:
                f.write(r.content)

            return f"img/news/{filename}"

    except Exception:
        pass

    return DEFAULT_IMG

def save_news(data):
    # 1️⃣ 작성일 처리
    try:
        created_at = datetime.strptime(data["created_at_raw"], "%Y-%m-%d")
    except:
        created_at = timezone.now()

    # 2️⃣ 뉴스 먼저 저장 (이미지 제외)
    news, created = News.objects.update_or_create(
        n_link=data["link"],   # 상세 링크 기준 중복 체크
        defaults={
            "n_title": data["title"],
            "n_writer": data["writer"],
            "n_contents": data["content"],
            "n_created_at": created_at,
        }
    )

    # 3️⃣ PK 기반 이미지 파일명
    filename = f"news_{news.id}.png"

    # 4️⃣ 이미지 다운로드
    image_path = download_news_image(
        data.get("img_url"),
        filename
    )

    # 5️⃣ 이미지 경로 DB 반영
    news.n_image_url = image_path
    news.save(update_fields=["n_image_url"])
