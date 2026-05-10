from __future__ import annotations

import json
import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

try:
    from data_preprocessing import (
        MODEL_FEATURE_COLUMNS,
        RAW_FEATURE_COLUMNS,
        TARGET_COLUMN,
        build_preprocessor,
        load_dataset,
        prepare_training_data,
    )
except ModuleNotFoundError:
    from src.data_preprocessing import (
        MODEL_FEATURE_COLUMNS,
        RAW_FEATURE_COLUMNS,
        TARGET_COLUMN,
        build_preprocessor,
        load_dataset,
        prepare_training_data,
    )

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "smart_mobility_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "traffic_congestion_model.pkl"
METRICS_PATH = MODEL_DIR / "training_metrics.json"


def build_training_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=None,
                    min_samples_split=2,
                    min_samples_leaf=1,
                    random_state=42,
                    n_jobs=1,
                    class_weight="balanced_subsample",
                ),
            ),
        ]
    )


def train() -> None:
    dataset = load_dataset(DATASET_PATH)
    features, target = prepare_training_data(dataset)

    target_encoder = LabelEncoder()
    encoded_target = target_encoder.fit_transform(target)

    stratify_target = encoded_target if len(set(encoded_target)) > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        encoded_target,
        test_size=0.2,
        random_state=42,
        stratify=stratify_target,
    )

    pipeline = build_training_pipeline()
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(
        y_test,
        predictions,
        target_names=target_encoder.classes_,
        output_dict=True,
        zero_division=0,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "pipeline": pipeline,
        "target_encoder": target_encoder,
        "raw_feature_columns": RAW_FEATURE_COLUMNS,
        "model_feature_columns": MODEL_FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
    }

    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(artifact, model_file)

    with METRICS_PATH.open("w", encoding="utf-8") as metrics_file:
        json.dump(
            {
                "accuracy": accuracy,
                "classification_report": report,
            },
            metrics_file,
            indent=2,
        )

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Training accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    train()
