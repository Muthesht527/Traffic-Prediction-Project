"""Load the trained ML models and expose a unified prediction interface.

Supports both:
1. Classifier — categorical (High/Medium/Low) with probability-based scoring
2. Regressor — directly predicts a 0-100 congestion score (preferred)
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from backend.config import MODEL_PATH, MODEL_DIR
from backend.utils.logger import get_logger

log = get_logger("model-loader")

_REGRESSOR_PATH = MODEL_DIR / "congestion_regressor.pkl"


class ModelLoader:
    """Singleton that loads both classifier and regressor models."""

    _instance: ModelLoader | None = None

    def __new__(cls) -> ModelLoader:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def __init__(self) -> None:
        if self._loaded:
            return
        # ── Classifier ───────────────────────────────────────────────
        self.classifier_pipeline = None
        self.target_encoder = None
        self.raw_feature_columns: list[str] = []
        self.model_feature_columns: list[str] = []
        self.target_column: str = ""

        # ── Regressor ────────────────────────────────────────────────
        self.regressor_pipeline = None
        self.regressor_feature_names: list[str] = []
        self.feature_importances: dict[str, float] = {}

        self._load()
        self._loaded = True

    def _load(self) -> None:
        # Load classifier
        classifier_path = Path(MODEL_PATH)
        if classifier_path.exists():
            with classifier_path.open("rb") as fh:
                artifact: dict[str, Any] = pickle.load(fh)
            self.classifier_pipeline = artifact["pipeline"]
            self.target_encoder = artifact["target_encoder"]
            self.raw_feature_columns = artifact["raw_feature_columns"]
            self.model_feature_columns = artifact["model_feature_columns"]
            self.target_column = artifact["target_column"]
            log.info(
                "Classifier loaded — classes: %s",
                list(self.target_encoder.classes_),
            )
        else:
            log.warning("Classifier model not found at %s", classifier_path)

        # Load regressor
        regressor_path = Path(_REGRESSOR_PATH)
        if regressor_path.exists():
            with regressor_path.open("rb") as fh:
                reg_artifact: dict[str, Any] = pickle.load(fh)
            self.regressor_pipeline = reg_artifact["pipeline"]
            self.regressor_feature_names = reg_artifact["feature_names"]
            self.feature_importances = reg_artifact["importances"]
            log.info("Regressor loaded — R² model ready")
        else:
            log.warning("Regressor model not found at %s", regressor_path)

    # ── Public helpers ─────────────────────────────────────────────────

    def get_classes(self) -> list[str]:
        """Return the human-readable target labels (classifier)."""
        if self.target_encoder is None:
            return []
        return list(self.target_encoder.classes_)

    def has_regressor(self) -> bool:
        return self.regressor_pipeline is not None

    def has_classifier(self) -> bool:
        return self.classifier_pipeline is not None

    def predict_score(self, features_df) -> dict:
        """Predict congestion score using the best available model.

        Returns::

            {
                "congestion_score": float,
                "predicted_condition": str | None,
                "class_probabilities": dict,
                "model": "regressor" | "classifier"
            }
        """
        if self.has_regressor():
            score = float(self.regressor_pipeline.predict(features_df)[0])
            score = round(max(0.0, min(100.0, score)), 1)

            # Derive condition label from score
            if score <= 20:
                condition = "Low"
            elif score <= 40:
                condition = "Low"
            elif score <= 70:
                condition = "Medium"
            else:
                condition = "High"

            # Build approximate probabilities from score
            probs = _score_to_probabilities(score)

            return {
                "congestion_score": score,
                "predicted_condition": condition,
                "class_probabilities": probs,
                "model": "regressor",
            }
        elif self.has_classifier():
            # Fallback to classifier
            encoded_preds = self.classifier_pipeline.predict(features_df)
            label = self.target_encoder.inverse_transform(encoded_preds)[0]

            probs = {}
            if hasattr(self.classifier_pipeline, "predict_proba"):
                raw_probs = self.classifier_pipeline.predict_proba(features_df)[0]
                classes = self.target_encoder.classes_
                probs = {
                    cls: round(float(p), 4)
                    for cls, p in zip(classes, raw_probs)
                }
                score = _probability_weighted_score(classes, raw_probs)
            else:
                anchors = {"Low": 10.0, "Medium": 55.0, "High": 85.0}
                score = anchors.get(label, 50.0)
                probs = {label: 1.0}

            return {
                "congestion_score": score,
                "predicted_condition": label,
                "class_probabilities": probs,
                "model": "classifier",
            }
        else:
            raise RuntimeError("No model loaded. Train a model first.")


def _probability_weighted_score(classes: list, probs: list) -> float:
    """Compute a 0-100 score from classifier probabilities."""
    anchors = {"Low": 10.0, "Medium": 55.0, "High": 85.0}
    score = sum(anchors.get(cls, 50.0) * p for cls, p in zip(classes, probs))
    return round(max(0.0, min(100.0, score)), 1)


def _score_to_probabilities(score: float) -> dict[str, float]:
    """Build approximate class probabilities from a congestion score.

    This is a soft mapping — not exact Bayesian posteriors — but gives
    the frontend meaningful confidence values to display.
    """
    # Triangular distributions centred on each anchor
    low = max(0, 1 - abs(score - 10) / 25)
    medium = max(0, 1 - abs(score - 55) / 30)
    high = max(0, 1 - abs(score - 85) / 25)

    total = low + medium + high
    if total == 0:
        return {"Low": 0.33, "Medium": 0.34, "High": 0.33}

    return {
        "Low": round(low / total, 4),
        "Medium": round(medium / total, 4),
        "High": round(high / total, 4),
    }
