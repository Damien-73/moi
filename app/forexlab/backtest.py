"""Backtest honnête — SPEC-LOT2, lot 2 comme point de décision.

Un backtest ne prouve rien à un client. Il sert à UNE chose : décider s'il faut
continuer. Encore faut-il qu'il ne se mente pas à lui-même.

Deux protections, toutes deux obligatoires :

  1. VALIDATION SÉQUENTIELLE (walk-forward). On calibre le seuil sur le passé,
     on l'évalue sur la période SUIVANTE, jamais sur la même. L'écart entre les
     deux est la mesure directe du surajustement.

  2. RATIO DE SHARPE DÉFLATÉ (Bailey & López de Prado). Tester 144 séries fait
     mécaniquement ressortir la meilleure. Le déflatage retire cet effet.
"""
from __future__ import annotations

import math

GAMMA = 0.5772156649015329          # constante d'Euler-Mascheroni


def _phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _phi_inverse(p):
    """Quantile de la loi normale centrée réduite (Acklam)."""
    if not 0 < p < 1:
        return float("-inf") if p <= 0 else float("inf")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl, ph = 0.02425, 1 - 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > ph:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q, r = p - 0.5, (p - 0.5) ** 2
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def _moments(rs):
    n = len(rs)
    m = sum(rs) / n
    v = sum((x - m) ** 2 for x in rs) / n
    s = math.sqrt(v)
    if s == 0:
        return m, 0.0, 0.0, 3.0
    g3 = sum((x - m) ** 3 for x in rs) / n / s ** 3
    g4 = sum((x - m) ** 4 for x in rs) / n / s ** 4
    return m, s, g3, g4


def sharpe(rs):
    """Sharpe par trade, non annualisé : le nombre de trades est ce qui compte."""
    if len(rs) < 2:
        return 0.0
    m, s, _, _ = _moments(rs)
    return m / s if s else 0.0


def sharpe_deflate(rs, essais, variance_sharpe=None):
    """Probabilité que le Sharpe observé ne soit PAS un artefact du test multiple.

    `essais` = nombre de séries réellement testées. Le déclarer honnêtement est
    tout l'enjeu : le sous-estimer revient à truquer le résultat.
    """
    n = len(rs)
    if n < 10 or essais < 1:
        return {"suffisant": False, "n": n}
    sr = sharpe(rs)
    _, _, g3, g4 = _moments(rs)
    v = variance_sharpe if variance_sharpe is not None else 1.0 / n
    e = math.e
    if essais > 1:
        sr0 = math.sqrt(v) * ((1 - GAMMA) * _phi_inverse(1 - 1 / essais)
                              + GAMMA * _phi_inverse(1 - 1 / (essais * e)))
    else:
        sr0 = 0.0
    denom = 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2
    if denom <= 0:
        return {"suffisant": False, "n": n, "sharpe": sr}
    z = (sr - sr0) * math.sqrt(n - 1) / math.sqrt(denom)
    return {"suffisant": True, "n": n, "sharpe": sr, "sharpe_seuil": sr0,
            "dsr": _phi(z), "essais": essais,
            "significatif": _phi(z) > 0.95}


def walk_forward(lignes, cible="methode", plis=5, seuils=None):
    """Calibre le seuil de score sur le passé, l'évalue sur la période suivante.

    LIRE `esperance_hors_echantillon`, PAS `degradation`. Mesuré à
    l'exécution : la dégradation absolue ne discrimine rien, parce qu'un score
    réellement prédictif part de plus haut et dégrade donc davantage en valeur
    absolue qu'un score de bruit. Le seul critère qui sépare les deux est
    CE QUI SURVIT hors échantillon.

    `degradation` reste publiée pour information, jamais comme critère.
    """
    ordonnees = sorted((l for l in lignes if l.issues.get(cible)),
                       key=lambda l: l.entree_ts)
    n = len(ordonnees)
    if n < plis * 40:
        return {"suffisant": False, "n": n, "requis": plis * 40}
    seuils = seuils or [i / 20 for i in range(0, 19)]
    taille = n // (plis + 1)
    resultats = []

    for k in range(plis):
        calib = ordonnees[:taille * (k + 1)]
        test = ordonnees[taille * (k + 1):taille * (k + 2)]
        if len(test) < 20:
            continue
        meilleur, esp_in = None, None
        for s in seuils:
            sel = [l.issues[cible]["r_net"] for l in calib
                   if l.score_normalise >= s]
            if len(sel) < 30:
                continue
            e = sum(sel) / len(sel)
            if esp_in is None or e > esp_in:
                meilleur, esp_in = s, e
        if meilleur is None:
            continue
        hors = [l.issues[cible]["r_net"] for l in test if l.score_normalise >= meilleur]
        if len(hors) < 10:
            continue
        resultats.append({"pli": k + 1, "seuil": meilleur,
                          "esperance_calibree": esp_in,
                          "esperance_hors_echantillon": sum(hors) / len(hors),
                          "n_calibration": len(calib), "n_test": len(hors)})

    if not resultats:
        return {"suffisant": False, "n": n, "raison": "aucun pli exploitable"}
    ins = sum(r["esperance_calibree"] for r in resultats) / len(resultats)
    outs = sum(r["esperance_hors_echantillon"] for r in resultats) / len(resultats)
    seuils_retenus = [r["seuil"] for r in resultats]
    return {
        "suffisant": True, "plis": resultats,
        "esperance_calibree": ins,
        "esperance_hors_echantillon": outs,
        "degradation": ins - outs,
        "seuil_stable": max(seuils_retenus) - min(seuils_retenus) <= 0.15,
        "seuils": seuils_retenus,
    }


def rapport_decision(lignes, series_testees, cible="methode"):
    """Le rapport du point de décision du lot 2 (cahier des charges §28.1)."""
    rs = [l.issues[cible]["r_net"] for l in lignes if l.issues.get(cible)]
    if len(rs) < 30:
        return {"verdict": "insuffisant", "n": len(rs)}
    esperance = sum(rs) / len(rs)
    d = sharpe_deflate(rs, series_testees)
    wf = walk_forward(lignes, cible)

    if esperance <= -0.05:
        verdict = "negatif"
        conduite = ("Le produit devient l'outil qui chiffre ce que l'analyse "
                    "technique coûte réellement. Position unique et vendable.")
    elif esperance < 0.02 or not d.get("significatif"):
        verdict = "nul"
        conduite = ("Basculer sur le discours comparatif et l'analyse "
                    "comportementale. Ne pas annoncer d'avantage.")
    else:
        verdict = "positif"
        conduite = ("Le discours « quelles configurations gagnent » est tenable, "
                    "sous réserve que la validation séquentielle confirme.")
    return {"verdict": verdict, "esperance": esperance, "n": len(rs),
            "deflate": d, "walk_forward": wf, "conduite": conduite}
