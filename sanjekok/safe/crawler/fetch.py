# safe/crawler/fetch.py
import requests

BASE_URL = "https://portal.kosha.or.kr/api/portal24/bizV/p/VCPDG01007/selectMediaList"

def fetch_page(shpCd, page=1, rows=12): 
    payload = {
        "shpCd": shpCd,  # 자료형태 요청 인자. 
        "searchCondition": "all",
        "searchValue": None,
        "ascDesc": "desc",
        "page": page,
        "rowsPerPage": rows,
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        headers={
            "Content-Type": "application/json;charset=UTF-8",
        }
    )
    response.raise_for_status()
    return response.json()
