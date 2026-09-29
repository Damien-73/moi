import numpy as np
import pandas as pd
import pytest

from src.data.resample import mid, resample
from src.setups.zone_a_zone import PARAMS, atr, detect
from tests.synth import make_m1


def _h1_mid(m1):
    return mid(resample(m1, "H1"))


def _bars(rows):
    idx = pd.date_range("2021-03-01", periods=len(rows), freq="1h", tz="UTC")
    df = pd.DataFrame(rows, columns=["o", "h", "l", "c"], index=idx)
    df["close_time"] = df.index + pd.Timedelta(hours=1)
    return df


def test_long_signal_on_first_rejection_of_demand_zone():
    rows = [(100, 100.5, 99.5, 100)] * 20
    rows += [(100, 100.5, 98.0, 100)]                 # 20 : pivot bas
    rows += [(100, 100.5, 99.5, 100)] * 9             # 21-23 confirment, 24-29 neutres
    rows += [(100, 100.2, 98.3, 99.0)]                # 30 : touche la zone, clôture au-dessus
    rows += [(99, 100.0, 98.3, 99.5)]                 # 31 : 2e contact -> zone déjà consommée
    rows += [(100, 100.5, 99.5, 100)] * 3
    bars = _bars(rows)
    sig = detect(bars, **PARAMS)
    assert len(sig) == 1
    s = sig.iloc[0]
    assert s["direction"] == 1
    assert s["signal_time"] == bars["close_time"].iloc[30]
    a = atr(bars["h"].to_numpy(float), bars["l"].to_numpy(float), bars["c"].to_numpy(float), 14)
    assert s["sl"] == pytest.approx(98.0 - 0.2 * a[30])


def test_no_signal_when_close_inside_zone_or_zone_not_yet_confirmed():
    rows = [(100, 100.5, 99.5, 100)] * 20
    rows += [(100, 100.5, 98.0, 100)]                 # 20 : pivot bas
    rows += [(100, 100.5, 98.2, 100)]                 # 21 : touche avant confirmation (c = 23) -> ignoré
    rows += [(100, 100.5, 99.5, 100)] * 4
    rows += [(99, 99.2, 98.1, 98.3)]                  # 26 : touche, clôture DANS la zone -> consommée, pas de signal
    rows += [(98.4, 100, 98.1, 99.5)] * 2
    assert len(detect(_bars(rows), **PARAMS)) == 0


@pytest.mark.parametrize("pivot_high, n_signals", [(101.8, 0), (104.0, 1)])
def test_room_filter_to_next_supply_zone(pivot_high, n_signals):
    rows = [(100, 100.5, 99.5, 100)] * 20
    rows += [(100, 100.5, 98.0, 100)]                 # 20 : pivot bas -> demande [98, ~98.55]
    rows += [(100, 100.5, 99.5, 100)] * 2
    rows += [(100, pivot_high, 99.5, 100)]            # 23 : pivot haut -> offre [haut - 0,5 ATR, haut]
    rows += [(100, 100.5, 99.5, 100)] * 6
    rows += [(100, 100.2, 98.3, 99.0)]                # 30 : rejet de la demande
    # 101,8 : offre à ~2,2 du prix < 2 R (~2,5) -> bloqué ; 104 : place suffisante -> signal
    assert len(detect(_bars(rows), **PARAMS)) == n_signals


def test_deterministic():
    h1 = _h1_mid(make_m1(days=40, seed=11))
    pd.testing.assert_frame_equal(detect(h1, **PARAMS), detect(h1, **PARAMS))


@pytest.mark.parametrize("seed", [11, 12, 13])
def test_zone_a_zone_has_no_look_ahead(seed):
    """Zéro look-ahead : couper les données en T, ou modifier tout ce qui suit T,
    ne change aucun signal émis avant T ; chaque signal n'utilise que des bougies clôturées."""
    m1 = make_m1(days=60, seed=seed, vol=0.0001)
    full = detect(_h1_mid(m1), **PARAMS)
    assert len(full) > 10
    rng = np.random.default_rng(seed)
    for T in m1.index[rng.integers(len(m1) // 4, len(m1), 5)]:
        cut = detect(_h1_mid(m1[m1.index <= T]), **PARAMS)
        a = full[full["signal_time"] <= T].reset_index(drop=True)
        b = cut[cut["signal_time"] <= T].reset_index(drop=True)
        pd.testing.assert_frame_equal(a, b)
        alt = m1.copy()
        fut = alt.index > T
        alt.loc[fut] = alt.loc[fut].to_numpy() * (1 + rng.normal(0, 0.01, (fut.sum(), 1)))
        c = detect(_h1_mid(alt), **PARAMS)
        pd.testing.assert_frame_equal(a, c[c["signal_time"] <= T].reset_index(drop=True))
    # un signal est émis à la clôture d'une bougie H1 : après toutes ses minutes
    h1 = _h1_mid(m1)
    assert full["signal_time"].isin(h1["close_time"]).all()
