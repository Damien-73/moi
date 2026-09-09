"""Harnais de déterminisme et test point-in-time — SPEC-LOT2 §8.

C'est le test le plus important du projet. Il vérifie qu'aucun calcul effectué
au barreau t n'utilise d'information postérieure à t.

Principe de l'attaque : on recalcule sur [0, T] après avoir collé APRÈS T des
données aberrantes. Si un seul résultat change, il existe une fuite
d'information future, et la mise en service est bloquée.
"""
from __future__ import annotations

import hashlib
import json


def empreinte(objets) -> str:
    """Empreinte stable d'une séquence de résultats.

    Sérialisation canonique (SPEC-LOT3 §4) : séparateur \\x1f, décimales sans
    zéros de queue, UTF-8. Deux implémentations doivent produire le même
    résultat, sinon aucune vérification tierce n'est possible.
    """
    h = hashlib.sha256()
    for o in objets:
        h.update(_canonique(o).encode("utf-8"))
        h.update(b"\x1e")
    return h.hexdigest()


def _canonique(o) -> str:
    if isinstance(o, dict):
        return "\x1f".join(f"{k}={_canonique(o[k])}" for k in sorted(o))
    if isinstance(o, (list, tuple)):
        return "\x1f".join(_canonique(x) for x in o)
    if isinstance(o, bool):
        return "true" if o else "false"
    if isinstance(o, float):
        s = f"{o:.10f}".rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    if o is None:
        return ""
    if hasattr(o, "isoformat"):
        return o.isoformat().replace("+00:00", "Z")
    return str(o)


def test_point_in_time(calcul, donnees, coupure: int, donnees_futures):
    """Retourne (succes, empreinte_reference, empreinte_avec_futur).

    `calcul(donnees, jusqu_a)` doit retourner la liste des résultats produits
    sur les `jusqu_a` premières bougies.
    """
    reference = empreinte(calcul(donnees[:coupure], coupure))
    etendu = empreinte(calcul(donnees[:coupure] + donnees_futures, coupure))
    return reference == etendu, reference, etendu


def donnees_aberrantes(modele, facteur: float = 10.0, nombre: int = 200):
    """Prolonge un historique par des bougies absurdes.

    Le test doit rester insensible à ces données : elles sont postérieures à la
    coupure et ne doivent donc influencer aucun résultat antérieur.
    """
    from datetime import timedelta
    sortie = []
    dernier = modele[-1]
    ts = dernier["ts"]
    prix = dernier["c"] * facteur
    for i in range(nombre):
        ts = ts + timedelta(minutes=1)
        prix = prix * (1.01 if i % 2 == 0 else 0.99)
        sortie.append({"ts": ts, "o": prix, "h": prix * 1.02,
                       "l": prix * 0.98, "c": prix})
    return sortie
