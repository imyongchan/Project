// static/JS/hospital/hospital_detail.js

document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;

  const KAKAO_KEY = body.dataset.kakaoKey;
  const LAT = parseFloat(body.dataset.lat || "0");
  const LNG = parseFloat(body.dataset.lng || "0");
  const HOSPITAL_NAME = body.dataset.hospitalName || "";

  if (!KAKAO_KEY || !LAT || !LNG) {
    // 좌표가 없으면 지도 로딩 생략
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
