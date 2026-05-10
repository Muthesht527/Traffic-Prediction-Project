from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from data_preprocessing import prepare_features
except ModuleNotFoundError:
    from src.data_preprocessing import prepare_features

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "traffic_speed_model.pkl"


class TrafficSpeedPredictor:
    def __init__(self, model_path: str | Path = MODEL_PATH) -> None:
        self.model_path = Path(model_path)
        self.pipeline = None
        self.feature_columns: list[str] = []
        self._load()

    def _load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {self.model_path}. Run train_model.py first."
            )

        with self.model_path.open("rb") as model_file:
            artifact = pickle.load(model_file)

        self.pipeline = artifact["pipeline"]
        self.feature_columns = artifact["feature_columns"]

    def _normalize_input(self, payload: dict[str, Any] | list[dict[str, Any]]) -> pd.DataFrame:
        if isinstance(payload, dict):
            rows = [payload]
        elif isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
            rows = payload
        else:
            raise ValueError("Input payload must be a JSON object or a list of JSON objects.")

        inference_frame = pd.DataFrame(rows)
        return prepare_features(inference_frame)

    def predict(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, float]]:
        if self.pipeline is None:
            raise RuntimeError("Prediction pipeline is not loaded.")

        features = self._normalize_input(payload)
        predictions = self.pipeline.predict(features)
        return [
            {"predicted_traffic_speed_kmh": round(float(prediction), 2)}
            for prediction in predictions
        ]


def predict_traffic_speed(payload: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, float]]:
    predictor = TrafficSpeedPredictor()
    return predictor.predict(payload)
