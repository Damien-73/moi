import numpy as np
import pandas as pd
import pytest

from src.backtest.engine import Market, run_backtest
from src.backtest.metrics import (equity_curve, longest_losing_streak, max_drawdown, monte_carlo_dd,
                                  profit_factor, summarize)
from src.config import SWAP_PIPS
from tests.synth import bars_m1

PIP = 0.0001
SLIP = 0.3 * PIP
SPREAD = 1.0 * PIP


def sig(t, direction, sl):
    return pd.DataFrame({"signal_time": [pd.Timestamp(t, tz="UTC")], "direction": [direction], "sl": [sl]})


def run(rows, direction, sl, spread=SPREAD, start="2021-03-01 10:00", **kw):
    m1 = bars_m1(rows, start=start, spread=spread)
    mk = Market.from_df("EURUSD", m1)
    return run_backtest(mk, sig(start, direction, sl), **kw)


def test_long_tp_costs_spread_and_slippage():
    rows = [(1.1000, 1.1002, 1.0998, 1.1001), (1.1001, 1.1025, 1.1000, 1.1020)]
    tr = run(rows, +1, 1.0990).iloc[0]
    entry = 1.1000 + SPREAD + SLIP                  # achat à l'ask + glissement
    risk = entry - 1.0990
    tp = entry + 2 * risk
    assert tr["entry"] == pytest.approx(entry)
    assert tr["exit_reason"] == "tp"
    assert tr["R"] == pytest.approx((tp - SLIP - entry) / risk)  # sortie au bid - glissement
    assert tr["R"] < 2.0                              # les coûts réduisent le gain


def test_sl_and_tp_same_m1_bar_is_a_loss():
    rows = [(1.1000, 1.1002, 1.0998, 1.1001), (1.1001, 1.1030, 1.0980, 1.1000)]
    tr = run(rows, +1, 1.0990).iloc[0]
    entry = 1.1000 + SPREAD + SLIP
    assert tr["exit_reason"] == "sl"
    assert tr["R"] == pytest.approx((1.0990 - SLIP - entry) / (entry - 1.0990))
    assert tr["R"] < -1.0


def test_gap_through_sl_fills_at_open():
    rows = [(1.1000, 1.1002, 1.0998, 1.1001), (1.0980, 1.0985, 1.0975, 1.0982)]
    tr = run(rows, +1, 1.0990).iloc[0]
    entry = 1.1000 + SPREAD + SLIP
    assert tr["R"] == pytest.approx((1.0980 - SLIP - entry) / (entry - 1.0990))


def test_short_uses_bid_entry_ask_exit():
    rows = [(1.1000, 1.1002, 1.0998, 1.1000), (1.1000, 1.1001, 1.0960, 1.0965)]
    tr = run(rows, -1, 1.1010).iloc[0]
    entry = 1.1000 - SLIP                  # vente au bid - glissement
    risk = 1.1010 - entry
    tp = entry - 2 * risk
    assert tr["exit_reason"] == "tp"
    assert tr["R"] == pytest.approx((entry - (tp + SLIP)) / risk)
    # le TP est touché côté ask : ask_l = 1.0960 + spread doit être <= tp
    assert 1.0960 + SPREAD <= tp


def test_short_sl_triggered_by_ask_not_bid():
    # bid_h = 1.1009 < SL mais ask_h = 1.1009 + 1 pip > SL -> stop touché
    rows = [(1.1000, 1.1002, 1.0998, 1.1000), (1.1000, 1.1009, 1.0999, 1.1000)]
    tr = run(rows, -1, 1.1010).iloc[0]
    assert tr["exit_reason"] == "sl"


def test_skip_when_sl_already_crossed():
    rows = [(1.1000, 1.1002, 1.0998, 1.1001)] * 3
    assert len(run(rows, +1, 1.1005)) == 0


