"""Référence d'entrées aléatoires et test de permutation.

Pour chaque simulation : même nombre de trades par paire que le setup, mêmes distances de SL
(tirées parmi celles du setup sur la paire), même mode de sortie et même R/R. Seuls l'instant
d'entrée (début d'une heure H1, dans la même période) et le sens (50/50) sont aléatoires.

p-value = (1 + nb simulations dont l'espérance >= celle du setup) / (1 + nb simulations).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.backtest.engine import Market, simulate_trade
from src.config import PIP, RR_TARGET, SLIPPAGE_PIPS


def hour_start_indices(mk: Market, start: pd.Timestamp, end: pd.Timestamp) -> np.ndarray:
    """Index M1 de la première minute de chaque heure entre start et end."""
    t = mk.t
    hours = t // 3_600_000_000_000
    first = np.r_[True, hours[1:] != hours[:-1]]
    idx = np.where(first & (t >= start.value) & (t <= end.value))[0]
    return idx[idx < len(t) - 1]


def random_trades(markets: dict[str, Market], setup_trades: pd.DataFrame, rng: np.random.Generator,
                  exit_mode: str = "simple", rr: float = RR_TARGET) -> np.ndarray:
    """Une simulation : renvoie les R des trades aléatoires."""
    out = []
    for pair, grp in setup_trades.groupby("pair"):
        mk = markets[pair]
        cand = hour_start_indices(mk, grp["entry_time"].min(), grp["entry_time"].max())
        dists = grp["risk_pips"].to_numpy() * PIP[pair]
        slip = SLIPPAGE_PIPS * PIP[pair]
        n = len(grp)
        got = 0
        while got < n:
            i0 = int(rng.choice(cand))
            d = 1 if rng.random() < 0.5 else -1
            entry = (mk.ask_o[i0] + slip) if d > 0 else (mk.bid_o[i0] - slip)
            sl = entry - d * float(rng.choice(dists))
            tr = simulate_trade(mk, i0, d, sl, exit_mode, rr)
            if tr is not None:
                out.append(tr["R"])
                got += 1
    return np.array(out)


def permutation_test(markets: dict[str, Market], setup_trades: pd.DataFrame, n_sims: int = 1000,
                     seed: int = 0, exit_mode: str = "simple", rr: float = RR_TARGET) -> dict:
    rng = np.random.default_rng(seed)
    obs = float(setup_trades["R"].mean())
    sims = np.array([random_trades(markets, setup_trades, rng, exit_mode, rr).mean() for _ in range(n_sims)])
    return {
        "observed_expectancy_R": obs,
        "random_mean_expectancy_R": float(sims.mean()),
        "random_p95_expectancy_R": float(np.quantile(sims, 0.95)),
        "p_value": float((1 + np.sum(sims >= obs)) / (1 + n_sims)),
        "n_sims": n_sims,
    }
