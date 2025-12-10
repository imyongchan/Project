# hospital/crawler/run.py
#
# SAFEMAP IF_0025 전체 페이지 크롤링 → Hospital 테이블 저장

import traceback

from .fetch import fetch_hospital_json
from .parse import parse_hospitals
from .save import save_hospitals

NUM_ROWS = 1000   # 1페이지당 요청 건수 (API 최대)
MAX_PAGE = 7      # 최대 7페이지(=7000건)까지 시도


def crawl_hospitals(max_page: int = MAX_PAGE):
    """
    SAFEMAP 산재지정병원(IF_0025) 데이터를 페이지 단위로 가져와
    hospital.models.Hospital 테이블에 저장.

    - pageNo = 1 ~ max_page(기본 7) 까지 반복
    - 각 페이지는 NUM_ROWS(1000) 건 요청
    - 해당 페이지에서 데이터가 0건이면 즉시 종료
    - 해당 페이지에서 데이터 개수가 NUM_ROWS 미만이면 마지막 페이지로 보고 종료
    """
    print("🏥 산재지정병원 IF_0025 크롤링 시작")

    total_saved = 0

    try:
        for page in range(1, max_page + 1):
            print(f"📄 IF_0025 page {page} 요청 중...")

            # 1) API 호출
            try:
                raw_json = fetch_hospital_json(page_no=page, num_rows=NUM_ROWS)
            except Exception as e:
                print(f"❌ IF_0025 요청 실패 (page={page}): {e}")
                traceback.print_exc()
                break

            # 2) 파싱
            try:
                hospitals = parse_hospitals(raw_json)
            except Exception as e:
                print(f"❌ IF_0025 파싱 중 오류 (page={page}): {e}")
                traceback.print_exc()
                break

            # parse_hospitals 가 None 이거나 빈 리스트면 종료
            if not hospitals:
                print("➡ 더 이상 병원 데이터가 없어 종료")
                break

            print(f"  ├─ 파싱된 병원 수: {len(hospitals)}")

            # 3) 저장
            try:
                saved = save_hospitals(hospitals)
            except Exception as e:
                print(f"❌ 병원 저장 중 오류 (page={page}): {e}")
                traceback.print_exc()
                break

            total_saved += saved
            print(f"✅ page {page}: {saved}건 저장 (누적 {total_saved}건)")

            # 이번 페이지가 꽉 차지 않았으면 마지막 페이지라고 판단
            if len(hospitals) < NUM_ROWS:
                print("✅ 마지막 페이지(행 수 < NUM_ROWS)로 판단, 종료")
                break

        if page == max_page and hospitals and len(hospitals) == NUM_ROWS:
            print(f"⏹ 최대 페이지 수({max_page})까지 모두 채움")

    except Exception as e:
        print("❌ 병원 크롤링 중 알 수 없는 오류:", e)
        traceback.print_exc()

    print(f"🏁 산재지정병원 IF_0025 크롤링 종료 (총 {total_saved}건 저장)")
