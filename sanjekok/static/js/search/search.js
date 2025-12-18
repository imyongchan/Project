let map;
let userMarker = null;
let incidentMarkers = [];
let incidentIndex = new Map();
let infoOverlay = null;

let selectedAccidentId = null;
let pendingAccidentSelect = null;

// ✅ (추가) 지도 줌/이동(idle)로 updateIncidents()가 연속 호출될 때,
// 늦게 도착한 이전 응답이 최신 상태를 덮어쓰지 않도록 방지
let incidentsRequestSeq = 0;
let incidentsAbortController = null;

const ctx = window.SEARCH_CONTEXT || { home: "", work: "", accidentList: [] };
const DEFAULT_DETAIL_TEXT = "위치를 선택하거나 마커를 클릭하면 상세 정보가 표시됩니다.";
const ACCIDENT_BTN_DEFAULT_TEXT = "사고지역";

// overlay를 항상 제일 위로
const OVERLAY_ZINDEX = 99999;

// 말풍선이 지도 경계에서 떨어져야 하는 여백(px)
const OVERLAY_PADDING = 20;

// ✅ 말풍선 고정 크기(줄이지 않음)
const DEFAULT_MAX_W = 360;
const DEFAULT_MAX_H = 260;

// ✅ 마커와 말풍선이 겹치지 않게 벌릴 간격(px)
const OVERLAY_GAP_PX = 20;

// ✅ 지도 축소(줌아웃) 제한: level이 클수록 더 축소됨
const MAP_MAX_LEVEL = 12;

