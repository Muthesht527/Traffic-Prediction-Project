"""Prediction service — runs the trained Random Forest and converts the
categorical output (High / Medium / Low) into a continuous congestion score
(0–100).
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Add src/ to path so we can reuse the existing preprocessing module
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from data_preprocessing import prepare_features

from backend.model.model_loader import ModelLoader
from backend.services.feature_engineering import build_features
from backend.utils.logger import get_logger

log = get_logger("prediction")

# Score anchors per class — the probability-weighted score falls between these
_SCORE_ANCHORS: dict[str, float] = {
    "Low": 10.0,
    "Medium": 55.0,
    "High": 85.0,
}


def _score_from_probabilities(
    classes: list[str], probabilities: list[float]
) -> float:
    """Compute a 0-100 congestion score from class probabilities.

    Weighted average using anchor values keyed by class label.
    """
    score = 0.0
    for cls, prob in zip(classes, probabilities):
        anchor = _SCORE_ANCHORS.get(cls, 50.0)
        score += anchor * prob
    return round(max(0.0, min(100.0, score)), 1)


def predict_congestion(
    origin: tuple[float, float],
    destination: tuple[float, float],
    target_dt: datetime,
    route: dict,
    weather: dict,
) -> dict:
    """Run the full prediction pipeline.

    Returns::

        {
            "congestion_score": 72.3,
            "predicted_condition": "High",
            "class_probabilities": {"High": 0.82, "Low": 0.05, "Medium": 0.13},
            "prediction_timestamp": "2024-03-01T08:30:00",
            "features_used": { … }
        }
    """
    loader = ModelLoader()

    # Build raw features (14 columns matching training data)
    raw_features_df = build_features(origin, destination, target_dt, route, weather)

    # Use existing preprocessing to extract hour, day_of_week from Timestamp
    # and select the correct model feature columns
    preprocessed_df = prepare_features(raw_features_df)

    log.info("Preprocessed features shape: %s", preprocessed_df.shape)

    # Predict
    encoded_preds = loader.pipeline.predict(preprocessed_df)
    predicted_label = loader.target_encoder.inverse_transform(encoded_preds)[0]

    # Probabilities
    probabilities_dict: dict[str, float] = {}
    if hasattr(loader.pipeline, "predict_proba"):
        probs = loader.pipeline.predict_proba(preprocessed_df)[0]
        classes = loader.target_encoder.classes_
        probabilities_dict = {
            cls: round(float(p), 4) for cls, p in zip(classes, probs)
        }
        score = _score_from_probabilities(list(classes), list(probs))
    else:
        # Fallback if model lacks predict_proba
        anchor = _SCORE_ANCHORS.get(predicted_label, 50.0)
        score = anchor
        probabilities_dict = {predicted_label: 1.0}

    log.info(
        "Prediction: condition=%s score=%.1f probs=%s",
        predicted_label,
        score,
        probabilities_dict,
    )

    return {
        "congestion_score": score,
        "predicted_condition": predicted_label,
        "class_probabilities": probabilities_dict,
        "prediction_timestamp": target_dt.isoformat(),
        "features_used": raw_features_df.iloc[0].to_dict(),
    }
