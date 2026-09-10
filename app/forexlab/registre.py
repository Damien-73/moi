"""Registre prospectif — SPEC-LOT3.

Arbre de Merkle par cycle, chaîne des racines. L'arbre permet de prouver
l'inclusion d'UNE détection avec une poignée d'empreintes, sans exiger toute
la base.

Rappel : le chaînage seul ne prouve rien — il n'a de valeur que couplé à
l'ancrage horaire chez des tiers. Ce module produit ce qui doit être ancré.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone

SEP = "\x1f"
ZERO = "0" * 64


def _nombre(x: float) -> str:
    """Décimale sans zéros de queue, sans notation exponentielle."""
    s = f"{x:.10f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def _instant(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def feuille(*, version, symbole, unite, sens, entree_ts, entree, invalidation,
            objectif_methode, objectif_1r5, objectif_2r, horizon,
            score_points, score_max, statut, motif_rejet="") -> str:
    """Empreinte canonique d'une détection. Ordre des champs figé (SPEC-LOT3 §4)."""
    champs = [
        version, symbole, unite, str(sens), _instant(entree_ts),
        _nombre(entree), _nombre(invalidation), _nombre(objectif_methode),
        _nombre(objectif_1r5), _nombre(objectif_2r), str(horizon),
        str(score_points), str(score_max), statut, motif_rejet or "",
    ]
    return hashlib.sha256(SEP.join(champs).encode("utf-8")).hexdigest()


def racine_merkle(feuilles) -> str:
    """Racine de Merkle. Feuille impaire dupliquée, convention standard."""
    if not feuilles:
        return hashlib.sha256(b"").hexdigest()
    niveau = list(feuilles)
    while len(niveau) > 1:
        if len(niveau) % 2:
            niveau.append(niveau[-1])
        niveau = [
            hashlib.sha256((niveau[i] + niveau[i + 1]).encode("utf-8")).hexdigest()
            for i in range(0, len(niveau), 2)
        ]
    return niveau[0]


def preuve_inclusion(feuilles, index) -> list[tuple[str, str]]:
    """Chemin permettant de recalculer la racine à partir d'une seule feuille."""
    chemin, niveau, i = [], list(feuilles), index
    while len(niveau) > 1:
        if len(niveau) % 2:
            niveau.append(niveau[-1])
        voisin = i + 1 if i % 2 == 0 else i - 1
        chemin.append(("droite" if i % 2 == 0 else "gauche", niveau[voisin]))
        niveau = [
            hashlib.sha256((niveau[k] + niveau[k + 1]).encode("utf-8")).hexdigest()
            for k in range(0, len(niveau), 2)
        ]
        i //= 2
    return chemin


def verifier_inclusion(f: str, chemin, racine: str) -> bool:
    courant = f
    for cote, voisin in chemin:
        pair = courant + voisin if cote == "droite" else voisin + courant
        courant = hashlib.sha256(pair.encode("utf-8")).hexdigest()
    return courant == racine


def tete(tete_precedente: str, racine: str, numero: int,
         horodatage: datetime, nb_feuilles: int) -> str:
    champs = [tete_precedente, racine, str(numero),
              _instant(horodatage), str(nb_feuilles)]
    return hashlib.sha256(SEP.join(champs).encode("utf-8")).hexdigest()


@dataclass
class Cycle:
    numero: int
    horodatage: datetime
    feuilles: list
    racine: str
    tete: str


class Chaine:
    """Suite de cycles. Un cycle VIDE est enregistré comme les autres :
    un cycle manquant serait indistinguable d'un cycle supprimé."""

    def __init__(self):
        self.cycles: list[Cycle] = []

    @property
    def derniere_tete(self) -> str:
        return self.cycles[-1].tete if self.cycles else ZERO

    def ajouter(self, horodatage: datetime, feuilles) -> Cycle:
        feuilles = sorted(feuilles)
        n = len(self.cycles)
        r = racine_merkle(feuilles)
        c = Cycle(n, horodatage, feuilles, r,
                  tete(self.derniere_tete, r, n, horodatage, len(feuilles)))
        self.cycles.append(c)
        return c

    def verifier(self) -> tuple[bool, str]:
        precedente = ZERO
        for c in self.cycles:
            if racine_merkle(c.feuilles) != c.racine:
                return False, f"racine incorrecte au cycle {c.numero}"
            if tete(precedente, c.racine, c.numero,
                    c.horodatage, len(c.feuilles)) != c.tete:
                return False, f"chaîne rompue au cycle {c.numero}"
            precedente = c.tete
        return True, "chaîne continue"
