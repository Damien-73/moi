"""Détection du range et de ses méthodes — SPEC-LOT2 §3 et §4.

Toutes les conditions ne portent que sur des pivots CONFIRMÉS au barreau
d'évaluation. Les bornes, une fois le range constitué, ne sont jamais
recalculées : un objet dont la définition change n'est pas mesurable.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .parametres import RANGE_V1 as P


@dataclass
class Range:
    debut: int              # barreau du premier pivot
    constitue: int          # barreau de confirmation du 4e pivot
    borne_haute: float
    borne_basse: float
    atr: float
    touches_haut: int
    touches_bas: int
    etat: str = "actif"     # actif | rompu | expire
    etat_barreau: int | None = None
    cassure_barreau: int | None = None
    cassure_sens: int = 0

    @property
    def hauteur(self) -> float:
        return self.borne_haute - self.borne_basse

    @property
    def milieu(self) -> float:
        return (self.borne_haute + self.borne_basse) / 2


@dataclass(frozen=True)
class Detection:
    methode: str            # R1a | R1b | R2 | R3
    sens: int
    barreau: int
    entree: float
    invalidation: float
    objectif: float
    range_id: int
    atr: float
    extra: dict = field(default_factory=dict)


def _pente(valeurs) -> float:
    """Pente d'une régression linéaire simple, par barreau."""
    n = len(valeurs)
    if n < 2:
        return 0.0
    mx = (n - 1) / 2
    my = sum(valeurs) / n
    num = sum((i - mx) * (v - my) for i, v in enumerate(valeurs))
    den = sum((i - mx) ** 2 for i in range(n))
    return num / den if den else 0.0


def constituer(pivots, hauts, bas, clotures, atrs, t) -> Range | None:
    """Tente de constituer un range au barreau `t`.

    CORRECTION DE CONCEPTION (voir SPEC-LOT2 §3.1, révisée).
    La première rédaction exigeait que tous les pivots hauts soient à moins de
    0,25 ATR de leur moyenne. Mesuré à la construction : cette condition rejette
    plus de 90 % des candidats et ne décrit pas ce qu'est un range. Un range
    n'est pas une zone où les sommets sont identiques, c'est une zone dont le
    prix ne parvient pas à sortir.

    Définition retenue, objective et vérifiable :
      - bornes = extrêmes des pivots, non moyennes ;
      - la fenêtre est ÉTENDUE VERS L'ARRIÈRE tant que le prix reste contenu,
        ce qui donne sa vraie durée au range ;
      - chaque borne doit avoir été touchée au moins deux fois.
    """
    connus = [p for p in pivots if p.confirmation <= t]
    if len(connus) < P["PIVOTS_MIN"]:
        return None
    derniers = connus[-P["PIVOTS_MIN"]:]

    # C1 — alternance
    for a, b in zip(derniers, derniers[1:]):
        if a.type == b.type:
            return None
    if derniers[-1].confirmation != t:
        return None                      # le range se constitue à l'instant exact

    a = atrs[t]
    if a is None:
        return None

    ph = [p.prix for p in derniers if p.type == "haut"]
    pb = [p.prix for p in derniers if p.type == "bas"]
    if not ph or not pb:
        return None

    # C2 — bornes : extrêmes des pivets, jamais moyennes
    haute, basse = max(ph), min(pb)
    if haute <= basse:
        return None

    # C3 — hauteur
    hauteur = haute - basse
    if not (P["HAUTEUR_MIN"] * a <= hauteur <= P["HAUTEUR_MAX"] * a):
        return None

    # C4 — extension arrière tant que le prix reste contenu
    tol = P["TOLERANCE_BORNE"] * a
    debut = derniers[0].barreau
    while debut > 0 and basse - tol <= clotures[debut - 1] <= haute + tol:
        debut -= 1

    # C5 — durée, mesurée sur la fenêtre étendue
    duree = t - debut
    if not (P["DUREE_MIN"] <= duree <= P["DUREE_MAX"]):
        return None

    # C6 — confinement des clôtures
    fenetre = clotures[debut:t + 1]
    hors = sum(1 for c in fenetre if c > haute + tol or c < basse - tol)
    if hors / len(fenetre) > P["DEBORDEMENT_MAX"]:
        return None

    # C7 — absence de dérive
    if abs(_pente(fenetre) * len(fenetre)) > P["PENTE_MAX"] * hauteur:
        return None

    # C8 — chaque borne doit avoir été touchée au moins deux fois
    zone = P["TOUCHE_ZONE"] * a
    th = sum(1 for i in range(debut, t + 1) if hauts[i] >= haute - zone)
    tb = sum(1 for i in range(debut, t + 1) if bas[i] <= basse + zone)
    if th < 2 or tb < 2:
        return None

    return Range(debut, t, haute, basse, a, th, tb)


