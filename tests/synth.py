"""Données M1 synthétiques (marche aléatoire) pour les tests. Aucun lien avec le marché réel."""
import numpy as np
import pandas as pd

from src.data.quality import market_open_mask


def make_m1(start="2020-01-06", days=10, seed=0, spread=0.00010, price=1.1000, vol=0.00008):
    rng = np.random.default_rng(seed)
    idx = pd.date_range(pd.Timestamp(start, tz="UTC"), periods=days * 1440, freq="1min")
    idx = idx[market_open_mask(idx)]
    n = len(idx)
    steps = rng.normal(0, vol, size=(n, 4))
    close = price + np.cumsum(steps[:, 3])
    open_ = np.r_[price, close[:-1]]
    hi = np.maximum(open_, close) + np.abs(steps[:, 1])
    lo = np.minimum(open_, close) - np.abs(steps[:, 2])
    df = pd.DataFrame({"bid_o": open_, "bid_h": hi, "bid_l": lo, "bid_c": close}, index=idx)
    for x in "ohlc":
        df[f"ask_{x}"] = df[f"bid_{x}"] + spread
    df.index.name = "time"
    return df


def bars_m1(rows, start="2021-03-01 10:00", spread=0.0):
    """M1 à partir d'une liste (o, h, l, c) sur le bid ; ask = bid + spread."""
    idx = pd.date_range(pd.Timestamp(start, tz="UTC"), periods=len(rows), freq="1min")
    a = np.array(rows, dtype=float)
    df = pd.DataFrame(a, columns=["bid_o", "bid_h", "bid_l", "bid_c"], index=idx)
    for x in "ohlc":
        df[f"ask_{x}"] = df[f"bid_{x}"] + spread
    df.index.name = "time"
    return df
