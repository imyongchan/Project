# 정보 추출
from .fetch import absolute_url

# 목록페이지
def parse_list_page(soup):

    items = soup.select("div#contents > div.basicList > ul > li")
    results = []

    for item in items:
        
        # 제목
        title = item.select_one("dt.title a").get_text(strip=True)
        
        # 내용(요약X)
        content = item.select_one("dd.content a").get_text(strip=True)

        # 이미지
        img_tag = item.select_one("a.image img")
        img_url = absolute_url(img_tag.get("src")) if img_tag else None  # 절대경로 변환

        # 상세 링크
        link_tag = item.select_one("dt.title a")
        link = absolute_url(link_tag.get("href"))

        # 작성일자
        date_tag = item.select_one("dd.registDate")
        created_at_raw = date_tag.text.strip() if date_tag else None

        results.append({
            "title": title,
            "content": content,
            "img_url": img_url,
            "link": link,
            "created_at_raw": created_at_raw,
        })

    return results

# 상세페이지 - 작성자 정보만..
def parse_detail_page(soup):
    writer_tag = soup.select_one("div.titleWrap > div.else-area > p")
    writer = writer_tag.text.strip() if writer_tag else None
    return {
        "writer": writer
        }
