// chart.js

// 이 파일 안에서만 차트 인스턴스를 관리하는 전역 객체
const charts = {};

/* =========================================
 *  공통 가로형 Bar 차트 생성/업데이트 함수
 * ========================================= */
function createHorizontalBarChart(chartKey, canvasId, labels, data, options) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.warn("canvas 없음:", canvasId);
        return;
    }

    const ctx = canvas.getContext("2d");
    const existing = charts[chartKey];

    if (existing) {
        // 기존 차트가 있으면 데이터만 교체
        existing.data.labels = labels;
        existing.data.datasets[0].data = data;
        existing.update();
        return;
    }

    charts[chartKey] = new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: options.label || "",
                data,
                backgroundColor: options.color || "#3b82f6",
                borderRadius: 12,
                borderSkipped: false,
                maxBarThickness: 26
            }]
        },
        options: {
            indexAxis: "y",              // ★ 가로형 바 차트
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: !!options.labelVisible
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const v = ctx.raw ?? 0;
                            return `${v.toLocaleString()}명`;
                        }
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
                        font: { size: 11 }
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 11 }
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
                backgroundColor: ["#4F46E5", "#F97316"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom"
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
            labels: ["남자 사망", "여자 사망"],
            datasets: [{
                data,
                backgroundColor: ["#EF4444", "#FACC15"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}

/* =========================
 *  2. 연령대별 바 차트
 * ========================= */

function AgeChart1(ageU18, age20s, age30s, age40s, age50s, age60p) {
    const labels = ["18세 미만", "20대", "30대", "40대", "50대", "60대 이상"];
    const data   = [ageU18, age20s, age30s, age40s, age50s, age60p];

    createHorizontalBarChart("age1", "ageChart1", labels, data, {
        color: "#22c55e",            // 연두색 계열
        label: "연령대별 재해자 수",
        labelVisible: false
    });
}

function AgeChart2(ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa) {
    const labels = ["18세 미만", "20대", "30대", "40대", "50대", "60대 이상"];
    const data   = [ageU18a, age20sa, age30sa, age40sa, age50sa, age60pa];

    createHorizontalBarChart("age2", "ageChart2", labels, data, {
        color: "#0f172a",            // 진한 남색
        label: "연령대별 사망자 수",
        labelVisible: false
    });
}

/* =========================
 *  3. 발생형태 / 질병형태 바 차트
 *     topList: [{ rank, name, count }, ...]
 * ========================= */

function InjuryChart1(topList) {
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
        color: "#f97316",            // 주황  
        label: "재해자 수",
        labelVisible: false
    });
}

function InjuryChart2(topList) {
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
        color: "#0f172a",            // 진한 남색
        label: "사망자 수",
        labelVisible: false
    });
}

function DiseaseChart1(topList) {
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
        color: "#38bdf8",            // 파랑
        label: "재해자 수",
        labelVisible: false
    });
}

function DiseaseChart2(topList) {
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
        color: "#f97373",            // 붉은 계열
        label: "사망자 수",
        labelVisible: false
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
