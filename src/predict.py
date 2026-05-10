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
MODEL_PATH = BASE_DIR / "model" / "traffic_congestion_model.pkl"


class TrafficCongestionPredictor:
    def __init__(self, model_path: str | Path = MODEL_PATH) -> None:
        self.model_path = Path(model_path)
        self.pipeline = None
        self.target_encoder = None
        self.raw_feature_columns: list[str] = []
        self._load()

    def _load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {self.model_path}. Run train_model.py first."
            )

        with self.model_path.open("rb") as model_file:
            artifact = pickle.load(model_file)

        self.pipeline = artifact["pipeline"]
        self.target_encoder = artifact["target_encoder"]
        self.raw_feature_columns = artifact["raw_feature_columns"]

    def _normalize_input(self, payload: dict[str, Any] | list[dict[str, Any]]) -> pd.DataFrame:
        if isinstance(payload, dict):
            rows = [payload]
        elif isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
            rows = payload
        else:
            raise ValueError("Input payload must be a JSON object or a list of JSON objects.")

        inference_frame = pd.DataFrame(rows)
        features = prepare_features(inference_frame)
        return features

    def predict(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self.pipeline is None or self.target_encoder is None:
            raise RuntimeError("Prediction pipeline is not loaded.")

        features = self._normalize_input(payload)
        encoded_predictions = self.pipeline.predict(features)
        decoded_predictions = self.target_encoder.inverse_transform(encoded_predictions)

        prediction_rows: list[dict[str, Any]] = []
        probabilities = None
        if hasattr(self.pipeline, "predict_proba"):
            probabilities = self.pipeline.predict_proba(features)

        for index, predicted_label in enumerate(decoded_predictions):
            response_row: dict[str, Any] = {
                "predicted_traffic_condition": predicted_label,
            }
            if probabilities is not None:
                class_probabilities = {
                    label: float(probabilities[index][class_index])
                    for class_index, label in enumerate(self.target_encoder.classes_)
                }
                response_row["class_probabilities"] = class_probabilities
            prediction_rows.append(response_row)

        return prediction_rows


def predict_traffic(payload: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    predictor = TrafficCongestionPredictor()
    return predictor.predict(payload)
