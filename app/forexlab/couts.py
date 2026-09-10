"""Modèle de coûts — SPEC-LOT2 §6 et SPEC-DONNEES-REFERENCE §2 et §3.

Trois postes, tous obligatoires : spread, glissement, portage.
Omettre le portage fausse le signe du résultat sur les unités de temps longues.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from .fuseaux import ZoneInfo

from .parametres import COUTS_V1

NY = ZoneInfo("America/New_York")
UTC = timezone.utc

# Spread médian par défaut, en fraction de prix, quand aucune donnée bid/ask
# n'est disponible. Les détections calculées ainsi sont marquées `spread_estime`.
SPREAD_DEFAUT = {
    "EURUSD": 0.000080, "GBPUSD": 0.000120, "USDJPY": 0.010,
    "USDCHF": 0.000130, "AUDUSD": 0.000110, "USDCAD": 0.000140,
    "NZDUSD": 0.000180,
}

# Taux courts annuels par devise. Sert à reconstruire le portage à partir de
# sources publiques plutôt que de la grille non archivée d'un courtier.
TAUX_COURT = {
    "USD": 0.0425, "EUR": 0.0250, "GBP": 0.0400, "JPY": 0.0050,
    "CHF": 0.0100, "AUD": 0.0385, "CAD": 0.0325, "NZD": 0.0450,
}


def creneau(ts: datetime) -> int:
    """Créneau horaire de la semaine, 0 à 167."""
    t = ts.astimezone(UTC)
    return t.weekday() * 24 + t.hour


def _multiplicateur(ts: datetime) -> float:
    """Le spread s'élargit au roulement et se resserre sur le chevauchement.

    Ignorer cette variation fausse tous les résultats de nuit.
    """
    h = ts.astimezone(NY).hour
    if 16 <= h < 18:      # roulement quotidien
        return 4.0
    if 18 <= h or h < 2:  # séance asiatique
        return 1.6
    if 8 <= h < 12:       # chevauchement Londres–New York
        return 0.9
    return 1.0


def spread(symbole: str, ts: datetime, grille=None) -> float:
    """Spread applicable. `grille` = {créneau: spread} issu des données tick."""
    if grille is not None:
        v = grille.get(creneau(ts))
        if v is not None:
            return v
    return SPREAD_DEFAUT[symbole] * _multiplicateur(ts)


def glissement(symbole: str, ts: datetime, grille=None) -> float:
    return COUTS_V1["GLISSEMENT_SPREAD"] * spread(symbole, ts, grille)


def portage_journalier(symbole: str, sens: int, prix: float) -> float:
    """Coût de portage d'un jour, en prix. Toujours défavorable d'au moins la marge.

    Reconstruit depuis les taux courts publics (SPEC-DONNEES-REFERENCE §2),
    et non depuis la grille d'un courtier, qui n'est pas archivée.
    """
    base, cotation = symbole[:3], symbole[3:]
    differentiel = TAUX_COURT[base] - TAUX_COURT[cotation]
    net = sens * differentiel - COUTS_V1["MARGE_COURTIER"]
    return net / COUTS_V1["BASE_JOURS"] * prix


def portage_total(symbole: str, sens: int, prix: float,
                  entree_ts: datetime, sortie_ts: datetime) -> float:
    """Somme des portages, comptés à chaque passage de 17:00 New York.

    Le mercredi compte triple : il porte le règlement du week-end.
    """
    if sortie_ts <= entree_ts:
        return 0.0
    unite = portage_journalier(symbole, sens, prix)
    total, jours = 0.0, 0
    t = entree_ts.astimezone(NY).replace(hour=17, minute=0, second=0, microsecond=0)
    if t <= entree_ts.astimezone(NY):
        t += timedelta(days=1)
    while t.astimezone(UTC) <= sortie_ts:
        if t.weekday() < 5:  # pas de portage le samedi ni le dimanche
            facteur = COUTS_V1["FACTEUR_MERCREDI"] if t.weekday() == 2 else 1
            total += unite * facteur
            jours += facteur
        t += timedelta(days=1)
    return total
