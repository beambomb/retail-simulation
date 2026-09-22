class ModalManager {
    constructor() {
        this.modal = document.getElementById('item-modal');
        this.closeBtn = document.getElementById('modal-close');
        this.tbody = document.getElementById('modal-items-tbody');
        this.title = document.getElementById('modal-title');
        this.bindEvents();
    }

    bindEvents() {
        this.closeBtn.addEventListener('click', () => this.close());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });
    }

    show(transaction) {
        if (!transaction) return;
        this.title.textContent = `Transaction ${transaction.transaction_id} Details`;
        this.tbody.innerHTML = transaction.items.map(it => `
            <tr>
                <td class="mono">${it.sku}</td>
                <td>${it.name}</td>
                <td class="mono">${it.qty}</td>
                <td class="mono">Rp ${Number(it.price).toLocaleString('id-ID')}</td>
                <td class="mono">Rp ${Number(it.qty * it.price).toLocaleString('id-ID')}</td>
                <td>${it.is_void ? 'VOIDED' : 'VALID'}</td>
                <td>${it.error}</td>
            </tr>
        `).join('');
        this.modal.classList.remove('hidden');
    }

    close() {
        this.modal.classList.add('hidden');
    }
}
