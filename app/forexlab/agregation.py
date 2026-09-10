"""Agrégation M1 vers H1, H4 et D1 — SPEC-LOT2 §1.1.

Aucun agrégat n'est repris d'un fournisseur : tout est reconstruit depuis M1,
seule façon de garantir la même convention sur tout l'historique.
"""
from __future__ import annotations

from datetime import datetime

from .calendrier import debut_bougie


def agreger(bougies_m1, unite: str):
    """bougies_m1 : liste de dicts {ts, o, h, l, c} triés par ts croissant.

    Retourne la liste des bougies agrégées, chacune portant `complete` :
    une bougie est incomplète si elle contient moins de minutes que prévu.
    """
    if unite == "M1":
        return list(bougies_m1)
    attendu = {"H1": 60, "H4": 240, "D1": 1440}[unite]
    seaux: dict[datetime, dict] = {}
    ordre: list[datetime] = []
    for b in bougies_m1:
        cle = debut_bougie(b["ts"], unite)
        s = seaux.get(cle)
        if s is None:
            s = {"ts": cle, "o": b["o"], "h": b["h"], "l": b["l"],
                 "c": b["c"], "minutes": 0}
            seaux[cle] = s
            ordre.append(cle)
        s["h"] = max(s["h"], b["h"])
        s["l"] = min(s["l"], b["l"])
        s["c"] = b["c"]
        s["minutes"] += 1
    sortie = []
    for cle in ordre:
        s = seaux[cle]
        # Le marché est fermé une partie du week-end : on ne peut pas exiger
        # 1440 minutes sur toutes les journées. Le seuil est un ratio.
        s["complete"] = s["minutes"] >= 0.90 * attendu if unite != "D1" else s["minutes"] >= 0.70 * attendu
        sortie.append(s)
    return sortie
