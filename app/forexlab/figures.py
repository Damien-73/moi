"""Catalogue des figures — SPEC-FIGURES.md.

Chaque figure est une version de stratégie distincte. Toutes les conditions ne
portent que sur des pivots CONFIRMÉS au barreau d'évaluation.

Les critères que la construction d'une figure satisfait d'office sont déclarés
dans NEUTRALISES : sans cela, les figures de continuation seraient mécaniquement
mieux notées que les figures de retournement (SPEC-FIGURES §2, CDC §11.7).
"""
from __future__ import annotations

from .range_v1 import Detection

C = {
    "TOL_NIVEAU": 0.25, "AMPLITUDE_MIN": 1.0, "CASSURE_MIN": 0.25,
    "STOP_MARGE": 0.50, "L_MIN": 10, "L_MAX": 200, "RETOUR_MAX": 10,
    "TETE_MIN": 0.50, "EPAULES_TOL": 0.50, "PENTE_ENCOLURE_MAX": 0.75,
    "IMPULSION_MIN": 3.0, "IMPULSION_BARRES": 10, "DRAPEAU_MIN": 5,
    "DRAPEAU_MAX": 20, "DRAPEAU_LARGEUR": 1.5, "RETRACEMENT_MAX": 0.5,
    "TRIANGLE_PIVOTS": 4, "NIVEAU_TOUCHES": 3, "NIVEAU_FUSEAU": 0.50,
    "PULLBACK_TOL": 0.30, "AMORCAGE": 300,
}

# Critères du score satisfaits par construction, donc neutralisés et retirés
# du maximum atteignable.
NEUTRALISES = {
    "range": ("zone",),
    "double_creux": ("zone",), "double_sommet": ("zone",),
    "ete": (), "ete_inversee": ("zone",),
    "triangle_asc": ("zone",), "triangle_desc": ("zone",),
    "triangle_sym": (),
    "drapeau": ("tendance",),
    "cassure_niveau": ("zone",),
    "pullback_tendance": ("tendance",),
}


def _connus(pivots, t):
    return [p for p in pivots if p.confirmation <= t]


def _emettre(figure, sens, t, entree, inval, objectif, a, methodes=("M1",)):
    return [Detection(f"{figure}.{m}", sens, t, entree, inval, objectif, -1, a, figure)
            for m in methodes]


# ─────────────────────────── retournements ───────────────────────────

def double_extreme(bougies, pivots, atrs, sens):
    """Double creux (sens=+1) ou double sommet (sens=−1) — SPEC-FIGURES §2.1."""
    figure = "double_creux" if sens > 0 else "double_sommet"
    cible = "bas" if sens > 0 else "haut"
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a = atrs[t]
        if a is None:
            continue
        ps = _connus(pivots, t)
        if len(ps) < 3:
            continue
        p1, p2, p3 = ps[-3:]
        if not (p1.type == cible and p2.type != cible and p3.type == cible):
            continue
        if abs(p3.prix - p1.prix) > C["TOL_NIVEAU"] * a:
            continue
        extreme = min(p1.prix, p3.prix) if sens > 0 else max(p1.prix, p3.prix)
        amplitude = (p2.prix - extreme) * sens
        if amplitude < C["AMPLITUDE_MIN"] * a:
            continue
        L = p3.barreau - p1.barreau
        if not (C["L_MIN"] <= L <= C["L_MAX"]):
            continue
        encolure = p2.prix
        if (clot[t] - encolure) * sens < C["CASSURE_MIN"] * a:
            continue
        if t > 0 and (clot[t - 1] - encolure) * sens >= C["CASSURE_MIN"] * a:
            continue                                    # cassure déjà émise
        out += _emettre(figure, sens, t, clot[t],
                        extreme - C["STOP_MARGE"] * a * sens,
                        encolure + (encolure - extreme), a, ("M1", "M3"))
    return out


