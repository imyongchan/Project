// chart.js

// 이 파일 안에서만 차트 인스턴스를 관리하는 전역 객체
const charts = {};

// datalabels 플러그인 등록 (HTML에서 chartjs-plugin-datalabels 추가되어 있어야 함)
if (window.Chart && window.ChartDataLabels) {
    Chart.register(window.ChartDataLabels);
}

/* =========================================
 * 공통 가로형 Bar 차트
 * chartRefName : 전역에 저장할 이름
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
    const existing = window[chartRefName];

    // 라벨별 색상 배열 (highlightLabel과 같은 라벨은 highlightColor)
    const colors = labels.map(l =>
        (highlightLabel && l === highlightLabel) ? highlightColor : color
    );

    if (existing) {
        existing.data.labels = labels;
        existing.data.datasets[0].data = data;
        existing.data.datasets[0].backgroundColor = colors;
        existing.update();
        return;
    }

    window[chartRefName] = new Chart(ctx, {
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
                        size: 13,      // 글씨 크게
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
                        font: { size: 13 },
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 13 },
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
                backgroundColor: ["#14b6f6", "#EF4444"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom" }
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
            labels: ["남자 사망", "여자 사망"],
            datasets: [{
                data,
                backgroundColor: ["#14b6f6", "#EF4444"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom" }
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

    createHorizontalBarChart("age1", "ageChart1", labels, data, {
        color: "#cfeff9ff",            // 연두색 계열
        label: "연령대별 재해자 수",
        labelVisible: false,
        highlightLabel
    });
}

function AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa, highlightLabel = null) {
    const labels = ["18세 미만", "20대", "30대", "40대", "50대", "60대 이상"];
    const data   = [ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa];

    createHorizontalBarChart("age2", "ageChart2", labels, data, {
        color: "#5c4ac2ff",            // 진한 남색
        label: "연령대별 사망자 수",
        labelVisible: false,
        highlightLabel
    });
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
        color: "#cfeff9ff",            // 주황  
        label: "재해자 수",
        labelVisible: false,
        highlightLabel,              // 내 발생형태
        highlightColor: "#ef4444"
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
        color: "#5c4ac2ff",            // 진한 남색
        label: "사망자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#ef4444"
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
        color: "#cfeff9ff",            // 파랑
        label: "재해자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#ef4444"
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
        color: "#5c4ac2ff",            // 붉은 계열
        label: "사망자 수",
        labelVisible: false,
        highlightLabel,
        highlightColor: "#a39d9d80"
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
