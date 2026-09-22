class StoreFloorManager {
    constructor() {
        this.grid = document.getElementById('till-grid');
    }

    renderDefault(cashierCount = 4) {
        if (!this.grid) return;
        const placeholders = [];
        for (let i = 1; i <= cashierCount; i++) {
            placeholders.push({
                counter_id: i,
                name: `Till #${i}`,
                experience: i % 2 === 0 ? 'SENIOR' : 'JUNIOR',
                tx_processed: 0,
                errors: 0,
                peak_fatigue: 0.0,
            });
        }
        this.updateCounters(placeholders);
    }

    updateCounters(cashiersStatus) {
        if (!this.grid || !cashiersStatus) return;

        this.grid.innerHTML = cashiersStatus.map(c => {
            const fatiguePct = Math.min(100, Math.round(c.peak_fatigue * 100));
            return `
                <div class="till-card">
                    <div class="till-header">
                        <span class="till-number">Counter #${c.counter_id}</span>
                        <span class="till-experience">${c.experience}</span>
                    </div>
                    <div class="till-cashier">${c.name}</div>
                    <div class="till-metrics-row">
                        <span>Items Scanned</span>
                        <span>${c.tx_processed}</span>
                    </div>
                    <div class="till-metrics-row">
                        <span>Errors Incurred</span>
                        <span>${c.errors}</span>
                    </div>
                    <div class="fatigue-section">
                        <div class="fatigue-label-row">
                            <span>Fatigue Level</span>
                            <span>${fatiguePct}%</span>
                        </div>
                        <div class="fatigue-meter-track">
                            <div class="fatigue-meter-fill" style="width: ${fatiguePct}%;"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
}
