document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('memberChart');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: DAYS,
            datasets: [
                {
                    label: '오늘 신규 가입자 수',
                    data: COUNTS,
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 5
                },
                {
                    label: '전체 산재 등록 수',
                    data: Array(DAYS.length).fill(TOTAL_INDIVIDUAL), // 고정값을 가로로 뿌림
                    borderWidth: 2,
                    borderDash: [5, 5],   // 점선 (구분용)
                    tension: 0.3,
                    pointRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '월별 신규가입 & 전체 산재 등록 수',
                    font: { size: 20 }
                },
                legend: { display: true }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
});