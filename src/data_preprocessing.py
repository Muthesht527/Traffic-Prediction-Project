from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "Traffic_Speed_kmh"
TIMESTAMP_COLUMN = "Timestamp"

RAW_FEATURE_COLUMNS = [
    TIMESTAMP_COLUMN,
    "Latitude",
    "Longitude",
    "Vehicle_Count",
    "Road_Occupancy_%",
    "Traffic_Light_State",
    "Weather_Condition",
    "Accident_Report",
]

NUMERIC_FEATURE_COLUMNS = [
    "Latitude",
    "Longitude",
    "Vehicle_Count",
    "Road_Occupancy_%",
    "Accident_Report",
    "hour",
    "day_of_week",
]

CATEGORICAL_FEATURE_COLUMNS = [
    "Traffic_Light_State",
    "Weather_Condition",
]

FEATURE_COLUMNS = NUMERIC_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS


def load_dataset(dataset_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(dataset_path)


def validate_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> None:
    missing_columns = sorted(set(required_columns) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    transformed = df.copy()
    transformed[TIMESTAMP_COLUMN] = pd.to_datetime(
        transformed[TIMESTAMP_COLUMN],
        errors="coerce",
        dayfirst=True,
    )
    transformed["hour"] = transformed[TIMESTAMP_COLUMN].dt.hour
    transformed["day_of_week"] = transformed[TIMESTAMP_COLUMN].dt.dayofweek
    return transformed.drop(columns=[TIMESTAMP_COLUMN])


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, RAW_FEATURE_COLUMNS)
    transformed = extract_time_features(df[RAW_FEATURE_COLUMNS])
    return transformed[FEATURE_COLUMNS]


def prepare_training_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    validate_columns(df, [*RAW_FEATURE_COLUMNS, TARGET_COLUMN])
    features = prepare_features(df)
    target = df[TARGET_COLUMN]
    return features, target


def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURE_COLUMNS),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURE_COLUMNS),
        ]
    )
