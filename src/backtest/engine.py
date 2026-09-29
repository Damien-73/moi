"""Moteur de backtest événementiel, résolution M1, coûts réels.

Règles d'exécution (toutes conservatrices) :
- Entrée : ouverture de la première bougie M1 dont l'heure est >= heure du signal
  (le signal n'existe qu'à la clôture de sa bougie). Achat au prix ask, vente au prix bid.
  Si cette bougie arrive plus de `max_entry_delay` après le signal (week-end, trou), le signal est abandonné.
- Sortie : une position acheteuse sort au bid, une vendeuse à l'ask -> le spread réel
  (ask - bid des données) est payé à l'entrée ET à la sortie.
- Glissement : SLIPPAGE_PIPS défavorable sur CHAQUE ordre (entrée, SL, TP, sorties partielles).
- SL et TP touchés dans la même bougie M1 -> perte.
- Gap au-delà du SL -> exécution au prix d'ouverture (pire que le SL).
- Swap : SWAP_PIPS par nuit pour chaque passage à 17h00 NY, triple le mercredi.
- Une seule position à la fois par paire et par setup.

Résultat de chaque trade en R : R = gain net / risque initial (distance entrée réelle -> SL).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.config import NY_TZ, PIP, ROLLOVER_HOUR_NY, RR_TARGET, SLIPPAGE_PIPS, SWAP_PIPS

PARTIAL_LEVELS = (1.0, 2.0, 3.0)        # TP1, TP2, TP3 en multiples de R
PARTIAL_FRACTIONS = (1 / 3, 1 / 3, 1 / 3)


def rollover_schedule(start: pd.Timestamp, end: pd.Timestamp) -> tuple[np.ndarray, np.ndarray]:
    """Instants UTC des roll-over 17h00 NY (lundi -> vendredi) et leur poids (3 le mercredi)."""
    days = pd.date_range(start.tz_convert(NY_TZ).normalize() - pd.Timedelta(days=1),
                         end.tz_convert(NY_TZ).normalize() + pd.Timedelta(days=1), freq="D")
    days = days[days.weekday < 5]
    times = (days + pd.Timedelta(hours=ROLLOVER_HOUR_NY)).tz_convert("UTC")
    weights = np.where(days.weekday == 2, 3, 1)
    return times.as_unit("ns").asi8, weights


@dataclass
class Market:
    """Données M1 d'une paire sous forme de tableaux numpy (accès rapide)."""
    pair: str
    t: np.ndarray  # int64 ns UTC, ouverture de la minute
    bid_o: np.ndarray
    bid_h: np.ndarray
    bid_l: np.ndarray
    bid_c: np.ndarray
    ask_o: np.ndarray
    ask_h: np.ndarray
    ask_l: np.ndarray
    ask_c: np.ndarray
    roll_t: np.ndarray
    roll_cw: np.ndarray  # poids cumulés des roll-over

    @classmethod
    def from_df(cls, pair: str, m1: pd.DataFrame) -> "Market":
        idx = m1.index
        rt, rw = rollover_schedule(idx[0], idx[-1])
        cols = {c: m1[c].to_numpy(dtype="float64") for c in
                ("bid_o", "bid_h", "bid_l", "bid_c", "ask_o", "ask_h", "ask_l", "ask_c")}
        return cls(pair=pair, t=idx.as_unit("ns").asi8, roll_t=rt, roll_cw=np.r_[0, np.cumsum(rw)], **cols)

    def nights(self, t_in: int, t_out: int) -> int:
        """Nombre de nuits de swap (mercredi = 3) entre deux instants (ns)."""
        a = np.searchsorted(self.roll_t, t_in, side="right")
        b = np.searchsorted(self.roll_t, t_out, side="right")
        return int(self.roll_cw[b] - self.roll_cw[a])


def _first_event(mk: Market, direction: int, start: int, sl: float, tp: float | None,
                 stop_idx: int) -> tuple[int, bool, bool]:
    """Première bougie M1 (index >= start, < stop_idx) qui touche le SL ou le TP.

    Retourne (index, sl_touché, tp_touché) ; index = -1 si rien avant stop_idx.
    """
    if direction > 0:   # long : on sort au bid
        lo, hi = mk.bid_l, mk.bid_h
    else:               # short : on sort à l'ask
        lo, hi = mk.ask_l, mk.ask_h
    i, chunk = start, 512
    while i < stop_idx:
        j = min(stop_idx, i + chunk)
        if direction > 0:
            s = lo[i:j] <= sl
            t = hi[i:j] >= tp if tp is not None else np.zeros(j - i, bool)
        else:
            s = hi[i:j] >= sl
            t = lo[i:j] <= tp if tp is not None else np.zeros(j - i, bool)
        m = s | t
        if m.any():
            k = int(np.argmax(m))
            return i + k, bool(s[k]), bool(t[k])
        i, chunk = j, chunk * 2
    return -1, False, False


def _stop_fill(mk: Market, direction: int, j: int, level: float, slip: float, gap: bool = True) -> float:
    """Prix d'exécution d'un stop touché dans la bougie j (gap => ouverture).

    gap=False quand le stop a été déplacé PENDANT la bougie j (breakeven) : l'ouverture de j
    est antérieure au stop, elle ne peut pas servir de prix d'exécution.
    """
    if not gap:
        return level - direction * slip
    if direction > 0:
        return min(level, mk.bid_o[j]) - slip
    return max(level, mk.ask_o[j]) + slip


def _market_exit(mk: Market, direction: int, j: int, slip: float) -> float:
    return (mk.bid_c[j] - slip) if direction > 0 else (mk.ask_c[j] + slip)


