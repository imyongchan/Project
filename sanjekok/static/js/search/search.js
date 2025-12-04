// search.js
// Kakao Map + Django API 연동 최종 버전

document.addEventListener("DOMContentLoaded", () => {
    const mapContainer = document.getElementById("map");
    const keywordInput = document.getElementById("keyword-input");
    const searchBtn = document.getElementById("search-btn");
    const resultList = document.getElementById("result-list");

    // 기본 지도 설정
    const map = new kakao.maps.Map(mapContainer, {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 5
    });

    // 장소 검색 서비스
    const places = new kakao.maps.services.Places();

    // 검색 실행 함수
    const searchPlaces = () => {
        const keyword = keywordInput.value.trim();
        if (!keyword) return;

        // Django API 호출
        fetch(`${SEARCH_API_URL}?q=` + encodeURIComponent(keyword))
            .then(res => res.json())
            .then(data => {
                displayResults(data.results);
            })
            .catch(err => {
                console.error("API Error:", err);
            });
    };

    // 검색 결과 렌더링
    const displayResults = (placesData) => {
        resultList.innerHTML = "";

        placesData.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.place_name} (${item.address})`;
            li.addEventListener("click", () => {
                map.panTo(new kakao.maps.LatLng(item.lat, item.lng));
            });
            resultList.appendChild(li);
        });
    };

    searchBtn.addEventListener("click", searchPlaces);
});
