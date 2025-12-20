document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('memberChart');

    if (!canvas) {
        console.error("memberChart canvas not found");
        return;
    }

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: DAYS,
            datasets: [
                {
                    label: '일별 신규 가입자 수',
                    data: COUNTS,
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 5,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,   // ⭐ 중요
            plugins: {
                title: {
                    display: true,
                    text: '일별 신규가입',
                    font: { size: 20 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
