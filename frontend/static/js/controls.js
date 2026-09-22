class ControlsManager {
    constructor() {
        this.days = document.getElementById('param-days');
        this.daysVal = document.getElementById('val-days');
        this.customers = document.getElementById('param-customers');
        this.customersVal = document.getElementById('val-customers');
        this.seasonality = document.getElementById('param-seasonality');

        this.quickGrab = document.getElementById('param-quick-grab');
        this.quickGrabVal = document.getElementById('val-quick-grab');
        this.family = document.getElementById('param-family');
        this.familyVal = document.getElementById('val-family');
        this.budget = document.getElementById('param-budget');
        this.budgetVal = document.getElementById('val-budget');
        this.impulse = document.getElementById('param-impulse');
        this.impulseVal = document.getElementById('val-impulse');

        this.cashiers = document.getElementById('param-cashiers');
        this.cashiersVal = document.getElementById('val-cashiers');
        this.juniorRatio = document.getElementById('param-junior-ratio');
        this.juniorRatioVal = document.getElementById('val-junior-ratio');
        this.fatigue = document.getElementById('param-fatigue');
        this.fatigueVal = document.getElementById('val-fatigue');
        this.errorMult = document.getElementById('param-error-mult');
        this.errorMultVal = document.getElementById('val-error-mult');

        this.bindEvents();
    }

    bindEvents() {
        this.bind(this.days, this.daysVal, v => `${v} Days`);
        this.bind(this.customers, this.customersVal, v => `${v}`);
        this.bind(this.quickGrab, this.quickGrabVal, v => `${v}%`);
        this.bind(this.family, this.familyVal, v => `${v}%`);
        this.bind(this.budget, this.budgetVal, v => `${v}%`);
        this.bind(this.impulse, this.impulseVal, v => `${v}%`);
        this.bind(this.cashiers, this.cashiersVal, v => `${v} Staff`);
        this.bind(this.juniorRatio, this.juniorRatioVal, v => `${v}%`);
        this.bind(this.fatigue, this.fatigueVal, v => `${parseFloat(v).toFixed(1)}x`);
        this.bind(this.errorMult, this.errorMultVal, v => `${parseFloat(v).toFixed(1)}x`);
    }

    bind(input, label, formatter) {
        input.addEventListener('input', e => {
            label.textContent = formatter(e.target.value);
        });
    }

    getPayload() {
        return {
            days: parseInt(this.days.value, 10),
            customers_per_day: parseInt(this.customers.value, 10),
            enable_seasonality: this.seasonality.checked,
            quick_grab_ratio: parseInt(this.quickGrab.value, 10) / 100,
            family_stocker_ratio: parseInt(this.family.value, 10) / 100,
            budget_hunter_ratio: parseInt(this.budget.value, 10) / 100,
            impulse_buyer_ratio: parseInt(this.impulse.value, 10) / 100,
            cashier_count: parseInt(this.cashiers.value, 10),
            junior_cashier_ratio: parseInt(this.juniorRatio.value, 10) / 100,
            fatigue_sensitivity: parseFloat(this.fatigue.value),
            error_multiplier: parseFloat(this.errorMult.value),
        };
    }
}
