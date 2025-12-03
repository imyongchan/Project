let map, marker;
let accidentMarkers = [];
const locations = {
  home: { lat: 37.5700, lng: 126.9768 },
  work: { lat: 37.5665, lng: 126.9780 }
};

// 카카오맵 로드
function loadKakaoMapScript(callback) {
  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&autoload=false`;
  script.onload = callback;
  document.head.appendChild(script);
}

loadKakaoMapScript(() => {
  kakao.maps.load(() => {
    const mapContainer = document.querySelector(".map-placeholder");
    map = new kakao.maps.Map(mapContainer, {
      center: new kakao.maps.LatLng(locations.home.lat, locations.home.lng),
      level: 4
    });

    marker = new kakao.maps.Marker({ position: map.getCenter(), map: map });

    updateTotalCount(0);
    enableMapFunctions();
  });
});

// 총 발생건수 업데이트
function updateTotalCount(count) {
  document.getElementById("totalCount").textContent = count;
}

// ------------------------------------------------------
// 산재 데이터 fetch (프록시 API 사용)
// ------------------------------------------------------
async function fetchAccidentData(lat, lng) {
  try {
    const res = await fetch(`/accident-proxy?numOfRows=200&pageNo=1`);
    const data = await res.json();

    if (!data?.response?.body?.items) return [];
    const items = data.response.body.items;

    return items.filter(item => {
      if (!item.la || !item.lo) return false;
      const dist = getDistance(lat, lng, parseFloat(item.la), parseFloat(item.lo));
      return dist <= 1000;
    });
  } catch (err) {
    console.error("API 오류:", err);
    return [];
  }
}

// 거리 계산
function getDistance(lat1, lng1, lat2, lng2) {
  const R = 6371000;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(lat1 * Math.PI / 180) *
            Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// ------------------------------------------------------
// 마커 표시 + InfoWindow
// ------------------------------------------------------
function showMarkers(items) {
  accidentMarkers.forEach(m => m.setMap(null));
  accidentMarkers = [];

  items.forEach(i => {
    const lat = parseFloat(i.la);
    const lng = parseFloat(i.lo);
    if (!lat || !lng) return;

    const m = new kakao.maps.Marker({
      position: new kakao.maps.LatLng(lat, lng),
      map: map
    });

    const info = new kakao.maps.InfoWindow({
      content: `<div style="padding:5px; font-size:12px;">
                  <strong>관할: ${i.area_nm}</strong><br/>
                  발생년도: ${i.syd_year}<br/>
                  소재지: ${i.locplc}
                </div>`
    });

    kakao.maps.event.addListener(m, 'click', () => info.open(map, m));

    accidentMarkers.push(m);
  });
}

// ------------------------------------------------------
// 지도 이동 + 데이터 갱신
// ------------------------------------------------------
async function moveToLocation(lat, lng) {
  if (!map || !marker) return;

  const position = new kakao.maps.LatLng(lat, lng);
  map.setCenter(position);
  marker.setPosition(position);

  const nearbyItems = await fetchAccidentData(lat, lng);
  updateTotalCount(nearbyItems.length);
  showMarkers(nearbyItems);
}

// ------------------------------------------------------
// 버튼/드롭다운 기능
// ------------------------------------------------------
function enableMapFunctions() {
  document.getElementById("home").addEventListener("click", () => {
    moveToLocation(locations.home.lat, locations.home.lng);
  });

  document.getElementById("loc").addEventListener("click", () => {
    moveToLocation(locations.work.lat, locations.work.lng);
  });

  const incidentBtn = document.getElementById("incidentBtn");
  const incidentMenu = document.getElementById("incidentMenu");

  incidentBtn.addEventListener("click", () => {
    incidentMenu.style.display =
      incidentMenu.style.display === "block" ? "none" : "block";
  });

  incidentMenu.querySelectorAll("div").forEach(item => {
  item.addEventListener("click", () => {
    const lat = parseFloat(item.dataset.lat);
    const lng = parseFloat(item.dataset.lng);

    if (!isNaN(lat) && !isNaN(lng)) moveToLocation(lat, lng);
    incidentMenu.style.display = "none";
  });
});
}
