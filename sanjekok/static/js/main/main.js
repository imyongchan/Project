function toggleMenu() {
    const nav = document.getElementById("menu");
    nav.classList.toggle("open");
}

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