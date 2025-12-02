from django.shortcuts import render
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


def news_list(request):

    news_list=[]
    page = 1

    while True:

        # 2페이지까지만 크롤링 제한
        if page > 2:
            break

        url = f'http://sanjaenews.co.kr/news/list.php?&mcode=m641vf2&vg=photo&page={page}'
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.select("div#contents > div.basicList > ul > li")

        if not items:
            print(f"더 이상 기사 없음 → 크롤링 종료")
            break

        for item in items:
            # 제목
            title = item.select_one("dt.title a").text.strip()
            # 내용 요약
            content = item.select_one("dd.content a").text.strip()

            # 이미지
            img_tag = item.select_one("a.image img")
            img_url = img_tag.get("src").lstrip(".") if img_tag else None
            if img_url and not img_url.startswith("http"):
                img_url = "http://sanjaenews.co.kr" + img_url

            # 상세 페이지 링크
            link_tag = item.select_one("a")
            link = link_tag.get("href").lstrip(".")
            if link and not link.startswith("http"):
                link = "http://sanjaenews.co.kr" + link

# ----------------------------------------------------------------------

            # 상세페이지에서 날짜, 작성자 가져오기
            time.sleep(0.2)
            
            detail_response = requests.get(link)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.text, "lxml")

            datetime = detail_soup.select_one("div.titleWrap > div.registModifyDate > ul > li")
            datetime = datetime.text.strip("기사등록") if datetime else None

            writer = detail_soup.select_one("div.titleWrap > div.else-area > p")
            writer = writer.text.strip() if writer else None

            news_list.append({
                "title": title,
                "content": content,
                "image_url": img_url,
                "link": link,
                "writer": writer,
                "created_at": datetime,
            })

            time.sleep(0.2)

        page += 1

    return render(request, "news_list.html", {
        "news": news_list
    })

