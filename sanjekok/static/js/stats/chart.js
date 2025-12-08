let genderChart1 = null;
let genderChart2 = null;


function GenderChart1(male, female) {
    const ctx = document.getElementById("genderChart1");
    if (!ctx) return;

    const data = [male, female];

    // 기존 차트 있으면 데이터만 교체
    if (genderChart1) {
        genderChart1.data.datasets[0].data = data;
        genderChart1.update();
        return;
    }

    genderChart1 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자", "여자"],
            datasets: [{
                data: data,
                backgroundColor: ["#4F46E5", "#F97316"], // 파랑 / 주황
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}


function GenderChart2(maleFatal, femaleFatal) {
    const ctx = document.getElementById("genderChart2");
    if (!ctx) return;

    const data = [maleFatal, femaleFatal];

    // 기존 차트 있으면 데이터만 교체
    if (genderChart2) {
        genderChart2.data.datasets[0].data = data;
        genderChart2.update();
        return;
    }

    genderChart2 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자 사망", "여자 사망"],
            datasets: [{
                data: data,
                backgroundColor: ["#EF4444", "#FACC15"], // 빨강 / 노랑
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}

// 다른 JS 파일에서도 쓸 수 있게 전역에 붙이기
window.GenderChart1 = GenderChart1;
window.GenderChart2 = GenderChart2;

