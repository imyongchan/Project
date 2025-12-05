import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from django.utils import timezone

from .models import News  # DB Model


def crawl_news():

    for page in range(1, 6):  # 1~5 페이지(임시)
        print(f"{page} 페이지... 크롤링 중") 

        url = f"http://sanjaenews.co.kr/news/list.php?&mcode=m641vf2&vg=photo&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        items = soup.select("div#contents > div.basicList > ul > li")
        if not items:
            print("더 이상 데이터 없음 → 종료")
            break

        for item in items:

            # 제목
            title = item.select_one("dt.title a").text.strip()

            # 목록 요약
            content = item.select_one("dd.content a").text.strip()
            

            # 이미지
            img_tag = item.select_one("a.image img")
            img_url = img_tag.get("src").lstrip(".") if img_tag else None
            if img_url and not img_url.startswith("http"):
                img_url = "http://sanjaenews.co.kr" + img_url

            # 상세 링크
            link = item.select_one("a").get("href").lstrip(".")
            if link and not link.startswith("http"):
                link = "http://sanjaenews.co.kr" + link

            # 중복 방지
            if News.objects.filter(n_link=link).exists():
                continue

            # 작성일자 
            date_tag = item.select_one("dd.registDate")
            created_at_raw = date_tag.text.strip() if date_tag else None
            # 문자열 → datetime 변환
            try:
                created_at = datetime.strptime(created_at_raw.strip(), "%Y-%m-%d")
            except:
                created_at = timezone.now()
            
            # 상세페이지 요청 --------------------------------------------------------
            time.sleep(0.15)
            detail_res = requests.get(link)
            detail_res.raise_for_status()
            detail_soup = BeautifulSoup(detail_res.text, "lxml")

            # 작성자
            writer_tag = detail_soup.select_one("div.titleWrap > div.else-area > p")
            writer = writer_tag.text.strip() if writer_tag else None

            # DB 저장 ---------------------------------------------------------------
            News.objects.create(
                n_title=title,
                n_writer=writer,
                n_contents=content,   
                n_link=link,
                n_image_url=img_url,
                n_created_at=created_at
            )

        

    print("=== 크롤링 전체 완료 ===")
