"""Statistiques d'un ensemble de trades (résultats en R)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def longest_losing_streak(r: np.ndarray) -> int:
    best = cur = 0
    for x in r:
        cur = cur + 1 if x <= 0 else 0
        best = max(best, cur)
    return best


def profit_factor(r: np.ndarray) -> float:
    gains, losses = r[r > 0].sum(), -r[r <= 0].sum()
    return float(gains / losses) if losses > 0 else float("inf")


def equity_curve(r: np.ndarray, risk: float) -> np.ndarray:
    """Capital relatif (départ 1) avec risque fixe en % du capital courant (intérêts composés)."""
    return np.cumprod(1 + risk * np.asarray(r, dtype=float))


def max_drawdown(equity: np.ndarray) -> float:
    """Drawdown maximal en fraction du plus haut (0.25 = -25 %)."""
    if len(equity) == 0:
        return 0.0
    eq = np.r_[1.0, equity]
    peak = np.maximum.accumulate(eq)
    return float(np.max(1 - eq / peak))


def monte_carlo_dd(r: np.ndarray, risk: float, n_sims: int = 5000, seed: int = 0, q: float = 0.95) -> float:
    """Drawdown max au percentile q, en rééchantillonnant les trades (tirage avec remise)."""
    r = np.asarray(r, dtype=float)
    if len(r) == 0:
        return 0.0
    rng = np.random.default_rng(seed)
    sims = rng.choice(r, size=(n_sims, len(r)), replace=True)
    eq = np.cumprod(1 + risk * sims, axis=1)
    eq = np.concatenate([np.ones((n_sims, 1)), eq], axis=1)
    dd = np.max(1 - eq / np.maximum.accumulate(eq, axis=1), axis=1)
    return float(np.quantile(dd, q))


def summarize(trades: pd.DataFrame, risks=(0.01, 0.02), mc_sims: int = 5000) -> dict:
    """Statistiques globales. Les trades sont ordonnés par heure de sortie."""
    t = trades.sort_values("exit_time")
    r = t["R"].to_numpy(dtype=float)
    out = {
        "trades": int(len(r)),
        "win_rate": float((r > 0).mean()) if len(r) else float("nan"),
        "expectancy_R": float(r.mean()) if len(r) else float("nan"),
        "profit_factor": profit_factor(r) if len(r) else float("nan"),
        "total_R": float(r.sum()),
        "longest_losing_streak": longest_losing_streak(r),
    }
    for risk in risks:
        tag = f"{int(risk * 100)}pct"
        eq = equity_curve(r, risk)
        out[f"return_{tag}"] = float(eq[-1] - 1) if len(eq) else 0.0
        out[f"max_dd_{tag}"] = max_drawdown(eq)
        out[f"mc_dd95_{tag}"] = monte_carlo_dd(r, risk, n_sims=mc_sims)
    return out


def per_pair(trades: pd.DataFrame) -> pd.DataFrame:
    g = trades.groupby("pair")["R"]
    return pd.DataFrame({
        "trades": g.size(),
        "win_rate": g.apply(lambda x: (x > 0).mean()),
        "expectancy_R": g.mean(),
        "profit_factor": g.apply(lambda x: profit_factor(x.to_numpy())),
        "total_R": g.sum(),
    })
