class ChartManager {
    constructor() {
        this.revenueChart = null;
        this.errorChart = null;
    }

    renderDailyRevenue(dailyData) {
        const ctx = document.getElementById('dailyRevenueChart').getContext('2d');
        const labels = dailyData.map(d => d.date);
        const revenues = dailyData.map(d => d.revenue);
        const transactions = dailyData.map(d => d.transactions);

        if (this.revenueChart) {
            this.revenueChart.destroy();
        }

        this.revenueChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Revenue (IDR)',
                        data: revenues,
                        borderColor: '#e4e4e7',
                        backgroundColor: 'rgba(228, 228, 231, 0.05)',
                        fill: true,
                        tension: 0.3,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Transactions',
                        data: transactions,
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

    renderErrorDistribution(metrics) {
        const ctx = document.getElementById('errorDistributionChart').getContext('2d');
        const labels = ['Double Scan', 'Typo SKU', 'Void Item', 'Walkouts'];
        const dataValues = [
            metrics.double_scan_count || 0,
            metrics.typo_sku_count || 0,
            metrics.void_count || 0,
            metrics.customer_abandonments || 0
        ];

        if (this.errorChart) {
            this.errorChart.destroy();
        }

        this.errorChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: [
                        '#e4e4e7',
                        '#a1a1aa',
                        '#71717a',
                        '#3f3f46'
                    ],
                    borderWidth: 1,
                    borderColor: '#121316'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#a1a1aa', font: { family: 'Inter', size: 11 } }
                    }
                }
            }
        });
    }
}
