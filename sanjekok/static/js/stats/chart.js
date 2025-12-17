// chart.js

// 이 파일 안에서만 차트 인스턴스를 관리하는 전역 객체
const charts = {};

// datalabels 플러그인 등록 (HTML에서 chartjs-plugin-datalabels 추가되어 있어야 함)
if (window.Chart && window.ChartDataLabels) {
    Chart.register(window.ChartDataLabels);
}

/* =========================================
 * 공통 가로형 Bar 차트
 * chartRefName : charts 객체에 저장할 이름
 * canvasId     : 캔버스 id
 * labels       : 라벨 배열
 * data         : 데이터 배열
 * options      : {
 *   color, label, labelVisible,
 *   highlightLabel, highlightColor
 * }
 * ========================================= */
function createHorizontalBarChart(chartRefName, canvasId, labels, data, options = {}) {
    const {
        color = "#3b82f6",
        label = "",
        labelVisible = false,
        highlightLabel = null,          // 회원이 속한 항목 라벨
        highlightColor = "#f97316"      // 강조 색
    } = options;

    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.warn("canvas 없음:", canvasId);
        return;
    }

    const ctx = canvas.getContext("2d");
    const existing = charts[chartRefName];

    const normalize = s => (s || "").replace(/\s+/g, "").toLowerCase();

    const colors = labels.map(l =>
        (highlightLabel && normalize(l) === normalize(highlightLabel))
            ? highlightColor
            : color
    );
    
    if (existing) {
        existing.data.labels = labels;
        existing.data.datasets[0].data = data;
        existing.data.datasets[0].backgroundColor = colors;
        existing.update();
        return;
    }

    charts[chartRefName] = new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors,
                borderRadius: 14,
                borderSkipped: false,
                maxBarThickness: 32
            }]
        },
        options: {
            indexAxis: "y",              // 가로형
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    right: 70   // 필요하면 50~60까지 늘려도 됨
                }
            },            
            plugins: {
                legend: { display: !!labelVisible },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${(ctx.raw ?? 0).toLocaleString()}명`
                    }
                },
                // 막대 옆에 수치 표시
                datalabels: {
                    anchor: "end",
                    align: "right",
                    clamp: true,
                    
                    formatter: (v) => `${(v ?? 0).toLocaleString()}명`,
                    color: "#111827",
                    font: {
                        size: 17,      // 글씨 크게
                        weight: "600"
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false,
                        color: "rgba(148, 163, 184, 0.25)"
                    },
                    ticks: {
                        font: { size: 20 },
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 20 },
                    }
                }
            }
        }
    });
}

/* =========================
 *  1. 성별 도넛 차트
 * ========================= */

function GenderChart1(male, female) {
    const canvas = document.getElementById("genderChart1");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const data = [male, female];
    const existing = charts.gender1;

    if (existing) {
        existing.data.datasets[0].data = data;
        existing.update();
        return;
    }

    charts.gender1 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자", "여자"],
            datasets: [{
                data,
                backgroundColor: ["#23333d", "#f99b18"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                  legend: {
                    position: "bottom",
                    labels: {
                        font: {
                            size: 25,   // ← 범례 글씨 크기 키움 (기본 12~14)
                            weight: "600"
                        },
                        color: "#111827"  // 글자색 (선택사항)
                        }
                    },
                    
                    datalabels: {
                            color: "#ffffff",
                            font: {
                                    size: 20,
                                    weight: "300"
                                },
                                formatter: (value, ctx) => {
                                    const total = ctx.chart.data.datasets[0].data
                                        .reduce((a, b) => a + b, 0) || 1;
                                    const percent = value / total * 100;
                                    return `${percent.toFixed(1)}%`;
                                }
                        }
            }
        }
    });
}

function GenderChart2(maleFatal, femaleFatal) {
    const canvas = document.getElementById("genderChart2");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const data = [maleFatal, femaleFatal];
    const existing = charts.gender2;

    if (existing) {
        existing.data.datasets[0].data = data;
        existing.update();
        return;
    }

    charts.gender2 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자", "여자"],
            datasets: [{
                data,
                backgroundColor: ["#23333d", "#f99b18"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                  legend: {
                    position: "bottom",
                    labels: {
                        font: {
                            size: 25,   // ← 범례 글씨 크기 키움 (기본 12~14)
                            weight: "600"
                        },
                        color: "#111827"  // 글자색 (선택사항)
                        }
                    },
                    
                    datalabels: {
                            color: "#ffffff",
                            font: {
                                    size: 20,
                                    weight: "300"
                                },
                                formatter: (value, ctx) => {
                                    const total = ctx.chart.data.datasets[0].data
                                        .reduce((a, b) => a + b, 0) || 1;
                                    const percent = value / total * 100;
                                    return `${percent.toFixed(1)}%`;
                                }
                        }
            }
        }
    });
}

/* =========================
 *  2. 연령대별 바 차트
 *  (highlightLabel은 나중에 내 연령대 라벨 넘기면 됨)
 * ========================= */

function AgeChart1(ageU18, age20s, age30s, age40s, age50s, age60p, highlightLabel = null) {
    const labels = ["18세 미만", "20대", "30대", "40대", "50대", "60대 이상"];
    const data   = [ageU18, age20s, age30s, age40s, age50s, age60p];

    const normalize = (s) => (s || "").replace(/\s+/g, "").toLowerCase();

    // 데이터/라벨 정렬(기존 그대로)
    const combined = labels.map((label, index) => ({ label, value: data[index] }));
    combined.sort((a, b) => b.value - a.value);
    const sortedLabels = combined.map(item => item.label);
    const sortedData   = combined.map(item => item.value);

    createHorizontalBarChart("age1", "ageChart1", sortedLabels, sortedData, {
        color: "#23333d",
        label: "연령대별 재해자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#f99b18"
    });

    const ageSummaryBox = document.getElementById("ageSummary1");
    if (ageSummaryBox && highlightLabel) {

        // ✅ 여기만 변경: 정규화로 index 찾기
        const highlightIndex = labels.findIndex(l => normalize(l) === normalize(highlightLabel));
        const highlightCount = data[highlightIndex] || 0;

        // 최댓값 찾기
        const maxValue = Math.max(...data);
        const maxIndex = data.indexOf(maxValue);
        const maxLabel = labels[maxIndex];

        ageSummaryBox.innerHTML = `
            <i class="fa-solid fa-triangle-exclamation"></i>
            <div>
                나의 연령대(<strong>${highlightLabel}</strong>)의 재해자 수는 <strong>${highlightCount}명</strong>입니다.<br>
                가장 많이 발생한 연령대는 <strong>${maxLabel}</strong>입니다.
            </div>
        `;
    }
}

function AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa, highlightLabel = null) {
    const labels = ["18세 미만", "20대", "30대", "40대", "50대", "60대 이상"];
    const data   = [ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa];
    const normalize = (s) => (s || "").replace(/\s+/g, "").toLowerCase();

    // 데이터/라벨 정렬(기존 그대로)
    const combined = labels.map((label, index) => ({ label, value: data[index] }));
    combined.sort((a, b) => b.value - a.value);
    const sortedLabels = combined.map(item => item.label);
    const sortedData   = combined.map(item => item.value);

    createHorizontalBarChart("age2", "ageChart2", sortedLabels, sortedData, {
        color: "#23333d",
        label: "연령대별 재해자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#f99b18"
    });

    const ageSummaryBox = document.getElementById("ageSummary2");
    if (ageSummaryBox && highlightLabel) {
        const highlightIndex = labels.findIndex(l => normalize(l) === normalize(highlightLabel));
        const highlightCount = data[highlightIndex] || 0;

        // 최댓값 찾기
        const maxValue = Math.max(...data);
        const maxIndex = data.indexOf(maxValue);
        const maxLabel = labels[maxIndex];

        ageSummaryBox.innerHTML = `
            <i class="fa-solid fa-triangle-exclamation"></i>
            <div>
                나의 연령대(<strong>${highlightLabel}</strong>)의 재해자 수는 <strong>${highlightCount}명</strong>입니다.<br>
                가장 많이 발생한 연령대는 <strong>${maxLabel}</strong>입니다.
            </div>
        `;
    }
}
/* =========================
 *  3. 발생형태 / 질병형태 바 차트
 *     topList: [{ rank, name, count }, ...]
 * ========================= */

function InjuryChart1(topList, highlightLabel = null) {
    const canvas = document.getElementById("injuryChart1");
    if (!canvas) return;

    if (!topList || !topList.length) {
        if (charts.injury1) {
            charts.injury1.destroy();
            charts.injury1 = null;
        }
        return;
    }

    const labels = topList.map(item => item.name);
    const data   = topList.map(item => item.count || 0);

    createHorizontalBarChart("injury1", "injuryChart1", labels, data, {
        color: "#23333d",            // 연한 하늘색
        label: "재해자 수",
        labelVisible: false,
        highlightLabel,              // 내 발생형태
        highlightColor: "#f99b18"
    });
}

function InjuryChart2(topList, highlightLabel = null) {
    const canvas = document.getElementById("injuryChart2");
    if (!canvas) return;

    if (!topList || !topList.length) {
        if (charts.injury2) {
            charts.injury2.destroy();
            charts.injury2 = null;
        }
        return;
    }

    const labels = topList.map(item => item.name);
    const data   = topList.map(item => item.count || 0);

    createHorizontalBarChart("injury2", "injuryChart2", labels, data, {
        color: "#23333d",            // 진한 남색
        label: "사망자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#f99b18"
    });
}

function DiseaseChart1(topList, highlightLabel = null) {
    const canvas = document.getElementById("diseaseChart1");
    if (!canvas) return;

    if (!topList || !topList.length) {
        if (charts.disease1) {
            charts.disease1.destroy();
            charts.disease1 = null;
        }
        return;
    }

    const labels = topList.map(item => item.name);
    const data   = topList.map(item => item.count || 0);

    createHorizontalBarChart("disease1", "diseaseChart1", labels, data, {
        color: "#23333d",            // 연한 하늘색
        label: "재해자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#f99b18"
    });
}

function DiseaseChart2(topList, highlightLabel = null) {
    const canvas = document.getElementById("diseaseChart2");
    if (!canvas) return;

    if (!topList || !topList.length) {
        if (charts.disease2) {
            charts.disease2.destroy();
            charts.disease2 = null;
        }
        return;
    }

    const labels = topList.map(item => item.name);
    const data   = topList.map(item => item.count || 0);

    createHorizontalBarChart("disease2", "diseaseChart2", labels, data, {
        color: "#23333d",            // 진한 남색
        label: "사망자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#f99b18"
    });
}


function createPieChart(chartRefName, canvasId, labels, data, options = {}) {
    const {
        colors = ["#EF4444", "#f99b18", "#FACC15", "#22C55E", "#3B82F6"],  // 최대 TOP5
        cutout = "55%"  // 도넛 형태, 필요 없으면 "0%"로 바꾸면 완전 파이
    } = options;

    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.warn("canvas 없음:", canvasId);
        return;
    }

    const ctx = canvas.getContext("2d");
    const existing = charts[chartRefName];

    // 데이터 없으면 차트 제거
    if (!labels || !labels.length || !data || !data.length) {
        if (existing) {
            existing.destroy();
            charts[chartRefName] = null;
        }
        return;
    }

    if (existing) {
        existing.data.labels = labels;
        existing.data.datasets[0].data = data;
        existing.update();
        return;
    }

    charts[chartRefName] = new Chart(ctx, {
        type: "doughnut",       // 필요하면 "pie" 로 변경 가능
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout,   // 도넛 안쪽 구멍 크기
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        font: {
                            size: 18,   // ← 범례 글씨 크기 키움 (기본 12~14)
                            weight: "500"
                        },
                        color: "#23333d"  // 글자색 (선택사항)
                    }
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0) || 1;
                            const val = ctx.raw ?? 0;
                            const percent = (val / total * 100).toFixed(1);
                            return `${ctx.label}: ${percent}% `;
                        }
                    }
                },
                datalabels: {
                    color: "#111827",
                    font: {
                        size: 15,
                        weight: "600"
                    },
                    formatter: (value, ctx) => {
                        const total = ctx.chart.data.datasets[0].data
                            .reduce((a, b) => a + b, 0) || 1;
                        const percent = value / total * 100;
                        return `${percent.toFixed(1)}%`;
                    }
                }
            }
        }
    });
}



function RiskAccidentPieChart(topList) {
  const labels = (topList || []).map(item => item.name);
  const data   = (topList || []).map(item => Number(item.percentage || 0));

  const sum = data.reduce((a,b)=>a+b,0);
  const etc = Math.max(0, +(100 - sum).toFixed(1)); // 소수 1자리 정리

  if (etc > 0) {
    labels.push("기타");
    data.push(etc);
  }

  createPieChart("riskAccident", "riskAccidentPie", labels, data, {
    colors: ["#dc2626", "#f99b18", "#FACC15", "#2fb34a", "#9cffaf", "#cbd5e1"], // 기타 색 하나 추가
    cutout: "55%"
  });
}

function RiskDiseasePieChart(topList) {
  const labels = (topList || []).map(item => item.name);
  const data   = (topList || []).map(item => Number(item.percentage || 0));

  const sum = data.reduce((a,b)=>a+b,0);
  const etc = Math.max(0, +(100 - sum).toFixed(1));

  if (etc > 0) {
    labels.push("기타");
    data.push(etc);
  }

  createPieChart("riskDisease", "riskDiseasePie", labels, data, {
    colors: ["#dc2626", "#f99b18", "#FACC15", "#2fb34a", "#9cffaf", "#cbd5e1"],
    cutout: "55%"
  });
}




/* =========================
 *  전역에서 호출할 수 있게 연결
 * ========================= */

window.GenderChart1  = GenderChart1;
window.GenderChart2  = GenderChart2;
window.AgeChart1     = AgeChart1;
window.AgeChart2     = AgeChart2;
window.InjuryChart1  = InjuryChart1;
window.InjuryChart2  = InjuryChart2;
window.DiseaseChart1 = DiseaseChart1;
window.DiseaseChart2 = DiseaseChart2;
window.RiskAccidentPieChart = RiskAccidentPieChart;
window.RiskDiseasePieChart  = RiskDiseasePieChart;