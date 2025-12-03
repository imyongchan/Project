let map, marker;
let accidentMarkers = [];

// 사용자 좌표 (TM 좌표)
const locationsTM = {
    home: { x: HOME_TM.x, y: HOME_TM.y },
    work: { x: WORK_TM.x, y: WORK_TM.y }
};

// -----------------------------
// Kakao Map Script Loader
// -----------------------------
function loadKakaoMapScript(callback) {
    const script = document.createElement("script");
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&libraries=services&autoload=false`;
    script.onload = callback;
    document.head.appendChild(script);
}

loadKakaoMapScript(() => {
    kakao.maps.load(() => {
        const mapContainer = document.querySelector(".map-placeholder");
        map = new kakao.maps.Map(mapContainer, {
            center: new kakao.maps.LatLng(37.5665, 126.9780),
            level: 4
        });

        // 기본 마커 (현재 위치)
        marker = new kakao.maps.Marker({
            position: map.getCenter(),
            map: map
        });

        enableMapFunctions();

        // 초기 위치: 집
        moveToTM(locationsTM.home);
    });
});

// -----------------------------
// TM 좌표 → 위도/경도 변환
// -----------------------------
function tmToLatLng(tmX, tmY, callback) {
    if (!kakao.maps.services.coordTrans || !kakao.maps.services.coordTrans.fromTM128) {
        console.error("coordTrans 라이브러리 불러오기 실패");
        return;
    }

    kakao.maps.services.coordTrans.fromTM128(
        new kakao.maps.LatLng(tmY, tmX),
        function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                callback(result.y, result.x);
            } else {
                console.error("좌표 변환 실패:", status);
            }
        }
    );
}

// -----------------------------
// 지도 이동 + 메인 마커 이동
// -----------------------------
function moveToTM(tm) {
    tmToLatLng(tm.x, tm.y, (lat, lng) => {
        const pos = new kakao.maps.LatLng(lat, lng);
        map.setCenter(pos);
        marker.setPosition(pos);

        fetchAndShowAccidents(lat, lng);
    });
}

// -----------------------------
// 산업재해 데이터 fetch + 마커 표시
// -----------------------------
async function fetchAndShowAccidents(lat, lng) {
    try {
        const res = await fetch(`/accident-proxy?numOfRows=200&pageNo=1`);
        const text = await res.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (err) {
            console.error("API 응답이 JSON이 아닙니다:", text);
            updateTotalCount(0);
            return;
        }

        const items = data?.response?.body?.items || [];
        const nearby = items.filter(item => {
            if (!item.la || !item.lo) return false;
            const dist = getDistance(lat, lng, parseFloat(item.la), parseFloat(item.lo));
            return dist <= 1000; // 1km 반경
        });

        updateTotalCount(nearby.length);
        showMarkers(nearby);
    } catch (err) {
        console.error("API 오류:", err);
        updateTotalCount(0);
    }
}

// -----------------------------
// 거리 계산 (Haversine)
// -----------------------------
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

// -----------------------------
// 산업재해 마커 표시
// -----------------------------
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
            content: `
                <div style="padding:5px; font-size:12px;">
                    <strong>${i.area_nm}</strong><br>
                    발생년도: ${i.syd_year}<br>
                    소재지: ${i.locplc}
                </div>`
        });

        kakao.maps.event.addListener(m, "click", () => info.open(map, m));
        accidentMarkers.push(m);
    });
}

// -----------------------------
// 총 발생건수 업데이트
// -----------------------------
function updateTotalCount(count) {
    document.getElementById("totalCount").textContent = count;
}

// -----------------------------
// 버튼 및 사고지역 클릭 이벤트
// -----------------------------
function enableMapFunctions() {
    // 집 버튼
    const homeBtn = document.getElementById("homeBtn");
    const workBtn = document.getElementById("workBtn");
    const incidentBtn = document.getElementById("incidentBtn");
    const incidentMenu = document.getElementById("incidentMenu");

    if (homeBtn) homeBtn.addEventListener("click", () => moveToTM(locationsTM.home));
    if (workBtn) workBtn.addEventListener("click", () => moveToTM(locationsTM.work));

    if (incidentBtn && incidentMenu) {
        incidentBtn.addEventListener("click", () => {
            incidentMenu.style.display = incidentMenu.style.display === "block" ? "none" : "block";
        });

        incidentMenu.querySelectorAll("div").forEach(item => {
            item.addEventListener("click", () => {
                const tmX = parseFloat(item.dataset.x);
                const tmY = parseFloat(item.dataset.y);
                if (!isNaN(tmX) && !isNaN(tmY)) {
                    moveToTM({ x: tmX, y: tmY });
                }
                incidentMenu.style.display = "none";
            });
        });
    }
}
