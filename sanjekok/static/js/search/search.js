let map;
let userMarker = null;
let incidentMarkers = [];
let infoOverlay = null;

const ctx = window.SEARCH_CONTEXT;

// 지도 형태
function initMap() {
    map = new kakao.maps.Map(document.getElementById("map"), {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 5
    });

    kakao.maps.event.addListener(map, "idle", updateIncidents);

    document.getElementById("btnHome").onclick = () => moveToAddress(ctx.home);
    document.getElementById("btnWork").onclick = () => moveToAddress(ctx.work);

    initAccidentDropdown();
}

// 주소 검색
function geocode(address, callback) {
    fetch(`/search/geocode/?query=${encodeURIComponent(address)}`)
        .then(res => res.json())
        .then(data => {
            if (!data.documents || data.documents.length === 0) {
                alert("주소를 찾을 수 없습니다.");
                return;
            }
            callback(data.documents[0]);
        });
}

// 지도 이동
function moveToAddress(address) {
    geocode(address, result => {
        const lat = result.y;
        const lng = result.x;
        const pos = new kakao.maps.LatLng(lat, lng);

        map.setCenter(pos);
        map.setLevel(5);

        if (!userMarker) {
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

        updateIncidents();
    });
}

// 반경(km)
function getRadiusKm(level) {
    return 100 * Math.pow(2, level - 5);
}

// 산업재해 API 호출
function updateIncidents() {
    const c = map.getCenter();
    const radius = getRadiusKm(map.getLevel());

    fetch(`/search/incidents/?lat=${c.getLat()}&lng=${c.getLng()}&radius=${radius}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("totalCount").textContent = data.totalCount;

            incidentMarkers.forEach(m => m.setMap(null));
            incidentMarkers = [];

            data.items.forEach(item => {
                const pos = new kakao.maps.LatLng(item.lat, item.lng);

                const marker = new kakao.maps.Marker({
                    map,
                    position: pos,
                    image: new kakao.maps.MarkerImage(
                        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/red_b.png",
                        new kakao.maps.Size(34, 39)
                    )
                });

                kakao.maps.event.addListener(marker, "click", () => {
                    showIncidentInfoWindow(item);
                });

                incidentMarkers.push(marker);
            });
        });
}

// 산재 상세정보
function showIncidentInfoWindow(item) {
    if (infoOverlay) infoOverlay.setMap(null);

    const content = `
        <div class="infowindow-wrap">
            <div class="infowindow-box">
                <div class="info-title">산업재해 정보</div>
                <div><strong>관할구역:</strong> ${item.area}</div>
                <div><strong>소재지:</strong> ${item.location}</div>
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
