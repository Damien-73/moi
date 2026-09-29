import numpy as np
import pandas as pd

from src.backtest.engine import Market, run_backtest
from src.validation.criteria import evaluate, suspicious
from src.validation.random_baseline import permutation_test
from src.validation.trials import count_trials, log_trial
from tests.synth import make_m1
from tests.test_engine import _random_signals


def _setup():
    m1 = make_m1(days=60, seed=5, vol=0.00006)
    mk = Market.from_df("EURUSD", m1)
    tr = run_backtest(mk, _random_signals(m1, 200, seed=6, sl_pips=6))
    return {"EURUSD": mk}, tr


def test_permutation_random_setup_not_significant_and_reproducible():
    markets, tr = _setup()
    a = permutation_test(markets, tr, n_sims=100, seed=1)
    b = permutation_test(markets, tr, n_sims=100, seed=1)
    assert a == b
    assert a["p_value"] > 0.05  # un « setup » aléatoire ne doit pas battre le hasard
    assert a["random_mean_expectancy_R"] < 0


def test_permutation_detects_real_edge():
    markets, tr = _setup()
    fake = tr.copy()
    fake["R"] = fake["R"] + 1.0  # avantage artificiel énorme
    assert permutation_test(markets, fake, n_sims=100, seed=1)["p_value"] < 0.05


def test_trials_log(tmp_path):
    p = tmp_path / "trials.csv"
    s = {"trades": 10, "expectancy_R": 0.1, "profit_factor": 1.2, "win_rate": 0.4}
    log_trial("x", "is", ["EURUSD"], "simple", {"a": 1}, s, p)
    log_trial("x", "is", ["EURUSD"], "simple", {"a": 2}, s, p)
    log_trial("y", "is", ["EURUSD"], "simple", {"a": 2}, s, p)
    assert count_trials("x", p) == 2 and count_trials("z", p) == 0


def test_criteria_and_suspicious():
    pairs = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]
    r = np.tile([2.0, -1.0, -1.0, 2.0, -1.0], 60)  # espérance 0,2 ; PF 1,33 ; win 40 %
    tr = pd.DataFrame({"R": r, "pair": np.resize(pairs, len(r))})
    res = {c["critere"]: c["ok"] for c in evaluate(tr, p_value=0.01)}
    assert all(res.values())
    assert not suspicious(tr)
    tr2 = tr.assign(R=np.tile([2.0, 2.0, -1.0], 100))
    assert suspicious(tr2)
    res = {c["critere"]: c["ok"] for c in evaluate(tr, 0.01, oos_trades=tr.iloc[:150].assign(R=0.05))}
    assert not res["Espérance OOS / in-sample"]
