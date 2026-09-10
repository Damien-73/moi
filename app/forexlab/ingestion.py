"""Lecture des fichiers M1 — SPEC-LOT2 §1.1.

Le fuseau du fichier source est un paramètre OBLIGATOIRE, jamais deviné.
HistData publie ses fichiers M1 en heure de l'Est SANS changement d'heure :
c'est un fuseau à décalage fixe, différent de 'America/New_York'. Se tromper
décale tout l'historique de une heure la moitié de l'année, et fausse
silencieusement toute analyse horaire.
"""
from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# HistData « ASCII M1 » : EST fixe, sans heure d'été.
EST_FIXE = timezone(timedelta(hours=-5))

FUSEAUX = {
    "UTC": timezone.utc,
    "EST_FIXE": EST_FIXE,
    "America/New_York": ZoneInfo("America/New_York"),
}


def lire_histdata(chemin: str | Path, fuseau: str = "EST_FIXE"):
    """Format HistData : AAAAMMJJ HHMMSS;ouv;haut;bas;clot;volume (séparateur ';')."""
    tz = FUSEAUX[fuseau]
    sortie, lues = [], 0
    with open(chemin, newline="", encoding="utf-8") as f:
        for ligne in csv.reader(f, delimiter=";"):
            lues += 1
            if len(ligne) < 5:
                continue
            try:
                ts = datetime.strptime(ligne[0], "%Y%m%d %H%M%S").replace(tzinfo=tz)
                o, h, l, c = (float(x) for x in ligne[1:5])
            except ValueError:
                continue
            if not (l <= o <= h and l <= c <= h):
                continue  # bougie incohérente : écartée, jamais corrigée
            sortie.append({"ts": ts.astimezone(timezone.utc),
                           "o": o, "h": h, "l": l, "c": c})
    sortie.sort(key=lambda b: b["ts"])
    return sortie, lues


def lire_csv_generique(chemin, fuseau="UTC", format_date="%Y-%m-%d %H:%M:%S",
                       delimiteur=",", colonnes=("ts", "o", "h", "l", "c")):
    """CSV avec en-tête. `colonnes` donne le nom des colonnes attendues."""
    tz = FUSEAUX[fuseau]
    sortie, lues = [], 0
    with open(chemin, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=delimiteur):
            lues += 1
            try:
                ts = datetime.strptime(r[colonnes[0]].strip(), format_date).replace(tzinfo=tz)
                o, h, l, c = (float(r[k]) for k in colonnes[1:5])
            except (ValueError, KeyError, TypeError):
                continue
            if not (l <= o <= h and l <= c <= h):
                continue
            sortie.append({"ts": ts.astimezone(timezone.utc),
                           "o": o, "h": h, "l": l, "c": c})
    sortie.sort(key=lambda b: b["ts"])
    return sortie, lues


def trous(bougies_m1):
    """Minutes manquantes pendant les heures d'ouverture du marché.

    Ne pas confondre absence de cotation et donnée manquante : le contrôle de
    complétude (cahier des charges §16) en dépend.
    """
    from .calendrier import marche_ouvert
    manquantes = []
    for prec, suiv in zip(bougies_m1, bougies_m1[1:]):
        ecart = int((suiv["ts"] - prec["ts"]).total_seconds() // 60)
        if ecart <= 1:
            continue
        t = prec["ts"]
        for _ in range(ecart - 1):
            t = t + timedelta(minutes=1)
            if marche_ouvert(t):
                manquantes.append(t)
    return manquantes
