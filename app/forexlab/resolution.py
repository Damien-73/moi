"""Résolution des détections — SPEC-LOT2 §6.2 et §6.3.

Règle conservatrice non négociable : quand l'objectif et l'invalidation sont
touchés à l'intérieur de la même bougie M1, l'ordre réel est inconnaissable.
L'issue est alors TOUJOURS comptée comme invalidation, et le cas est marqué.

Choisir l'inverse, ou tirer au sort, gonflerait les taux de réussite d'une
manière invérifiable. C'est ce qui rend flatteurs la quasi-totalité des
backtests amateurs.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from . import couts


@dataclass(frozen=True)
class Issue:
    resultat: str          # 'atteint' | 'invalide' | 'sans_issue'
    sortie_ts: datetime
    prix_sortie: float
    ambigu_m1: bool
    cout_spread: float
    cout_glissement: float
    cout_portage: float    # positif = payé par le trader
    r_brut: float
    r_net: float
    excursion_fav: float   # en R, ≥ 0
    excursion_def: float   # en R, ≤ 0


def resoudre(m1, symbole, sens, entree_ts, entree, invalidation, objectif,
             fin_ts, grille=None) -> Issue | None:
    """Parcourt les bougies M1 de `entree_ts` (exclu) à `fin_ts` (inclus).

    `sens` vaut +1 à l'achat, −1 à la vente.
    """
    risque = abs(entree - invalidation)
    if risque <= 0:
        return None

    fenetre = [b for b in m1 if entree_ts < b["ts"] <= fin_ts]
    if not fenetre:
        return None

    resultat, ambigu = "sans_issue", False
    sortie_ts, prix_sortie = fenetre[-1]["ts"], fenetre[-1]["c"]
    mfe = mae = 0.0

    for b in fenetre:
        if sens > 0:
            mfe = max(mfe, b["h"] - entree)
            mae = min(mae, b["l"] - entree)
            touche_stop = b["l"] <= invalidation
            touche_cible = b["h"] >= objectif
        else:
            mfe = max(mfe, entree - b["l"])
            mae = min(mae, entree - b["h"])
            touche_stop = b["h"] >= invalidation
            touche_cible = b["l"] <= objectif

        if touche_stop and touche_cible:
            resultat, ambigu = "invalide", True       # règle conservatrice
        elif touche_stop:
            resultat = "invalide"
        elif touche_cible:
            resultat = "atteint"

        if resultat != "sans_issue":
            sortie_ts = b["ts"]
            prix_sortie = invalidation if resultat == "invalide" else objectif
            break

    cout_spread = couts.spread(symbole, entree_ts, grille)       # aller-retour
    cout_gliss = (couts.glissement(symbole, sortie_ts, grille)
                  if resultat == "invalide" else 0.0)
    # portage_total est signé : positif = reçu. On le stocke en coût, donc inversé.
    cout_portage = -couts.portage_total(symbole, sens, entree, entree_ts, sortie_ts)

    brut = (prix_sortie - entree) * sens
    net = brut - cout_spread - cout_gliss - cout_portage

    return Issue(resultat, sortie_ts, prix_sortie, ambigu,
                 cout_spread, cout_gliss, cout_portage,
                 brut / risque, net / risque, mfe / risque, mae / risque)
