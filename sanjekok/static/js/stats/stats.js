// static/js/stats/stats.js

document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn   = document.getElementById("myInjuryBtn");
    const dropdown      = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea    = document.getElementById("stats-visual-area");

    const injuryDetail    = document.getElementById("injuryDetail");
    const accidentSummary = document.getElementById("accidentSummary");  // 재해 요약
    const fatalSummary    = document.getElementById("fatalSummary");     // 사망 요약

    const genderSummary1  = document.getElementById("genderSummary1");   // 재해 성비 
    const genderSummary2  = document.getElementById("genderSummary2");   // 재해 사망 성비
    const ageSummary1     = document.getElementById("ageSummary1");      // 연령별 재해 현황
    const ageSummary2     = document.getElementById("ageSummary2");      // 연령별 재해 사망 현황
    const injurySummary1  = document.getElementById("injurySummary1");   // 재해유형 (발생형태 TOP 10)
    const injurySummary2  = document.getElementById("injurySummary2");   // 사망 발생형태
    const diseaseSummary1 = document.getElementById("diseaseSummary1");  // 질병 발생형태
    const diseaseSummary2 = document.getElementById("diseaseSummary2");  // 질병 사망형태 

    let injurySelected        = false;  // 나의 산재 선택 여부
    let selectedInjuryType    = null;   // 나의 발생형태 
    let selectedDiseaseType   = null;   // 나의 질병형태

    let injuryStatsByPeriod       = null;
    let fatalStatsByPeriod        = null;
    let diseaseStatsByPeriod      = null;
    let diseaseFatalStatsByPeriod = null;

    /* =========================
     *  0. 백엔드에서 넘긴 JSON 파싱
     * ========================= */

    // 발생형태
    if (visualArea && visualArea.dataset.summary6) {
        try {
            injuryStatsByPeriod = JSON.parse(visualArea.dataset.summary6);
        } catch (e) {
            console.error("summary6_JSON_파싱_실패:", e);
            injuryStatsByPeriod = null;
        }
    }

    // 사망 발생형태
    if (visualArea && visualArea.dataset.summary7) {
        try {
            fatalStatsByPeriod = JSON.parse(visualArea.dataset.summary7);
        } catch (e) {
            console.error("summary7_JSON_파싱_실패:", e);
            fatalStatsByPeriod = null;
        }
    }

    // 질병형태
    if (visualArea && visualArea.dataset.summary8) {
        try {
            diseaseStatsByPeriod = JSON.parse(visualArea.dataset.summary8);
        } catch (e) {
            console.error("summary8_JSON_파싱_실패:", e);
            diseaseStatsByPeriod = null;
        }
    }

    // 질병 사망형태
    if (visualArea && visualArea.dataset.summary9) {
        try {
            diseaseFatalStatsByPeriod = JSON.parse(visualArea.dataset.summary9);
        } catch (e) {
            console.error("summary9_JSON_파싱_실패:", e);
            diseaseFatalStatsByPeriod = null;
        }
    }

    /* =========================
     *  1. 나의 산재 드롭다운
     * ========================= */

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
                injurySelected      = true;
                selectedInjuryType  = injury  || "";
                selectedDiseaseType = disease || ""; 

                // 분석기간 초기화 + 통계 숨김 + 요약 초기화
                periodButtons.forEach(b => b.classList.remove("active"));
                if (visualArea) visualArea.classList.add("hidden");

                if (accidentSummary) accidentSummary.textContent = "";
                if (fatalSummary)    fatalSummary.textContent    = "";
                if (genderSummary1)  genderSummary1.textContent  = "";
                if (genderSummary2)  genderSummary2.textContent  = "";
                if (ageSummary1)     ageSummary1.innerHTML       = "";
                if (ageSummary2)     ageSummary2.innerHTML       = "";
                if (injurySummary1)  injurySummary1.innerHTML    = "";
                if (injurySummary2)  injurySummary2.innerHTML    = "";
                if (diseaseSummary1) diseaseSummary1.innerHTML   = "";
                if (diseaseSummary2) diseaseSummary2.innerHTML   = "";

                dropdown.classList.add("hidden");
            });
        });
    }

    /* =========================
     *  2. 분석 기간 버튼 클릭
     * ========================= */

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

            const yearFlag = btn.dataset.year;
            let periodKey  = "최근 1년";
            if (yearFlag === "2") periodKey = "2년";
            else if (yearFlag === "3") periodKey = "3년";

            /* ----------  기본 수치들 ---------- */

            const accCount    = Number(btn.dataset.accCount    || 0); // 재해자수
            const accRate     = Number(btn.dataset.accRate     || 0); // 재해율
            const fatalCount  = Number(btn.dataset.fatalCount  || 0); // 사망자수
            const fatalRate   = Number(btn.dataset.fatalRate   || 0); // 사망만인율

            const male        = Number(btn.dataset.male        || 0); // 남자
            const female      = Number(btn.dataset.female      || 0); // 여자
            const maleRate    = Number(btn.dataset.maleRate    || 0); // 남자비율(%)
            const femaleRate  = Number(btn.dataset.femaleRate  || 0); // 여자비율(%)

            const male2       = Number(btn.dataset.male2       || 0); // 사망남자
            const female2     = Number(btn.dataset.female2     || 0); // 사망여자
            const maleRate2   = Number(btn.dataset.maleRate2   || 0); // 사망남자비율(%)
            const femaleRate2 = Number(btn.dataset.femaleRate2 || 0); // 사망여자비율(%)

            const ageU18  = Number(btn.dataset.ageU18  || 0); // 18세 미만
            const age20s  = Number(btn.dataset.age20s  || 0); // 20대
            const age30s  = Number(btn.dataset.age30s  || 0); // 30대
            const age40s  = Number(btn.dataset.age40s  || 0); // 40대
            const age50s  = Number(btn.dataset.age50s  || 0); // 50대
            const age60p  = Number(btn.dataset.age60p  || 0); // 60대 이상
            
            const ageU18a = Number(btn.dataset.ageU18a || 0); // 사망 18세 미만
            const age20sa = Number(btn.dataset.age20sa || 0); // 사망 20대
            const age30sa = Number(btn.dataset.age30sa || 0); // 사망 30대
            const age40sa = Number(btn.dataset.age40sa || 0); // 사망 40대
            const age50sa = Number(btn.dataset.age50sa || 0); // 사망 50대
            const age60pa = Number(btn.dataset.age60pa || 0); // 사망 60대 이상

            /* =========================
             *  2-1. 상단 재해율 / 사망만인율 카드
             * ========================= */

            if (accidentSummary) {
                const rateText = isNaN(accRate) ? "-" : accRate.toFixed(2);
                accidentSummary.innerHTML =
                    `<strong style="font-size:24px;color:#14b6f6;">${rateText}</strong>` +
                    `<span style="font-size:13px;color:#64748b;margin-left:6px;">‰ / 재해자수 ${accCount.toLocaleString()}명</span>`;
            }

            if (fatalSummary) {
                const rateText = isNaN(fatalRate) ? "-" : fatalRate.toFixed(2);
                fatalSummary.innerHTML =
                    `<strong style="font-size:24px;color:#14b6f6;">${rateText}</strong>` +
                    `<span style="font-size:13px;color:#64748b;margin-left:6px;">명 / 사망자수 ${fatalCount.toLocaleString()}명</span>`;
            }

            /* =========================
             *  2-2. 성별 도넛 차트
             * ========================= */

            if (genderSummary1) {
                const maleRateText   = isNaN(maleRate)   ? "-" : maleRate.toFixed(1);
                const femaleRateText = isNaN(femaleRate) ? "-" : femaleRate.toFixed(1);

                genderSummary1.textContent =
                    `남자: ${male.toLocaleString()}명 (${maleRateText}%), ` +
                    `여자: ${female.toLocaleString()}명 (${femaleRateText}%)`;

                if (window.GenderChart1) {
                    window.GenderChart1(male, female);
                }
            }        

            if (genderSummary2) {
                const maleRateText2   = isNaN(maleRate2)   ? "-" : maleRate2.toFixed(1);
                const femaleRateText2 = isNaN(femaleRate2) ? "-" : femaleRate2.toFixed(1);

                genderSummary2.textContent =
                    `남자: ${male2.toLocaleString()}명 (${maleRateText2}%), ` +
                    `여자: ${female2.toLocaleString()}명 (${femaleRateText2}%)`;

                if (window.GenderChart2) {
                    window.GenderChart2(male2, female2);
                }
            }

            /* =========================
             *  2-3. 연령대별 현황 + 차트
             * ========================= */

            if (window.AgeChart1) {
                window.AgeChart1(ageU18, age20s, age30s, age40s, age50s, age60p);
            }



            if (window.AgeChart2) {
                window.AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa);
            }

            // 11) 발생형태 TOP10 + 나의 부상형태 순위 + 바차트
            if (injurySummary1 && injuryStatsByPeriod) {
                const periodData = injuryStatsByPeriod[periodKey];

                if (!periodData) {
                    injurySummary1.textContent = "발생형태 데이터가 없습니다.";
                    if (window.InjuryChart1) window.InjuryChart1([]);
                    return;
                }

                const topList = periodData.top10 || [];
                const rankMap = periodData.rank_map || {};

                let html = "";
                if (!topList.length) {
                    html = "발생형태 데이터가 없습니다.";
                } else if (selectedInjuryType) {
                    const myRank = rankMap[selectedInjuryType];
                    if (myRank) {
                        if (myRank <= 10) {
                            html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                                `<strong>${myRank}위</strong> 입니다.`;
                        } else {
                            html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                                `<strong>${myRank}위</strong>로, TOP 10에는 포함되지 않습니다.`;
                        }
                    } else {
                        html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                            `해당 업종 통계에 집계되어 있지 않습니다.`;
                    }
                } else {
                    html = "나의 산재를 선택하면 발생형태 순위를 확인할 수 있습니다.";
                }

                injurySummary1.innerHTML = html;

                // 바 차트 (TOP10 막대만)
                if (window.InjuryChart1) {
                    window.InjuryChart1(topList,selectedInjuryType);
                }
            }

            // 12) 사망 발생형태 + 나의 순위 + 바차트
            if (injurySummary2 && fatalStatsByPeriod) {
                const periodData = fatalStatsByPeriod[periodKey];

                if (!periodData) {
                    injurySummary2.textContent = "사망 발생형태 데이터가 없습니다.";
                    if (window.InjuryChart2) window.InjuryChart2([]);
                    return;
                }

                const topList = periodData.top10 || [];
                const rankMap = periodData.rank_map || {};

                let html = "";
                if (!topList.length) {
                    html = "사망 발생형태 데이터가 없습니다.";
                } else if (selectedInjuryType) {
                    const myRank = rankMap[selectedInjuryType];
                    if (myRank) {
                        if (myRank <= 10) {
                            html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                                `사망 재해 기준으로 <strong>${myRank}위</strong> 입니다.`;
                        } else {
                            html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                                `사망 재해 기준으로 <strong>${myRank}위</strong>이며, ` +
                                `TOP 10에는 포함되지 않습니다.`;
                        }
                    } else {
                        html = `나의 부상형태(<strong>${selectedInjuryType}</strong>)는 ` +
                            `사망 재해 통계에 집계되어 있지 않습니다.`;
                    }
                } else {
                    html = "나의 산재를 선택하면 사망 발생형태 순위를 확인할 수 있습니다.";
                }

                injurySummary2.innerHTML = html;

                if (window.InjuryChart2) {
                    window.InjuryChart2(topList,selectedInjuryType);
                }
            }

            // 13) 질병형태별 + 나의 질병 순위 + 바차트
            if (diseaseSummary1 && diseaseStatsByPeriod) {
                const periodData = diseaseStatsByPeriod[periodKey];

                if (!periodData) {
                    diseaseSummary1.textContent = "질병형태 데이터가 없습니다.";
                    if (window.DiseaseChart1) window.DiseaseChart1([]);
                    return;
                }

                const topList = periodData.top10 || [];
                const rankMap = periodData.rank_map || {};

                let html = "";
                if (!topList.length) {
                    html = "질병형태 데이터가 없습니다.";
                } else if (selectedDiseaseType) {
                    const myRank = rankMap[selectedDiseaseType];
                    if (myRank) {
                        if (myRank <= 10) {
                            html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                                `<strong>${myRank}위</strong> 입니다.`;
                        } else {
                            html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                                `<strong>${myRank}위</strong>로, TOP 10에는 포함되지 않습니다.`;
                        }
                    } else {
                        html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                            `해당 업종 질병 통계에 집계되어 있지 않습니다.`;
                    }
                } else {
                    html = "나의 산재를 선택하면 질병형태 순위를 확인할 수 있습니다.";
                }

                diseaseSummary1.innerHTML = html;

                if (window.DiseaseChart1) {
                    window.DiseaseChart1(topList,selectedDiseaseType);
                }
            }

            // 14) 질병 사망형태 + 나의 순위 + 바차트
            if (diseaseSummary2 && diseaseFatalStatsByPeriod) {
                const periodData = diseaseFatalStatsByPeriod[periodKey];

                if (!periodData) {
                    diseaseSummary2.textContent = "질병 사망유형 데이터가 없습니다.";
                    if (window.DiseaseChart2) window.DiseaseChart2([]);
                    return;
                }

                const topList = periodData.top10 || [];
                const rankMap = periodData.rank_map || {};

                let html = "";
                if (!topList.length) {
                    html = "질병 사망유형 데이터가 없습니다.";
                } else if (selectedDiseaseType) {
                    const myRank = rankMap[selectedDiseaseType];
                    if (myRank) {
                        if (myRank <= 10) {
                            html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                                `사망 재해 기준으로 <strong>${myRank}위</strong> 입니다.`;
                        } else {
                            html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                                `사망 재해 기준으로 <strong>${myRank}위</strong>이며, ` +
                                `TOP 10에는 포함되지 않습니다.`;
                        }
                    } else {
                        html = `나의 질병(<strong>${selectedDiseaseType}</strong>)은 ` +
                            `질병 사망 통계에 집계되어 있지 않습니다.`;
                    }
                } else {
                    html = "나의 산재를 선택하면 질병 사망형태 순위를 확인할 수 있습니다.";
                }

                diseaseSummary2.innerHTML = html;

                if (window.DiseaseChart2) {
                    window.DiseaseChart2(topList,selectedDiseaseType);
                }
            }
        });
    });
});
