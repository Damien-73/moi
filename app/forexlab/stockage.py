"""Stockage — SQLite, sans aucune installation.

Choix d'ingénierie assumé : SQLite pour les lots 1 et 2 (développement local,
un seul auteur, ~1,1 million de bougies — ce qui est peu). Le passage à
PostgreSQL + TimescaleDB interviendra au lot 3, quand le service devient
public et multi-utilisateur. Le SQL est volontairement standard pour que la
migration soit mécanique.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS instrument (
    id              INTEGER PRIMARY KEY,
    symbole         TEXT NOT NULL UNIQUE,
    valeur_pip      REAL NOT NULL,
    pas_niveau_rond REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS bougie (
    instrument_id  INTEGER NOT NULL REFERENCES instrument(id),
    unite_temps    TEXT    NOT NULL,
    ouverture_ts   TEXT    NOT NULL,          -- ISO 8601 UTC, à la seconde
    o REAL NOT NULL, h REAL NOT NULL, l REAL NOT NULL, c REAL NOT NULL,
    minutes        INTEGER NOT NULL DEFAULT 1,
    complete       INTEGER NOT NULL DEFAULT 1,
    source         TEXT    NOT NULL,
    PRIMARY KEY (instrument_id, unite_temps, ouverture_ts)
);

CREATE INDEX IF NOT EXISTS idx_bougie_lecture
    ON bougie (instrument_id, unite_temps, ouverture_ts);

CREATE TABLE IF NOT EXISTS import (
    id           INTEGER PRIMARY KEY,
    fichier      TEXT NOT NULL,
    symbole      TEXT NOT NULL,
    fuseau_source TEXT NOT NULL,
    lignes_lues  INTEGER NOT NULL,
    lignes_gardees INTEGER NOT NULL,
    horodatage   TEXT NOT NULL
);
"""

PAIRES = {
    "EURUSD": (0.0001, 0.0050), "GBPUSD": (0.0001, 0.0050),
    "AUDUSD": (0.0001, 0.0050), "NZDUSD": (0.0001, 0.0050),
    "USDCHF": (0.0001, 0.0050), "USDCAD": (0.0001, 0.0050),
    "USDJPY": (0.01, 0.50),
}


def ouvrir(chemin: str | Path = "data/forexlab.db") -> sqlite3.Connection:
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(chemin)
    cx.row_factory = sqlite3.Row
    cx.executescript(SCHEMA)
    for symbole, (pip, pas) in PAIRES.items():
        cx.execute(
            "INSERT OR IGNORE INTO instrument (symbole, valeur_pip, pas_niveau_rond)"
            " VALUES (?,?,?)", (symbole, pip, pas))
    cx.commit()
    return cx


def id_instrument(cx, symbole: str) -> int:
    r = cx.execute("SELECT id FROM instrument WHERE symbole=?", (symbole,)).fetchone()
    if r is None:
        raise ValueError(f"instrument inconnu : {symbole}")
    return r["id"]


def enregistrer_bougies(cx, symbole: str, unite: str, bougies, source: str) -> int:
    iid = id_instrument(cx, symbole)
    lignes = [(iid, unite, _iso(b["ts"]), b["o"], b["h"], b["l"], b["c"],
               b.get("minutes", 1), 1 if b.get("complete", True) else 0, source)
              for b in bougies]
    cx.executemany(
        "INSERT OR REPLACE INTO bougie (instrument_id, unite_temps, ouverture_ts,"
        " o,h,l,c, minutes, complete, source) VALUES (?,?,?,?,?,?,?,?,?,?)", lignes)
    cx.commit()
    return len(lignes)


def lire_bougies(cx, symbole: str, unite: str, depuis=None, jusqu_a=None):
    iid = id_instrument(cx, symbole)
    sql = ("SELECT ouverture_ts,o,h,l,c,minutes,complete FROM bougie"
           " WHERE instrument_id=? AND unite_temps=?")
    args = [iid, unite]
    if depuis:
        sql += " AND ouverture_ts>=?"; args.append(_iso(depuis))
    if jusqu_a:
        sql += " AND ouverture_ts<?"; args.append(_iso(jusqu_a))
    sql += " ORDER BY ouverture_ts"
    return [{"ts": _parse(r["ouverture_ts"]), "o": r["o"], "h": r["h"],
             "l": r["l"], "c": r["c"], "minutes": r["minutes"],
             "complete": bool(r["complete"])}
            for r in cx.execute(sql, args)]


def _iso(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
