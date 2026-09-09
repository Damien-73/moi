"""Conventions de temps du marché des changes.

Règle figée (SPEC-LOT2 §1.1) : la journée de négociation ouvre et clôture à
17:00 America/New_York. On raisonne sur le fuseau, jamais sur un décalage fixe,
pour que le changement d'heure soit absorbé automatiquement.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
UTC = timezone.utc

HEURE_BASCULE = 17  # 17:00 heure de New York

UNITES = {"M1": 1, "H1": 60, "H4": 240, "D1": 1440}


def jour_negociation(ts: datetime) -> str:
    """Nom de la journée de négociation à laquelle appartient un instant.

    Convention retenue, alignée sur celle des courtiers : la journée est nommée
    par sa date de CLÔTURE. La bougie qui couvre [4 janv. 17:00, 5 janv. 17:00]
    heure de New York s'appelle donc « 2026-01-05 ».

    Retourne une date ISO.
    """
    local = ts.astimezone(NY)
    decale = local - timedelta(hours=HEURE_BASCULE)
    return (decale.date() + timedelta(days=1)).isoformat()


def ouverture_jour(jour_iso: str) -> datetime:
    """Instant UTC d'ouverture de la journée de négociation nommée `jour_iso`.

    Réciproque exacte de `jour_negociation` : l'ouverture d'une journée nommée
    J est le 17:00 New York de J−1.
    """
    d = datetime.fromisoformat(jour_iso) - timedelta(days=1)
    local = datetime(d.year, d.month, d.day, HEURE_BASCULE, tzinfo=NY)
    return local.astimezone(UTC)


def debut_bougie(ts: datetime, unite: str) -> datetime:
    """Instant d'ouverture de la bougie de `unite` contenant `ts`.

    H1 est aligné sur l'heure UTC. H4 et D1 sont alignés sur l'ouverture de la
    journée de négociation, ce qui garantit qu'une bougie H4 ne chevauche jamais
    deux journées.
    """
    ts = ts.astimezone(UTC)
    if unite == "M1":
        return ts.replace(second=0, microsecond=0)
    if unite == "H1":
        return ts.replace(minute=0, second=0, microsecond=0)
    if unite in ("H4", "D1"):
        ouverture = ouverture_jour(jour_negociation(ts))
        if unite == "D1":
            return ouverture
        ecart = int((ts - ouverture).total_seconds() // 60)
        return ouverture + timedelta(minutes=(ecart // 240) * 240)
    raise ValueError(f"unité inconnue : {unite}")


def marche_ouvert(ts: datetime) -> bool:
    """Le marché est fermé du vendredi 17:00 au dimanche 17:00, heure de New York."""
    local = ts.astimezone(NY)
    jsem, heure = local.weekday(), local.hour  # lundi = 0
    if jsem == 4 and heure >= HEURE_BASCULE:
        return False
    if jsem == 5:
        return False
    if jsem == 6 and heure < HEURE_BASCULE:
        return False
    return True
