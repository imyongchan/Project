// static/js/stats/stats.js
document.addEventListener("DOMContentLoaded", () => {
    const myInjuryBtn = document.getElementById("myInjuryBtn");
    const dropdown = document.getElementById("injuryDropdown");
    const periodButtons = document.querySelectorAll(".period-btn");
    const visualArea = document.getElementById("stats-visual-area");
    const accidentSummary = document.getElementById("accidentSummary");
    const fatalSummary = document.getElementById("fatalSummary");
    const genderSummary1 = document.getElementById("genderSummary1");
    const genderSummary2 = document.getElementById("genderSummary2");
    const ageSummary1 = document.getElementById("ageSummary1");
    const ageSummary2 = document.getElementById("ageSummary2");
    const injurySummary1 = document.getElementById("injurySummary1");
    const injurySummary2 = document.getElementById("injurySummary2");
    const diseaseSummary1 = document.getElementById("diseaseSummary1");
    const diseaseSummary2 = document.getElementById("diseaseSummary2");

    // 카드 요소들
    const cardInjury = document.getElementById("card-injury");
    const cardInjuryFatal = document.getElementById("card-injury-fatal");
    const cardDisease = document.getElementById("card-disease");
    const cardDiseaseFatal = document.getElementById("card-disease-fatal");

    
    let injurySelected = false;
    let selectedInjuryType = null;
    let selectedDiseaseType = null;
    let injuryStatsByPeriod = null;
    let fatalStatsByPeriod = null;
    let diseaseStatsByPeriod = null;
    let diseaseFatalStatsByPeriod = null;
    const memberageband = visualArea ? (visualArea.dataset.ageBand || null) : null;

    if (visualArea) {
    const hasSelection = visualArea.dataset.hasSelection === "1";

    if (hasSelection) {
        injurySelected = true;
        if (visualArea.dataset.selectedInjury) {
            selectedInjuryType = visualArea.dataset.selectedInjury;
        }
        if (visualArea.dataset.selectedDisease) {
            selectedDiseaseType = visualArea.dataset.selectedDisease;
        }
    }
}

    /* ========================= 
     * 0. 백엔드에서 넘긴 JSON 파싱
     * ========================= */
    if (visualArea && visualArea.dataset.summary6) {
        try {
            injuryStatsByPeriod = JSON.parse(visualArea.dataset.summary6);
        } catch (e) {
            console.error("summary6_JSON_파싱_실패:", e);
            injuryStatsByPeriod = null;
        }
    }

    if (visualArea && visualArea.dataset.summary7) {
        try {
            fatalStatsByPeriod = JSON.parse(visualArea.dataset.summary7);
        } catch (e) {
            console.error("summary7_JSON_파싱_실패:", e);
            fatalStatsByPeriod = null;
        }
    }

    if (visualArea && visualArea.dataset.summary8) {
        try {
            diseaseStatsByPeriod = JSON.parse(visualArea.dataset.summary8);
        } catch (e) {
            console.error("summary8_JSON_파싱_실패:", e);
            diseaseStatsByPeriod = null;
        }
    }

    if (visualArea && visualArea.dataset.summary9) {
        try {
            diseaseFatalStatsByPeriod = JSON.parse(visualArea.dataset.summary9);
        } catch (e) {
            console.error("summary9_JSON_파싱_실패:", e);
            diseaseFatalStatsByPeriod = null;
        }
    }

    let riskDataByPeriod = {};

    if (visualArea && visualArea.dataset.riskAnalysis) {
        try {
            riskDataByPeriod = JSON.parse(visualArea.dataset.riskAnalysis);
        } catch (e) {
            console.error("riskAnalysis JSON 파싱 실패:", e);
        }
    }

    /* ========================= 
     * 1. 나의 산재 드롭다운
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
                const accidentId = item.dataset.accidentId;   // ★ data-accident-id

                if (!accidentId) {
                    return;
                }

                // 현재 URL 기준으로 accident_id 파라미터 세팅 후 이동
                const url = new URL(window.location.href);
                url.searchParams.set("accident_id", accidentId);
                window.location.href = url.toString();
            });
        });
    }
    /* ========================= 
     * 2. 분석 기간 버튼 클릭
     * ========================= */
    periodButtons.forEach(btn => {
        btn.addEventListener("click", () => {

        const hasInjury = visualArea ? visualArea.dataset.hasInjury === "1" : false;

            // 1) 산재 정보 자체가 없는 경우
            if (!hasInjury) {
                alert("산재 정보가 없습니다. 마이페이지에서 산재 정보를 등록해주세요.");
                window.location.href = "/member/mypage/individual-list/";
                return;
            }

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
            let periodKey = "최근 1년";
            if (yearFlag === "2") periodKey = "2년";
            else if (yearFlag === "3") periodKey = "3년";

            /* ---------- 기본 수치들 ---------- */
            const accCount = Number(btn.dataset.accCount || 0);
            const accRate = Number(btn.dataset.accRate || 0);
            const fatalCount = Number(btn.dataset.fatalCount || 0);
            const fatalRate = Number(btn.dataset.fatalRate || 0);
            const male = Number(btn.dataset.male || 0);
            const female = Number(btn.dataset.female || 0);
            const maleRate = Number(btn.dataset.maleRate || 0);
            const femaleRate = Number(btn.dataset.femaleRate || 0);
            const male2 = Number(btn.dataset.male2 || 0);
            const female2 = Number(btn.dataset.female2 || 0);
            const maleRate2 = Number(btn.dataset.maleRate2 || 0);
            const femaleRate2 = Number(btn.dataset.femaleRate2 || 0);
            const ageU18 = Number(btn.dataset.ageU18 || 0); //연령별 수치
            const age20s = Number(btn.dataset.age20s || 0);
            const age30s = Number(btn.dataset.age30s || 0);
            const age40s = Number(btn.dataset.age40s || 0);
            const age50s = Number(btn.dataset.age50s || 0);
            const age60p = Number(btn.dataset.age60p || 0);
            const ageU18a = Number(btn.dataset.ageU18a || 0);//연령별 사망수치
            const age20sa = Number(btn.dataset.age20sa || 0);
            const age30sa = Number(btn.dataset.age30sa || 0);
            const age40sa = Number(btn.dataset.age40sa || 0);
            const age50sa = Number(btn.dataset.age50sa || 0);
            const age60pa = Number(btn.dataset.age60pa || 0);

            /* ========================= 
             * 2-1. 상단 재해율 / 사망만인율 카드
             * ========================= */
            if (accidentSummary) {
                const rateText = isNaN(accRate) ? "-" : accRate.toFixed(2);
                accidentSummary.innerHTML = `<strong style="font-size:27px;color:#f99b18;">${rateText}‰ </strong>` +
                    `<span style="font-size:20px;color:#23333d;margin-left:6px;">
                     재해자수 ${accCount.toLocaleString()}명</span>`;
            }

            if (fatalSummary) {
                const rateText = isNaN(fatalRate) ? "-" : fatalRate.toFixed(2);
                fatalSummary.innerHTML = `<strong style="font-size:27px;color:#f99b18;">${rateText}%</strong>` +
                    `<span style="font-size:20px;color:#23333d;margin-left:6px;">
                     사망자수 ${fatalCount.toLocaleString()}명</span>`;
            }

            /* ========================= 
             * 2-2. 성별 도넛 차트
             * ========================= */
            if (genderSummary1) {
                const maleRateText = isNaN(maleRate) ? "-" : maleRate.toFixed(1);
                const femaleRateText = isNaN(femaleRate) ? "-" : femaleRate.toFixed(1);
                genderSummary1.innerHTML = `<p style="font-size:23px;color:#f99b18;"> 남자: ${maleRateText}%</p> ` +
                    `<p style="font-size:23px;color:#f99b18;"> 여자:  ${femaleRateText}% </p>`;
                if (window.GenderChart1) {
                    window.GenderChart1(male, female);
                }
            }

            if (genderSummary2) {
                const maleRateText2 = isNaN(maleRate2) ? "-" : maleRate2.toFixed(1);
                const femaleRateText2 = isNaN(femaleRate2) ? "-" : femaleRate2.toFixed(1);
                genderSummary2.innerHTML = `<p style="font-size:23px;color:#f99b18;"> 남자: ${maleRateText2}%</p> ` +
                    `<p style="font-size:23px;color:#f99b18;"> 여자:  ${femaleRateText2}% </p>`;
                if (window.GenderChart2) {
                    window.GenderChart2(male2, female2);
                }
            }

            /* ========================= 
             * 2-3. 연령대별 현황 + 차트
             * ========================= */
            if 
                (window.AgeChart1) {
                window.AgeChart1(ageU18, age20s, age30s, age40s, age50s, age60p,memberageband);
            }
            if (window.AgeChart2) {
                window.AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa,memberageband);
            }

            /* ========================= 
             * 발생형태 관련 통계 (selectedInjuryType이 있을 때만)
             * ========================= */
            // 11) 발생형태 TOP10
            if (selectedInjuryType) {
                if (cardInjury) cardInjury.style.display = "block";
                if (injurySummary1 && injuryStatsByPeriod) {
                    const periodData = injuryStatsByPeriod[periodKey];
                    if (!periodData) {
                        injurySummary1.textContent = "발생형태 데이터가 없습니다.";
                        if (window.InjuryChart1) window.InjuryChart1([]);
                    } else {
                        const topList = periodData.top10 || [];
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        if (!topList.length) {
                            html = "발생형태 데이터가 없습니다.";
                        } else {
                            const myRank = rankMap[selectedInjuryType];
                            if (myRank) {
                                if (myRank <= 10) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html =`<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>` 
                                }
                            } else {
                                html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    해당 업종 통계에 집계되어 있지 않습니다.
                                                </div>
                                            </div>` 

                            }
                        }
                        
                        injurySummary1.innerHTML = html;
                        if (window.InjuryChart1) {
                            window.InjuryChart1(topList, selectedInjuryType);
                        }
                    }
                }

                // 12) 사망 발생형태
                if (cardInjuryFatal) cardInjuryFatal.style.display = "block";
                if (injurySummary2 && fatalStatsByPeriod) {
                    const periodData = fatalStatsByPeriod[periodKey];
                    if (!periodData) {
                        injurySummary2.textContent = "사망 발생형태 데이터가 없습니다.";
                        if (window.InjuryChart2) window.InjuryChart2([]);
                    } else {
                        const topList = periodData.top10 || [];
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        if (!topList.length) {
                            html = "사망 발생형태 데이터가 없습니다.";
                        } else {
                            const myRank = rankMap[selectedInjuryType];
                            if (myRank) {
                                if (myRank <= 10) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html =`<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>` 
                                }
                            } else {
                                html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    해당 업종 통계에 집계되어 있지 않습니다.
                                                </div>
                                            </div>` 

                            }
                        }
                        
                        injurySummary2.innerHTML = html;
                        if (window.InjuryChart2) {
                            window.InjuryChart2(topList, selectedInjuryType);
                        }
                    }
                }
            } else {
                // selectedInjuryType이 없으면 발생형태 카드 숨김
                if (cardInjury) cardInjury.style.display = "none";
                if (cardInjuryFatal) cardInjuryFatal.style.display = "none";
            }

            /* ========================= 
             * 질병형태 관련 통계 (selectedDiseaseType이 있을 때만)
             * ========================= */
            // 13) 질병형태별
            if (selectedDiseaseType) {
                if (cardDisease) cardDisease.style.display = "block";
                if (diseaseSummary1 && diseaseStatsByPeriod) {
                    const periodData = diseaseStatsByPeriod[periodKey];
                    if (!periodData) {
                        diseaseSummary1.textContent = "질병형태 데이터가 없습니다.";
                        if (window.DiseaseChart1) window.DiseaseChart1([]);
                    } else {
                        const topList = periodData.top10 || [];
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        if (!topList.length) {
                            html = "질병형태 데이터가 없습니다.";
                        } else {
                            const myRank = rankMap[selectedDiseaseType];
                            if (myRank) {
                                if (myRank <= 10) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html =`<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>` 
                                }
                            } else {
                                html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)는 
                                                    해당 업종 통계에 집계되어 있지 않습니다.
                                                </div>
                                            </div>` 

                            }
                        }
                        
                        diseaseSummary1.innerHTML = html;
                        if (window.DiseaseChart1) {
                            window.DiseaseChart1(topList, selectedDiseaseType);
                        }
                    }
                }

                // 14) 질병 사망형태
                if (cardDiseaseFatal) cardDiseaseFatal.style.display = "block";
                if (diseaseSummary2 && diseaseFatalStatsByPeriod) {
                    const periodData = diseaseFatalStatsByPeriod[periodKey];
                    if (!periodData) {
                        diseaseSummary2.textContent = "질병 사망유형 데이터가 없습니다.";
                        if (window.DiseaseChart2) window.DiseaseChart2([]);
                    } else {
                        const topList = periodData.top10 || [];
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        if (!topList.length) {
                            html = "질병 사망유형 데이터가 없습니다.";
                        } else {
                            const myRank = rankMap[selectedDiseaseType];
                            if (myRank) {
                                if (myRank <= 10) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html =`<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>` 
                                }
                            } else {
                                html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)는 
                                                    해당 업종 통계에 집계되어 있지 않습니다.
                                                </div>
                                            </div>` 

                            }
                        }
                        
                        diseaseSummary2.innerHTML = html;
                        if (window.DiseaseChart2) {
                            window.DiseaseChart2(topList, selectedDiseaseType);
                        }
                    }
                }
            } else {
                // selectedDiseaseType이 없으면 질병 카드 숨김
                if (cardDisease) cardDisease.style.display = "none";
                if (cardDiseaseFatal) cardDiseaseFatal.style.display = "none";
            }

                const riskData = riskDataByPeriod[yearFlag];

                const riskGrid = document.getElementById("riskGrid");
                const riskNoData = document.getElementById("riskNoData");

                if (riskData && riskData.has_data) {
                // 텍스트
                const textEl = document.getElementById("riskConditionText");
                if (textEl) {
                    textEl.innerHTML = `
                    <strong>${riskData.industry}</strong>, 
                    <strong>${riskData.age_group}</strong>, 
                    <strong>${riskData.gender}</strong> 조건에서<br>
                    최근 ${yearFlag}년간 가장 많이 발생한 위험 요인입니다.
                    `;
                }

                // 영역 토글
                if (riskGrid) riskGrid.style.display = "grid";
                if (riskNoData) riskNoData.style.display = "none";

                // 리스트 렌더
                const renderRiskList = (containerId, list) => {
                    const container = document.getElementById(containerId);
                    if (!container) return;
                    container.innerHTML = (list || []).map(item => `
                    <div class="risk-item">
                        <span class="risk-rank rank-${item.rank}">${item.rank}</span>
                        <span class="risk-name">${item.name}</span>
                        <span class="risk-percentage">${item.percentage}%</span>
                    </div>
                    `).join("");
                };

                renderRiskList("injuryRiskList", riskData.injury_top5);
                renderRiskList("diseaseRiskList", riskData.disease_top5);

                // ✅ 캔버스가 있을 때만 차트 호출 (안전장치)
                if (document.getElementById("riskAccidentPie")) {
                    window.RiskAccidentPieChart?.(riskData.injury_top5);
                }
                if (document.getElementById("riskDiseasePie")) {
                    window.RiskDiseasePieChart?.(riskData.disease_top5);
                }

                } else {
                // 데이터 없을 때
                const textEl = document.getElementById("riskConditionText");
                if (textEl) textEl.innerHTML = "충분한 통계 데이터가 없습니다.";

                if (riskGrid) riskGrid.style.display = "none";
                if (riskNoData) riskNoData.style.display = "block";

                const a = document.getElementById("injuryRiskList");
                const b = document.getElementById("diseaseRiskList");
                if (a) a.innerHTML = "";
                if (b) b.innerHTML = "";
                }

                });

            if (visualArea && visualArea.dataset.hasSelection === "1") {
            const defaultBtn = document.querySelector('.period-btn[data-year="1"]');
            defaultBtn?.click();
            }
});
});