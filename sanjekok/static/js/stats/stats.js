document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn   = document.getElementById("myInjuryBtn");
    const dropdown      = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea    = document.getElementById("stats-visual-area");
    const injuryDetail  = document.getElementById("injuryDetail");

    // 재해자수 데이터
    const accidentItems   = document.querySelectorAll(".accident-item");
    const accidentSummary = document.getElementById("accidentSummary");

    // 산재 선택 여부
    let injurySelected = false;

    // accident_list에서 가장 최신 연도 구하기 
    let maxYear = null;
    if (accidentItems.length > 0) {
        const years = Array.from(accidentItems).map(li => parseInt(li.dataset.year, 10));
        maxYear = Math.max(...years);
    }

    // "나의 산재" 버튼 → 드롭다운 열기/닫기
    myInjuryBtn.addEventListener("click", () => {
        dropdown.classList.toggle("hidden");
    });

    // 산재 선택
    dropdown.querySelectorAll("li").forEach(item => {
        item.addEventListener("click", () => {

            const title   = item.dataset.title;
            const injury  = item.dataset.injury;
            const disease = item.dataset.disease;
            const date    = item.dataset.date;

            let html = "";

            if (title)   html += `<p>산재명: ${title}</p>`;
            if (injury)  html += `<p>발생 형태: ${injury}</p>`;
            if (disease) html += `<p>질병: ${disease}</p>`;
            if (date)    html += `<p>발생일자: ${date}</p>`;

            // 출력 영역 업데이트
            injuryDetail.innerHTML = html;

            // 산재가 하나 선택되었음
            injurySelected = true;

            // 분석기간 초기화 + 통계 숨김 + 합계 초기화
            periodButtons.forEach((b) => b.classList.remove("active"));
            visualArea.classList.add("hidden");
            if (accidentSummary) {
                accidentSummary.textContent = "";
            }

            dropdown.classList.add("hidden");
        });
    });

    // 분석 기간 버튼 클릭 → 산재를 먼저 선택해야 동작
    periodButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            // 산재를 아직 선택 안 했으면 막기
            if (!injurySelected) {
                alert("먼저 '나의 산재'를 선택해주세요.");
                return;
            }

            // accident 데이터 없으면 합산 안 함
            if (!accidentItems.length || maxYear === null) {
                return;
            }

            // 버튼 active 표시
            periodButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // 통계 영역 보이기
            visualArea.classList.remove("hidden");

            // 최근 N년 계산
            const nYear    = parseInt(btn.dataset.year, 10);  // 1, 2, 3
            const startYear = maxYear - nYear + 1;

            let total = 0;

            // li 순회하면서 합산
            accidentItems.forEach(li => {
                const year  = parseInt(li.dataset.year, 10);
                const count = parseInt(li.dataset.count, 10);

                if (year >= startYear && year <= maxYear) {
                    total += isNaN(count) ? 0 : count;
                }
            });

            // 합계 문구 출력
            if (accidentSummary) {
                accidentSummary.textContent =
                    `재해자수: ` +
                    `${total.toLocaleString()}명`;
            }
        });
    });
});
