document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn   = document.getElementById("myInjuryBtn");
    const dropdown      = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea    = document.getElementById("stats-visual-area");
    const injuryDetail  = document.getElementById("injuryDetail");
    const accidentSummary = document.getElementById("accidentSummary"); // 재해 요약
    const fatalSummary    = document.getElementById("fatalSummary");    // 사망 요약
    const genderSummary1   = document.getElementById("genderSummary1");   // 재해 성비 
    const genderSummary2   = document.getElementById("genderSummary2");   // 재해 사망 성비
    const ageSummary1     = document.getElementById("ageSummary1");      // 연령별 재해 현황
    const ageSummary2     = document.getElementById("ageSummary2");      // 연령별 재해 사망 현황
    const injurySummary1  = document.getElementById("injurySummary1");   // 재해유형 (발생현황 TOP 10)
    const injurySummary2  = document.getElementById("injurySummary2"); // 사망 발생형태

    // 산재 선택 여부 + 내가 선택한 발생형태
    let injurySelected = false;
    let selectedInjuryType = null;


    let injuryStatsByPeriod = null;
    if (visualArea && visualArea.dataset.summary6) {
        try {
            console.log("raw summary6:", visualArea.dataset.summary6);   // 디버깅용
            injuryStatsByPeriod = JSON.parse(visualArea.dataset.summary6);
        } catch (e) {
            console.error("summary6_JSON_파싱_실패:", e);
            injuryStatsByPeriod = null;
        }
    }

    // ★ 사망 발생형태
    let fatalStatsByPeriod = null;
    if (visualArea && visualArea.dataset.summary7) {
        try {
            console.log("raw summary7:", visualArea.dataset.summary7);
            fatalStatsByPeriod = JSON.parse(visualArea.dataset.summary7);
        } catch (e) {
            console.error("summary7_JSON_파싱_실패:", e);
            fatalStatsByPeriod = null;
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

                // 산재 선택 완료
                injurySelected = true;
                selectedInjuryType = injury || ""; 

                // 분석기간 초기화 + 통계 숨김 + 요약 초기화
                periodButtons.forEach((b) => b.classList.remove("active"));
                if (visualArea) {
                    visualArea.classList.add("hidden");
                }
                if (accidentSummary) accidentSummary.textContent = "";
                if (fatalSummary)    fatalSummary.textContent    = "";
                if (genderSummary1)   genderSummary1.textContent   = "";
                if (genderSummary2)   genderSummary2.textContent   = "";
                if (ageSummary1)      ageSummary1.innerHTML        = "";
                if (ageSummary2)      ageSummary2.innerHTML        = "";
                if (injurySummary1)  injurySummary1.innerHTML    = "";
                if (injurySummary2)  injurySummary2.innerHTML    = "";


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

            const accCount    = Number(btn.dataset.accCount    || 0); // 재해자수
            const accRate     = Number(btn.dataset.accRate     || 0); // 재해율
            const fatalCount  = Number(btn.dataset.fatalCount  || 0); // 사망자수
            const fatalRate   = Number(btn.dataset.fatalRate   || 0); // 사망만인율

            const male        = Number(btn.dataset.male        || 0); // 남자
            const female      = Number(btn.dataset.female      || 0); // 여자
            const maleRate    = Number(btn.dataset.maleRate    || 0); // 남자비율(%)
            const femaleRate  = Number(btn.dataset.femaleRate  || 0); // 여자비율(%)
 
            const male2        = Number(btn.dataset.male2        || 0); // 사망남자
            const female2     = Number(btn.dataset.female2      || 0); // 사망여자
            const maleRate2   = Number(btn.dataset.maleRate2    || 0); // 사망남자비율(%)
            const femaleRate2  = Number(btn.dataset.femaleRate2  || 0); // 사망여자비율(%)

            const ageU18  = Number(btn.dataset.ageU18  || 0); // 18세 미만
            const age20s  = Number(btn.dataset.age20s  || 0); // 20대
            const age30s  = Number(btn.dataset.age30s  || 0); // 30대
            const age40s  = Number(btn.dataset.age40s  || 0); // 40대
            const age50s  = Number(btn.dataset.age50s  || 0); // 50대
            const age60p  = Number(btn.dataset.age60p  || 0); // 60대 이상
            
            const ageU18a  = Number(btn.dataset.ageU18a  || 0); // 사망 18세 미만
            const age20sa  = Number(btn.dataset.age20sa  || 0); // 사망 20대
            const age30sa  = Number(btn.dataset.age30sa  || 0); // 사망 30대
            const age40sa  = Number(btn.dataset.age40sa  || 0); // 사망 40대
            const age50sa  = Number(btn.dataset.age50sa  || 0); // 사망 50대
            const age60pa  = Number(btn.dataset.age60pa  || 0); // 사망 60대 이상

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
            if (genderSummary1) {
                const maleRateText   = isNaN(maleRate)   ? "-" : maleRate.toFixed(1);
                const femaleRateText = isNaN(femaleRate) ? "-" : femaleRate.toFixed(1);

                genderSummary1.textContent =
                    `남자: ${male.toLocaleString()}명 (${maleRateText}%), ` +
                    `여자: ${female.toLocaleString()}명 (${femaleRateText}%)`;
            }            

            // 8) (성별 재해사망 비율)
            if (genderSummary2) {
                const maleRateText2   = isNaN(maleRate2)   ? "-" : maleRate2.toFixed(1);
                const femaleRateText2 = isNaN(femaleRate2) ? "-" : femaleRate2.toFixed(1);

                genderSummary2.textContent =
                    `남자: ${male2.toLocaleString()}명 (${maleRateText2}%), ` +
                    `여자: ${female2.toLocaleString()}명 (${femaleRateText2}%)`;
            }

            // 9) (연령별 재해 현황)
            if (ageSummary1) {
                ageSummary1.innerHTML =
                    `18세 미만: ${ageU18.toLocaleString()}명<br>` +
                    `20대: ${age20s.toLocaleString()}명<br>` +
                    `30대: ${age30s.toLocaleString()}명<br>` +
                    `40대: ${age40s.toLocaleString()}명<br>` +
                    `50대: ${age50s.toLocaleString()}명<br>` +
                    `60대 이상: ${age60p.toLocaleString()}명`;
            
            }     
            // 10) (연령별 사망 재해 현황)
            if (ageSummary2) {
                ageSummary2.innerHTML =
                    `18세 미만: ${ageU18a.toLocaleString()}명<br>` +
                    `20대: ${age20sa.toLocaleString()}명<br>` +
                    `30대: ${age30sa.toLocaleString()}명<br>` +
                    `40대: ${age40sa.toLocaleString()}명<br>` +
                    `50대: ${age50sa.toLocaleString()}명<br>` +
                    `60대 이상: ${age60pa.toLocaleString()}명`;
            
            }     
            // 11) ★ 발생형태 TOP10 + 나의 부상형태 순위
            
            if (injurySummary1 && injuryStatsByPeriod) {
                // data-year("1","2","3") → "최근 1년"/"2년"/"3년" 으로 매핑
                const yearFlag = btn.dataset.year;
                let periodKey = "최근 1년";
                if (yearFlag === "2") periodKey = "2년";
                else if (yearFlag === "3") periodKey = "3년";

                const periodData = injuryStatsByPeriod[periodKey];
                console.log("periodKey:", periodKey, "periodData:", periodData); // 디버깅

                if (!periodData) {
                    injurySummary1.textContent = "발생형태 데이터가 없습니다.";
                    return;
                }

                const topList = periodData.top10 || [];
                const rankMap = periodData.rank_map || {};

                let html = "";

                if (!topList.length) {
                    html += "발생형태 데이터가 없습니다.";
                } else {
                    topList.forEach(item => {
                        const cnt = typeof item.count === "number"
                            ? item.count.toLocaleString()
                            : item.count;
                        html += `${item.rank}위: ${item.name} (${cnt}명)<br>`;
                    });
                }

                if (selectedInjuryType) {
                    const myRank = rankMap[selectedInjuryType];
                    html += "<br>";
                    if (myRank) {
                        if (myRank <= 10) {
                            html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                                  + `<strong>${myRank}위</strong> 입니다.`;
                        } else {
                            html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                                  + `<strong>${myRank}위</strong>로, TOP 10에는 포함되지 않습니다.`;
                        }
                    } else {
                        html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                              + `해당 업종 통계에 집계되어 있지 않습니다.`;
                    }
                }

                injurySummary1.innerHTML = html;
            

                // 12) 사망 발생형태 TOP10 + 나의 순위
                if (injurySummary2 && fatalStatsByPeriod) {
                    const yearFlag = btn.dataset.year;
                    let periodKey = "최근 1년";
                    if (yearFlag === "2") periodKey = "2년";
                    else if (yearFlag === "3") periodKey = "3년";

                    const periodData = fatalStatsByPeriod[periodKey];

                    if (!periodData) {
                        injurySummary2.textContent = "사망 발생형태 데이터가 없습니다.";
                        return;
                    }

                    const topList = periodData.top10 || [];
                    const rankMap = periodData.rank_map || {};

                    let html = "";
                    if (!topList.length) {
                        html += "사망 발생형태 데이터가 없습니다.";
                    } else {
                        topList.forEach(item => {
                            const cnt = typeof item.count === "number"
                                ? item.count.toLocaleString()
                                : item.count;
                            html += `${item.rank}위: ${item.name} (${cnt}명)<br>`;
                        });
                    }

                    if (selectedInjuryType) {
                        const myRank = rankMap[selectedInjuryType];
                        html += "<br>";
                        if (myRank) {
                            if (myRank <= 10) {
                                html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                                    + `사망 재해 기준으로 <strong>${myRank}위</strong> 입니다.`;
                            } else {
                                html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                                    + `사망 재해 기준으로 <strong>${myRank}위</strong>이며, TOP 10에는 포함되지 않습니다.`;
                            }
                        } else {
                            html += `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 `
                                + `사망 재해 통계에 집계되어 있지 않습니다.`;
                        }
                    }

                    injurySummary2.innerHTML = html;
                }            
            
            }

        });
    });
});
        
        
        
        
 