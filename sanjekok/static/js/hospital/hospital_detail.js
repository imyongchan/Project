// static/JS/hospital/hospital_detail.js

document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;

  const KAKAO_KEY = body.dataset.kakaoKey;
  const LAT = parseFloat(body.dataset.lat || "0");
  const LNG = parseFloat(body.dataset.lng || "0");
  const HOSPITAL_NAME = body.dataset.hospitalName || "";

  /* =======================
   * 1. 상단 평균 평점 별(반칸) 표시
   * ======================= */
  (function renderHeaderStars() {
    const ratingEl = document.querySelector(".hospital-meta .meta-rating");
    const starsWrap = document.querySelector(".hospital-meta .meta-stars");
    if (!ratingEl || !starsWrap) return;

    // avg_rating: 0.0 ~ 10.0
    let rating = parseFloat(ratingEl.textContent) || 0;
    if (rating < 0) rating = 0;
    if (rating > 10) rating = 10;

    // 기존 "★★★★★" 텍스트 제거
    starsWrap.textContent = "";

    // 별 5개를 1~10점(반칸) 기준으로 표시
    for (let i = 1; i <= 5; i++) {
      const span = document.createElement("span");
      span.classList.add("meta-star");

      const fullValue = i * 2;        // 2,4,6,8,10
      const halfValue = fullValue - 1; // 1,3,5,7,9

      if (rating >= fullValue) {
        // 꽉 찬 별
        span.classList.add("full");
        span.textContent = "★";
      } else if (rating >= halfValue) {
        // 반칸 별
        span.classList.add("half");
        span.classList.add("empty");   // 모양은 ☆, 색은 CSS에서 처리
        span.textContent = "☆";
      } else {
        // 빈 별
        span.classList.add("empty");
        span.textContent = "☆";
      }

      starsWrap.appendChild(span);
    }
  })();

  /* =======================
   * 2. 지도 표시 (카카오맵)
   * ======================= */
  // 좌표가 없으면 지도만 생략 (위 별 표시에는 영향 없음)
  if (!KAKAO_KEY || !LAT || !LNG) {
    return;
  }

  function initDetailMap() {
    const container = document.getElementById("detail-map");
    if (!container) return;

    const options = {
      center: new kakao.maps.LatLng(LAT, LNG),
      level: 4,
    };

    const map = new kakao.maps.Map(container, options);

    const markerPosition = new kakao.maps.LatLng(LAT, LNG);
    const marker = new kakao.maps.Marker({
      position: markerPosition,
      map: map,
    });

    const iwContent =
      '<div style="padding:5px;font-size:12px;"><b>' +
      HOSPITAL_NAME +
      "</b></div>";

    const infowindow = new kakao.maps.InfoWindow({
      content: iwContent,
    });
    infowindow.open(map, marker);
  }

  function loadKakaoMapScript() {
    const script = document.createElement("script");
    script.src =
      "//dapi.kakao.com/v2/maps/sdk.js?appkey=" +
      encodeURIComponent(KAKAO_KEY) +
      "&autoload=false";
    script.onload = function () {
      kakao.maps.load(initDetailMap);
    };
    document.head.appendChild(script);
  }

  loadKakaoMapScript();
});
