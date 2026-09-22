class ChartManager {
    constructor() {
        this.revenueChart = null;
        this.errorChart = null;
        this.initRevenueChart();
        this.initErrorChart();
    }

    initRevenueChart() {
        const ctx = document.getElementById('dailyRevenueChart').getContext('2d');
        this.revenueChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Daily Revenue (IDR)',
                        data: [],
                        borderColor: '#e4e4e7',
                        backgroundColor: 'rgba(228, 228, 231, 0.05)',
                        fill: true,
                        tension: 0.3,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Transactions',
                        data: [],
                        borderColor: '#71717a',
                        backgroundColor: 'transparent',
                        borderDash: [4, 4],
                        tension: 0.2,
                        yAxisID: 'y1',
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 350,
                },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        grid: { color: '#1c1e22' },
                        ticks: { color: '#71717a', font: { family: 'Inter', size: 11 } }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: { color: '#1c1e22' },
                        ticks: {
                            color: '#a1a1aa',
                            font: { family: 'JetBrains Mono', size: 11 },
                            callback: value => 'Rp ' + (value / 1000).toLocaleString() + 'k'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#71717a', font: { family: 'JetBrains Mono', size: 11 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#a1a1aa', font: { family: 'Inter', size: 12 } }
                    }
                }
            }
        });
    }

    initErrorChart() {
        const ctx = document.getElementById('errorDistributionChart').getContext('2d');
        this.errorChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Double Scan', 'Typo SKU', 'Void Item', 'Walkouts'],
                datasets: [{
                    data: [0, 0, 0, 0],
                    backgroundColor: ['#e4e4e7', '#a1a1aa', '#71717a', '#3f3f46'],
                    borderWidth: 1,
                    borderColor: '#121316'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 300 },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#a1a1aa', font: { family: 'Inter', size: 11 } }
                    }
                }
            }
        });
    }

    reset() {
        if (this.revenueChart) {
            this.revenueChart.data.labels = [];
            this.revenueChart.data.datasets[0].data = [];
            this.revenueChart.data.datasets[1].data = [];
            this.revenueChart.update();
        }
        if (this.errorChart) {
            this.errorChart.data.datasets[0].data = [0, 0, 0, 0];
            this.errorChart.update();
        }
    }

    appendDailyPoint(daySummary) {
        if (!this.revenueChart) return;
        this.revenueChart.data.labels.push(daySummary.date);
        this.revenueChart.data.datasets[0].data.push(daySummary.revenue);
        this.revenueChart.data.datasets[1].data.push(daySummary.transactions);
        this.revenueChart.update();
    }

    updateErrorDistribution(doubleScan, typo, voidCount, walkouts) {
        if (!this.errorChart) return;
        this.errorChart.data.datasets[0].data = [doubleScan, typo, voidCount, walkouts];
        this.errorChart.update();
    }
}
