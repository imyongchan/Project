let map, marker;
let totalCount = 0;

const locations = {
  home: { lat: 37.5700, lng: 126.9768 },
  work: { lat: 37.5665, lng: 126.9780 }
};

function loadKakaoMapScript(callback) {
  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_API_KEY}&autoload=false`;
  script.onload = callback;
  document.head.appendChild(script);
}

loadKakaoMapScript(() => {
  kakao.maps.load(() => {
    const mapContainer = document.querySelector(".map-placeholder");

    const mapOption = {
      center: new kakao.maps.LatLng(locations.home.lat, locations.home.lng),
      level: 4
    };

    map = new kakao.maps.Map(mapContainer, mapOption);

    marker = new kakao.maps.Marker({
      position: map.getCenter()
    });

    marker.setMap(map);

    updateTotalCount(15);
  });
});

function updateTotalCount(count) {
  document.getElementById("totalCount").textContent = count;
}

function moveToLocation(lat, lng) {
  const position = new kakao.maps.LatLng(lat, lng);

  map.setCenter(position);
  marker.setPosition(position);

  const dummyCount = Math.floor(Math.random() * 50);
  updateTotalCount(dummyCount);
}

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

    moveToLocation(lat, lng);
    incidentMenu.style.display = "none";
  });
});
