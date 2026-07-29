"""Load the trained Random Forest model and expose a prediction interface."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from backend.config import MODEL_PATH
from backend.utils.logger import get_logger

log = get_logger("model-loader")


class ModelLoader:
    """Singleton-style wrapper around the pickled sklearn pipeline."""

    _instance: ModelLoader | None = None

    def __new__(cls) -> ModelLoader:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def __init__(self) -> None:
        if self._loaded:
            return
        self.pipeline = None
        self.target_encoder = None
        self.raw_feature_columns: list[str] = []
        self.model_feature_columns: list[str] = []
        self.target_column: str = ""
        self._load()
        self._loaded = True

    def _load(self) -> None:
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {model_path}. Run src/train_model.py first."
            )
        with model_path.open("rb") as fh:
            artifact: dict[str, Any] = pickle.load(fh)
        self.pipeline = artifact["pipeline"]
        self.target_encoder = artifact["target_encoder"]
        self.raw_feature_columns = artifact["raw_feature_columns"]
        self.model_feature_columns = artifact["model_feature_columns"]
        self.target_column = artifact["target_column"]
        log.info(
            "Model loaded — classes: %s",
            list(self.target_encoder.classes_),
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get_classes(self) -> list[str]:
        """Return the human-readable target labels."""
        return list(self.target_encoder.classes_)
