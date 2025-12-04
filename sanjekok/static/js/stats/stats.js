document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn   = document.getElementById("myInjuryBtn");
    const dropdown      = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea    = document.getElementById("stats-visual-area");
    const injuryDetail  = document.getElementById("injuryDetail");
    const accidentSummary = document.getElementById("accidentSummary"); // 재해 요약
    const fatalSummary    = document.getElementById("fatalSummary");    // 사망 요약
    const genderSummary   = document.getElementById("genderSummary");   // 성비 요약(있으면)

    // 산재 선택 여부
    let injurySelected = false;

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

                // 산재 선택 완료
                injurySelected = true;

                // 분석기간 초기화 + 통계 숨김 + 요약 초기화
                periodButtons.forEach((b) => b.classList.remove("active"));
                if (visualArea) {
                    visualArea.classList.add("hidden");
                }
                if (accidentSummary) accidentSummary.textContent = "";
                if (fatalSummary)    fatalSummary.textContent    = "";
                if (genderSummary)   genderSummary.textContent   = "";

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

            // 2) 통계 영역 보이기
            if (visualArea) {
                visualArea.classList.remove("hidden");
            }

            // 3) 버튼 active 표시
            periodButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // 4) 버튼에 박혀 있는 데이터 읽기
            const label = btn.innerText.trim(); // "최근 1년" / "2년" / "3년"

            const accCount    = Number(btn.dataset.accCount    || 0); // 재해자수
            const accRate     = Number(btn.dataset.accRate     || 0); // 재해율
            const fatalCount  = Number(btn.dataset.fatalCount  || 0); // 사망자수
            const fatalRate   = Number(btn.dataset.fatalRate   || 0); // 사망만인율

            const male        = Number(btn.dataset.male        || 0); // 남자
            const female      = Number(btn.dataset.female      || 0); // 여자
            const maleRate    = Number(btn.dataset.maleRate    || 0); // 남자비율(%)
            const femaleRate  = Number(btn.dataset.femaleRate  || 0); // 여자비율(%)

            // 5) (재해)
            if (accidentSummary) {
                const rateText = isNaN(accRate) ? "-" : accRate.toFixed(2);
                accidentSummary.textContent =
                    `재해자수: ${accCount.toLocaleString()}명, ` +
                    `재해율: ${rateText}`;
            }

            // 6)  (사망)
            if (fatalSummary) {
                const rateText = isNaN(fatalRate) ? "-" : fatalRate.toFixed(2);
                fatalSummary.textContent =
                    `사망자수: ${fatalCount.toLocaleString()}명, ` +
                    `사망만인율: ${rateText}`;
            }

            // 7) (성별 재해 비율)
            if (genderSummary) {
                const maleRateText   = isNaN(maleRate)   ? "-" : maleRate.toFixed(1);
                const femaleRateText = isNaN(femaleRate) ? "-" : femaleRate.toFixed(1);

                genderSummary.textContent =
                    `남자: ${male.toLocaleString()}명 (${maleRateText}%), ` +
                    `여자: ${female.toLocaleString()}명 (${femaleRateText}%)`;
            }
        });
    });
});
