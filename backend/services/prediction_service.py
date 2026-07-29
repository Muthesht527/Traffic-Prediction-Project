"""Prediction service — orchestrates feature engineering → ML → scoring.

Uses the regressor model (preferred) or falls back to the classifier.
Returns a congestion score (0–100) plus metadata.
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
            "class_probabilities": {"High": 0.62, "Low": 0.05, "Medium": 0.33},
            "prediction_timestamp": "2024-03-01T08:30:00",
            "model": "regressor",
            "features_used": { … }
        }
    """
    loader = ModelLoader()

    # Build raw features (14 columns matching training data)
    raw_features_df = build_features(origin, destination, target_dt, route, weather)

    # Use existing preprocessing to extract hour, day_of_week from Timestamp
    preprocessed_df = prepare_features(raw_features_df)

    log.info("Features prepared — shape: %s", preprocessed_df.shape)

    # Get prediction from the best available model
    result = loader.predict_score(preprocessed_df)

    log.info(
        "Prediction: model=%s condition=%s score=%.1f",
        result["model"],
        result["predicted_condition"],
        result["congestion_score"],
    )

    return {
        "congestion_score": result["congestion_score"],
        "predicted_condition": result["predicted_condition"],
        "class_probabilities": result["class_probabilities"],
        "prediction_timestamp": target_dt.isoformat(),
        "model": result["model"],
        "features_used": raw_features_df.iloc[0].to_dict(),
    }
