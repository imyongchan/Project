// static/js/hospital/hospital.js

let currentBaseAddress = null;  // 기준 주소 문자열
let currentSort = "distance";   // distance | rating | review

const hospitalApiUrl =
  document.body.dataset.hospitalApiUrl || "/hospital/api/";

const ctx = window.HOSPITAL_CONTEXT || {
  home: "",
  work: "",
  accidents: []   // [{ id, title, address }, ...]
};

// 메시지 출력 (오류 상황 등에만 사용)
function setMessage(text) {
  const msgEl = document.getElementById("hospital-message");
  if (!msgEl) return;
  msgEl.textContent = text || "";
}

// 특정 주소를 기준 위치로 사용 (지오코딩 없이 주소만 넘김)
function useAddress(address, label) {
  if (!address || address.trim() === "") {
    alert(`${label} 주소가 등록되어 있지 않습니다.`);
    return;
  }

  currentBaseAddress = address;
  loadHospitals();
}

// 사고 1건을 선택해서 사용 (label 은 산재제목)
function useAccident(accident) {
  if (!accident || !accident.address) {
    alert("해당 사고의 주소 정보가 없습니다.");
    return;
  }
  useAddress(accident.address, accident.title || "사고지역");
}

// 병원 리스트 렌더링
// [번호] / 의료 기관명 / 주소 / 전화번호 / >>상세보기 만 출력
function renderHospitalList(hospitals) {
  const listEl = document.getElementById("hospital-list");
  if (!listEl) return;

  listEl.innerHTML = "";

  if (!hospitals || hospitals.length === 0) {
    return;
  }

  hospitals.forEach((h, index) => {
    const li = document.createElement("li");
    li.className = "hospital-item";

    const name = h.name || "의료기관명 없음";
    const addr = h.road_address || h.address || "-";
    const tel = h.tel || "-";
    const detailUrl = h.detail_url || "#";

    li.innerHTML =
      '<div class="hospital-rank">[' + (index + 1) + ']</div>' +
      '<div class="hospital-info">' +
      '  <div class="hospital-line"><span class="label">의료 기관명:</span> ' + name + '</div>' +
      '  <div class="hospital-line"><span class="label">주소:</span> ' + addr + '</div>' +
      '  <div class="hospital-line"><span class="label">전화번호:</span> ' + tel + '</div>' +
      '</div>' +
      '<a class="btn-detail" href="' + detailUrl + '">>>상세보기</a>';

    listEl.appendChild(li);
  });
}

// 병원 API 호출
function loadHospitals() {
  if (!currentBaseAddress) {
    setMessage("먼저 조회할 위치(집/근무지/사고지역)를 선택해 주세요.");
    renderHospitalList([]);
    return;
  }

  const url =
    hospitalApiUrl +
    "?addr=" + encodeURIComponent(currentBaseAddress) +
    "&sort=" + encodeURIComponent(currentSort);

  fetch(url)
    .then(res => {
      if (!res.ok) {
        throw new Error("HTTP " + res.status);
      }
      return res.json();
    })
    .then(data => {
      if (data.error) {
        setMessage("병원 조회 중 오류가 발생했습니다: " + data.error);
        renderHospitalList([]);
        return;
      }
      const hospitals = data.hospitals || [];
      renderHospitalList(hospitals);
    })
    .catch(err => {
      console.error(err);
      renderHospitalList([]);
    });
}

// 정렬 드롭다운 (사진 오른쪽 '구분' 영역)
function initSortDropdown() {
  const sortBtn = document.getElementById("sortBtn");
  const sortMenu = document.getElementById("sortMenu");
  if (!sortBtn || !sortMenu) return;

  sortBtn.addEventListener("click", () => {
    sortMenu.classList.toggle("open");
  });

  sortMenu.querySelectorAll(".sort-option").forEach(opt => {
    opt.addEventListener("click", () => {
      const sort = opt.dataset.sort || "distance";
      currentSort = sort;

      let label = "거리순";
      if (sort === "rating") label = "평점순";
      else if (sort === "review") label = "리뷰 많은 순";

      sortBtn.textContent = label + " ▼";
      sortMenu.classList.remove("open");

      if (currentBaseAddress) {
        loadHospitals();
      }
    });
  });

  document.addEventListener("click", e => {
    if (!sortMenu.classList.contains("open")) return;
    if (!sortMenu.contains(e.target) && e.target !== sortBtn) {
      sortMenu.classList.remove("open");
    }
  });
}

// 버튼 이벤트 초기화 (위치선택: 집 / 근무지 / 사고지역들)
function initUIEvents() {
  const btnHome = document.getElementById("btn-home");
  const btnWork = document.getElementById("btn-work");
  const btnAcc  = document.getElementById("btn-accident");
  const accMenu = document.getElementById("accidentMenu");

  // 집 버튼
  if (btnHome) {
    if (ctx.home && ctx.home.trim() !== "") {
      btnHome.addEventListener("click", () => useAddress(ctx.home, "집"));
    } else {
      btnHome.addEventListener("click", () =>
        alert("등록된 집 주소가 없습니다.")
      );
      btnHome.classList.add("btn-disabled");
    }
  }

  // 근무지 버튼
  if (btnWork) {
    if (ctx.work && ctx.work.trim() !== "") {
      btnWork.addEventListener("click", () => useAddress(ctx.work, "근무지"));
    } else {
      btnWork.addEventListener("click", () =>
        alert("등록된 근무지 주소가 없습니다.")
      );
      btnWork.classList.add("btn-disabled");
    }
  }

  // 사고지역 드롭다운 (여러 사고)
  if (btnAcc && accMenu) {
  if (ctx.accidents && ctx.accidents.length > 0) {
    // 메뉴 항목 생성
    accMenu.innerHTML = "";
    ctx.accidents.forEach(accident => {
      const item = document.createElement("div");
      item.className = "accident-option";
      item.textContent = accident.title || "사고지역";
      item.addEventListener("click", () => {
        accMenu.classList.remove("open");
        useAccident(accident);
      });
      accMenu.appendChild(item);
    });

    // 버튼 클릭 시 메뉴 열기/닫기
    btnAcc.addEventListener("click", () => {
      accMenu.classList.toggle("open");
    });

    // 바깥 클릭 시 메뉴 닫기
    document.addEventListener("click", e => {
      if (!accMenu.classList.contains("open")) return;
      if (!accMenu.contains(e.target) && e.target !== btnAcc) {
        accMenu.classList.remove("open");
      }
    });
  } else {
    btnAcc.addEventListener("click", () =>
      alert("등록된 사고지역이 없습니다.")
    );
    btnAcc.classList.add("btn-disabled");
  }
}

  initSortDropdown();

  // 기본값: 집 → 근무지 → 첫 번째 사고
  if (btnHome && !btnHome.classList.contains("btn-disabled")) {
    btnHome.click();
  } else if (btnWork && !btnWork.classList.contains("btn-disabled")) {
    btnWork.click();
  } else if (ctx.accidents && ctx.accidents.length > 0) {
    useAccident(ctx.accidents[0]);
  }
}

document.addEventListener("DOMContentLoaded", initUIEvents);
