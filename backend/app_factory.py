import os
from flask import Flask, render_template
from .routes import simulation_bp, catalog_bp, data_bp


def create_app() -> Flask:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_dir = os.path.join(base_dir, "frontend", "templates")
    static_dir = os.path.join(base_dir, "frontend", "static")

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )

    app.register_blueprint(simulation_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(data_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