def epaule_tete_epaule(bougies, pivots, atrs, sens):
    """ETE (sens=−1) et ETE inversée (sens=+1) — SPEC-FIGURES §2.3.

    Deux invalidations mesurées séparément : au sommet de la tête (large) ou au
    sommet de l'épaule droite (serrée). Débat de trente ans, jamais chiffré.
    """
    figure = "ete_inversee" if sens > 0 else "ete"
    t_ext = "bas" if sens > 0 else "haut"
    o_ext = "haut" if sens > 0 else "bas"
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a = atrs[t]
        if a is None:
            continue
        ps = _connus(pivots, t)
        if len(ps) < 5:
            continue
        p1, p2, p3, p4, p5 = ps[-5:]
        if [p.type for p in (p1, p2, p3, p4, p5)] != [t_ext, o_ext, t_ext, o_ext, t_ext]:
            continue
        # tête dominante
        tete_domine = ((min(p1.prix, p5.prix) - p3.prix) if sens > 0
                       else (p3.prix - max(p1.prix, p5.prix)))
        if tete_domine < C["TETE_MIN"] * a:
            continue
        if abs(p5.prix - p1.prix) > C["EPAULES_TOL"] * a:
            continue
        if abs(p4.prix - p2.prix) > C["PENTE_ENCOLURE_MAX"] * a:
            continue
        d1 = p3.barreau - p1.barreau
        d2 = p5.barreau - p3.barreau
        if d1 <= 0 or not (0.5 <= d2 / d1 <= 2.0):
            continue
        encolure = (p2.prix + p4.prix) / 2
        if (clot[t] - encolure) * sens < C["CASSURE_MIN"] * a:
            continue
        if t > 0 and (clot[t - 1] - encolure) * sens >= C["CASSURE_MIN"] * a:
            continue
        objectif = encolure + (encolure - p3.prix)
        out += _emettre(figure + ".large", sens, t, clot[t],
                        p3.prix - C["STOP_MARGE"] * a * sens, objectif, a, ("M1",))
        out += _emettre(figure + ".serree", sens, t, clot[t],
                        p5.prix - C["STOP_MARGE"] * a * sens, objectif, a, ("M1",))
    return out


# ─────────────────────────── continuations ───────────────────────────

def triangle(bougies, pivots, atrs, sens):
    """Triangle ascendant (+1) : sommets alignés, creux croissants. — §3.2"""
    figure = "triangle_asc" if sens > 0 else "triangle_desc"
    plat = "haut" if sens > 0 else "bas"
    mobile = "bas" if sens > 0 else "haut"
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a = atrs[t]
        if a is None:
            continue
        ps = _connus(pivots, t)
        if len(ps) < C["TRIANGLE_PIVOTS"]:
            continue
        der = ps[-C["TRIANGLE_PIVOTS"]:]
        plats = [p for p in der if p.type == plat]
        mobiles = [p for p in der if p.type == mobile]
        if len(plats) < 2 or len(mobiles) < 2:
            continue
        moy = sum(p.prix for p in plats) / len(plats)
        if any(abs(p.prix - moy) > C["TOL_NIVEAU"] * a for p in plats):
            continue
        # les creux (ou sommets) doivent converger vers le niveau plat
        ok = all((b.prix - x.prix) * sens > 0
                 for x, b in zip(mobiles, mobiles[1:]))
        if not ok:
            continue
        largeur = abs(moy - mobiles[0].prix)
        if largeur < C["AMPLITUDE_MIN"] * a:
            continue
        L = der[-1].barreau - der[0].barreau
        if not (C["L_MIN"] <= L <= C["L_MAX"]):
            continue
        if (clot[t] - moy) * sens < C["CASSURE_MIN"] * a:
            continue
        if t > 0 and (clot[t - 1] - moy) * sens >= C["CASSURE_MIN"] * a:
            continue
        out += _emettre(figure, sens, t, clot[t],
                        mobiles[-1].prix - C["STOP_MARGE"] * a * sens,
                        moy + largeur * sens, a, ("M1", "M3"))
    return out


def drapeau(bougies, pivots, atrs, sens):
    """Impulsion franche, puis consolidation contre-tendance — §3.4.

    Critère de tendance NEUTRALISÉ : la figure n'existe que dans une tendance.
    """
    haut = [b["h"] for b in bougies]
    bas = [b["l"] for b in bougies]
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a = atrs[t]
        if a is None:
            continue
        for duree in range(C["DRAPEAU_MIN"], C["DRAPEAU_MAX"] + 1):
            d = t - duree
            i = d - C["IMPULSION_BARRES"]
            if i < 1:
                break
            impulsion = (clot[d] - clot[i]) * sens
            if impulsion < C["IMPULSION_MIN"] * a:
                continue
            fen_h = max(haut[d:t + 1])
            fen_b = min(bas[d:t + 1])
            if fen_h - fen_b > C["DRAPEAU_LARGEUR"] * a:
                continue
            retrace = (clot[d] - min(clot[d:t + 1])) if sens > 0 else (max(clot[d:t + 1]) - clot[d])
            if retrace > C["RETRACEMENT_MAX"] * impulsion:
                continue
            borne = fen_h if sens > 0 else fen_b
            if (clot[t] - borne) * sens < C["CASSURE_MIN"] * a:
                continue
            out += _emettre("drapeau", sens, t, clot[t],
                            (fen_b if sens > 0 else fen_h) - C["STOP_MARGE"] * a * sens,
                            clot[t] + impulsion * sens, a, ("M1",))
            break
    return out


