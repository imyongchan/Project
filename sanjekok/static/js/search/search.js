let map;
let userMarker = null;
let incidentMarkers = [];
let infoOverlay = null;

const ctx = window.SEARCH_CONTEXT || { home: "", work: "", accidentList: [] };

// 지도 형태
function initMap() {
    map = new kakao.maps.Map(document.getElementById("map"), {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 5
    });

    // 지도 이동/확대/축소가 끝날 때마다 주변 산재 새로 조회
    kakao.maps.event.addListener(map, "idle", updateIncidents);

    const homeBtn = document.getElementById("btnHome");
    const workBtn = document.getElementById("btnWork");

    // 집 버튼
    if (ctx.home && ctx.home.trim() !== "") {
        homeBtn.onclick = () => moveToAddress(ctx.home);
    } else {
        homeBtn.onclick = () => alert("등록된 집 주소가 없습니다.");
        homeBtn.classList.add("btn-disabled");
    }

    // 근무지 버튼
    if (ctx.work && ctx.work.trim() !== "") {
        workBtn.onclick = () => moveToAddress(ctx.work);
    } else {
        workBtn.onclick = () => alert("등록된 근무지 주소가 없습니다.");
        workBtn.classList.add("btn-disabled");
    }

    initAccidentDropdown();
}

// 주소 검색
function geocode(address, callback) {
    if (!address || address.trim() === "") {
        alert("유효한 주소가 없습니다.");
        return;
    }

    fetch(`/search/geocode/?query=${encodeURIComponent(address)}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("지오코딩 요청 실패 (status: " + res.status + ")");
            }
            return res.json();
        })
        .then(data => {
            if (!data.documents || data.documents.length === 0) {
                alert("주소를 찾을 수 없습니다.");
                return;
            }
            callback(data.documents[0]);
        })
        .catch(err => {
            console.error("GEOCODE ERROR:", err);
            alert("주소 검색 중 오류가 발생했습니다.");
        });
}

// 지도 이동
function moveToAddress(address) {
    if (!address || address.trim() === "") {
        alert("등록된 주소가 없습니다.");
        return;
    }

    geocode(address, result => {
        // 문자열 → 숫자로 변환해서 LatLng 생성
        const lat = parseFloat(result.y);
        const lng = parseFloat(result.x);
        const pos = new kakao.maps.LatLng(lat, lng);

        // 항상 중심/레벨 재설정
        map.setCenter(pos);
        map.setLevel(5);

        if (!userMarker) {
            // 집/근무지 기준 마커 (기존 그대로 사용)
            userMarker = new kakao.maps.Marker({
                map,
                position: pos,
                image: new kakao.maps.MarkerImage(
                    "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png",
                    new kakao.maps.Size(24, 35)
                )
            });
        } else {
            userMarker.setPosition(pos);
        }

        // 중심 변경 후 주변 산재 재조회
        updateIncidents();
    });
}

// 반경(km)
function getRadiusKm(level) {
    return 100 * Math.pow(2, level - 5);
}

// 산업재해 API 호출
function updateIncidents() {
    if (!map) return;

    const c = map.getCenter();
    const radius = getRadiusKm(map.getLevel());

    fetch(`/search/incidents/?lat=${c.getLat()}&lng=${c.getLng()}&radius=${radius}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("산재 조회 요청 실패 (status: " + res.status + ")");
            }
            return res.json();
        })
        .then(data => {
            if (!data || data.error) {
                console.error("INCIDENT API ERROR:", data && data.error);
                return;
            }

            document.getElementById("totalCount").textContent = data.totalCount ?? 0;

            // 기존 마커 제거
            incidentMarkers.forEach(m => m.setMap(null));
            incidentMarkers = [];

            if (!data.items || !Array.isArray(data.items)) return;

            // ✅ 산재 전용 마커 이미지 (출발 아이콘 대신 다른 아이콘)
            const accidentMarkerImage = new kakao.maps.MarkerImage(
                "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png",
                new kakao.maps.Size(24, 35),
                {
                    offset: new kakao.maps.Point(12, 35) // 기준점을 하단 중앙으로
                }
            );

            data.items.forEach(item => {
                if (item.lat == null || item.lng == null) return;

                const pos = new kakao.maps.LatLng(item.lat, item.lng);

                const marker = new kakao.maps.Marker({
                    map,
                    position: pos,
                    image: accidentMarkerImage   // ← 여기서 산재용 마커 사용
                });

                kakao.maps.event.addListener(marker, "click", () => {
                    showIncidentInfoWindow(item);
                });

                incidentMarkers.push(marker);
            });
        })
        .catch(err => {
            console.error("INCIDENT FETCH ERROR:", err);
        });
}

// 산재 상세정보
function showIncidentInfoWindow(item) {
    if (infoOverlay) infoOverlay.setMap(null);

    const content = `
        <div class="infowindow-wrap">
            <div class="infowindow-box">
                <div class="info-title">산업재해 정보</div>
                <div><strong>관할구역:</strong> ${item.area || "-"}</div>
                <div><strong>소재지:</strong> ${item.location || "-"}</div>
            </div>
            <div class="infowindow-arrow"></div>
        </div>
    `;

    infoOverlay = new kakao.maps.CustomOverlay({
        position: new kakao.maps.LatLng(item.lat, item.lng),
        content: content,
        yAnchor: 1.3
    });

    infoOverlay.setMap(map);
}

// 사고지역 드롭다운
function initAccidentDropdown() {
    const btn = document.getElementById("accidentDropdownBtn");
    const menu = document.getElementById("accidentDropdownMenu");

    if (!btn || !menu) return;

    if (!ctx.accidentList || ctx.accidentList.length === 0) {
        btn.textContent = "등록된 사고지역 없음";
        btn.disabled = true;
        btn.classList.add("btn-disabled");
        return;
    }

    ctx.accidentList.forEach(ac => {
        const d = document.createElement("div");
        d.className = "dropdown-item";
        d.textContent = ac.alias;

        d.onclick = () => {
            btn.textContent = ac.alias + " ▼";
            menu.style.display = "none";
            moveToAddress(ac.address);
        };

        menu.appendChild(d);
    });

    btn.onclick = () => {
        menu.style.display = menu.style.display === "block" ? "none" : "block";
    };

    document.addEventListener("click", e => {
        if (!btn.contains(e.target) && !menu.contains(e.target)) {
            menu.style.display = "none";
        }
    });
}

window.onload = initMap;
