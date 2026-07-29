"""Enhanced model training with regression target (0–100 congestion score).

Produces TWO artefacts:
1. The original classifier (kept for backward compatibility).
2. A regression model that directly predicts a 0–100 congestion score,
   evaluated with MAE, RMSE, R², plus feature importance.

Both are saved so the prediction service can use either.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split

import sys

# Import preprocessing from the original src/ module
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from data_preprocessing import (
    MODEL_FEATURE_COLUMNS,
    RAW_FEATURE_COLUMNS,
    TARGET_COLUMN,
    build_preprocessor,
    load_dataset,
    prepare_training_data,
)

MODEL_DIR = PROJECT_ROOT / "model"
DATASET_PATH = PROJECT_ROOT / "dataset" / "smart_mobility_dataset.csv"

# Congestion score anchors for converting classification targets to regression
_LABEL_TO_SCORE = {"Low": 10.0, "Medium": 55.0, "High": 85.0}


def _add_regression_target(df: pd.DataFrame) -> pd.DataFrame:
    """Add a continuous 'congestion_score' column derived from Traffic_Condition."""
    result = df.copy()
    result["congestion_score"] = result[TARGET_COLUMN].map(_LABEL_TO_SCORE)
    # Add small per-row variance so the regressor has something to learn
    rng = np.random.RandomState(42)
    noise = rng.normal(0, 5, len(result))
    result["congestion_score"] = (result["congestion_score"] + noise).clip(0, 100)
    return result


def train_classifier() -> dict:
    """Train the classification model (original approach)."""
    dataset = load_dataset(DATASET_PATH)
    features, target = prepare_training_data(dataset)

    from sklearn.preprocessing import LabelEncoder
    target_encoder = LabelEncoder()
    encoded_target = target_encoder.fit_transform(target)

    X_train, X_test, y_train, y_test = train_test_split(
        features, encoded_target, test_size=0.2, random_state=42,
        stratify=encoded_target if len(set(encoded_target)) > 1 else None,
    )

    preprocessor = build_preprocessor()
    classifier = RandomForestClassifier(
        n_estimators=300, max_depth=None, min_samples_split=2,
        min_samples_leaf=1, random_state=42, n_jobs=1,
        class_weight="balanced_subsample",
    )

    from sklearn.pipeline import Pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", classifier),
    ])
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    report = classification_report(
        y_test, preds, target_names=target_encoder.classes_,
        output_dict=True, zero_division=0,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "pipeline": pipeline,
        "target_encoder": target_encoder,
        "raw_feature_columns": RAW_FEATURE_COLUMNS,
        "model_feature_columns": MODEL_FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
    }
    with (MODEL_DIR / "traffic_congestion_model.pkl").open("wb") as f:
        pickle.dump(artifact, f)

    metrics = {"accuracy": accuracy, "classification_report": report}
    with (MODEL_DIR / "training_metrics.json").open("w") as f:
        json.dump(metrics, f, indent=2)

    print(f"[Classifier] Accuracy: {accuracy:.4f}")
    return metrics


def train_regressor() -> dict:
    """Train a regression model that directly outputs a 0–100 congestion score."""
    dataset = load_dataset(DATASET_PATH)
    dataset = _add_regression_target(dataset)

    # Reuse the feature prep logic
    from data_preprocessing import prepare_features
    features = prepare_features(dataset[RAW_FEATURE_COLUMNS])
    target = dataset["congestion_score"].values

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42,
    )

    preprocessor = build_preprocessor()
    regressor = RandomForestRegressor(
        n_estimators=300, max_depth=None, min_samples_split=2,
        min_samples_leaf=1, random_state=42, n_jobs=1,
    )

    from sklearn.pipeline import Pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", regressor),
    ])
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    # Feature importance (from the tree model, post-preprocessing)
    model = pipeline.named_steps["model"]
    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    importances = dict(zip(feature_names, model.feature_importances_.tolist()))
    # Sort descending
    importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

    # Save regression model
    reg_artifact = {
        "pipeline": pipeline,
        "feature_names": list(feature_names),
        "importances": importances,
    }
    with (MODEL_DIR / "congestion_regressor.pkl").open("wb") as f:
        pickle.dump(reg_artifact, f)

    reg_metrics = {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "feature_importance_top10": dict(list(importances.items())[:10]),
    }
    with (MODEL_DIR / "regression_metrics.json").open("w") as f:
        json.dump(reg_metrics, f, indent=2)

    print(f"[Regressor] MAE: {mae:.4f}  RMSE: {rmse:.4f}  R²: {r2:.4f}")
    print(f"[Regressor] Top 5 features: {list(importances.keys())[:5]}")
    return reg_metrics


if __name__ == "__main__":
    print("=" * 60)
    print("TRAINING BOTH MODELS")
    print("=" * 60)
    train_classifier()
    print()
    train_regressor()
    print("=" * 60)
    print("DONE — artefacts saved to model/")
    print("=" * 60)