def test_swap_counts_nights_wednesday_triple():
    # mardi 2021-03-02 20:00 UTC -> jeudi 00:00 UTC : roll-over mardi 22:00 UTC (x1) et mercredi 22:00 UTC (x3)
    n = 28 * 60
    rows = [(1.1000, 1.1001, 1.0999, 1.1000)] * n
    tr = run(rows, +1, 1.0950, start="2021-03-02 20:00", max_hold=pd.Timedelta(hours=27)).iloc[0]
    assert tr["exit_reason"] == "timeout"
    assert tr["nights"] == 4
    risk = (1.1000 + SPREAD + SLIP) - 1.0950
    assert tr["swap_R"] == pytest.approx(4 * SWAP_PIPS["EURUSD"]["long"] * PIP / risk)
    # swap inclus dans R : sortie au bid_c - glissement, plus le swap
    entry = 1.1000 + SPREAD + SLIP
    assert tr["R"] == pytest.approx((1.1000 - SLIP - entry) / risk + tr["swap_R"])


def test_no_swap_intraday():
    rows = [(1.1000, 1.1002, 1.0998, 1.1001), (1.1001, 1.1025, 1.1000, 1.1020)]
    assert run(rows, +1, 1.0990).iloc[0]["nights"] == 0


def test_partial_tp1_then_breakeven():
    e = 1.1000 + SPREAD + SLIP
    risk = e - 1.0990
    rows = [(1.1000, 1.1002, 1.0998, 1.1001),
            (1.1001, e + 1.2 * risk, 1.1001, 1.1010),   # TP1 touché, pas le retour à l'entrée
            (1.1010, 1.1011, e - 0.0002, e - 0.0001)]    # retour sous l'entrée -> breakeven
    tr = run(rows, +1, 1.0990, exit_mode="partial").iloc[0]
    assert tr["exit_reason"] == "tp1+breakeven"
    expected = (1 / 3) * (risk - SLIP) + (2 / 3) * (-SLIP)
    assert tr["R"] == pytest.approx(expected / risk)


def test_partial_all_targets():
    e = 1.1000 + SPREAD + SLIP
    risk = e - 1.0990
    rows = [(1.1000, 1.1002, 1.0998, 1.1001),
            (e + 0.00002, e + 1.1 * risk, e + 0.00001, e + risk),
            (e + risk, e + 3.2 * risk, e + 0.9 * risk, e + 3 * risk)]
    tr = run(rows, +1, 1.0990, exit_mode="partial").iloc[0]
    assert tr["exit_reason"] == "tp1+tp2+tp3"
    assert tr["R"] == pytest.approx((risk * (1 + 2 + 3) / 3 - SLIP) / risk)


def test_partial_same_bar_tp1_and_breakeven_is_pessimistic():
    e = 1.1000 + SPREAD + SLIP
    risk = e - 1.0990
    rows = [(1.1000, 1.1002, 1.0998, 1.1001),
            (1.1001, e + 1.5 * risk, e - 0.0003, 1.1001)]  # TP1 et retour sous l'entrée dans la même bougie
    tr = run(rows, +1, 1.0990, exit_mode="partial").iloc[0]
    assert tr["exit_reason"] == "tp1+breakeven"


def test_entry_never_before_signal_and_stale_signal_skipped():
    m1 = bars_m1([(1.1, 1.1001, 1.0999, 1.1)] * 120, start="2021-03-01 10:00", spread=SPREAD)
    mk = Market.from_df("EURUSD", m1)
    s = sig("2021-03-01 10:30", +1, 1.0990)
    tr = run_backtest(mk, s, max_hold=pd.Timedelta(minutes=5))
    assert tr.iloc[0]["entry_time"] >= s.iloc[0]["signal_time"]
    # signal après la fin des données / trop loin de la prochaine bougie : ignoré
    late = bars_m1([(1.1, 1.1001, 1.0999, 1.1)] * 10, start="2021-03-01 13:00", spread=SPREAD)
    both = pd.concat([m1, late])
    tr2 = run_backtest(Market.from_df("EURUSD", both), sig("2021-03-01 12:10", +1, 1.0990))
    assert len(tr2) == 0


