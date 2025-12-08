# 데이터 수집
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://sanjaenews.co.kr"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def fetch_html(url: str):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def absolute_url(path: str):
    if not path:
        return None 

    # 이미 절대경로면 그대로 반환
    if path.startswith("http"):
        return path

    return BASE_URL + path.lstrip(".")  # 상대경로 → 절대경로로 변환

