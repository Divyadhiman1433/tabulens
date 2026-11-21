from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    numeric_columns: int
    categorical_columns: int
    constant_columns: int
    quality_score: int


class DatasetAnalyzer:
    def __init__(self, frame: pd.DataFrame):
        if frame.empty:
            raise ValueError("The dataset must contain at least one row")
        self.frame = frame.copy()

    def profile(self) -> DatasetProfile:
        rows, columns = self.frame.shape
        missing_cells = int(self.frame.isna().sum().sum())
        duplicate_rows = int(self.frame.duplicated().sum())
        numeric_columns = int(self.frame.select_dtypes(include=np.number).shape[1])
        categorical_columns = columns - numeric_columns
        constant_columns = int((self.frame.nunique(dropna=False) <= 1).sum())
        total_cells = max(rows * columns, 1)
        missing_rate = missing_cells / total_cells
        missing_column_rate = float((self.frame.isna().sum() > 0).sum()) / max(columns, 1)
        duplicate_rate = duplicate_rows / max(rows, 1)
        constant_rate = constant_columns / max(columns, 1)
        score = 100 - 30 * missing_column_rate - 20 * missing_rate - 40 * duplicate_rate - 20 * constant_rate
        return DatasetProfile(
            rows=rows,
            columns=columns,
            missing_cells=missing_cells,
            duplicate_rows=duplicate_rows,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            constant_columns=constant_columns,
            quality_score=int(round(max(0, min(100, score)))),
        )

    def column_report(self) -> pd.DataFrame:
        rows = max(len(self.frame), 1)
        report = pd.DataFrame(
            {
                "column": self.frame.columns,
                "type": [str(dtype) for dtype in self.frame.dtypes],
                "missing": self.frame.isna().sum().values,
                "missing_percent": (self.frame.isna().sum().values / rows * 100).round(1),
                "unique": self.frame.nunique(dropna=True).values,
            }
        )
        report["status"] = np.select(
            [report["missing"] > 0, report["unique"] <= 1],
            ["Missing values", "Constant"],
            default="Ready",
        )
        return report

    def clean(self, drop_duplicates: bool = True, fill_missing: bool = True) -> pd.DataFrame:
        cleaned = self.frame.copy()
        if drop_duplicates:
            cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        if fill_missing:
            numeric = cleaned.select_dtypes(include=np.number).columns
            categorical = cleaned.columns.difference(numeric)
            for column in numeric:
                cleaned[column] = cleaned[column].fillna(cleaned[column].median())
            for column in categorical:
                mode = cleaned[column].mode(dropna=True)
                fallback = mode.iloc[0] if not mode.empty else "Unknown"
                cleaned[column] = cleaned[column].fillna(fallback)
        if drop_duplicates:
            cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        return cleaned

    def detect_anomalies(self, contamination: float = 0.05) -> pd.DataFrame:
        numeric = self.frame.select_dtypes(include=np.number)
        usable = numeric.loc[:, numeric.nunique(dropna=True) > 1]
        if usable.empty:
            raise ValueError("Anomaly detection requires at least one varying numeric column")
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            IsolationForest(contamination=contamination, random_state=42),
        )
        labels = model.fit_predict(usable)
        forest = model.named_steps["isolationforest"]
        transformed = model.named_steps["standardscaler"].transform(
            model.named_steps["simpleimputer"].transform(usable)
        )
        scores = forest.decision_function(transformed)
        result = self.frame.copy()
        result["anomaly_score"] = scores.round(4)
        result["is_anomaly"] = labels == -1
        return result.sort_values("anomaly_score", ascending=True).reset_index(drop=True)
