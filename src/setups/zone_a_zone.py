"""Setup 1 « zone à zone » H1 — implémentation de docs/setups/zone_a_zone.md.

Détection déterministe sur bougies H1 clôturées (prix milieu). Même entrée -> même sortie.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import RR_TARGET

NAME = "zone_a_zone"
PARAMS = {"k": 3, "w": 0.5, "b": 0.2, "n": 14}


def atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, n: int) -> np.ndarray:
    prev_c = np.r_[np.nan, c[:-1]]
    tr = np.fmax(h, prev_c) - np.fmin(l, prev_c)
    tr[0] = h[0] - l[0]
    out = pd.Series(tr).rolling(n, min_periods=n).mean().to_numpy(copy=True)
    out[:n] = np.nan  # règle « t >= n »
    return out


def detect(bars: pd.DataFrame, k: int = 3, w: float = 0.5, b: float = 0.2, n: int = 14,
           rr: float = RR_TARGET) -> pd.DataFrame:
    """bars : H1 en prix milieu, colonnes o, h, l, c, close_time (index = open_time).

    Retourne les signaux : signal_time (= close_time de la bougie), direction (+1/-1), sl.
    """
    H = bars["h"].to_numpy(dtype=float)
    L = bars["l"].to_numpy(dtype=float)
    C = bars["c"].to_numpy(dtype=float)
    A = atr(H, L, C, n)
    close_time = bars["close_time"].to_numpy()

    # zones actives : tableaux [bas, haut]
    dem = np.empty((0, 2))
    sup = np.empty((0, 2))
    out = []
    for t in range(len(C)):
        # --- 1. signal sur la bougie t, avec les zones actives au début de t
        long_sig = short_sig = None
        if not np.isnan(A[t]):
            if len(dem):
                touched = L[t] <= dem[:, 1]
                if touched.any():
                    z = dem[touched][np.argmax(dem[touched, 1])]
                    if C[t] > z[1]:
                        sl = z[0] - b * A[t]
                        r_est = C[t] - sl
                        above = sup[sup[:, 0] > C[t], 0] if len(sup) else np.empty(0)
                        if len(above) == 0 or above.min() - C[t] >= rr * r_est:
                            long_sig = sl
            if len(sup):
                touched = H[t] >= sup[:, 0]
                if touched.any():
                    z = sup[touched][np.argmin(sup[touched, 0])]
                    if C[t] < z[0]:
                        sl = z[1] + b * A[t]
                        r_est = sl - C[t]
                        below = dem[dem[:, 1] < C[t], 1] if len(dem) else np.empty(0)
                        if len(below) == 0 or C[t] - below.max() >= rr * r_est:
                            short_sig = sl
        if (long_sig is None) != (short_sig is None):
            d, sl = (1, long_sig) if long_sig is not None else (-1, short_sig)
            out.append((close_time[t], d, sl))

        # --- 2. cycle de vie : zones touchées (consommées) ou cassées
        if len(dem):
            dem = dem[~((L[t] <= dem[:, 1]) | (C[t] < dem[:, 0]))]
        if len(sup):
            sup = sup[~((H[t] >= sup[:, 0]) | (C[t] > sup[:, 1]))]

        # --- 3. zones confirmées à la clôture de t (pivot en i = t - k), actives dès t + 1
        i = t - k
        if i >= k and not np.isnan(A[t]):
            if L[i] < L[i - k:i].min() and L[i] <= L[i + 1:t + 1].min():
                dem = np.vstack([dem, [L[i], L[i] + w * A[t]]])
            if H[i] > H[i - k:i].max() and H[i] >= H[i + 1:t + 1].max():
                sup = np.vstack([sup, [H[i] - w * A[t], H[i]]])

    sig = pd.DataFrame(out, columns=["signal_time", "direction", "sl"])
    sig["signal_time"] = pd.to_datetime(sig["signal_time"], utc=True)
    return sig
