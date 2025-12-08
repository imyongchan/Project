let genderChart1 = null;
let genderChart2 = null;

function GenderChart1(male, female) {
    const ctx = document.getElementById("genderChart1");
    if (!ctx) return;  


    if (genderChart1) {
        genderChart1.data.datasets[0].data = [male, female];
        genderChart1.update();
        return;
    }

    // 새로 생성
    genderChart1 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자", "여자"],
            datasets: [{
                data: [male, female],
                backgroundColor: ["#4F46E5", "#F97316"], 
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

function GenderChart2(male2, female2) {
    const ctx = document.getElementById("genderChart2");
    if (!ctx) return;  


    if (genderChart2) {
        genderChart2.data.datasets[0].data = [male2, female2];
        genderChart2.update();
        return;
    }

    // 새로 생성
    genderChart2 = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["남자", "여자"],
            datasets: [{
                data: [male2, female2],
                backgroundColor: ["#4F46E5", "#F97316"], 
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