def simulate_trade(mk: Market, i0: int, direction: int, sl: float, exit_mode: str = "simple",
                   rr: float = RR_TARGET, max_hold_idx: int | None = None) -> dict | None:
    """Simule un trade entré à l'ouverture de la bougie M1 i0. None si le trade est impossible."""
    pip = PIP[mk.pair]
    slip = SLIPPAGE_PIPS * pip
    entry = (mk.ask_o[i0] + slip) if direction > 0 else (mk.bid_o[i0] - slip)
    risk = (entry - sl) * direction
    if not risk > 0:
        return None
    n = len(mk.t)
    stop_idx = n if max_hold_idx is None else min(n, max_hold_idx)
    swap_side = "long" if direction > 0 else "short"

    if exit_mode == "simple":
        levels, fractions = (rr,), (1.0,)
    elif exit_mode == "partial":
        levels, fractions = PARTIAL_LEVELS, PARTIAL_FRACTIONS
    else:
        raise ValueError(exit_mode)

    pieces = []  # (fraction, prix de sortie, index de sortie, raison)
    cur_sl, k, idx = sl, 0, i0
    remaining = 1.0
    while remaining > 1e-12:
        tp = entry + direction * levels[k] * risk
        j, s_hit, t_hit = _first_event(mk, direction, idx, cur_sl, tp, stop_idx)
        if j < 0:  # ni SL ni TP : sortie au marché (durée max ou fin des données)
            j = stop_idx - 1
            pieces.append((remaining, _market_exit(mk, direction, j, slip), j, "timeout"))
            break
        if s_hit:  # SL (y compris SL + TP dans la même bougie -> perte)
            reason = "sl" if k == 0 else "breakeven"
            gap = not (k > 0 and j == idx)
            pieces.append((remaining, _stop_fill(mk, direction, j, cur_sl, slip, gap), j, reason))
            break
        frac = fractions[k]
        pieces.append((frac, tp - direction * slip, j, f"tp{k + 1}" if exit_mode == "partial" else "tp"))
        remaining -= frac
        k += 1
        cur_sl = entry  # après TP1 : stop au point d'entrée (breakeven)
        idx = j         # la même bougie est ré-examinée : ordre inconnu => hypothèse pessimiste

    t_in = int(mk.t[i0])
    pnl, swap_price, nights_w = 0.0, 0.0, 0.0
    for frac, px, j, _ in pieces:
        nts = mk.nights(t_in, int(mk.t[j]))
        sw = nts * SWAP_PIPS[mk.pair][swap_side] * pip
        pnl += frac * ((px - entry) * direction + sw)
        swap_price += frac * sw
        nights_w += frac * nts
    last = pieces[-1]
    return {
        "entry_time": pd.Timestamp(t_in, tz="UTC"),
        "exit_time": pd.Timestamp(int(mk.t[last[2]]), tz="UTC"),
        "exit_idx": last[2],
        "direction": direction,
        "entry": entry,
        "sl": sl,
        "exit": sum(f * p for f, p, _, _ in pieces),
        "risk_pips": risk / pip,
        "spread_entry_pips": (mk.ask_o[i0] - mk.bid_o[i0]) / pip,
        "nights": nights_w,
        "swap_R": swap_price / risk,
        "R": pnl / risk,
        "exit_reason": "+".join(p[3] for p in pieces),
    }


def run_backtest(mk: Market, signals: pd.DataFrame, exit_mode: str = "simple", rr: float = RR_TARGET,
                 max_entry_delay: pd.Timedelta = pd.Timedelta(minutes=15),
                 max_hold: pd.Timedelta | None = None,
                 news_times: np.ndarray | None = None,
                 news_window: pd.Timedelta = pd.Timedelta(minutes=30)) -> pd.DataFrame:
    """Exécute une liste de signaux (colonnes : signal_time, direction, sl) sur une paire.

    `news_times` : instants UTC (int64 ns, triés) des annonces à fort impact ; aucune entrée
    à moins de `news_window` d'une annonce.
    """
    rows = []
    last_exit = -1
    sig = signals.sort_values("signal_time")
    for s in sig.itertuples(index=False):
        st = pd.Timestamp(s.signal_time).value
        i0 = int(np.searchsorted(mk.t, st, side="left"))
        if i0 >= len(mk.t) or i0 <= last_exit:
            continue
        if mk.t[i0] - st > max_entry_delay.value:
            continue
        if news_times is not None and len(news_times):
            p = np.searchsorted(news_times, mk.t[i0])
            near = [news_times[q] for q in (p - 1, p) if 0 <= q < len(news_times)]
            if any(abs(int(mk.t[i0]) - int(x)) <= news_window.value for x in near):
                continue
        max_hold_idx = None
        if max_hold is not None:
            max_hold_idx = int(np.searchsorted(mk.t, mk.t[i0] + max_hold.value, side="left")) + 1
        tr = simulate_trade(mk, i0, int(s.direction), float(s.sl), exit_mode, rr, max_hold_idx)
        if tr is None:
            continue
        tr["pair"] = mk.pair
        tr["signal_time"] = pd.Timestamp(s.signal_time)
        rows.append(tr)
        last_exit = tr["exit_idx"]
    cols = ["pair", "signal_time", "entry_time", "exit_time", "direction", "entry", "sl", "exit",
            "risk_pips", "spread_entry_pips", "nights", "swap_R", "R", "exit_reason"]
    return pd.DataFrame(rows, columns=cols + ["exit_idx"]).drop(columns="exit_idx")
