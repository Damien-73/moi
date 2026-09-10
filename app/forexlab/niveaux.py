"""Niveaux de référence et zones — SPEC-LOT2 §5.2, critères 2 à 4."""
from __future__ import annotations

from datetime import timedelta

from .parametres import SCORE_V1 as S


def zones(pivots, t, atr, fenetre=500):
    """Regroupe les pivots confirmés en niveaux. Un niveau exige ≥ 3 pivots."""
    connus = [p for p in pivots if p.confirmation <= t and p.barreau >= t - fenetre]
    if not connus:
        return []
    prix = sorted(p.prix for p in connus)
    fuseau = S["ZONE_FUSEAU"] * atr
    groupes, courant = [], [prix[0]]
    for x in prix[1:]:
        if x - courant[0] <= fuseau:
            courant.append(x)
        else:
            groupes.append(courant)
            courant = [x]
    groupes.append(courant)
    return [sum(g) / len(g) for g in groupes if len(g) >= S["ZONE_TOUCHES_MIN"]]


def niveau_rond(prix, pas):
    """Distance au multiple de `pas` le plus proche."""
    k = round(prix / pas)
    return abs(prix - k * pas)


def references(d1, ts):
    """Plus haut, plus bas et clôture de la veille, extrêmes de la semaine
    précédente, ouverture du jour. Uniquement des bougies déjà clôturées."""
    passees = [b for b in d1 if b["ts"] < ts]
    if not passees:
        return []
    out = []
    veille = passees[-1]
    out += [veille["h"], veille["l"], veille["c"]]
    semaine = [b for b in passees if b["ts"] >= veille["ts"] - timedelta(days=7)]
    if semaine:
        out += [max(b["h"] for b in semaine), min(b["l"] for b in semaine)]
    ouverture = [b for b in d1 if b["ts"] <= ts]
    if ouverture:
        out.append(ouverture[-1]["o"])
    return out
