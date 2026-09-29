import sys

import pandas as pd

import src.backtest.runner as runner
import src.data.store as store
import src.validation.trials as trials
from tests.synth import make_m1


def test_runner_end_to_end_in_sample(tmp_path, monkeypatch):
    m1dir = tmp_path / "m1"; m1dir.mkdir()
    res = tmp_path / "results"; res.mkdir()
    oos_part = make_m1(start="2023-01-02", days=5, seed=8)
    pd.concat([make_m1(start="2021-01-04", days=90, seed=7, vol=0.0001), oos_part]).to_parquet(m1dir / "EURUSD.parquet")
    monkeypatch.setattr(store, "M1_DIR", m1dir)
    monkeypatch.setattr(runner, "RESULTS_DIR", res)
    monkeypatch.setattr(trials, "RESULTS_DIR", res)
    monkeypatch.setattr(sys, "argv", ["runner", "--setup", "zone_a_zone", "--pairs", "EURUSD", "--sims", "20"])
    runner.main()
    report = (res / "report_zone_a_zone_is_EURUSD.md").read_text(encoding="utf-8")
    assert "Essais journalisés pour ce setup : **2**" in report
    assert "Critères de validation" in report and "Verdict" not in report
    assert trials.count_trials("zone_a_zone", res / "trials.csv") == 2
    # aucune donnée >= 2023 n'a été utilisée en in-sample
    _, trades = runner.run(__import__("src.setups.zone_a_zone", fromlist=["x"]), ["EURUSD"], "is")
    assert (trades["simple"]["exit_time"] < pd.Timestamp("2023-01-01", tz="UTC")).all()
