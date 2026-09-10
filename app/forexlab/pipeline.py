"""Chaîne complète : bougies → détections → score → issues → registre."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from datetime import timedelta

from . import (agregation, calendrier_eco, figures, indicateurs, pivots,
               range_v1, registre, resolution, score)
from .parametres import RANGE_V1 as R

DUREES = {"H1": timedelta(hours=1), "H4": timedelta(hours=4), "D1": timedelta(days=1)}


@dataclass
class Ligne:
    symbole: str
    unite: str
    figure: str
    methode: str
    sens: int
    entree_ts: object
    entree: float
    invalidation: float
    objectif: float
    objectif_1r5: float
    objectif_2r: float
    score_points: int
    score_max: int
    score_normalise: float
    statut: str
    motif_rejet: str
    detail: dict
    issues: dict
    empreinte: str


def _serie(bougies):
    return ([b["h"] for b in bougies], [b["l"] for b in bougies],
            [b["c"] for b in bougies])


def contexte(symbole, unite, bougies, uts_bougies, d1, calendrier, pas_rond):
    h, l, c = _serie(bougies)
    atrs = indicateurs.atr(h, l, c, R["ATR_PERIODE"])
    uh, ul, uc = _serie(uts_bougies)
    uatrs = indicateurs.atr(uh, ul, uc, R["ATR_PERIODE"])
    return score.Contexte(
        symbole=symbole, unite=unite, bougies=bougies, atrs=atrs,
        rsis=indicateurs.rsi(c, 14), adxs=indicateurs.adx(h, l, c, 14),
        ema20=indicateurs.ema(c, 20),
        pivots=pivots.detecter_pivots(h, l, atrs),
        uts_bougies=uts_bougies,
        uts_ema200=indicateurs.ema(uc, 200) if len(uc) >= 200 else [None] * len(uc),
        uts_atrs=uatrs,
        uts_pivots=pivots.detecter_pivots(uh, ul, uatrs),
        d1=d1, calendrier=calendrier, pas_rond=pas_rond)


def executer(symbole, unite, bougies, m1, uts_bougies, d1,
             calendrier=None, pas_rond=0.0050, grille=None, catalogue=True):
    """Produit les lignes complètes, résolues, prêtes à être enregistrées.

    `catalogue` ajoute toutes les figures de SPEC-FIGURES au range.
    """
    ctx = contexte(symbole, unite, bougies, uts_bougies, d1,
                   calendrier or calendrier_eco.Calendrier(), pas_rond)
    ranges, detections = range_v1.detecter(bougies, ctx.pivots, ctx.atrs)
    if catalogue:
        c = [b["c"] for b in bougies]
        detections = detections + figures.toutes(
            bougies, ctx.pivots, ctx.atrs,
            indicateurs.ema(c, 20), indicateurs.ema(c, 50))
        detections.sort(key=lambda d: (d.barreau, d.methode, d.sens))
    duree = DUREES[unite]
    lignes = []

    for det in detections:
        rng = ranges[det.range_id] if 0 <= det.range_id < len(ranges) else None
        neutr = figures.NEUTRALISES.get(det.figure, ())
        sc = score.evaluer(ctx, det, rng, neutralises=neutr)
        entree_ts = bougies[det.barreau]["ts"] + duree
        fin_ts = entree_ts + duree * R["HORIZON"]
        risque = abs(det.entree - det.invalidation)
        o15 = det.entree + det.sens * 1.5 * risque
        o20 = det.entree + det.sens * 2.0 * risque

        issues = {}
        for nom, cible in (("methode", det.objectif), ("1r5", o15), ("2r", o20)):
            iss = resolution.resoudre(m1, symbole, det.sens, entree_ts, det.entree,
                                      det.invalidation, cible, fin_ts, grille)
            issues[nom] = asdict(iss) if iss else None

        statut = "annoncee" if sc.annoncee else "ecartee"
        motif = "" if sc.annoncee else (
            ";".join(sc.filtres) if sc.filtres else "score_insuffisant")
        emp = registre.feuille(
            version=f'{det.figure}.v1', symbole=symbole, unite=unite, sens=det.sens,
            entree_ts=entree_ts, entree=det.entree, invalidation=det.invalidation,
            objectif_methode=det.objectif, objectif_1r5=o15, objectif_2r=o20,
            horizon=R["HORIZON"], score_points=sc.points, score_max=sc.maximum,
            statut=statut, motif_rejet=motif)

        lignes.append(Ligne(symbole, unite, det.figure, det.methode, det.sens, entree_ts,
                            det.entree, det.invalidation, det.objectif, o15, o20,
                            sc.points, sc.maximum, sc.normalise, statut, motif,
                            sc.detail, issues, emp))
    return ranges, lignes


def statistiques(lignes, cible="methode"):
    """Agrégat élémentaire — SPEC-LOTS-6-15 §9.1. Aucun chiffre sous 100 occurrences."""
    rs = [l.issues[cible]["r_net"] for l in lignes
          if l.issues.get(cible) is not None]
    n = len(rs)
    if n == 0:
        return {"n": 0, "publiable": False, "statut": "insuffisant"}
    moy = sum(rs) / n
    var = sum((x - moy) ** 2 for x in rs) / (n - 1) if n > 1 else 0.0
    et = math.sqrt(var)
    res = [l.issues[cible]["resultat"] for l in lignes if l.issues.get(cible)]
    return {
        "n": n,
        "esperance": moy,
        "ecart_type": et,
        "ic95": 1.96 * et / math.sqrt(n) if n else 0.0,
        "atteint": res.count("atteint") / n,
        "invalide": res.count("invalide") / n,
        "sans_issue": res.count("sans_issue") / n,
        "ambigu": sum(1 for l in lignes if l.issues.get(cible)
                      and l.issues[cible]["ambigu_m1"]) / n,
        "publiable": n >= 100,
        "statut": "établi" if n >= 400 else ("provisoire" if n >= 100 else "insuffisant"),
    }
