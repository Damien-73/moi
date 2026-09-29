"""Verrou des données out-of-sample (>= 2023-01-01).

Les données OOS ne sont accessibles qu'avec un jeton `OOSToken`, obtenu une seule fois
par setup via `unlock_oos`, et seulement si :
1. docs/setups/<setup>.md existe et contient la ligne « Statut : FIGÉ » ;
2. la variable d'environnement OOS_ACCORD vaut le nom du setup (accord explicite de Damien) ;
3. le setup n'a jamais été testé en OOS (journal results/oos_log.csv).
"""
from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.config import RESULTS_DIR, ROOT


class OOSLocked(PermissionError):
    pass


@dataclass(frozen=True)
class OOSToken:
    setup: str
    params_json: str
    _secret: object


_SECRET = object()


def _log_path() -> Path:
    return RESULTS_DIR / "oos_log.csv"


def already_used(setup: str, log_path: Path | None = None) -> bool:
    path = log_path or _log_path()
    if not path.exists():
        return False
    with path.open() as f:
        return any(row["setup"] == setup for row in csv.DictReader(f))


def unlock_oos(setup: str, params: dict, docs_dir: Path | None = None,
               log_path: Path | None = None) -> OOSToken:
    docs = (docs_dir or ROOT / "docs" / "setups") / f"{setup}.md"
    if not docs.exists() or "Statut : FIGÉ" not in docs.read_text(encoding="utf-8"):
        raise OOSLocked(f"{docs} absent ou setup non figé (ligne « Statut : FIGÉ » manquante).")
    if os.environ.get("OOS_ACCORD") != setup:
        raise OOSLocked("Accord explicite requis : OOS_ACCORD=<nom du setup>.")
    path = log_path or _log_path()
    if already_used(setup, path):
        raise OOSLocked(f"Le test out-of-sample de {setup} a déjà été utilisé. Usage unique.")
    params_json = json.dumps(params, sort_keys=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp_utc", "setup", "params"])
        w.writerow([datetime.now(timezone.utc).isoformat(), setup, params_json])
    return OOSToken(setup, params_json, _SECRET)


def check_token(token: object) -> None:
    if not isinstance(token, OOSToken) or token._secret is not _SECRET:
        raise OOSLocked("Données out-of-sample verrouillées : jeton OOS valide requis.")