def test_one_position_at_a_time_per_pair():
    m1 = bars_m1([(1.1, 1.1001, 1.0999, 1.1)] * 200, spread=SPREAD)
    mk = Market.from_df("EURUSD", m1)
    s = pd.concat([sig("2021-03-01 10:00", +1, 1.0990), sig("2021-03-01 10:30", +1, 1.0990),
                   sig("2021-03-01 12:00", +1, 1.0990)])
    tr = run_backtest(mk, s, max_hold=pd.Timedelta(hours=1))
    assert len(tr) == 2  # le signal de 10:30 tombe pendant la position ouverte


def test_news_filter_blocks_entries():
    m1 = bars_m1([(1.1, 1.1001, 1.0999, 1.1)] * 200, spread=SPREAD)
    mk = Market.from_df("EURUSD", m1)
    news = np.array([pd.Timestamp("2021-03-01 10:20", tz="UTC").value])
    assert len(run_backtest(mk, sig("2021-03-01 10:00", +1, 1.099), news_times=news, max_hold=pd.Timedelta(minutes=5))) == 0
    assert len(run_backtest(mk, sig("2021-03-01 11:00", +1, 1.099), news_times=news, max_hold=pd.Timedelta(minutes=5))) == 1


def test_metrics():
    r = np.array([2, -1, -1, 2, -1, -1, -1, 2.0])
    assert profit_factor(r) == pytest.approx(6 / 5)
    assert longest_losing_streak(r) == 3
    eq = equity_curve(np.array([-1, -1, 2.0]), 0.01)
    assert max_drawdown(eq) == pytest.approx(1 - 0.99 * 0.99)
    assert monte_carlo_dd(r, 0.01) >= 0
    tr = pd.DataFrame({"R": r, "exit_time": pd.date_range("2021", periods=8, freq="D"), "pair": "EURUSD"})
    s = summarize(tr, mc_sims=200)
    assert s["trades"] == 8 and s["expectancy_R"] == pytest.approx(1 / 8)
    assert s["max_dd_2pct"] > s["max_dd_1pct"]


def _random_signals(m1, n, seed, sl_pips=15):
    rng = np.random.default_rng(seed)
    hours = m1.index.floor("1h").unique()[1:]
    t = np.sort(rng.choice(hours, size=n, replace=False))
    d = rng.choice([-1, 1], size=n)
    px = m1["bid_c"].reindex(pd.DatetimeIndex(t), method="ffill").to_numpy()
    return pd.DataFrame({"signal_time": t, "direction": d, "sl": px - d * sl_pips * PIP})


def test_engine_has_no_look_ahead():
    """Modifier les prix APRÈS T ne change aucun trade clôturé avant T."""
    from tests.synth import make_m1
    m1 = make_m1(days=30, seed=1)
    sigs = _random_signals(m1, 150, seed=2, sl_pips=5)
    T = m1.index[len(m1) // 2]
    base = run_backtest(Market.from_df("EURUSD", m1), sigs)
    alt = m1.copy()
    fut = alt.index > T
    noise = np.random.default_rng(9).normal(0, 0.002, fut.sum())
    alt.loc[fut] = alt.loc[fut].to_numpy() + noise[:, None]
    other = run_backtest(Market.from_df("EURUSD", alt), sigs)
    a = base[base["exit_time"] < T].reset_index(drop=True)
    b = other[other["exit_time"] < T].reset_index(drop=True)
    assert len(a) > 20
    pd.testing.assert_frame_equal(a, b)


def test_random_entries_lose_after_costs():
    """Marche aléatoire + coûts : espérance négative attendue. Sinon le moteur est faux."""
    from tests.synth import make_m1
    m1 = make_m1(days=120, seed=3, vol=0.00006)
    tr = run_backtest(Market.from_df("EURUSD", m1), _random_signals(m1, 600, seed=4, sl_pips=5))
    assert len(tr) > 300
    assert tr["R"].mean() < 0
    assert 0.2 < (tr["R"] > 0).mean() < 0.4  # ~1/3 avec R/R 1:2, un peu moins après coûts
