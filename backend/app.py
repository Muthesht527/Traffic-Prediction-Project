"""Flask application entry point for the Traffic Forecast platform."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so ``backend.*`` imports work
# regardless of how the app is launched.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from flask import Flask

from backend.api.routes import bp as api_bp
from backend.config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from backend.utils.logger import get_logger

log = get_logger("app")


def create_app() -> Flask:
    """Application factory."""
    app = Flask(
        __name__,
        static_folder=None,
    )
    app.register_blueprint(api_bp)

    @app.get("/")
    def root():
        return {
            "service": "Traffic Forecast API",
            "version": "1.0.0",
            "endpoints": ["/api/health", "/api/forecast", "/api/geocode", "/api/coverage"],
        }

    return app


if __name__ == "__main__":
    log.info("Starting Traffic Forecast backend …")
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
