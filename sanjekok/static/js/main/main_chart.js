// ⭐ datalabels 플러그인 등록 (필수)
Chart.register(ChartDataLabels);

let currentChart;

function showChart(type, btn) {
    // ⭐ 버튼 active 처리
    document.querySelectorAll('.chart-btn').forEach(b => {
        b.classList.remove('active');
    });
    if (btn) btn.classList.add('active');

    let labels = [];
    let data = [];

    if (type === 'age') {
        labels = Object.keys(ageData);
        data = Object.values(ageData);
    } else if (type === 'gender') {
        labels = Object.keys(genderData);
        data = Object.values(genderData);
    } else if (type === 'industry') {
        labels = Object.keys(industryData);
        data = Object.values(industryData);
    }

    const ctx = document.getElementById('mainChart').getContext('2d');

    // ⭐ 이미 차트가 있으면 데이터만 교체
    if (currentChart) {
        currentChart.data.labels = labels;
        currentChart.data.datasets[0].data = data;
        currentChart.update();
        return;
    }

    // ⭐ 최초 1회 차트 생성
    currentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: '사고 수',
                data: data,
                backgroundColor: [
                    '#8884d8', '#82ca9d', '#ffc658', '#ff7f50', '#8dd1e1',
                    '#a4de6c', '#d0ed57', '#d88884', '#a28dd1', '#ca82c9'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percent = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${percent}% (${value}건)`;
                        }
                    }
                },
                datalabels: {
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 12
                    },
                    formatter: (value, ctx) => {
                        const dataArr = ctx.chart.data.datasets[0].data;
                        const total = dataArr.reduce((a, b) => a + b, 0);
                        return ((value / total) * 100).toFixed(1) + '%';
                    }
                }
            }
        }
    });
}

// ⭐ 페이지 로드 시 연령 버튼 자동 active
window.onload = function() {
    const firstBtn = document.querySelector('.chart-btn');
    showChart('age', firstBtn);
};




function updateDateTime() {
    const dateEl = document.querySelector('.clock-date');
    const timeEl = document.querySelector('.clock-time .time');
    const ampmEl = document.querySelector('.clock-time .ampm');

    if (!dateEl || !timeEl || !ampmEl) return;

    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const date = String(now.getDate()).padStart(2, '0');

    const days = ['일','월','화','수','목','금','토'];
    const day = days[now.getDay()];

    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');

    let period = '오전';
    if (hours >= 12) period = '오후';

    hours = hours % 12 || 12;

    dateEl.innerHTML = `
        ${year}.${month}.${date}
        <span class="day">${day}</span>
    `;

    ampmEl.innerText = period;
    timeEl.innerText = `${hours}:${minutes}`;
}

document.addEventListener('DOMContentLoaded', () => {
    updateDateTime();
    setInterval(updateDateTime, 1000);
});