function makeSvgPinMarkerImage(colorHex) {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="38" viewBox="0 0 28 38">
      <defs>
        <radialGradient id="grad" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="${colorHex}" stop-opacity="0.9"/>
          <stop offset="100%" stop-color="${colorHex}" stop-opacity="1"/>
        </radialGradient>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="rgba(0,0,0,0.3)"/>
        </filter>
      </defs>
      <path d="M14 1C7 1 1.5 6.5 1.5 13.5c0 8.5 12.5 22.5 12.5 22.5S26.5 22 26.5 13.5C26.5 6.5 21 1 14 1z"
            fill="url(#grad)" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
      <circle cx="14" cy="13.5" r="4.2" fill="#fff" stroke="${colorHex}" stroke-width="1.2" opacity="0.95"/>
    </svg>`;

  const src = "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg);
  return new kakao.maps.MarkerImage(src, new kakao.maps.Size(28, 38), {
    offset: new kakao.maps.Point(14, 38)
  });
}

const MY_ACCIDENT_IMG = makeSvgPinMarkerImage("#f99b18");    // red
const OTHER_ACCIDENT_IMG = makeSvgPinMarkerImage("#bcbcbc"); // yellow
const MY_PLACE_IMG = makeSvgPinMarkerImage("#23333d");       // blue

function getDetailEl() {
  // id가 없으면(class만 있는 경우)도 대비
  return document.getElementById("detail") || document.querySelector(".detail-box");
}

function setDetail(htmlOrText) {
  const detailEl = getDetailEl();
  if (!detailEl) return;
  detailEl.innerHTML = htmlOrText;
}

// ✅ (추가) 안내 문구(DEFAULT_DETAIL_TEXT)는 항상 유지하고, 아래에 상세정보를 붙여서 표시
function setDetailWithItem(item) {
  const detailEl = getDetailEl();
  if (!detailEl) return;

  const infoHtml = `
    <div style="margin-top:10px;">
      <div style="font-weight:800; margin-bottom:6px; color:#2e7d32;">산업재해 상세</div>
      <div><strong>업종(대분류):</strong> ${item.i_industry_type1 || "-"}</div>
      <div><strong>업종(중분류):</strong> ${item.i_industry_type2 || "-"}</div>
      <div><strong>재해일자:</strong> ${item.i_accident_date || "-"}</div>
      <div><strong>발생형태:</strong> ${item.i_injury || "-"}</div>
      <div><strong>질병:</strong> ${item.i_disease_type || "-"}</div>
      <div><strong>발생주소:</strong> ${item.i_address || "-"}</div>
    </div>
  `;

  detailEl.innerHTML = `
    <div>${DEFAULT_DETAIL_TEXT}</div>
    ${infoHtml}
  `;
}

function clearIncidentInfo() {
  if (infoOverlay) {
    infoOverlay.setMap(null);
    infoOverlay = null;
  }
  selectedAccidentId = null;
  setDetail(DEFAULT_DETAIL_TEXT);
}

function clearUserMarker() {
  if (userMarker) {
    userMarker.setMap(null);
    userMarker = null;
  }
}

function resetAccidentDropdownSelection() {
  pendingAccidentSelect = null;

  const btn = document.getElementById("accidentDropdownBtn");
  const menu = document.getElementById("accidentDropdownMenu");

  if (btn) {
    const icon = btn.querySelector("i");
    const label = document.createElement("span");
    label.textContent = ACCIDENT_BTN_DEFAULT_TEXT;

    btn.innerHTML = ""; // 기존 내용 비우고
    if (icon) btn.appendChild(icon); // 아이콘 유지
    btn.appendChild(label);
  }

  if (menu) menu.style.display = "none";
}

function normalizeAddress(addr) {
  return String(addr || "").replace(/\s+/g, "").replace(/[()]/g, "").trim();
}

function spreadOverlappingItems(items) {
  const groups = new Map();

  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const lat = Number(it.lat);
    const lng = Number(it.lng);
    if (!isFinite(lat) || !isFinite(lng)) continue;

    const key = lat.toFixed(6) + "," + lng.toFixed(6);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }

  groups.forEach(group => {
    if (group.length === 1) {
      group[0]._dispLat = group[0].lat;
      group[0]._dispLng = group[0].lng;
      return;
    }

    const baseLat = Number(group[0].lat);
    const baseLng = Number(group[0].lng);

    const radiusLat = 0.00009;
    const latRad = (baseLat * Math.PI) / 180;
    const cosLat = Math.max(Math.cos(latRad), 0.2);

    const n = group.length;
    for (let i = 0; i < n; i++) {
      const angle = (2 * Math.PI * i) / n;
      const dLat = radiusLat * Math.cos(angle);
      const dLng = (radiusLat * Math.sin(angle)) / cosLat;

      group[i]._dispLat = baseLat + dLat;
      group[i]._dispLng = baseLng + dLng;
    }
  });

  return items;
}

/* =========================
 *  말풍선(오버레이) 위치 자동 조정
 *  - 지도 이동 없음
 *  - 크기 줄이지 않음(항상 DEFAULT_MAX_W/H)
 *  - 위/아래/좌/우 + 마커와 간격(px)만 조절
 * ========================= */

function getMarkerPoint(latlng) {
  try {
    const proj = map.getProjection();
    return proj.pointFromCoords(latlng); // container px
  } catch (e) {
    return null;
  }
}

// ✅ 크기 조정(maxW/maxH) 없고, placement/align만 결정
function computeLayoutFromRects(pos, overlayRect) {
  const mapEl = document.getElementById("map");
  if (!mapEl) return { placement: "above", align: "center" };

  const mapW = mapEl.clientWidth;
  const mapH = mapEl.clientHeight;
  const pad = OVERLAY_PADDING;

  // 위/아래
  let placement = "above";
  if (overlayRect.top < pad) placement = "below";
  if (overlayRect.bottom > mapH - pad) placement = "above";

  if (overlayRect.top < pad && overlayRect.bottom > mapH - pad) {
    const pt = getMarkerPoint(pos);
    const y = pt ? pt.y : mapH / 2;
    const roomAbove = y - pad;
    const roomBelow = (mapH - y) - pad;
    placement = roomBelow >= roomAbove ? "below" : "above";
  }

  // 좌/우
  let align = "center";
  if (overlayRect.left < pad) align = "left";
  if (overlayRect.right > mapW - pad) align = "right";

  if (overlayRect.left < pad && overlayRect.right > mapW - pad) {
    const pt = getMarkerPoint(pos);
    const x = pt ? pt.x : mapW / 2;
    const roomLeft = x - pad;
    const roomRight = (mapW - x) - pad;
    align = roomRight >= roomLeft ? "left" : "right";
  }

  return { placement, align };
}

// ✅ 말풍선 HTML: 크기는 고정(360x260) + 마커와 간격(OVERLAY_GAP_PX)
function buildInfoHtml(item, layout) {
  const placement = (layout && layout.placement) ? layout.placement : "above"; // above|below
  const align = (layout && layout.align) ? layout.align : "center";            // left|center|right

  const alignItems =
    align === "left" ? "flex-start" :
    align === "right" ? "flex-end" : "center";

  // ✅ 화살표가 없으니, 마커와 겹치지 않게 박스 자체에 간격만 둠
  const gapStyle =
    placement === "below"
      ? ("margin-top:" + OVERLAY_GAP_PX + "px;")
      : ("margin-bottom:" + OVERLAY_GAP_PX + "px;");

  const boxStyle =
    gapStyle +
    "width:" + DEFAULT_MAX_W + "px;" +
    "max-width:" + DEFAULT_MAX_W + "px;" +
    "max-height:" + DEFAULT_MAX_H + "px;" +
    "overflow:auto;" +
    "background:#fff;" +
    "border:2px solid #2e7d32;" +
    "border-radius:10px;" +
    "padding:12px 14px;" +
    "box-shadow:0 2px 10px rgba(0,0,0,0.15);" +
    "font-size:13px;" +
    "line-height:1.35;";

  const titleStyle =
    "font-weight:800;" +
    "color:#2e7d32;" +
    "margin-bottom:8px;" +
    "font-size:16px;";

  const boxHtml =
    '<div class="oai-box" style="' + boxStyle + '">' +
      '<div style="' + titleStyle + '">산업재해 정보</div>' +
      "<div><strong>업종(대분류):</strong> " + (item.i_industry_type1 || "-") + "</div>" +
      "<div><strong>업종(중분류):</strong> " + (item.i_industry_type2 || "-") + "</div>" +
      "<div><strong>재해일자:</strong> " + (item.i_accident_date || "-") + "</div>" +
      "<div><strong>발생형태:</strong> " + (item.i_injury || "-") + "</div>" +
      "<div><strong>질병:</strong> " + (item.i_disease_type || "-") + "</div>" +
      "<div><strong>발생주소:</strong> " + (item.i_address || "-") + "</div>" +
    "</div>";

  // ✅ 화살표 없이 박스만 렌더
  return (
    '<div class="oai-overlay-root" style="position:relative;z-index:' + OVERLAY_ZINDEX +
      ';display:flex;flex-direction:column;align-items:' + alignItems +
      ';pointer-events:auto;">' +
      boxHtml +
    "</div>"
  );
}

// ✅ yAnchor를 px 기준으로 조절해서 "마커-말풍선 간격"을 일정하게 유지
function calcYAnchorWithGap(placement, overlayHeightPx) {
  const h = Math.max(1, Number(overlayHeightPx || 1));
  const ratio = OVERLAY_GAP_PX / h;

  // above: 기본 1.0(바닥이 마커) → 1.0 + ratio 만큼 더 올림
  // below: 기본 0.0(천장이 마커) → 0.0 - ratio 만큼 더 내림
  return (placement === "below") ? (0.0 - ratio) : (1.0 + ratio);
}

function renderOverlay(item, pos, layout, measuredHeightPx) {
  // xAnchor: left=0, center=0.5, right=1
  let xAnchor = 0.5;
  if (layout.align === "left") xAnchor = 0.0;
  if (layout.align === "right") xAnchor = 1.0;

  const yAnchor = calcYAnchorWithGap(layout.placement, measuredHeightPx);

  const html = buildInfoHtml(item, layout);

  if (infoOverlay) infoOverlay.setMap(null);

  infoOverlay = new kakao.maps.CustomOverlay({
    position: pos,
    content: html,
    xAnchor: xAnchor,
    yAnchor: yAnchor,
    zIndex: OVERLAY_ZINDEX
  });

  infoOverlay.setMap(map);
  // ✅ 안내 문구는 유지하고 상세정보만 추가
  setDetailWithItem(item);
}

function showIncidentInfoWindow(item, markerPos) {
  selectedAccidentId = item.accident_id != null ? item.accident_id : null;

  const pos = markerPos || new kakao.maps.LatLng(item.lat, item.lng);

  // 1) 1차 렌더: 기본(위/중앙)로 띄워서 실제 DOM 높이를 측정
  const firstLayout = { placement: "above", align: "center" };
  renderOverlay(item, pos, firstLayout, DEFAULT_MAX_H);

  // 2) DOM 측정 → 화면 밖이면 placement/align만 바꿔 재렌더(크기 고정)
  setTimeout(function () {
    const mapEl = document.getElementById("map");
    if (!mapEl) return;

    const root = mapEl.querySelector(".oai-overlay-root");
    if (!root) return;

    const mapW = mapEl.clientWidth;
    const mapH = mapEl.clientHeight;

    const r = root.getBoundingClientRect();
    const mapR = mapEl.getBoundingClientRect();

    const rect = {
      left: r.left - mapR.left,
      right: r.right - mapR.left,
      top: r.top - mapR.top,
      bottom: r.bottom - mapR.top,
      width: r.width,
      height: r.height
    };

    const pad = OVERLAY_PADDING;
    const fits =
      rect.left >= pad &&
      rect.top >= pad &&
      rect.right <= mapW - pad &&
      rect.bottom <= mapH - pad;

    if (fits) {
      // ✅ 간격(px) 보정 위해 실제 높이로 한 번 더 yAnchor만 맞춰 재렌더
      renderOverlay(item, pos, firstLayout, rect.height);
      return;
    }

    const nextLayout = computeLayoutFromRects(pos, rect);

    // ✅ 크기는 그대로, 위치만 조정 + 간격(px)은 rect.height로 계산
    renderOverlay(item, pos, nextLayout, rect.height);
  }, 0);
}

function initMap() {
  map = new kakao.maps.Map(document.getElementById("map"), {
    center: new kakao.maps.LatLng(37.5665, 126.978),
    level: 5
  });

  

  // 클릭 + 드래그 + 줌 시작 시 말풍선/상세 닫기
  kakao.maps.event.addListener(map, "click", clearIncidentInfo);
  kakao.maps.event.addListener(map, "dragstart", clearIncidentInfo);
  kakao.maps.event.addListener(map, "zoom_start", clearIncidentInfo);

  map.setMaxLevel(MAP_MAX_LEVEL);
  
  // 지도 이동/줌 끝나면 산재 갱신
  kakao.maps.event.addListener(map, "idle", updateIncidents);

  const homeBtn = document.getElementById("btnHome");
  const workBtn = document.getElementById("btnWork");

  if (ctx.home && ctx.home.trim() !== "") {
    homeBtn.onclick = function () {
      resetAccidentDropdownSelection();
      clearIncidentInfo();
      moveToAddress(ctx.home, { showUserMarker: true });
    };
  } else {
    homeBtn.onclick = function () { alert("등록된 집 주소가 없습니다."); };
    homeBtn.classList.add("btn-disabled");
  }

  if (ctx.work && ctx.work.trim() !== "") {
    workBtn.onclick = function () {
      resetAccidentDropdownSelection();
      clearIncidentInfo();
      moveToAddress(ctx.work, { showUserMarker: true });
    };
  } else {
    workBtn.onclick = function () { alert("등록된 근무지 주소가 없습니다."); };
    workBtn.classList.add("btn-disabled");
  }

  initAccidentDropdown();
  updateIncidents();
}

function geocode(address, callback) {
  if (!address || address.trim() === "") {
    alert("유효한 주소가 없습니다.");
    return;
  }

  fetch("/search/geocode/?query=" + encodeURIComponent(address))
    .then(function (res) {
      if (!res.ok) throw new Error("지오코딩 요청 실패 (status: " + res.status + ")");
      return res.json();
    })
    .then(function (data) {
      if (!data.documents || data.documents.length === 0) {
        alert("주소를 찾을 수 없습니다.");
        return;
      }
      callback(data.documents[0]);
    })
    .catch(function (err) {
      console.error("GEOCODE ERROR:", err);
      alert("주소 검색 중 오류가 발생했습니다.");
    });
}

function moveToAddress(address, opts) {
  opts = opts || {};
  const showUserMarker = opts.showUserMarker !== false;

  if (!address || address.trim() === "") {
    alert("등록된 주소가 없습니다.");
    return;
  }

  geocode(address, function (result) {
    const lat = parseFloat(result.y);
    const lng = parseFloat(result.x);
    const pos = new kakao.maps.LatLng(lat, lng);

    map.setCenter(pos);
    map.setLevel(5);

    if (showUserMarker) {
    if (!userMarker) {
      userMarker = new kakao.maps.Marker({
        map: map,
        position: pos,
        image: MY_PLACE_IMG
      });
    } else {
      userMarker.setMap(map);
      userMarker.setPosition(pos);
      userMarker.setImage(MY_PLACE_IMG);
    }

      // 파랑은 노랑보다 위, 빨강보단 아래
      userMarker.setZIndex(5);
    } else {
      // 사고지역 이동 등: 파란 마커를 표시하지 않음
      clearUserMarker();
    }

    // ✅ 주소 이동 직후 건수 갱신
    setTimeout(updateIncidents, 0);
  });
}

function updateIncidents() {
  if (!map) return;

  // ✅ (추가) 이전 요청 취소 + 마지막 요청만 반영
  if (incidentsAbortController) {
    try { incidentsAbortController.abort(); } catch (e) { /* noop */ }
  }
  incidentsAbortController = (window.AbortController) ? new AbortController() : null;
  const myReqSeq = ++incidentsRequestSeq;

  const bounds = map.getBounds();
  const sw = bounds.getSouthWest();
  const ne = bounds.getNorthEast();

  const url =
    "/search/incidents/?" +
    "swLat=" + sw.getLat() +
    "&swLng=" + sw.getLng() +
    "&neLat=" + ne.getLat() +
    "&neLng=" + ne.getLng();

  const fetchOpts = incidentsAbortController
    ? { signal: incidentsAbortController.signal, cache: "no-store" }
    : { cache: "no-store" };

  fetch(url, fetchOpts)
    .then(function (res) {
      if (!res.ok) throw new Error("산재 조회 요청 실패 (status: " + res.status + ")");
      return res.json();
    })
    .then(function (data) {
      // ✅ 오래된 응답이면 무시
      if (myReqSeq !== incidentsRequestSeq) return;

      if (!data || data.error) {
        console.error("INCIDENT API ERROR:", data && data.error);
        return;
      }

      const count = data.totalCount || 0;
      const countEl = document.getElementById("totalCount");
      if (countEl) countEl.textContent = count;

      incidentMarkers.forEach(function (m) { m.setMap(null); });
      incidentMarkers = [];
      incidentIndex.clear();

      if (!data.items || !Array.isArray(data.items)) {
        if (selectedAccidentId) clearIncidentInfo();
        return;
      }

      const items = spreadOverlappingItems(data.items);

      items.forEach(function (item) {
        if (item.lat == null || item.lng == null) return;

        const dispLat = isFinite(item._dispLat) ? item._dispLat : item.lat;
        const dispLng = isFinite(item._dispLng) ? item._dispLng : item.lng;

        const pos = new kakao.maps.LatLng(dispLat, dispLng);

        const marker = new kakao.maps.Marker({
          map: map,
          position: pos,
          image: item.is_mine ? MY_ACCIDENT_IMG : OTHER_ACCIDENT_IMG
        });

        // 빨강이 노랑보다 앞
        marker.setZIndex(item.is_mine ? 10 : 1);

        kakao.maps.event.addListener(marker, "click", function () {
          showIncidentInfoWindow(item, pos);
        });

        incidentMarkers.push(marker);

        if (item.accident_id != null) {
          incidentIndex.set(String(item.accident_id), { item: item, pos: pos, marker: marker });
        }
      });

      if (selectedAccidentId && !incidentIndex.has(String(selectedAccidentId))) {
        clearIncidentInfo();
      }

      if (pendingAccidentSelect) {
        const want = pendingAccidentSelect;
        pendingAccidentSelect = null;

        const wantNorm = normalizeAddress(want.address);

        let found = items.find(function (it) {
          return it.is_mine === true && normalizeAddress(it.i_address) === wantNorm;
        });

        if (!found) {
          found = items.find(function (it) {
            return normalizeAddress(it.i_address) === wantNorm;
          });
        }

        if (found) {
          const idx = incidentIndex.get(String(found.accident_id));
          const markerPos = idx ? idx.pos : new kakao.maps.LatLng(found.lat, found.lng);

          // 사고지역 선택은 이동 허용
          map.panTo(markerPos);
          showIncidentInfoWindow(found, markerPos);
        }
      }
    })
    .catch(function (err) {
      if (err && err.name === "AbortError") return; // 정상: 이전 요청 취소
      console.error("INCIDENT FETCH ERROR:", err);
    });
}

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

  menu.innerHTML = "";

  ctx.accidentList.forEach(function (ac) {
    const d = document.createElement("div");
    d.className = "dropdown-item";
    d.textContent = ac.alias;

    d.onclick = function () {
      clearIncidentInfo();
      clearUserMarker(); // 사고지역은 파란 마커 표시하지 않음

      btn.textContent = ac.alias;
      menu.style.display = "none";

      pendingAccidentSelect = { address: ac.address };
      moveToAddress(ac.address, { showUserMarker: false });
    };

    menu.appendChild(d);
  });

  btn.onclick = function () {
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  };

  document.addEventListener("click", function (e) {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.style.display = "none";
    }
  });
}

window.onload = initMap;
