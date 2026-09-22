import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .models import (
    SimulationConfig,
    Customer,
    Cashier,
    Transaction,
    TransactionItem,
    ShiftLog,
    ShiftType,
    PaymentMethod,
    PersonaType,
    ErrorCategory,
)
from .catalog import CatalogRepository
from .strategies import StrategyFactory, CashierErrorEngine
from .factories import CustomerFactory, CashierFactory


class SimulationEngine:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.catalog = CatalogRepository()
        self.error_engine = CashierErrorEngine()
        self.cashiers = CashierFactory.create_cashiers(
            config.cashier_count, config.junior_cashier_ratio
        )
        self.transactions: List[Transaction] = []
        self.shift_logs: List[ShiftLog] = []
        self.customer_abandonments = 0
        self.double_scan_count = 0
        self.typo_sku_count = 0
        self.void_count = 0

    def run(self) -> Dict[str, Any]:
        start_date = datetime(2026, 9, 1, 8, 0, 0)
        customer_seq = 1
        tx_seq = 1
        daily_summaries: List[Dict[str, Any]] = []

        for day_idx in range(self.config.days):
            current_date = start_date + timedelta(days=day_idx)
            day_transactions: List[Transaction] = []
            day_abandonments = 0
            is_weekend = current_date.weekday() >= 5
            is_payday = current_date.day >= 25 or current_date.day <= 2

            traffic_multiplier = 1.0
            if self.config.enable_seasonality:
                if is_weekend:
                    traffic_multiplier *= 1.35
                if is_payday:
                    traffic_multiplier *= 1.25

            target_customers = int(self.config.customers_per_day * traffic_multiplier)

            morning_cashiers = [c for c in self.cashiers if c.shift == ShiftType.MORNING]
            evening_cashiers = [c for c in self.cashiers if c.shift == ShiftType.EVENING]

            for c in self.cashiers:
                c.fatigue = 0.0

            shift_stats: Dict[str, Dict[str, Any]] = {
                c.cashier_id: {"tx_count": 0, "errors": 0, "peak_fatigue": 0.0}
                for c in self.cashiers
            }

            hours = list(range(8, 22))
            hour_weights = [
                0.03, 0.04, 0.06, 0.08,
                0.12, 0.10, 0.05, 0.06,
                0.09, 0.13, 0.12, 0.06,
                0.04, 0.02
            ]

            hourly_distribution = random.choices(hours, weights=hour_weights, k=target_customers)
            hourly_distribution.sort()

            active_queues: Dict[int, int] = {i: 0 for i in range(1, 5)}

            for hour in hourly_distribution:
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                tx_time = current_date.replace(hour=hour, minute=minute, second=second)

                customer = CustomerFactory.create_customer(customer_seq, self.config)
                customer_seq += 1

                min_queue_counter = min(active_queues, key=active_queues.get)
                current_queue_len = active_queues[min_queue_counter]

                if current_queue_len > customer.patience_threshold:
                    day_abandonments += 1
                    self.customer_abandonments += 1
                    continue

                active_queues[min_queue_counter] += 1

                active_shift = ShiftType.MORNING if hour < 15 else ShiftType.EVENING
                pool = morning_cashiers if active_shift == ShiftType.MORNING else evening_cashiers
                if not pool:
                    pool = self.cashiers
                cashier = random.choice(pool)

                elapsed_hours = (hour - 8) if active_shift == ShiftType.MORNING else (hour - 15)
                fatigue_increment = (0.015 * self.config.fatigue_sensitivity) + (current_queue_len * 0.005)
                cashier.fatigue = min(1.0, (elapsed_hours * 0.08 * self.config.fatigue_sensitivity) + (shift_stats[cashier.cashier_id]["tx_count"] * fatigue_increment))
                if cashier.fatigue > shift_stats[cashier.cashier_id]["peak_fatigue"]:
                    shift_stats[cashier.cashier_id]["peak_fatigue"] = cashier.fatigue

                strategy = StrategyFactory.get_shopping_strategy(customer.persona)
                raw_items = strategy.select_items(customer, self.catalog)

                if not raw_items:
                    active_queues[min_queue_counter] = max(0, active_queues[min_queue_counter] - 1)
                    continue

                tx_id = f"TRX-{tx_time.strftime('%Y%m%d')}-{tx_seq:06d}"
                tx_seq += 1

                tx_items: List[TransactionItem] = []
                item_sequence = 1
                tx_has_error = False

                for product, qty in raw_items:
                    base_item = TransactionItem(
                        item_id=f"{tx_id}-{item_sequence:03d}",
                        transaction_id=tx_id,
                        sequence=item_sequence,
                        sku=product.sku,
                        product_name=product.name,
                        quantity=qty,
                        unit_price=product.sell_price,
                        subtotal=product.sell_price * qty,
                        discount_applied=0.0,
                        is_void=False,
                        error_type=ErrorCategory.NONE,
                    )
                    processed_items = self.error_engine.process_item(
                        cashier, customer, base_item, self.catalog, self.config.error_multiplier
                    )

                    for p_it in processed_items:
                        if p_it.error_type != ErrorCategory.NONE:
                            tx_has_error = True
                            shift_stats[cashier.cashier_id]["errors"] += 1
                            if p_it.error_type == ErrorCategory.DOUBLE_SCAN:
                                self.double_scan_count += 1
                            elif p_it.error_type == ErrorCategory.TYPO_SKU:
                                self.typo_sku_count += 1
                            elif p_it.error_type == ErrorCategory.VOID_ITEM:
                                self.void_count += 1

                        tx_items.append(p_it)
                        item_sequence += 1

                payment_method = random.choices(
                    [PaymentMethod.QRIS, PaymentMethod.CASH, PaymentMethod.DEBIT, PaymentMethod.CREDIT],
                    weights=[0.45, 0.30, 0.18, 0.07],
                )[0]

                active_items = [it for it in tx_items if not it.is_void]
                total_val = sum(it.subtotal for it in active_items)

                tx = Transaction(
                    transaction_id=tx_id,
                    store_id="STR-001",
                    cashier_id=cashier.cashier_id,
                    customer_id=customer.customer_id,
                    timestamp=tx_time.strftime("%Y-%m-%d %H:%M:%S"),
                    payment_method=payment_method,
                    total_amount=total_val,
                    item_count=len(active_items),
                    has_error=tx_has_error,
                    items=tx_items,
                )

                self.error_engine.resolve_payment_and_loyalty(
                    cashier, customer, tx, self.config.error_multiplier
                )

                shift_stats[cashier.cashier_id]["tx_count"] += 1
                day_transactions.append(tx)
                self.transactions.append(tx)

                active_queues[min_queue_counter] = max(0, active_queues[min_queue_counter] - 1)

            for c in self.cashiers:
                s_stat = shift_stats[c.cashier_id]
                self.shift_logs.append(
                    ShiftLog(
                        shift_id=f"SHF-{current_date.strftime('%Y%m%d')}-{c.cashier_id}",
                        cashier_id=c.cashier_id,
                        counter_id=c.counter_id,
                        date=current_date.strftime("%Y-%m-%d"),
                        shift_type=c.shift,
                        transactions_processed=s_stat["tx_count"],
                        errors_occurred=s_stat["errors"],
                        peak_fatigue=s_stat["peak_fatigue"],
                    )
                )

            daily_revenue = sum(t.total_amount for t in day_transactions)
            daily_errors = sum(1 for t in day_transactions if t.has_error)
            daily_items = sum(t.item_count for t in day_transactions)

            cashiers_status = [
                {
                    "cashier_id": c.cashier_id,
                    "name": c.name,
                    "counter_id": c.counter_id,
                    "experience": c.experience.value,
                    "shift": c.shift.value,
                    "tx_processed": shift_stats[c.cashier_id]["tx_count"],
                    "errors": shift_stats[c.cashier_id]["errors"],
                    "peak_fatigue": round(shift_stats[c.cashier_id]["peak_fatigue"], 3),
                }
                for c in self.cashiers
            ]

            day_summary = {
                "day_number": day_idx + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "is_weekend": is_weekend,
                "is_payday": is_payday,
                "revenue": daily_revenue,
                "transactions": len(day_transactions),
                "items": daily_items,
                "errors": daily_errors,
                "abandonments": day_abandonments,
                "cashiers_status": cashiers_status,
                "sample_transactions": [
                    {
                        "transaction_id": t.transaction_id,
                        "timestamp": t.timestamp,
                        "cashier_id": t.cashier_id,
                        "customer_id": t.customer_id,
                        "payment_method": t.payment_method.value,
                        "total_amount": t.total_amount,
                        "item_count": t.item_count,
                        "has_error": t.has_error,
                        "items": [
                            {
                                "sku": it.sku,
                                "name": it.product_name,
                                "qty": it.quantity,
                                "price": it.unit_price,
                                "is_void": it.is_void,
                                "error": it.error_type.value,
                            }
                            for it in t.items
                        ],
                    }
                    for t in day_transactions[-6:]
                ],
            }
            daily_summaries.append(day_summary)

        total_rev = sum(t.total_amount for t in self.transactions)
        total_items = sum(t.item_count for t in self.transactions)
        total_tx = len(self.transactions)
        error_tx_count = sum(1 for t in self.transactions if t.has_error)

        metrics = {
            "total_revenue": total_rev,
            "total_transactions": total_tx,
            "total_items_sold": total_items,
            "error_transactions": error_tx_count,
            "error_rate_pct": round((error_tx_count / total_tx * 100) if total_tx > 0 else 0.0, 2),
            "double_scan_count": self.double_scan_count,
            "typo_sku_count": self.typo_sku_count,
            "void_count": self.void_count,
            "customer_abandonments": self.customer_abandonments,
            "average_basket_value": round((total_rev / total_tx) if total_tx > 0 else 0.0, 2),
            "daily_summaries": daily_summaries,
            "daily_frames": daily_summaries,
        }

        return {
            "transactions": self.transactions,
            "shift_logs": self.shift_logs,
            "catalog": self.catalog.get_all(),
            "metrics": metrics,
            "daily_frames": daily_summaries,
        }
