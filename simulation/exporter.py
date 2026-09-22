import os
import csv
import json
from typing import List, Dict, Any
from .models import Transaction, ShiftLog, Product


class DataExporter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_all(
        self,
        transactions: List[Transaction],
        shift_logs: List[ShiftLog],
        catalog_products: List[Product],
        metrics: Dict[str, Any],
    ) -> Dict[str, str]:
        tx_path = self.export_transactions(transactions)
        items_path = self.export_transaction_items(transactions)
        shifts_path = self.export_shifts(shift_logs)
        cat_path = self.export_catalog(catalog_products)
        metrics_path = self.export_metrics(metrics)
        return {
            "transactions": tx_path,
            "transaction_items": items_path,
            "cashier_shifts": shifts_path,
            "inventory_catalog": cat_path,
            "metrics": metrics_path,
        }

    def export_transactions(self, transactions: List[Transaction]) -> str:
        filepath = os.path.join(self.output_dir, "pos_transactions.csv")
        fieldnames = [
            "transaction_id",
            "store_id",
            "cashier_id",
            "customer_id",
            "timestamp",
            "payment_method",
            "total_amount",
            "item_count",
            "has_error",
        ]
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for tx in transactions:
                writer.writerow(
                    {
                        "transaction_id": tx.transaction_id,
                        "store_id": tx.store_id,
                        "cashier_id": tx.cashier_id,
                        "customer_id": tx.customer_id,
                        "timestamp": tx.timestamp,
                        "payment_method": tx.payment_method.value,
                        "total_amount": round(tx.total_amount, 2),
                        "item_count": tx.item_count,
                        "has_error": tx.has_error,
                    }
                )
        return filepath

    def export_transaction_items(self, transactions: List[Transaction]) -> str:
        filepath = os.path.join(self.output_dir, "pos_transaction_items.csv")
        fieldnames = [
            "item_id",
            "transaction_id",
            "sequence",
            "sku",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
            "discount_applied",
            "is_void",
            "error_type",
        ]
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for tx in transactions:
                for it in tx.items:
                    writer.writerow(
                        {
                            "item_id": it.item_id,
                            "transaction_id": it.transaction_id,
                            "sequence": it.sequence,
                            "sku": it.sku,
                            "product_name": it.product_name,
                            "quantity": it.quantity,
                            "unit_price": round(it.unit_price, 2),
                            "subtotal": round(it.subtotal, 2),
                            "discount_applied": round(it.discount_applied, 2),
                            "is_void": it.is_void,
                            "error_type": it.error_type.value,
                        }
                    )
        return filepath

    def export_shifts(self, shift_logs: List[ShiftLog]) -> str:
        filepath = os.path.join(self.output_dir, "cashier_shifts.csv")
        fieldnames = [
            "shift_id",
            "cashier_id",
            "counter_id",
            "date",
            "shift_type",
            "transactions_processed",
            "errors_occurred",
            "peak_fatigue",
        ]
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in shift_logs:
                writer.writerow(
                    {
                        "shift_id": s.shift_id,
                        "cashier_id": s.cashier_id,
                        "counter_id": s.counter_id,
                        "date": s.date,
                        "shift_type": s.shift_type.value,
                        "transactions_processed": s.transactions_processed,
                        "errors_occurred": s.errors_occurred,
                        "peak_fatigue": round(s.peak_fatigue, 3),
                    }
                )
        return filepath

    def export_catalog(self, products: List[Product]) -> str:
        filepath = os.path.join(self.output_dir, "inventory_catalog.csv")
        fieldnames = ["sku", "barcode", "name", "category", "cost_price", "sell_price", "stock"]
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in products:
                writer.writerow(
                    {
                        "sku": p.sku,
                        "barcode": p.barcode,
                        "name": p.name,
                        "category": p.category,
                        "cost_price": round(p.cost_price, 2),
                        "sell_price": round(p.sell_price, 2),
                        "stock": p.stock,
                    }
                )
        return filepath

    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, "simulation_metrics.json")
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        return filepath
