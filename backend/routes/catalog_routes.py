from flask import Blueprint, jsonify
from simulation.catalog import CatalogRepository

catalog_bp = Blueprint("catalog_bp", __name__)


@catalog_bp.route("/api/catalog", methods=["GET"])
def get_catalog():
    repo = CatalogRepository()
    products = repo.get_all()
    return jsonify([p.__dict__ for p in products])
