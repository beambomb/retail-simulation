class TableManager {
    constructor(onInspectCallback) {
        this.tbody = document.getElementById('transactions-tbody');
        this.search = document.getElementById('tx-search');
        this.filter = document.getElementById('error-filter');
        this.onInspect = onInspectCallback;
        this.transactions = [];
        this.bindEvents();
    }

    bindEvents() {
        this.search.addEventListener('input', () => this.render());
        this.filter.addEventListener('change', () => this.render());
    }

    setTransactions(transactions) {
        this.transactions = transactions || [];
        this.render();
    }

    render() {
        const query = this.search.value.toLowerCase().trim();
        const filterVal = this.filter.value;

        const filtered = this.transactions.filter(tx => {
            const matchesQuery = !query || 
                tx.transaction_id.toLowerCase().includes(query) ||
                tx.cashier_id.toLowerCase().includes(query) ||
                tx.customer_id.toLowerCase().includes(query);

            const matchesFilter = 
                filterVal === 'ALL' ||
                (filterVal === 'ERROR_ONLY' && tx.has_error) ||
                (filterVal === 'CLEAN_ONLY' && !tx.has_error);

            return matchesQuery && matchesFilter;
        });

        if (filtered.length === 0) {
            this.tbody.innerHTML = `<tr><td colspan="9" class="empty-state">No matching transactions found.</td></tr>`;
            return;
        }

        this.tbody.innerHTML = filtered.map((tx, idx) => `
            <tr>
                <td class="mono">${tx.transaction_id}</td>
                <td>${tx.timestamp}</td>
                <td class="mono">${tx.cashier_id}</td>
                <td class="mono">${tx.customer_id}</td>
                <td>${tx.payment_method}</td>
                <td class="mono">${tx.item_count}</td>
                <td class="mono">Rp ${Number(tx.total_amount).toLocaleString('id-ID')}</td>
                <td>${tx.has_error ? 'ANOMALY DETECTED' : 'CLEAN'}</td>
                <td><button class="btn btn-secondary btn-sm" onclick="app.inspectByIndex(${idx})">Inspect</button></td>
            </tr>
        `).join('');
    }
}