def detecter(bougies, pivots, atrs):
    """Parcourt l'historique et produit ranges et détections, en point-in-time."""
    hauts = [b["h"] for b in bougies]
    bas = [b["l"] for b in bougies]
    clotures = [b["c"] for b in bougies]
    n = len(bougies)

    ranges: list[Range] = []
    detections: list[Detection] = []
    actif: Range | None = None
    dernier_touche = {1: -10**9, -1: -10**9}

    for t in range(P["AMORCAGE_MIN"], n):
        a = atrs[t]
        if a is None:
            continue

        # cycle de vie du range actif
        if actif is not None:
            if t - actif.debut > P["DUREE_MAX"]:
                actif.etat, actif.etat_barreau = "expire", t
                actif = None

        if actif is None:
            r = constituer(pivots, hauts, bas, clotures, atrs, t)
            if r is not None:
                ranges.append(r)
                actif = r
                dernier_touche = {1: -10**9, -1: -10**9}
            continue

        rid = len(ranges) - 1
        zone = P["TOUCHE_ZONE"] * a
        marge = P["STOP_MARGE"] * a
        cassure = P["CASSURE_MIN"] * a

        # R2 — cassure confirmée en clôture
        if clotures[t] >= actif.borne_haute + cassure:
            detections.append(Detection(
                "R2", 1, t, clotures[t],
                actif.borne_haute - marge,
                actif.borne_haute + actif.hauteur, rid, a))
            actif.etat, actif.etat_barreau = "rompu", t
            actif.cassure_barreau, actif.cassure_sens = t, 1
            actif = None
            continue
        if clotures[t] <= actif.borne_basse - cassure:
            detections.append(Detection(
                "R2", -1, t, clotures[t],
                actif.borne_basse + marge,
                actif.borne_basse - actif.hauteur, rid, a))
            actif.etat, actif.etat_barreau = "rompu", t
            actif.cassure_barreau, actif.cassure_sens = t, -1
            actif = None
            continue

        # R1 — retour sur borne, range actif uniquement
        if bas[t] <= actif.borne_basse + zone and clotures[t] > actif.borne_basse:
            if clotures[t - 1] > actif.milieu or dernier_touche[1] < 0:
                detections.append(Detection(
                    "R1a", 1, t, clotures[t],
                    actif.borne_basse - marge, actif.milieu, rid, a))
                detections.append(Detection(
                    "R1b", 1, t, clotures[t],
                    actif.borne_basse - marge, actif.borne_haute, rid, a))
                dernier_touche[1] = t
        if hauts[t] >= actif.borne_haute - zone and clotures[t] < actif.borne_haute:
            if clotures[t - 1] < actif.milieu or dernier_touche[-1] < 0:
                detections.append(Detection(
                    "R1a", -1, t, clotures[t],
                    actif.borne_haute + marge, actif.milieu, rid, a))
                detections.append(Detection(
                    "R1b", -1, t, clotures[t],
                    actif.borne_haute + marge, actif.borne_basse, rid, a))
                dernier_touche[-1] = t

    # R3 — retour après cassure, sur les ranges rompus
    for rid, r in enumerate(ranges):
        if r.cassure_barreau is None:
            continue
        b, s = r.cassure_barreau, r.cassure_sens
        borne = r.borne_haute if s > 0 else r.borne_basse
        for t in range(b + 1, min(b + 1 + P["RETOUR_MAX"], n)):
            a = atrs[t]
            if a is None:
                continue
            zone, marge = P["TOUCHE_ZONE"] * a, P["STOP_MARGE"] * a
            revenu = (bas[t] <= borne + zone) if s > 0 else (hauts[t] >= borne - zone)
            tenu = (clotures[t] >= borne) if s > 0 else (clotures[t] <= borne)
            if revenu and tenu:
                detections.append(Detection(
                    "R3", s, t, clotures[t],
                    borne - marge * s,
                    borne + r.hauteur * s, rid, a))
                break
    detections.sort(key=lambda d: (d.barreau, d.methode, d.sens))
    return ranges, detections
