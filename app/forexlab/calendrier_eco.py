"""Calendrier économique — SPEC-DONNEES-REFERENCE §1.

On classe par TYPE d'événement, jamais par l'étiquette « fort impact » d'un
fournisseur : cette étiquette est subjective, révisable après coup et non
historisée. L'utiliser reviendrait à filtrer une détection de 2019 avec un
jugement porté en 2026, c'est-à-dire à introduire une information future.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

TYPES_RETENUS = {
    "taux_directeur", "emploi", "inflation", "croissance", "activite_flash",
    "discours_gouverneur",
}


@dataclass(frozen=True)
class Evenement:
    ts: datetime
    devise: str
    type: str

    def valide(self) -> bool:
        return self.type in TYPES_RETENUS


class Calendrier:
    def __init__(self, evenements=()):
        self.evenements = [e for e in evenements if e.valide()]

    def impacte(self, symbole: str, debut: datetime, fin: datetime,
                marge_minutes: int = 30) -> bool:
        """Un événement concernant l'une des deux devises tombe-t-il dans la fenêtre ?

        La marge amont couvre le positionnement qui précède l'annonce.
        """
        devises = {symbole[:3], symbole[3:]}
        d = debut - timedelta(minutes=marge_minutes)
        return any(e.devise in devises and d <= e.ts <= fin for e in self.evenements)
