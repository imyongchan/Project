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
    const injurySummary1 = document.getElementById("injurySummary1");
    const injurySummary2 = document.getElementById("injurySummary2");
    const diseaseSummary1 = document.getElementById("diseaseSummary1");
    const diseaseSummary2 = document.getElementById("diseaseSummary2");

    // 카드 요소들
    const cardInjury = document.getElementById("card-injury");
    const cardInjuryFatal = document.getElementById("card-injury-fatal");
    const cardDisease = document.getElementById("card-disease");
    const cardDiseaseFatal = document.getElementById("card-disease-fatal");

    const toggleRiskDetailsBtn = document.getElementById("toggleRiskDetailsBtn");
    const riskDetailsPanel = document.getElementById("riskDetailsPanel");

    if (toggleRiskDetailsBtn && riskDetailsPanel) {
        toggleRiskDetailsBtn.addEventListener("click", () => {
            const isOpen = riskDetailsPanel.style.display === "block";

            riskDetailsPanel.style.display = isOpen ? "none" : "block";
            toggleRiskDetailsBtn.textContent = isOpen
                ? "상세 보기 ▼"
                : "상세 닫기 ▲";
        });
    }

    

     
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

    function updateKPIByRiskData(riskData, visualArea,accRate, fatalRate) {
        if (!visualArea) return;

        const selectedInjury = visualArea.dataset.selectedInjury || null;
        const selectedDisease = visualArea.dataset.selectedDisease || null;

        /* =====================
        * KPI 재해율 (상단 카드와 동일 데이터)
        * ===================== */
        const accidentRateEl = document.getElementById("kpi-accident-rate");
        if (accidentRateEl) {
            accidentRateEl.textContent =
                isNaN(accRate) ? "-" : `${accRate.toFixed(2)}%`;
            accidentRateEl.parentElement.style.display = "block";
        }

        /* =====================
        * KPI 사망만인율 (상단 카드와 동일 데이터)
        * ===================== */
        const fatalRateEl = document.getElementById("kpi-fatal-rate");
        if (fatalRateEl) {
            if ((selectedInjury && !selectedDisease) || (!selectedInjury && selectedDisease)) {
                fatalRateEl.textContent =
                    isNaN(fatalRate) ? "-" : `${fatalRate.toFixed(2)}‱`;
                fatalRateEl.parentElement.style.display = "block";
            } else {
                fatalRateEl.parentElement.style.display = "none";
            }
        }


        // ✅ 발생형태 TOP
        const injuryTopEl = document.getElementById("kpi-injury-top");
        if (injuryTopEl) {
            injuryTopEl.textContent = selectedInjury
                ? (riskData.injury_top5?.[0]?.name || "-")
                : "-";
            injuryTopEl.parentElement.style.display = selectedInjury ? "block" : "none";
        }

        // ✅ 질병 TOP
        const diseaseTopEl = document.getElementById("kpi-disease-top");
        if (diseaseTopEl) {
            diseaseTopEl.textContent = selectedDisease
                ? (riskData.disease_top5?.[0]?.name || "-")
                : "-";
            diseaseTopEl.parentElement.style.display = selectedDisease ? "block" : "none";
        }

        // ✅ 종합 위험도
        const scoreEl = document.getElementById("kpi-risk-score");
        if (scoreEl) {
            scoreEl.textContent = `${riskData.total_score ?? 0}점`;
            const card = scoreEl.closest(".kpi-card");
            if (card) {
                let sub = card.querySelector(".kpi-sub");
                if (!sub) {
                    sub = document.createElement("span");
                    sub.className = "kpi-sub";
                    card.appendChild(sub);
                }
                sub.textContent = riskData.risk_level ?? "-";
            }
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
                const accidentId = item.dataset.accidentId;

                if (!accidentId) {
                    return;
                }

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

            // 2) 산재를 아직 선택 안 했으면 막기
            if (!injurySelected) {
                alert("먼저 '나의 산재'를 선택해주세요.");
                return;
            }

            // 3) 통계 영역 보이기
            if (visualArea) {
                visualArea.classList.remove("hidden");
            }

            // 4) 버튼 active 표시
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
            const ageU18 = Number(btn.dataset.ageU18 || 0);
            const age20s = Number(btn.dataset.age20s || 0);
            const age30s = Number(btn.dataset.age30s || 0);
            const age40s = Number(btn.dataset.age40s || 0);
            const age50s = Number(btn.dataset.age50s || 0);
            const age60p = Number(btn.dataset.age60p || 0);
            const ageU18a = Number(btn.dataset.ageU18a || 0);
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
                accidentSummary.innerHTML = `<strong style="font-size:27px;color:#f99b18;">${rateText}%</strong>` +
                    `<span style="font-size:20px;color:#23333d;margin-left:6px;">
                     재해자수 ${accCount.toLocaleString()}명</span>`;
            }

            if (fatalSummary) {
                const rateText = isNaN(fatalRate) ? "-" : fatalRate.toFixed(2);
                fatalSummary.innerHTML = `<strong style="font-size:27px;color:#f99b18;">${rateText}‱ </strong>` +
                    `<span style="font-size:20px;color:#23333d;margin-left:6px;">
                     사망자수 ${fatalCount.toLocaleString()}명</span>`;
            }

            /* ========================= 
             * 2-2. 성별 도넛 차트
             * ========================= */
            if (genderSummary1) {
                const maleRateText = isNaN(maleRate) ? "-" : maleRate.toFixed(1);
                const femaleRateText = isNaN(femaleRate) ? "-" : femaleRate.toFixed(1);
                genderSummary1.innerHTML = `<p style="font-size:20px;color:#23333d;"> 남자: ${maleRateText}%</p> ` +
                    `<p style="font-size:20px;color:#23333d;"> 여자:  ${femaleRateText}% </p>`;
                if (window.GenderChart1) {
                    window.GenderChart1(male, female);
                }
            }

            if (genderSummary2) {
                const maleRateText2 = isNaN(maleRate2) ? "-" : maleRate2.toFixed(1);
                const femaleRateText2 = isNaN(femaleRate2) ? "-" : femaleRate2.toFixed(1);
                genderSummary2.innerHTML = `<p style="font-size:20px;color:#23333d;"> 남자: ${maleRateText2}%</p> ` +
                    `<p style="font-size:20px;color:#23333d;"> 여자:  ${femaleRateText2}% </p>`;
                if (window.GenderChart2) {
                    window.GenderChart2(male2, female2);
                }
            }

            /* ========================= 
             * 2-3. 연령대별 현황 + 차트
             * ========================= */
            if (window.AgeChart1) {
                window.AgeChart1(ageU18, age20s, age30s, age40s, age50s, age60p, memberageband);
            }
            if (window.AgeChart2) {
                window.AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa, memberageband);
            }

            /* ========================= 
             * 발생형태 관련 통계
             * ========================= */
            if (selectedInjuryType) {
                // 11) 발생형태 TOP7
                if (cardInjury) cardInjury.style.display = "block";
                
                if (injurySummary1 && injuryStatsByPeriod) {
                    const periodData = injuryStatsByPeriod[periodKey];
                    if (!periodData || !periodData.top7 || periodData.top7.length === 0) {
                        // ✅ 데이터가 없으면 카드에 no-data 클래스 추가
                        if (cardInjury) cardInjury.classList.add("no-data");
                        injurySummary1.innerHTML = '<div class="no-data-message">발생형태 데이터가 없습니다.</div>';
                        // 차트 숨김
                        const chart1 = document.getElementById("injuryChart1");
                        if (chart1) chart1.style.display = "none";
                    } else {
                        // ✅ 데이터가 있으면 no-data 클래스 제거
                        if (cardInjury) cardInjury.classList.remove("no-data");
                        const chart1 = document.getElementById("injuryChart1");
                        if (chart1) chart1.style.display = "block";
                        const topList = periodData.top7;
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        {
                            const myRank = rankMap[selectedInjuryType];
                            const inChart = topList.some(item => item.name === selectedInjuryType);
                            if (myRank) {
                                if (inChart) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>`;
                                }
                            } else {
                                html = `<div class="result-box">
                                            <i class="fa-solid fa-triangle-exclamation"></i>
                                            <div>
                                                나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                해당 업종 통계에 집계되어 있지 않습니다.
                                            </div>
                                        </div>`;
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
                    if (!periodData || !periodData.top7 || periodData.top7.length === 0) {
                        // ✅ 데이터가 없으면 카드에 no-data 클래스 추가
                        if (cardInjuryFatal) cardInjuryFatal.classList.add("no-data");
                        injurySummary2.innerHTML = '<div class="no-data-message">사망 발생형태 데이터가 없습니다.</div>';
                        // 차트 숨김
                        const chart2 = document.getElementById("injuryChart2");
                        if (chart2) chart2.style.display = "none";
                    } else {
                        // ✅ 데이터가 있으면 no-data 클래스 제거
                        if (cardInjuryFatal) cardInjuryFatal.classList.remove("no-data");
                        const chart2 = document.getElementById("injuryChart2");
                        if (chart2) chart2.style.display = "block";
                        const topList = periodData.top7;
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        {
                            const myRank = rankMap[selectedInjuryType];
                            const inChart = topList.some(item => item.name === selectedInjuryType);

                            if (myRank) {
                                if (inChart ) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>`;
                                }
                            } else {
                                html = `<div class="result-box">
                                            <i class="fa-solid fa-triangle-exclamation"></i>
                                            <div>
                                                나의 부상형태(<strong>${selectedInjuryType}</strong>)는 
                                                해당 업종 통계에 집계되어 있지 않습니다.
                                            </div>
                                        </div>`;
                            }
                        }
                        
                        injurySummary2.innerHTML = html;
                        if (window.InjuryChart2) {
                            window.InjuryChart2(topList, selectedInjuryType);
                        }
                    }
                }
            } else {
                if (cardInjury) cardInjury.style.display = "none";
                if (cardInjuryFatal) cardInjuryFatal.style.display = "none";
            }

            /* ========================= 
             * 질병형태 관련 통계
             * ========================= */
            if (selectedDiseaseType) {
                // 13) 질병형태별
                if (cardDisease) cardDisease.style.display = "block";
                
                if (diseaseSummary1 && diseaseStatsByPeriod) {
                    const periodData = diseaseStatsByPeriod[periodKey];
                    if (!periodData || !periodData.top7 || periodData.top7.length === 0) {
                        // ✅ 데이터가 없으면 카드에 no-data 클래스 추가
                        if (cardDisease) cardDisease.classList.add("no-data");
                        diseaseSummary1.innerHTML = '<div class="no-data-message">질병형태 데이터가 없습니다.</div>';
                        // 차트 숨김
                        const chart1 = document.getElementById("diseaseChart1");
                        if (chart1) chart1.style.display = "none";
                    } else {
                        // ✅ 데이터가 있으면 no-data 클래스 제거
                        if (cardDisease) cardDisease.classList.remove("no-data");
                        const chart1 = document.getElementById("diseaseChart1");
                        if (chart1) chart1.style.display = "block";
                        const topList = periodData.top7;
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        {
                            const myRank = rankMap[selectedDiseaseType];
                            const inChart = topList.some(item => item.name === selectedDiseaseType);
                            if (myRank) {
                                if (inChart) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>`;
                                }
                            } else {
                                html = `<div class="result-box">
                                            <i class="fa-solid fa-triangle-exclamation"></i>
                                            <div>
                                                나의 질병(<strong>${selectedDiseaseType}</strong>)는 
                                                해당 업종 통계에 집계되어 있지 않습니다.
                                            </div>
                                        </div>`;
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
                    if (!periodData || !periodData.top7 || periodData.top7.length === 0) {
                        // ✅ 데이터가 없으면 카드에 no-data 클래스 추가
                        if (cardDiseaseFatal) cardDiseaseFatal.classList.add("no-data");
                        diseaseSummary2.innerHTML = '<div class="no-data-message">질병 사망유형 데이터가 없습니다.</div>';
                        // 차트 숨김
                        const chart2 = document.getElementById("diseaseChart2");
                        if (chart2) chart2.style.display = "none";
                    } else {
                        // ✅ 데이터가 있으면 no-data 클래스 제거
                        if (cardDiseaseFatal) cardDiseaseFatal.classList.remove("no-data");
                        const chart2 = document.getElementById("diseaseChart2");
                        if (chart2) chart2.style.display = "block";
                        const topList = periodData.top7;
                        const rankMap = periodData.rank_map || {};
                        let html = "";
                        
                        {
                            const myRank = rankMap[selectedDiseaseType];
                            const inChart = topList.some(item => item.name === selectedDiseaseType);
                            if (myRank) {
                                if (inChart) {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    <strong>${myRank}위</strong> 입니다.
                                                </div>
                                            </div>`;
                                } else {
                                    html = `<div class="result-box">
                                                <i class="fa-solid fa-triangle-exclamation"></i>
                                                <div>
                                                    나의 질병(<strong>${selectedDiseaseType}</strong>)은 
                                                    순위에는 포함되지 않습니다.
                                                </div>
                                            </div>`;
                                }
                            } else {
                                html = `<div class="result-box">
                                            <i class="fa-solid fa-triangle-exclamation"></i>
                                            <div>
                                                나의 질병(<strong>${selectedDiseaseType}</strong>)는 
                                                해당 업종 통계에 집계되어 있지 않습니다.
                                            </div>
                                        </div>`;
                            }
                        }
                        
                        diseaseSummary2.innerHTML = html;
                        if (window.DiseaseChart2) {
                            window.DiseaseChart2(topList, selectedDiseaseType);
                        }
                    }
                }
            } else {
                if (cardDisease) cardDisease.style.display = "none";
                if (cardDiseaseFatal) cardDiseaseFatal.style.display = "none";
            }


            /* =========================
            * 종합 위험도 평가 (점수 + details 토글)
            * ========================= */
            const riskData = riskDataByPeriod[yearFlag];
            updateKPIByRiskData(riskData, visualArea, accRate, fatalRate);

            const riskGrid = document.getElementById("riskGrid");
            const riskNoData = document.getElementById("riskNoData");

            // 점수/문구 영역
            const riskScoreWrap = document.getElementById("riskScoreWrap");
            const riskScoreNumber = document.getElementById("riskScoreNumber");
            const riskLevelText = document.getElementById("riskLevelText");
            const riskMessageText = document.getElementById("riskMessageText");

            // breakdown
            const breakdownBase = document.getElementById("breakdownBase");
            const breakdownPersonal = document.getElementById("breakdownPersonal");
            const breakdownSeverity = document.getElementById("breakdownSeverity");

            // details (토글 패널 내부)
            const detailAccidentRate = document.getElementById("detailAccidentRate");
            const detailDeathRate = document.getElementById("detailDeathRate");
            const detailSeverityRatio = document.getElementById("detailSeverityRatio");
            const detailGenderFactor = document.getElementById("detailGenderFactor");
            const detailAgeFactor = document.getElementById("detailAgeFactor");

            // 토글 패널은 기간 바뀔 때 기본 닫힘으로 리셋
            const toggleBtn = document.getElementById("toggleRiskDetailsBtn");
            const detailsPanel = document.getElementById("riskDetailsPanel");
            if (detailsPanel) detailsPanel.style.display = "none";
            if (toggleBtn) toggleBtn.textContent = "상세 지표 보기 ▼";

            // 점수 영역은 데이터 유무와 상관없이 보여주되(없으면 0점/메시지)
            if (riskScoreWrap) riskScoreWrap.style.display = "block";

            // ✅ 메시지는 한 곳(riskConditionText)에만 출력해서 겹침 제거
            const conditionEl = document.getElementById("riskConditionText");

            if (!riskData) {
                if (conditionEl) conditionEl.textContent = "충분한 통계 데이터가 없습니다.";

                if (riskScoreNumber) riskScoreNumber.textContent = "0";
                if (riskLevelText) riskLevelText.textContent = "데이터 없음";

                // ✅ 여기엔 message 대신 짧은 안내만
                if (riskMessageText) riskMessageText.textContent = `최근 ${yearFlag}년 분석`;

                if (breakdownBase) breakdownBase.textContent = "0점";
                if (breakdownPersonal) breakdownPersonal.textContent = "0점";
                if (breakdownSeverity) breakdownSeverity.textContent = "0점";

                if (riskGrid) riskGrid.style.display = "none";
                if (riskNoData) riskNoData.style.display = "block";
            } else {
                // ===== 1) 상단 문구: 백엔드 message만 표시 =====
                if (conditionEl) {
                    conditionEl.textContent = riskData.message || "충분한 통계 데이터가 없습니다.";
                }

                // ===== 2) 점수 표시 =====
                const totalScore = (riskData.total_score ?? 0);
                if (riskScoreNumber) riskScoreNumber.textContent = totalScore;

                if (riskLevelText) riskLevelText.textContent = (riskData.risk_level ?? "-");


                // ===== 3) breakdown 표시 =====
                const base = riskData.breakdown?.base_score ?? 0;
                const personal = riskData.breakdown?.personal_score ?? 0;
                const severity = riskData.breakdown?.severity_score ?? 0;

                if (breakdownBase) breakdownBase.textContent = `${base}점`;
                if (breakdownPersonal) breakdownPersonal.textContent = `${personal}점`;
                if (breakdownSeverity) breakdownSeverity.textContent = `${severity}점`;

                const explanationListEl = document.getElementById("riskExplanationList");

                if (explanationListEl) {
                    const explanations = riskData.explanation || [];

                    if (explanations.length === 0) {
                        explanationListEl.innerHTML = `
                            <li>현재 조건에서는 비교적 안정적인 위험 수준을 보이고 있습니다.</li>
                        `;
                    } else {
                        explanationListEl.innerHTML = explanations
                            .map(text => `<li>${text}</li>`)
                            .join("");
                    }
                }

                // ===== 4) details(토글) 값 채우기 =====
                const accRate = riskData.details?.accident_rate ?? 0;
                const deathRate = riskData.details?.death_rate ?? 0;
                const sevRatio = riskData.details?.severity_ratio ?? 0;
                const genderFactor = riskData.details?.gender_factor ?? 0;
                const ageFactor = riskData.details?.age_factor ?? 0;

                if (detailAccidentRate) detailAccidentRate.textContent = accRate;
                if (detailDeathRate) detailDeathRate.textContent = deathRate;
                if (detailSeverityRatio) detailSeverityRatio.textContent = `${sevRatio}%`;
                if (detailGenderFactor) detailGenderFactor.textContent = `${genderFactor}%`;
                if (detailAgeFactor) detailAgeFactor.textContent = `${ageFactor}%`;

                // ===== 5) TOP5 + 파이차트 영역 (has_data가 true일 때만) =====
                if (riskData.has_data) {
                    if (riskGrid) riskGrid.style.display = "grid";
                    if (riskNoData) riskNoData.style.display = "none";

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

                    if (document.getElementById("riskAccidentPie")) {
                        window.RiskAccidentPieChart?.(riskData.injury_top5);
                    }
                    if (document.getElementById("riskDiseasePie")) {
                        window.RiskDiseasePieChart?.(riskData.disease_top5);
                    }
                } else {
                    if (riskGrid) riskGrid.style.display = "none";
                    if (riskNoData) riskNoData.style.display = "block";

                    const a = document.getElementById("injuryRiskList");
                    const b = document.getElementById("diseaseRiskList");
                    if (a) a.innerHTML = "";
                    if (b) b.innerHTML = "";
                }
            }
            });
        });

    // 페이지 로드 시 산재가 선택되어 있으면 자동으로 1년 버튼 클릭
    if (visualArea && visualArea.dataset.hasSelection === "1") {
        const defaultBtn = document.querySelector('.period-btn[data-year="1"]');
        defaultBtn?.click();
    }
});

