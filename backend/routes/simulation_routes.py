import os
from flask import Blueprint, request, jsonify
from simulation.domain import SimulationConfig
from simulation.engine import SimulationEngine
from simulation.exporter import DataExporter

simulation_bp = Blueprint("simulation_bp", __name__)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw"))
exporter = DataExporter(DATA_DIR)


@simulation_bp.route("/api/simulate", methods=["POST"])
def run_simulation():
    body = request.get_json() or {}
    try:
        config = SimulationConfig(
            days=int(body.get("days", 7)),
            customers_per_day=int(body.get("customers_per_day", 120)),
            cashier_count=int(body.get("cashier_count", 4)),
            error_multiplier=float(body.get("error_multiplier", 1.0)),
            fatigue_sensitivity=float(body.get("fatigue_sensitivity", 1.0)),
            enable_seasonality=bool(body.get("enable_seasonality", True)),
            junior_cashier_ratio=float(body.get("junior_cashier_ratio", 0.5)),
            quick_grab_ratio=float(body.get("quick_grab_ratio", 0.35)),
            family_stocker_ratio=float(body.get("family_stocker_ratio", 0.25)),
            budget_hunter_ratio=float(body.get("budget_hunter_ratio", 0.25)),
            impulse_buyer_ratio=float(body.get("impulse_buyer_ratio", 0.15)),
        )

        engine = SimulationEngine(config)
        results = engine.run()
        exporter.export_all(
            results["transactions"],
            results["shift_logs"],
            results["catalog"],
            results["metrics"],
        )

        sample_transactions = []
        for t in results["transactions"][-30:]:
            sample_transactions.append(
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
            )

        return jsonify(
            {
                "status": "success",
                "metrics": results["metrics"],
                "daily_frames": results["daily_frames"],
                "sample_transactions": sample_transactions,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
