let currentChart;


function showChart(type) {
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
        if (currentChart) {
            currentChart.destroy();
        }  
        const ctx = document.getElementById('mainChart').getContext('2d');
        currentChart = new Chart(ctx, {
            type: 'doughnut',  // 도넛 모양으로 변경
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
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }  
    // 페이지 로드 시 연령별 차트 표시
    window.onload = function() {
        showChart('age');
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
