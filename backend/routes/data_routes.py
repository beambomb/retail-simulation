import os
import json
from flask import Blueprint, jsonify, send_from_directory

data_bp = Blueprint("data_bp", __name__)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw"))


@data_bp.route("/api/metrics", methods=["GET"])
def get_metrics():
    metrics_path = os.path.join(DATA_DIR, "simulation_metrics.json")
    if not os.path.exists(metrics_path):
        return jsonify({"status": "empty", "message": "No simulation run yet"}), 404
    with open(metrics_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@data_bp.route("/api/download/<filename>", methods=["GET"])
def download_file(filename):
    allowed_files = [
        "pos_transactions.csv",
        "pos_transaction_items.csv",
        "cashier_shifts.csv",
        "inventory_catalog.csv",
        "simulation_metrics.json",
    ]
    if filename not in allowed_files:
        return jsonify({"error": "File not permitted"}), 403
    return send_from_directory(DATA_DIR, filename, as_attachment=True)
