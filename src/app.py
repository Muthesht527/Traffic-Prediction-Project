from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

try:
    from predict import TrafficSpeedPredictor
except ModuleNotFoundError:
    from src.predict import TrafficSpeedPredictor

try:
    from data_preprocessing import RAW_FEATURE_COLUMNS, load_dataset
except ModuleNotFoundError:
    from src.data_preprocessing import RAW_FEATURE_COLUMNS, load_dataset

app = Flask(__name__)
predictor = TrafficSpeedPredictor()
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "smart_mobility_dataset.csv"


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.get("/traffic-data")
def traffic_data():
    try:
        dataset = load_dataset(DATASET_PATH)
        records = []
        for index, row in dataset.iterrows():
            records.append(
                {
                    "index": int(index),
                    "timestamp": row["Timestamp"],
                    "latitude": float(row["Latitude"]),
                    "longitude": float(row["Longitude"]),
                    "vehicle_count": float(row["Vehicle_Count"]),
                    "road_occupancy": float(row["Road_Occupancy_%"]),
                    "traffic_light_state": row["Traffic_Light_State"],
                    "weather_condition": row["Weather_Condition"],
                    "accident_report": float(row["Accident_Report"]),
                    "traffic_speed_kmh": float(row["Traffic_Speed_kmh"]),
                }
            )
        return jsonify({"records": records}), 200
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception as exc:
        return jsonify({"error": f"Unable to load traffic data: {exc}"}), 500


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
    except Exception as exc:
        return jsonify({"error": f"Unexpected server error: {exc}"}), 500


@app.post("/prediction-line")
def prediction_line():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        dataset = load_dataset(DATASET_PATH)
        min_vehicle_count = int(dataset["Vehicle_Count"].min())
        max_vehicle_count = int(dataset["Vehicle_Count"].max())
        step = max((max_vehicle_count - min_vehicle_count) // 40, 1)

        missing_fields = sorted(set(RAW_FEATURE_COLUMNS) - set(payload))
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        instances = []
        for vehicle_count in range(min_vehicle_count, max_vehicle_count + 1, step):
            instance = {column: payload[column] for column in RAW_FEATURE_COLUMNS}
            instance["Vehicle_Count"] = vehicle_count
            instances.append(instance)

        predictions = predictor.predict(instances)
        points = [
            {
                "vehicle_count": instance["Vehicle_Count"],
                "predicted_traffic_speed_kmh": prediction["predicted_traffic_speed_kmh"],
            }
            for instance, prediction in zip(instances, predictions)
        ]
        return jsonify({"points": points}), 200
    except KeyError as exc:
        return jsonify({"error": f"Missing required field: {exc}"}), 400
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Unable to build prediction line: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
