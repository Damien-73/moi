"""Critères de validation d'un setup (tous obligatoires, après coûts)."""
from __future__ import annotations

import pandas as pd

from src.backtest.metrics import per_pair, profit_factor


def suspicious(trades: pd.DataFrame) -> bool:
    """Règle 8 : résultat trop beau -> chercher un bug avant de rapporter."""
    r = trades["R"].to_numpy()
    return len(r) > 0 and (profit_factor(r) > 2 or (r > 0).mean() > 0.65)


def evaluate(is_trades: pd.DataFrame, p_value: float, oos_trades: pd.DataFrame | None = None,
             n_pairs_required: int = 5) -> list[dict]:
    r = is_trades["R"].to_numpy()
    exp_is = float(r.mean()) if len(r) else float("nan")
    pp = per_pair(is_trades)
    pos_pairs = int((pp["expectancy_R"] > 0).sum())
    rows = [
        ("Trades in-sample", len(r), ">= 200", len(r) >= 200),
        ("Espérance in-sample (R)", round(exp_is, 3), "> 0,1", exp_is > 0.1),
        ("Profit factor in-sample", round(profit_factor(r), 2), ">= 1,3", profit_factor(r) >= 1.3),
        ("Paires positives", pos_pairs, f">= {n_pairs_required} / 7", pos_pairs >= n_pairs_required),
        ("p-value vs entrées aléatoires", round(p_value, 4), "< 0,05", p_value < 0.05),
    ]
    if oos_trades is not None:
        ro = oos_trades["R"].to_numpy()
        exp_oos = float(ro.mean()) if len(ro) else float("nan")
        rows += [
            ("Trades out-of-sample", len(ro), ">= 100", len(ro) >= 100),
            ("Espérance OOS / in-sample", round(exp_oos / exp_is, 2) if exp_is else float("nan"),
             ">= 0,5", exp_is > 0 and exp_oos >= 0.5 * exp_is),
        ]
    return [{"critere": a, "valeur": b, "seuil": c, "ok": bool(d)} for a, b, c, d in rows]
