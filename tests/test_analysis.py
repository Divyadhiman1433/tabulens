import pandas as pd

from tabulens import DatasetAnalyzer


def test_profile_counts_quality_issues():
    frame = pd.DataFrame({"a": [1.0, None, 1.0], "b": ["x", "y", "x"]})
    profile = DatasetAnalyzer(frame).profile()
    assert profile.rows == 3
    assert profile.columns == 2
    assert profile.missing_cells == 1
    assert profile.quality_score < 100


def test_clean_removes_duplicates_and_fills_missing_values():
    frame = pd.DataFrame({"a": [1.0, None, 1.0], "b": ["x", None, "x"]})
    cleaned = DatasetAnalyzer(frame).clean()
    assert cleaned.isna().sum().sum() == 0
    assert cleaned.duplicated().sum() == 0


def test_anomaly_output_contains_review_fields():
    frame = pd.DataFrame({"a": list(range(30)) + [500], "b": list(range(30)) + [700]})
    result = DatasetAnalyzer(frame).detect_anomalies(contamination=0.05)
    assert {"anomaly_score", "is_anomaly"}.issubset(result.columns)
    assert result["is_anomaly"].any()