# ─────────────────────── structures de référence ───────────────────────

def cassure_niveau(bougies, pivots, atrs, sens):
    """Cassure d'un niveau construit par regroupement de pivots — §4.1.

    Sert d'ÉTALON : si une figure chartiste ne bat pas une simple cassure de
    niveau, elle n'apporte rien.
    """
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a = atrs[t]
        if a is None:
            continue
        ps = [p for p in _connus(pivots, t) if p.barreau >= t - 300]
        if len(ps) < C["NIVEAU_TOUCHES"]:
            continue
        prix = sorted(p.prix for p in ps)
        fuseau = C["NIVEAU_FUSEAU"] * a
        groupes, cur = [], [prix[0]]
        for x in prix[1:]:
            if x - cur[0] <= fuseau:
                cur.append(x)
            else:
                groupes.append(cur); cur = [x]
        groupes.append(cur)
        for g in groupes:
            if len(g) < C["NIVEAU_TOUCHES"]:
                continue
            niveau = sum(g) / len(g)
            if (clot[t] - niveau) * sens < C["CASSURE_MIN"] * a:
                continue
            if t > 0 and (clot[t - 1] - niveau) * sens >= C["CASSURE_MIN"] * a:
                continue
            amplitude = (max(g) - min(g)) + C["AMPLITUDE_MIN"] * a
            out += _emettre("cassure_niveau", sens, t, clot[t],
                            niveau - C["STOP_MARGE"] * a * sens,
                            niveau + 2 * amplitude * sens, a, ("M1",))
            break
    return out


def pullback_tendance(bougies, pivots, atrs, ema20, ema50, sens):
    """Retour sur la moyenne en tendance établie — §4.2.

    Critère de tendance NEUTRALISÉ : il est dans la définition.
    """
    haut = [b["h"] for b in bougies]
    bas = [b["l"] for b in bougies]
    clot = [b["c"] for b in bougies]
    out = []
    for t in range(C["AMORCAGE"], len(bougies)):
        a, e20, e50 = atrs[t], ema20[t], ema50[t]
        if a is None or e20 is None or e50 is None:
            continue
        if (e20 - e50) * sens <= 0:
            continue                                   # tendance non établie
        touche = (bas[t] if sens > 0 else haut[t])
        if abs(touche - e20) > C["PULLBACK_TOL"] * a:
            continue
        if (clot[t] - e50) * sens <= 0:
            continue
        if (clot[t] - touche) * sens <= 0:
            continue                                   # pas de reprise
        ps = _connus(pivots, t)
        extremes = [p.prix for p in ps if p.type == ("haut" if sens > 0 else "bas")]
        if not extremes:
            continue
        objectif = max(extremes[-3:]) if sens > 0 else min(extremes[-3:])
        if (objectif - clot[t]) * sens <= 0:
            continue
        out += _emettre("pullback_tendance", sens, t, clot[t],
                        touche - C["STOP_MARGE"] * a * sens, objectif, a, ("M1",))
    return out


def toutes(bougies, pivots, atrs, ema20=None, ema50=None):
    """Exécute tout le catalogue. Retourne la liste des détections."""
    out = []
    for sens in (1, -1):
        out += double_extreme(bougies, pivots, atrs, sens)
        out += epaule_tete_epaule(bougies, pivots, atrs, sens)
        out += triangle(bougies, pivots, atrs, sens)
        out += drapeau(bougies, pivots, atrs, sens)
        out += cassure_niveau(bougies, pivots, atrs, sens)
        if ema20 and ema50:
            out += pullback_tendance(bougies, pivots, atrs, ema20, ema50, sens)
    out.sort(key=lambda d: (d.barreau, d.methode, d.sens))
    return out
