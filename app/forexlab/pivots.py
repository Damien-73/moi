"""Détection des pivots — SPEC-LOT2 §2.

LA RÈGLE QUI DÉCIDE DE LA VALIDITÉ DE TOUT LE SYSTÈME
-----------------------------------------------------
Un pivot situé au barreau `p` n'existe qu'à partir du barreau `c` où il est
confirmé, avec c > p. Le graphique l'affiche à `p`, ce qui donne l'illusion
qu'il était connu à ce moment : il ne l'était pas.

Chaque pivot porte donc DEUX indices. Toute détection au barreau t ne doit
utiliser que les pivots dont `confirmation <= t`. C'est l'erreur la plus
répandue des systèmes chartistes automatisés, et elle rend les résultats
spectaculaires et faux.
"""
from __future__ import annotations

from dataclasses import dataclass

ZZ_K = 1.5  # seuil ZigZag, en multiples d'ATR


@dataclass(frozen=True)
class Pivot:
    type: str        # 'haut' ou 'bas'
    barreau: int     # p — où se situe le pivot
    confirmation: int  # c — où il devient connaissable (toujours > p)
    prix: float

    def connu_a(self, t: int) -> bool:
        return self.confirmation <= t


def detecter_pivots(hauts, bas, atrs, k: float = ZZ_K, amorcage: int = 0):
    """ZigZag à seuil adaptatif. Retourne la liste des pivots confirmés."""
    n = len(hauts)
    pivots: list[Pivot] = []
    depart = amorcage
    while depart < n and atrs[depart] is None:
        depart += 1
    if depart >= n:
        return pivots

    etat = "recherche_haut" if hauts[depart] - bas[depart] >= 0 else "recherche_bas"
    extreme = hauts[depart]
    i_extreme = depart
    if etat == "recherche_bas":
        extreme = bas[depart]

    for i in range(depart + 1, n):
        seuil = k * atrs[i] if atrs[i] is not None else None
        if seuil is None:
            continue
        if etat == "recherche_haut":
            if hauts[i] > extreme:
                extreme, i_extreme = hauts[i], i
            elif extreme - bas[i] >= seuil:
                pivots.append(Pivot("haut", i_extreme, i, extreme))
                etat, extreme, i_extreme = "recherche_bas", bas[i], i
        else:
            if bas[i] < extreme:
                extreme, i_extreme = bas[i], i
            elif hauts[i] - extreme >= seuil:
                pivots.append(Pivot("bas", i_extreme, i, extreme))
                etat, extreme, i_extreme = "recherche_haut", hauts[i], i
    return pivots


def pivots_connus(pivots, t: int):
    """Sous-ensemble utilisable au barreau t. À utiliser SYSTÉMATIQUEMENT."""
    return [p for p in pivots if p.connu_a(t)]
