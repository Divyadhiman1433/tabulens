import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from tabulens import DatasetAnalyzer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "campus_energy_sample.csv"
FIGURES = ROOT / "assets" / "figures"
ARTIFACTS = ROOT / "artifacts"


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(DATA)
    analyzer = DatasetAnalyzer(frame)
    profile = analyzer.profile()
    cleaned = analyzer.clean()
    cleaned_profile = DatasetAnalyzer(cleaned).profile()
    anomaly_frame = analyzer.detect_anomalies(contamination=0.05)
    report = analyzer.column_report()

    payload = {
        "source": profile.__dict__,
        "cleaned": cleaned_profile.__dict__,
        "rows_removed": len(frame) - len(cleaned),
        "anomalies_flagged": int(anomaly_frame["is_anomaly"].sum()),
    }
    (ARTIFACTS / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    report.to_csv(ARTIFACTS / "column_readiness.csv", index=False)
    anomaly_frame.query("is_anomaly").to_csv(ARTIFACTS / "anomaly_records.csv", index=False)
    cleaned.to_csv(ARTIFACTS / "cleaned_sample.csv", index=False)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    missing = report.set_index("column")["missing"].sort_values()
    colors = ["#a1a1aa" if value == 0 else "#0f766e" for value in missing]
    missing.plot.barh(ax=ax, color=colors)
    ax.set_title("Missing values are concentrated in three columns", loc="left", weight="bold")
    ax.set_xlabel("Missing cells")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(FIGURES / "missing_values.png", dpi=180, facecolor="#fafafa")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    normal = anomaly_frame[~anomaly_frame["is_anomaly"]]
    unusual = anomaly_frame[anomaly_frame["is_anomaly"]]
    ax.scatter(normal["occupancy"], normal["energy_kwh"], s=26, color="#a1a1aa", alpha=0.72, label="Typical")
    ax.scatter(unusual["occupancy"], unusual["energy_kwh"], s=48, color="#be123c", label="Review")
    ax.set_title("Isolation Forest suggests unusual energy records for review", loc="left", weight="bold")
    ax.set_xlabel("Occupancy")
    ax.set_ylabel("Energy use (kWh)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "anomaly_screen.png", dpi=180, facecolor="#fafafa")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    labels = ["Original", "Cleaned copy"]
    scores = [profile.quality_score, cleaned_profile.quality_score]
    bars = ax.bar(labels, scores, color=["#71717a", "#0f766e"], width=0.56)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Readiness score")
    ax.set_title("Simple cleaning removes the detected quality issues", loc="left", weight="bold")
    ax.bar_label(bars, labels=[f"{score}/100" for score in scores], padding=5, weight="bold")
    fig.tight_layout()
    fig.savefig(FIGURES / "quality_comparison.png", dpi=180, facecolor="#fafafa")
    plt.close(fig)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
