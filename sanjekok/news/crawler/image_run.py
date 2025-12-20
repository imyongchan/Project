import time
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path
from news.models import News
from django.conf import settings

# 저장 폴더
NEWS_IMG_DIR = Path(settings.BASE_DIR) / "static/img/news"
NEWS_IMG_DIR.mkdir(parents=True, exist_ok=True)  # 폴더 없으면 생성

def download_news_image(url, save_name, max_size_kb=100):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img_format = img.format if img.format else "PNG"

        buffer = BytesIO()
        quality = 95

        if img_format.upper() in ["JPEG", "JPG"]:
            img.save(buffer, format="JPEG", quality=quality)
        else:
            img.save(buffer, format="PNG", optimize=True)

        while buffer.getbuffer().nbytes > max_size_kb * 1024 and quality > 10:
            buffer = BytesIO()
            if img_format.upper() in ["JPEG", "JPG"]:
                quality -= 5
                img.save(buffer, format="JPEG", quality=quality)
            else:
                width, height = img.size
                img = img.resize((int(width * 0.9), int(height * 0.9)))
                img.save(buffer, format="PNG", optimize=True)

        # 실제 저장 경로
        save_path = NEWS_IMG_DIR / save_name
        with open(save_path, "wb") as f:
            f.write(buffer.getvalue())

        return f"img/news/{save_name}"  # DB에 저장할 상대경로

    except Exception as e:
        print("이미지 다운로드 실패:", e)
        return None


def crawl_news_images(limit=30, max_size_kb=100):
    print("\n===== 🟢 뉴스 이미지 다운로드 시작 =====")

    qs = News.objects.filter(
        n_image_url__startswith="http"
    ).order_by("-n_created_at")[:limit]

    for idx, news in enumerate(qs, start=1):
        print(f"🖼 이미지 {idx} 다운로드 중...")

        local_path = download_news_image(
            news.n_image_url,
            f"news_{news.id}.png",
            max_size_kb=max_size_kb
        )

        if local_path:
            news.n_image_url = local_path
            news.save(update_fields=["n_image_url"])

        time.sleep(0.5)

    print("✅ 이미지 다운로드 완료")
