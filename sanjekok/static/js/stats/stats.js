document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn   = document.getElementById("myInjuryBtn");
    const dropdown      = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea    = document.getElementById("stats-visual-area");
    const injuryDetail  = document.getElementById("injuryDetail");
    const accidentItems   = document.querySelectorAll(".accident-item");
    const accidentSummary = document.getElementById("accidentSummary");
    const fatalItems      = document.querySelectorAll(".fatal-item");
    const fatalSummary    = document.getElementById("fatalSummary");

    // 산재 선택 여부
    let injurySelected = false;

    // 가장 최신 연도 구하기 (재해 데이터 기준)
    let maxYear = null;
    if (accidentItems.length > 0) {
        const years = Array.from(accidentItems)
            .map(li => parseInt(li.dataset.year, 10))
            .filter(y => !isNaN(y));
        if (years.length > 0) {
            maxYear = Math.max(...years);
        }
    }

    // "나의 산재" 버튼 → 드롭다운 열기/닫기
    if (myInjuryBtn && dropdown) {
        myInjuryBtn.addEventListener("click", () => {
            dropdown.classList.toggle("hidden");
        });
    }

    // 산재 선택
    if (dropdown) {
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

                if (injuryDetail) {
                    injuryDetail.innerHTML = html;
                }

                injurySelected = true;

                // 분석기간 초기화 + 통계 숨김 + 요약 초기화
                periodButtons.forEach((b) => b.classList.remove("active"));
                if (visualArea) {
                    visualArea.classList.add("hidden");
                }
                if (accidentSummary) {
                    accidentSummary.textContent = "";
                }
                if (fatalSummary) {
                    fatalSummary.textContent = "";
                }

                dropdown.classList.add("hidden");
            });
        });
    }

    // 분석 기간 버튼 클릭
    periodButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            // 1) 산재를 아직 선택 안 했으면 막기
            if (!injurySelected) {
                alert("먼저 '나의 산재'를 선택해주세요.");
                return;
            }

            // 2) 통계 영역은 무조건 열기
            if (visualArea) {
                visualArea.classList.remove("hidden");
            }

            // 데이터가 아예 없으면 안내만 띄우기
            if (!accidentItems.length || maxYear === null || isNaN(maxYear)) {
                if (accidentSummary) {
                    accidentSummary.textContent = "통계 데이터가 없습니다.";
                }
                if (fatalSummary) {
                    fatalSummary.textContent = "";
                }
                return;
            }

            // 버튼 active 표시
            periodButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

           
            const nYear     = parseInt(btn.dataset.year, 10);  // 1, 2, 3
            const startYear = maxYear - nYear + 1;

            // ───────────── 재해자수 + 재해율 집계 ─────────────
            let accTotalCount = 0;    // 재해자수 합계
            let accRateSum    = 0;    // 재해율 합
            let accYearCount  = 0;    // 포함된 연도 개수

            accidentItems.forEach(li => {
                const year  = parseInt(li.dataset.year, 10);
                const count = parseInt(li.dataset.count, 10);
                const rate  = parseFloat(li.dataset.rate);

                if (!isNaN(year) && year >= startYear && year <= maxYear) {
                    accTotalCount += isNaN(count) ? 0 : count;
                    if (!isNaN(rate)) {
                        accRateSum   += rate;
                        accYearCount += 1;
                    }
                }
            });

            const accRateAvg = accYearCount ? accRateSum / accYearCount : 0;

            if (accidentSummary) {
                accidentSummary.textContent =
                    `재해자수: ${accTotalCount.toLocaleString()}명, ` +
                    `재해율: ${accRateAvg.toFixed(2)}`;
            }

            // ───────────── 사망자수 + 사망만인율 집계 ─────────────
            if (fatalItems.length && fatalSummary) {
                let fatalTotalCount = 0;   // 사망자수 합계
                let fatalRateSum    = 0;   // 사망만인율 합
                let fatalYearCount  = 0;   // 포함된 연도 개수

                fatalItems.forEach(li => {
                    const year  = parseInt(li.dataset.year, 10);
                    const count = parseInt(li.dataset.count, 10);
                    const rate  = parseFloat(li.dataset.rate);

                    if (!isNaN(year) && year >= startYear && year <= maxYear) {
                        fatalTotalCount += isNaN(count) ? 0 : count;
                        if (!isNaN(rate)) {
                            fatalRateSum   += rate;
                            fatalYearCount += 1;
                        }
                    }
                });

                const fatalRateAvg = fatalYearCount ? fatalRateSum / fatalYearCount : 0;

                fatalSummary.textContent =
                    `사망자수: ${fatalTotalCount.toLocaleString()}명, ` +
                    `사망만인율: ${fatalRateAvg.toFixed(2)}`;
            }
        });
    });
});
