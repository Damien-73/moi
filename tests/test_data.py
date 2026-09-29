import numpy as np
import pandas as pd
import pytest

from src.data.download import merge_bid_ask
from src.data.quality import clean, find_gaps, market_open_mask, quality_report
from src.data.resample import resample
from src.data.store import clip_period
from src.validation.oos_lock import OOSLocked, unlock_oos
from tests.synth import make_m1


def test_market_hours_ny():
    # Hiver (UTC-5) : vendredi 21:59 UTC ouvert, 22:00 fermé ; dimanche 22:00 UTC ouvert.
    t = pd.DatetimeIndex(["2021-01-08 21:59", "2021-01-08 22:00", "2021-01-10 21:59", "2021-01-10 22:00"], tz="UTC")
    assert market_open_mask(t).tolist() == [True, False, False, True]
    # Été (UTC-4) : fermeture vendredi 21:00 UTC.
    t = pd.DatetimeIndex(["2021-07-09 20:59", "2021-07-09 21:00"], tz="UTC")
    assert market_open_mask(t).tolist() == [True, False]


def test_clean_drops_weekend_negative_spread_invalid():
    df = make_m1(days=8)
    wk = pd.DataFrame(df.iloc[[0]].to_numpy(), columns=df.columns,
                      index=pd.DatetimeIndex([pd.Timestamp("2020-01-11 12:00", tz="UTC")]))  # samedi
    df = pd.concat([df, wk]).sort_index()
    for x in "ohlc":  # spread négatif sur toute la bougie
        df.iloc[10, df.columns.get_loc(f"ask_{x}")] = df.iloc[10][f"bid_{x}"] - 0.0001
    df.iloc[20, df.columns.get_loc("bid_h")] = df.iloc[20]["bid_l"] - 0.01   # high < low
    out, stats = clean(df)
    assert stats == {"weekend_bars": 1, "negative_spread": 1, "invalid_ohlc": 1, "dropped": 3}
    assert len(out) == len(df) - 3


def test_gaps_ignore_weekend_detect_hole():
    df = make_m1(days=14)
    assert len(find_gaps(df)) == 0  # le week-end n'est pas un trou
    hole = (df.index >= "2020-01-08 10:00") & (df.index < "2020-01-08 11:30")
    gaps = find_gaps(df[~hole])
    assert len(gaps) == 1 and gaps.iloc[0]["minutes"] == 90


def test_quality_report_runs():
    r = quality_report(make_m1(days=8), "EURUSD")
    assert r["spread_median_pips"] == pytest.approx(1.0)
    assert r["gaps_over_30min"] == 0


def test_merge_bid_ask_inner():
    idx = pd.date_range("2021-01-04", periods=3, freq="1min", tz="UTC")
    bid = pd.DataFrame({"open": [1, 1, 1], "high": [2, 2, 2], "low": [0.5] * 3, "close": [1] * 3}, index=idx, dtype=float)
    ask = bid.iloc[1:] + 0.1
    m, stats = merge_bid_ask(bid, ask)
    assert list(m.columns) == ["bid_o", "bid_h", "bid_l", "bid_c", "ask_o", "ask_h", "ask_l", "ask_c"]
    assert stats == {"bid_only": 1, "ask_only": 0, "merged": 2}


def test_resample_d1_h4_aligned_on_17h_new_york():
    df = make_m1(start="2021-01-04", days=12)  # hiver
    d1 = resample(df, "D1")
    ny = d1.index.tz_convert("America/New_York")
    assert set(ny.hour) == {17} and set(ny.minute) == {0}
    assert (d1["close_time"] - d1.index == pd.Timedelta(days=1)).all()
    assert d1.index.tz_convert("America/New_York").weekday.isin([6, 0, 1, 2, 3]).all()  # pas de bougie du vendredi soir
    h4 = resample(df, "H4")
    assert set(h4.index.tz_convert("America/New_York").hour) == {17, 21, 1, 5, 9, 13}
    # été : même alignement NY malgré le changement d'heure
    d1s = resample(make_m1(start="2021-07-05", days=8), "D1")
    assert set(d1s.index.tz_convert("America/New_York").hour) == {17}


def test_resample_values_match_minutes():
    df = make_m1(days=3)
    h1 = resample(df, "H1")
    t0 = h1.index[5]
    sl = df[(df.index >= t0) & (df.index < t0 + pd.Timedelta(hours=1))]
    row = h1.loc[t0]
    assert row["bid_o"] == sl["bid_o"].iloc[0] and row["bid_c"] == sl["bid_c"].iloc[-1]
    assert row["ask_h"] == sl["ask_h"].max() and row["bid_l"] == sl["bid_l"].min()
    # aucune minute d'une bougie n'est postérieure à sa clôture
    d1 = resample(df, "D1")
    for t, r in d1.iterrows():
        sl = df[(df.index >= t) & (df.index < r["close_time"])]
        assert len(sl) == r["n_minutes"]


def test_oos_locked_by_default():
    idx = pd.date_range("2022-12-31 23:58", periods=4, freq="1min", tz="UTC")
    df = pd.DataFrame({"bid_c": np.arange(4.0)}, index=idx)
    assert clip_period(df, "is").index.max() < pd.Timestamp("2023-01-01", tz="UTC")
    with pytest.raises(OOSLocked):
        clip_period(df, "oos")
    with pytest.raises(OOSLocked):
        clip_period(df, "oos", oos_token="triche")


def test_oos_unlock_requires_frozen_doc_accord_and_single_use(tmp_path, monkeypatch):
    docs = tmp_path / "docs"; docs.mkdir()
    log = tmp_path / "oos_log.csv"
    (docs / "s.md").write_text("Statut : brouillon", encoding="utf-8")
    monkeypatch.setenv("OOS_ACCORD", "s")
    with pytest.raises(OOSLocked):
        unlock_oos("s", {}, docs, log)  # pas figé
    (docs / "s.md").write_text("Statut : FIGÉ", encoding="utf-8")
    monkeypatch.delenv("OOS_ACCORD")
    with pytest.raises(OOSLocked):
        unlock_oos("s", {}, docs, log)  # pas d'accord
    monkeypatch.setenv("OOS_ACCORD", "s")
    tok = unlock_oos("s", {"a": 1}, docs, log)
    idx = pd.date_range("2023-01-02", periods=2, freq="1min", tz="UTC")
    assert len(clip_period(pd.DataFrame({"x": [1, 2]}, index=idx), "oos", tok)) == 2
    with pytest.raises(OOSLocked):
        unlock_oos("s", {"a": 1}, docs, log)  # usage unique
