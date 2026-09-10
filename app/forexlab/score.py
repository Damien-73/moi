"""Score de confluence — SPEC-LOT2 §5, CAHIER-DES-CHARGES §11.

Trois filtres durs, puis un seuil. Le score est exprimé en pourcentage du
maximum ATTEIGNABLE par la figure : les critères qu'une figure satisfait par
construction sont neutralisés, sinon les figures de continuation seraient
mécaniquement mieux notées que les figures de retournement.

Asymétrie volontaire : une contradiction retire plus qu'une confirmation
n'ajoute. Une figure haussière contient déjà l'information « haussier » ;
c'est la contradiction qui apporte l'information nouvelle.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import timedelta
from zoneinfo import ZoneInfo

from . import niveaux
from .parametres import RANGE_V1 as R
from .parametres import SCORE_V1 as S

LONDRES = ZoneInfo("Europe/London")
NEW_YORK = ZoneInfo("America/New_York")
TOKYO = ZoneInfo("Asia/Tokyo")


@dataclass
class Contexte:
    symbole: str
    unite: str
    bougies: list
    atrs: list
    rsis: list
    adxs: list
    ema20: list
    pivots: list
    uts_bougies: list = field(default_factory=list)   # unité de temps supérieure
    uts_ema200: list = field(default_factory=list)
    uts_atrs: list = field(default_factory=list)
    uts_pivots: list = field(default_factory=list)
    d1: list = field(default_factory=list)
    calendrier: object = None
    pas_rond: float = S["PAS_ROND"]


@dataclass
class Score:
    points: int
    maximum: int
    detail: dict
    filtres: list
    normalise: float = 0.0
    annoncee: bool = False


def _tendance_uts(ctx, ts):
    """+1 haussière, −1 baissière, 0 neutre. Uniquement des bougies clôturées."""
    idx = [i for i, b in enumerate(ctx.uts_bougies) if b["ts"] + _duree(ctx) <= ts]
    if not idx:
        return 0
    i = idx[-1]
    e, a = ctx.uts_ema200[i], ctx.uts_atrs[i]
    if e is None or a is None or i < 20 or ctx.uts_ema200[i - 20] is None:
        return 0
    pente = (e - ctx.uts_ema200[i - 20]) / a
    c = ctx.uts_bougies[i]["c"]
    connus = [p for p in ctx.uts_pivots if p.confirmation <= i]
    hauts = [p.prix for p in connus if p.type == "haut"][-2:]
    bas = [p.prix for p in connus if p.type == "bas"][-2:]
    croissant = len(hauts) == 2 and len(bas) == 2 and hauts[1] > hauts[0] and bas[1] > bas[0]
    decroissant = len(hauts) == 2 and len(bas) == 2 and hauts[1] < hauts[0] and bas[1] < bas[0]
    if c > e and pente >= S["PENTE_TENDANCE"] and croissant:
        return 1
    if c < e and pente <= -S["PENTE_TENDANCE"] and decroissant:
        return -1
    return 0


def _duree(ctx):
    return {"H1": timedelta(hours=1), "H4": timedelta(hours=4),
            "D1": timedelta(days=1)}[ctx.unite]


def _seance(ts):
    """+1 chevauchement Londres–New York, −1 séance asiatique ou roulement."""
    hl = ts.astimezone(LONDRES)
    hn = ts.astimezone(NEW_YORK)
    ht = ts.astimezone(TOKYO)
    londres = 8 <= hl.hour < 17
    newyork = 8 <= hn.hour < 17
    if londres and newyork:
        return 1
    if 16 <= hn.hour < 19:                       # fenêtre de roulement
        return -1
    if 9 <= ht.hour < 15 and not londres:        # séance de Tokyo
        return -1
    return 0


def _divergence(ctx, t, sens):
    connus = [p for p in ctx.pivots if p.confirmation <= t and p.barreau >= t - 50]
    cible = "bas" if sens > 0 else "haut"
    ext = [p for p in connus if p.type == cible][-2:]
    if len(ext) < 2:
        return False
    p1, p2 = ext
    r1, r2 = ctx.rsis[p1.barreau], ctx.rsis[p2.barreau]
    if r1 is None or r2 is None:
        return False
    if sens > 0:
        return p2.prix < p1.prix and r2 > r1 + S["DIVERGENCE_RSI_MIN"]
    return p2.prix > p1.prix and r2 < r1 - S["DIVERGENCE_RSI_MIN"]


def evaluer(ctx, det, rng=None, neutralises=("zone",)) -> Score:
    """Évalue une détection. `neutralises` liste les critères satisfaits d'office."""
    t, ts = det.barreau, ctx.bougies[det.barreau]["ts"] + _duree(ctx)
    a = det.atr
    detail, points, maximum, filtres = {}, 0, 0, []

    def ajoute(nom, valeur, obtenu, max_possible, mesure=""):
        nonlocal points, maximum
        if nom in neutralises:
            detail[nom] = {"points": None, "neutralise": True}
            return
        points += obtenu
        maximum += max_possible
        detail[nom] = {"points": obtenu, "valeur": valeur, "mesure": mesure}

    # 1 — tendance de l'unité supérieure  (filtre dur si opposée)
    tend = _tendance_uts(ctx, ts)
    if tend != 0 and tend != det.sens:
        filtres.append("contre_tendance")
    ajoute("tendance", tend, 2 if tend == det.sens else 0, 2)

    # 2 — zone support/résistance  (neutralisée pour le range)
    if "zone" not in neutralises:
        zs = niveaux.zones(ctx.pivots, t, a)
        proche = any(abs(det.entree - z) <= S["TOL_ZONE"] * a for z in zs)
        ajoute("zone", proche, 2 if proche else 0, 2)
    else:
        detail["zone"] = {"points": None, "neutralise": True}

    # 3 — niveau rond
    d_rond = niveaux.niveau_rond(det.entree, ctx.pas_rond)
    ok = d_rond <= S["TOL_NIVEAU_ROND"] * a
    ajoute("niveau_rond", ok, 1 if ok else 0, 1, f"{d_rond / a:.2f} ATR")

    # 4 — niveaux de référence
    refs = niveaux.references(ctx.d1, ts)
    ok = any(abs(det.entree - r) <= S["TOL_REFERENCE"] * a for r in refs)
    ajoute("references", ok, 1 if ok else 0, 1)

    # 5 — divergence de momentum
    ok = _divergence(ctx, t, det.sens)
    ajoute("divergence", ok, 1 if ok else 0, 1)

    # 6 — faisabilité de l'objectif  (filtre dur si irréaliste)
    # Le déplacement d'un actif sur N bougies évolue en √N, non en N.
    D = abs(det.objectif - det.entree) / (a * math.sqrt(R["HORIZON"]))
    if D > S["FAISABILITE_MAX"]:
        filtres.append("objectif_irrealiste")
    ajoute("faisabilite", D, 1 if D <= S["FAISABILITE_BON"] else 0, 1, f"D={D:.2f}")

    # 7 — séance : peut retirer un point. Le détail doit montrer les points
    # RÉELLEMENT appliqués, sinon l'explication donnée à l'utilisateur est fausse.
    s = _seance(ts)
    ajoute("seance", s, s, 1, ts.strftime("%H:%M UTC"))

    # 8 — calendrier économique  (filtre dur)
    if ctx.calendrier is not None:
        fin = ts + _duree(ctx) * R["HORIZON"]
        if ctx.calendrier.impacte(ctx.symbole, ts, fin, S["MARGE_CALENDRIER_MIN"]):
            filtres.append("evenement_macro")
    detail["calendrier"] = {"points": 0, "filtre": "evenement_macro" in filtres}

    # 9 — extension du mouvement : critère purement négatif, il n'ajoute
    # aucun maximum atteignable.
    e20 = ctx.ema20[t]
    etendu = e20 is not None and abs(det.entree - e20) / a > S["EXTENSION_MAX"]
    ajoute("extension", etendu, -1 if etendu else 0, 0,
           f"{abs(det.entree - e20) / a:.2f} ATR" if e20 is not None else "")

    # 10 — qualité géométrique
    q = 0
    if rng is not None:
        if min(rng.touches_haut, rng.touches_bas) >= S["QUALITE_TOUCHES"]:
            q += 1
    ajoute("qualite", q, q, 2)

    # 11 — régime de marché
    adx = ctx.adxs[t]
    coherent = False
    if adx is not None:
        if det.methode.startswith("R1"):
            coherent = adx < S["ADX_RANGE"]
        else:
            coherent = adx > S["ADX_TENDANCE"]
    ajoute("regime", adx, 1 if coherent else 0, 1,
           f"ADX={adx:.1f}" if adx is not None else "")

    sc = Score(points, maximum, detail, filtres)
    sc.normalise = max(0.0, points) / maximum if maximum else 0.0
    sc.annoncee = (not filtres) and sc.normalise >= R["SEUIL_ANNONCE"]
    return sc
