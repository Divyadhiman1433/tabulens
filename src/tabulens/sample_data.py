from pathlib import Path

import numpy as np
import pandas as pd


def build_sample(rows: int = 180, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=rows, freq="D")
    buildings = rng.choice(["Academic", "Library", "Hostel", "Lab"], size=rows)
    occupancy = rng.integers(40, 420, size=rows).astype(float)
    temperature = rng.normal(27, 5, size=rows).round(1)
    baseline = np.select(
        [buildings == "Lab", buildings == "Hostel", buildings == "Library"],
        [210, 170, 125],
        default=145,
    )
    energy = (baseline + occupancy * 0.42 + np.maximum(temperature - 24, 0) * 7 + rng.normal(0, 18, rows)).round(1)
    maintenance = np.where(rng.random(rows) < 0.12, "Required", "Normal")
    frame = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "building": buildings,
            "occupancy": occupancy,
            "temperature_c": temperature,
            "energy_kwh": energy,
            "maintenance_status": maintenance,
        }
    )
    frame.loc[[7, 39, 88], "occupancy"] = np.nan
    frame.loc[[20, 67], "temperature_c"] = np.nan
    frame.loc[[31, 114], "maintenance_status"] = np.nan
    frame.loc[146, "energy_kwh"] = frame["energy_kwh"].median() * 2.9
    return pd.concat([frame, frame.iloc[[16, 72]]], ignore_index=True)


def write_sample(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    build_sample().to_csv(path, index=False)
    return path
