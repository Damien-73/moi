"""Journal des essais de paramètres : results/trials.csv (un essai = une ligne)."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from src.config import RESULTS_DIR

FIELDS = ["timestamp_utc", "setup", "sample", "pairs", "exit_mode", "params",
          "trades", "expectancy_R", "profit_factor", "win_rate"]


def _path(path: Path | None) -> Path:
    return path or RESULTS_DIR / "trials.csv"


def log_trial(setup: str, sample: str, pairs: list[str], exit_mode: str, params: dict,
              summary: dict, path: Path | None = None) -> None:
    p = _path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    new = not p.exists()
    with p.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "setup": setup, "sample": sample, "pairs": " ".join(pairs), "exit_mode": exit_mode,
            "params": json.dumps(params, sort_keys=True),
            "trades": summary["trades"],
            "expectancy_R": round(summary["expectancy_R"], 4),
            "profit_factor": round(summary["profit_factor"], 4),
            "win_rate": round(summary["win_rate"], 4),
        })


def count_trials(setup: str, path: Path | None = None) -> int:
    p = _path(path)
    if not p.exists():
        return 0
    with p.open() as f:
        return sum(1 for r in csv.DictReader(f) if r["setup"] == setup)
