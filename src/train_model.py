from __future__ import annotations

import json
import pickle
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

try:
    from data_preprocessing import (
        FEATURE_COLUMNS,
        TARGET_COLUMN,
        build_preprocessor,
        load_dataset,
        prepare_training_data,
    )
except ModuleNotFoundError:
    from src.data_preprocessing import (
        FEATURE_COLUMNS,
        TARGET_COLUMN,
        build_preprocessor,
        load_dataset,
        prepare_training_data,
    )

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "smart_mobility_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "traffic_speed_model.pkl"
METRICS_PATH = MODEL_DIR / "training_metrics.json"


def build_training_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", LinearRegression()),
        ]
    )


def train() -> None:
    dataset = load_dataset(DATASET_PATH)
    features, target = prepare_training_data(dataset)

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
    )

    pipeline = build_training_pipeline()
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse**0.5
    r2 = r2_score(y_test, predictions)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "pipeline": pipeline,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
    }

    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(artifact, model_file)

    with METRICS_PATH.open("w", encoding="utf-8") as metrics_file:
        json.dump(
            {
                "model": "LinearRegression",
                "target": TARGET_COLUMN,
                "features": FEATURE_COLUMNS,
                "mean_absolute_error": mae,
                "root_mean_squared_error": rmse,
                "r2_score": r2,
            },
            metrics_file,
            indent=2,
        )

    print(f"Model saved to: {MODEL_PATH}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2 score: {r2:.4f}")


if __name__ == "__main__":
    train()
