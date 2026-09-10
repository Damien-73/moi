"""Export du registre pour publication et vérification tierce — SPEC-LOT3 §8."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _iso(ts):
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _propre(o):
    """Les horodatages des issues doivent sortir en ISO, pas en objets."""
    if isinstance(o, datetime):
        return _iso(o)
    if isinstance(o, dict):
        return {k: _propre(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_propre(v) for v in o]
    return o


def exporter(lignes, chaine, chemin: Path):
    """Écrit le jeu de données public. Tout doit y être pour recalculer."""
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "format": 1,
        "genere_le": _iso(datetime.now(timezone.utc)),
        "detections": [{
            "version": f"{l.figure}.v1", "symbole": l.symbole, "unite": l.unite,
            "figure": l.figure, "methode": l.methode, "sens": l.sens,
            "entree_ts": _iso(l.entree_ts), "entree": l.entree,
            "invalidation": l.invalidation, "objectif_methode": l.objectif,
            "objectif_1r5": l.objectif_1r5, "objectif_2r": l.objectif_2r,
            "horizon": 20, "score_points": l.score_points,
            "score_max": l.score_max, "statut": l.statut,
            "motif_rejet": l.motif_rejet, "empreinte": l.empreinte,
            "issues": _propre(l.issues),
        } for l in lignes],
        "cycles": [{
            "numero": c.numero, "horodatage": _iso(c.horodatage),
            "feuilles": c.feuilles, "racine": c.racine, "tete": c.tete,
        } for c in chaine.cycles],
    }
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return chemin
