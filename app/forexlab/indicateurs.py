"""Indicateurs — définitions exactes de SPEC-LOT2 §1.2.

Toutes les fonctions retournent une liste de la même longueur que l'entrée,
avec None tant que l'amorçage n'est pas atteint. Aucune valeur n'est jamais
calculée à partir d'une bougie postérieure.
"""
from __future__ import annotations


def true_range(h, l, c_prec):
    return max(h - l, abs(h - c_prec), abs(l - c_prec))


def atr(hauts, bas, clotures, periode: int = 14):
    """ATR de Wilder. Amorçage : moyenne arithmétique des `periode` premiers TR."""
    n = len(clotures)
    out = [None] * n
    if n <= periode:
        return out
    trs = [None]
    for i in range(1, n):
        trs.append(true_range(hauts[i], bas[i], clotures[i - 1]))
    valeur = sum(trs[1: periode + 1]) / periode
    out[periode] = valeur
    for i in range(periode + 1, n):
        valeur = ((periode - 1) * valeur + trs[i]) / periode
        out[i] = valeur
    return out


def ema(valeurs, periode: int):
    """Moyenne mobile exponentielle. Amorçage : moyenne des `periode` premières."""
    n = len(valeurs)
    out = [None] * n
    if n < periode:
        return out
    alpha = 2.0 / (periode + 1)
    courant = sum(valeurs[:periode]) / periode
    out[periode - 1] = courant
    for i in range(periode, n):
        courant = alpha * valeurs[i] + (1 - alpha) * courant
        out[i] = courant
    return out


def rsi(clotures, periode: int = 14):
    """RSI de Wilder."""
    n = len(clotures)
    out = [None] * n
    if n <= periode:
        return out
    gains, pertes = [0.0], [0.0]
    for i in range(1, n):
        d = clotures[i] - clotures[i - 1]
        gains.append(max(d, 0.0))
        pertes.append(max(-d, 0.0))
    mg = sum(gains[1: periode + 1]) / periode
    mp = sum(pertes[1: periode + 1]) / periode
    out[periode] = 100.0 if mp == 0 else 100 - 100 / (1 + mg / mp)
    for i in range(periode + 1, n):
        mg = ((periode - 1) * mg + gains[i]) / periode
        mp = ((periode - 1) * mp + pertes[i]) / periode
        out[i] = 100.0 if mp == 0 else 100 - 100 / (1 + mg / mp)
    return out


def adx(hauts, bas, clotures, periode: int = 14):
    """ADX de Wilder. Sert au critère de régime de marché (SPEC-LOT2 §5.2, n° 11)."""
    n = len(clotures)
    out = [None] * n
    if n < 2 * periode + 1:
        return out
    trs, dm_plus, dm_moins = [0.0], [0.0], [0.0]
    for i in range(1, n):
        trs.append(true_range(hauts[i], bas[i], clotures[i - 1]))
        haut = hauts[i] - hauts[i - 1]
        bas_ = bas[i - 1] - bas[i]
        dm_plus.append(haut if (haut > bas_ and haut > 0) else 0.0)
        dm_moins.append(bas_ if (bas_ > haut and bas_ > 0) else 0.0)
    str_ = sum(trs[1: periode + 1])
    sdp = sum(dm_plus[1: periode + 1])
    sdm = sum(dm_moins[1: periode + 1])
    dxs = []
    for i in range(periode + 1, n):
        str_ = str_ - str_ / periode + trs[i]
        sdp = sdp - sdp / periode + dm_plus[i]
        sdm = sdm - sdm / periode + dm_moins[i]
        if str_ == 0:
            dxs.append(0.0)
            continue
        dip, dim = 100 * sdp / str_, 100 * sdm / str_
        somme = dip + dim
        dxs.append(0.0 if somme == 0 else 100 * abs(dip - dim) / somme)
        if len(dxs) == periode:
            out[i] = sum(dxs) / periode
        elif len(dxs) > periode:
            out[i] = ((periode - 1) * out[i - 1] + dxs[-1]) / periode
    return out
