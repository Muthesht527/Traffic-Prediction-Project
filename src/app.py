from __future__ import annotations

from flask import Flask, jsonify, render_template, request

try:
    from predict import TrafficCongestionPredictor
except ModuleNotFoundError:
    from src.predict import TrafficCongestionPredictor

app = Flask(__name__)
predictor = TrafficCongestionPredictor()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        instances = payload.get("instances", payload) if isinstance(payload, dict) else payload
        predictions = predictor.predict(instances)
        return jsonify({"predictions": predictions}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": f"Unexpected server error: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
