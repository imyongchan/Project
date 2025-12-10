// static/js/hospital/hospital.js

let currentCenter = null;
let currentSort = "distance";

// Ajax로 병원 리스트 가져오기
function loadHospitals() {
  if (!currentCenter) return;

  const lat = currentCenter.lat;
  const lng = currentCenter.lng;
  const url = "/hospital/api/?lat=" + lat + "&lng=" + lng + "&sort=" + currentSort;

  fetch(url)
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      if (data.error) {
        console.error(data.error);
        return;
      }
      const hospitals = data.hospitals || [];
      renderHospitalList(hospitals);
    })
    .catch(function (err) {
      console.error("병원 조회 실패", err);
    });
}

// 리스트 렌더링
function renderHospitalList(hospitals) {
  const listEl = document.getElementById("hospital-list");
  listEl.innerHTML = "";

  hospitals.forEach(function (h, idx) {
    const li = document.createElement("li");
    li.className = "hospital-item";

    const detailUrl = h.detail_url;

    li.innerHTML =
      '<div class="rank">[' + (idx + 1) + ']</div>' +
      '<div class="info">' +
      '  <div class="name">' + (h.name || "이름 없음") + "</div>" +
      '  <div class="addr">주소: ' + (h.road_address || h.address || "-") + "</div>" +
      '  <div class="tel">전화번호: ' + (h.tel || "-") + "</div>" +
      '  <div class="extra">거리: ' + h.distance_km + "km" +
      '    &nbsp;|&nbsp; 평점: ' + (h.rating ?? "-") +
      '    &nbsp;|&nbsp; 리뷰: ' + (h.review_count ?? "-") +
      "  </div>" +
      "</div>" +
      '<a class="btn-detail" href="' + detailUrl + '">>>상세보기</a>';

    listEl.appendChild(li);
  });
}

// 이벤트 등록
function initUIEvents() {
  const btnHome = document.getElementById("btn-home");
  const btnWork = document.getElementById("btn-work");
  const btnAcc  = document.getElementById("btn-accident");
  const sortBtn = document.getElementById("sortBtn");
  const sortMenu = document.getElementById("sortMenu");

  function bindLocationButton(btn) {
    if (!btn || btn.disabled) return;
    btn.addEventListener("click", function () {
      const lat = parseFloat(btn.dataset.lat);
      const lng = parseFloat(btn.dataset.lng);
      if (isNaN(lat) || isNaN(lng)) return;
      currentCenter = { lat: lat, lng: lng };
      loadHospitals();
    });
  }

  bindLocationButton(btnHome);
  bindLocationButton(btnWork);
  bindLocationButton(btnAcc);

  // 정렬 드롭다운
  sortBtn.addEventListener("click", function () {
    sortMenu.classList.toggle("open");
  });

  sortMenu.querySelectorAll(".sort-option").forEach(function (item) {
    item.addEventListener("click", function () {
      const sort = item.dataset.sort;
      currentSort = sort;

      let label = "거리순";
      if (sort === "rating") label = "평점순";
      if (sort === "review") label = "리뷰 많은 순";

      sortBtn.textContent = label + " ▼";
      sortMenu.classList.remove("open");

      loadHospitals();
    });
  });

  // 기본값: 집 → 근무지 → 사고지역 순으로 사용 가능한 버튼 자동 클릭
  if (btnHome && !btnHome.disabled) {
    btnHome.click();
  } else if (btnWork && !btnWork.disabled) {
    btnWork.click();
  } else if (btnAcc && !btnAcc.disabled) {
    btnAcc.click();
  }
}

document.addEventListener("DOMContentLoaded", initUIEvents);
