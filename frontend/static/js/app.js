class DashboardApp {
    constructor() {
        this.controls = new ControlsManager();
        this.charts = new ChartManager();
        this.modal = new ModalManager();
        this.table = new TableManager(idx => this.inspectByIndex(idx));

        this.runBtn = document.getElementById('run-sim-btn');
        this.statRevenue = document.getElementById('stat-revenue');
        this.statTransactions = document.getElementById('stat-transactions');
        this.statItems = document.getElementById('stat-items');
        this.statErrors = document.getElementById('stat-errors');
        this.statErrorRate = document.getElementById('stat-error-rate');
        this.statAbandonments = document.getElementById('stat-abandonments');

        this.cachedTransactions = [];
        this.bindEvents();
        this.loadInitialState();
    }

    bindEvents() {
        this.runBtn.addEventListener('click', () => this.handleRunSimulation());
    }

    async loadInitialState() {
        try {
            const metrics = await SimulationService.fetchMetrics();
            this.updateStats(metrics);
            if (metrics.daily_summaries) {
                this.charts.renderDailyRevenue(metrics.daily_summaries);
            }
            this.charts.renderErrorDistribution(metrics);
        } catch (e) {
            console.info(e.message);
        }
    }

    async handleRunSimulation() {
        this.runBtn.disabled = true;
        this.runBtn.textContent = 'Simulating...';

        try {
            const payload = this.controls.getPayload();
            const result = await SimulationService.triggerSimulation(payload);
            const metrics = result.metrics;
            this.cachedTransactions = result.sample_transactions || [];

            this.updateStats(metrics);
            if (metrics.daily_summaries) {
                this.charts.renderDailyRevenue(metrics.daily_summaries);
            }
            this.charts.renderErrorDistribution(metrics);
            this.table.setTransactions(this.cachedTransactions);
        } catch (err) {
            alert('Simulation error: ' + err.message);
        } finally {
            this.runBtn.disabled = false;
            this.runBtn.textContent = 'Run Simulation';
        }
    }

    updateStats(metrics) {
        this.statRevenue.textContent = 'Rp ' + Number(metrics.total_revenue || 0).toLocaleString('id-ID');
        this.statTransactions.textContent = Number(metrics.total_transactions || 0).toLocaleString();
        this.statItems.textContent = Number(metrics.total_items_sold || 0).toLocaleString();
        this.statErrors.textContent = Number(metrics.error_transactions || 0).toLocaleString();
        this.statErrorRate.textContent = (metrics.error_rate_pct || 0) + '%';
        this.statAbandonments.textContent = Number(metrics.customer_abandonments || 0).toLocaleString();
    }

    inspectByIndex(idx) {
        const tx = this.cachedTransactions[idx];
        if (tx) {
            this.modal.show(tx);
        }
    }
}

let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new DashboardApp();
});
