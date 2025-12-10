// static/js/hospital/hospital.js

let currentCenter = null;
let currentSort = "distance";

// Django 템플릿에서 전달한 API URL (없으면 기본값 사용)
const hospitalApiUrl =
  document.body.dataset.hospitalApiUrl || "/hospital/api/";

// 메시지 영역에 텍스트 표시
function setMessage(text) {
  const msgEl = document.getElementById("hospital-message");
  if (!msgEl) return;
  msgEl.textContent = text || "";
}

// Ajax로 병원 리스트 가져오기
function loadHospitals() {
  if (!currentCenter) return;

  const lat = currentCenter.lat;
  const lng = currentCenter.lng;
  const url =
    hospitalApiUrl + "?lat=" + lat + "&lng=" + lng + "&sort=" + currentSort;

  setMessage("전국 산재 지정병원 중에서 가까운 병원 Top 10을 찾는 중입니다...");

  fetch(url)
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      if (data.error) {
        console.error(data.error);
        setMessage("병원 조회 중 오류가 발생했습니다: " + data.error);
        renderHospitalList([]);
        return;
      }
      const hospitals = data.hospitals || [];
      renderHospitalList(hospitals);
      if (hospitals.length === 0) {
        setMessage("주변에 검색된 산재지정의료기관이 없습니다.");
      } else {
        setMessage("");
      }
    })
    .catch(function (err) {
      console.error("병원 조회 실패", err);
      setMessage("병원 조회 실패: " + err);
      renderHospitalList([]);
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

  function clearActiveButtons() {
    [btnHome, btnWork, btnAcc].forEach(function (btn) {
      if (!btn) return;
      btn.classList.remove("active");
    });
  }

  function bindLocationButton(btn) {
    if (!btn || btn.disabled) return;
    btn.addEventListener("click", function () {
      const lat = parseFloat(btn.dataset.lat);
      const lng = parseFloat(btn.dataset.lng);
      if (isNaN(lat) || isNaN(lng)) {
        setMessage("좌표 정보가 올바르지 않습니다.");
        return;
      }
      currentCenter = { lat: lat, lng: lng };

      // 어떤 위치 버튼을 선택했는지 표시(선택 상태)
      clearActiveButtons();
      btn.classList.add("active");

      loadHospitals();
    });
  }

  bindLocationButton(btnHome);
  bindLocationButton(btnWork);
  bindLocationButton(btnAcc);

  // 정렬 드롭다운
  if (sortBtn && sortMenu) {
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
  }

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
