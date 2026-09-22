class DashboardApp {
    constructor() {
        this.controls = new ControlsManager();
        this.charts = new ChartManager();
        this.modal = new ModalManager();
        this.table = new TableManager(idx => this.inspectByIndex(idx));
        this.storeFloor = new StoreFloorManager();

        this.playback = new PlaybackManager(
            (frame, current, total, finished) => this.handleDayTick(frame, current, total, finished),
            () => this.handleSimulationComplete(),
            () => this.handleReset()
        );

        this.initUIElements();
        this.bindEvents();
        this.storeFloor.renderDefault(4);
        this.loadInitialState();
    }

    initUIElements() {
        this.btnPlay = document.getElementById('btn-play');
        this.btnPause = document.getElementById('btn-pause');
        this.btnStep = document.getElementById('btn-step');
        this.btnReset = document.getElementById('btn-reset');
        this.speedButtons = document.querySelectorAll('.speed-btn');

        this.currentDayLabel = document.getElementById('current-day-label');
        this.totalDaysLabel = document.getElementById('total-days-label');
        this.currentDateLabel = document.getElementById('current-date-label');
        this.progressBar = document.getElementById('sim-progress-bar');

        this.statRevenue = document.getElementById('stat-revenue');
        this.statTransactions = document.getElementById('stat-transactions');
        this.statItems = document.getElementById('stat-items');
        this.statErrors = document.getElementById('stat-errors');
        this.statErrorRate = document.getElementById('stat-error-rate');
        this.statAbandonments = document.getElementById('stat-abandonments');

        this.cachedTransactions = [];
        this.cumulativeStats = this.getEmptyStats();
    }

    getEmptyStats() {
        return { revenue: 0, transactions: 0, items: 0, errors: 0, abandonments: 0, doubleScan: 0, typo: 0, voidCount: 0 };
    }

    bindEvents() {
        this.btnPlay.addEventListener('click', () => this.handlePlayClick());
        this.btnPause.addEventListener('click', () => this.handlePauseClick());
        this.btnStep.addEventListener('click', () => this.handleStepClick());
        this.btnReset.addEventListener('click', () => this.playback.reset());

        this.speedButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.speedButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const speed = parseInt(btn.dataset.speed, 10);
                this.playback.setSpeed(speed);
            });
        });
    }

    async loadInitialState() {
        try {
            const metrics = await SimulationService.fetchMetrics();
            if (metrics.daily_summaries && metrics.daily_summaries.length > 0) {
                this.totalDaysLabel.textContent = metrics.daily_summaries.length;
                this.updateStatsDisplay(metrics.total_revenue, metrics.total_transactions, metrics.total_items_sold, metrics.error_transactions, metrics.error_rate_pct, metrics.customer_abandonments);
                metrics.daily_summaries.forEach(d => this.charts.appendDailyPoint(d));
                this.charts.updateErrorDistribution(metrics.double_scan_count, metrics.typo_sku_count, metrics.void_count, metrics.customer_abandonments);
            }
        } catch (e) {
            console.info(e.message);
        }
    }

    async handlePlayClick() {
        if (this.playback.dailyFrames.length === 0 || this.playback.currentIndex >= this.playback.dailyFrames.length) {
            await this.requestNewSimulation();
        }
        this.btnPlay.disabled = true;
        this.btnPause.disabled = false;
        this.playback.play();
    }

    handlePauseClick() {
        this.playback.pause();
        this.btnPlay.disabled = false;
        this.btnPause.disabled = true;
    }

    async handleStepClick() {
        if (this.playback.dailyFrames.length === 0 || this.playback.currentIndex >= this.playback.dailyFrames.length) {
            await this.requestNewSimulation();
        }
        this.playback.step();
    }

    async requestNewSimulation() {
        this.handleReset();
        this.btnPlay.textContent = 'Generating...';
        this.btnPlay.disabled = true;

        try {
            const payload = this.controls.getPayload();
            const result = await SimulationService.triggerSimulation(payload);
            const frames = result.daily_frames || [];

            this.totalDaysLabel.textContent = frames.length;
            this.playback.loadFrames(frames);
        } catch (err) {
            alert('Simulation error: ' + err.message);
        } finally {
            this.btnPlay.textContent = 'Run Simulation';
            this.btnPlay.disabled = false;
        }
    }

    handleDayTick(frame, current, total, finished) {
        this.currentDayLabel.textContent = current;
        this.currentDateLabel.textContent = `${frame.date} (${frame.is_weekend ? 'Weekend Surge' : 'Regular'}${frame.is_payday ? ' • Payday' : ''})`;
        const pct = Math.round((current / total) * 100);
        this.progressBar.style.width = `${pct}%`;

        this.cumulativeStats.revenue += frame.revenue;
        this.cumulativeStats.transactions += frame.transactions;
        this.cumulativeStats.items += frame.items;
        this.cumulativeStats.errors += frame.errors;
        this.cumulativeStats.abandonments += frame.abandonments;

        const errRate = this.cumulativeStats.transactions > 0
            ? ((this.cumulativeStats.errors / this.cumulativeStats.transactions) * 100).toFixed(2)
            : '0.0';

        this.updateStatsDisplay(
            this.cumulativeStats.revenue,
            this.cumulativeStats.transactions,
            this.cumulativeStats.items,
            this.cumulativeStats.errors,
            errRate,
            this.cumulativeStats.abandonments
        );

        this.charts.appendDailyPoint(frame);
        this.charts.updateErrorDistribution(
            Math.round(this.cumulativeStats.errors * 0.4),
            Math.round(this.cumulativeStats.errors * 0.35),
            Math.round(this.cumulativeStats.errors * 0.25),
            this.cumulativeStats.abandonments
        );

        this.storeFloor.updateCounters(frame.cashiers_status);

        if (frame.sample_transactions) {
            this.cachedTransactions = [...frame.sample_transactions, ...this.cachedTransactions].slice(0, 35);
            this.table.setTransactions(this.cachedTransactions);
        }
    }

    handleSimulationComplete() {
        this.btnPlay.disabled = false;
        this.btnPlay.textContent = 'Replay';
        this.btnPause.disabled = true;
    }

    handleReset() {
        this.cumulativeStats = this.getEmptyStats();
        this.cachedTransactions = [];
        this.currentDayLabel.textContent = '0';
        this.currentDateLabel.textContent = 'Standby';
        this.progressBar.style.width = '0%';
        this.btnPlay.textContent = 'Start Simulation';
        this.btnPlay.disabled = false;
        this.btnPause.disabled = true;

        this.updateStatsDisplay(0, 0, 0, 0, 0.0, 0);
        this.charts.reset();
        this.table.setTransactions([]);
        this.storeFloor.renderDefault(parseInt(this.controls.cashiers.value, 10));
    }

    updateStatsDisplay(rev, tx, items, errors, errRate, abandonments) {
        this.statRevenue.textContent = 'Rp ' + Number(rev || 0).toLocaleString('id-ID');
        this.statTransactions.textContent = Number(tx || 0).toLocaleString();
        this.statItems.textContent = Number(items || 0).toLocaleString();
        this.statErrors.textContent = Number(errors || 0).toLocaleString();
        this.statErrorRate.textContent = errRate + '%';
        this.statAbandonments.textContent = Number(abandonments || 0).toLocaleString();
    }

    inspectByIndex(idx) {
        const tx = this.cachedTransactions[idx];
        if (tx) this.modal.show(tx);
    }
}

let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new DashboardApp();
});
