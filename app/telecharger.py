"""Téléchargement des données réelles depuis Dukascopy.

    python3 telecharger.py EURUSD 2025-01-01 2025-12-31

Pourquoi Dukascopy plutôt que HistData : ses fichiers contiennent le **bid et
l'ask**, donc le VRAI spread. Sans eux, le modèle de coûts est estimé et toutes
les détections doivent être marquées comme telles (SPEC-DONNEES-REFERENCE §3).

Aucune dépendance : urllib, lzma et struct sont dans la bibliothèque standard.

Format Dukascopy : un fichier par heure, LZMA, enregistrements de 20 octets
    >I  millisecondes depuis le début de l'heure
    >I  ask, entier à multiplier par le pas de cotation
    >I  bid, idem
    >f  volume ask
    >f  volume bid
Le mois dans l'adresse est indexé à partir de ZÉRO : 00 = janvier.
"""
from __future__ import annotations

import csv
import lzma
import struct
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
BASE = "https://datafeed.dukascopy.com/datafeed"
ENTETE = {"User-Agent": "Mozilla/5.0"}

# Facteur d'échelle des prix entiers, par symbole.
ECHELLE = {
    "EURUSD": 1e5, "GBPUSD": 1e5, "AUDUSD": 1e5, "NZDUSD": 1e5,
    "USDCHF": 1e5, "USDCAD": 1e5, "USDJPY": 1e3,
}


def adresse(symbole: str, t: datetime) -> str:
    return (f"{BASE}/{symbole}/{t.year}/{t.month - 1:02d}/{t.day:02d}/"
            f"{t.hour:02d}h_ticks.bi5")


def decoder(brut: bytes, symbole: str, heure: datetime):
    """Décode un fichier horaire. Retourne une liste de ticks."""
    if not brut:
        return []
    try:
        data = lzma.decompress(brut)
    except lzma.LZMAError:
        return []
    e = ECHELLE[symbole]
    ticks = []
    for i in range(len(data) // 20):
        ms, ask, bid, _, _ = struct.unpack(">IIIff", data[i * 20:(i + 1) * 20])
        ticks.append({
            "ts": heure + timedelta(milliseconds=ms),
            "bid": bid / e,
            "ask": ask / e,
        })
    return ticks


def telecharger_heure(symbole: str, heure: datetime, essais: int = 3):
    url = adresse(symbole, heure)
    for k in range(essais):
        try:
            req = urllib.request.Request(url, headers=ENTETE)
            with urllib.request.urlopen(req, timeout=60) as r:
                return decoder(r.read(), symbole, heure)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return []           # heure fermée : normal le week-end
            time.sleep(2 * (k + 1))
        except Exception:
            time.sleep(2 * (k + 1))
    print(f"  ! échec après {essais} essais : {url}", file=sys.stderr)
    return []


def ticks_vers_m1(ticks):
    """Agrège en bougies M1, en conservant le spread médian de la minute."""
    seaux, ordre = {}, []
    for t in ticks:
        cle = t["ts"].replace(second=0, microsecond=0)
        mid = (t["bid"] + t["ask"]) / 2
        s = seaux.get(cle)
        if s is None:
            s = {"ts": cle, "o": mid, "h": mid, "l": mid, "c": mid, "spreads": []}
            seaux[cle] = s
            ordre.append(cle)
        s["h"] = max(s["h"], mid)
        s["l"] = min(s["l"], mid)
        s["c"] = mid
        s["spreads"].append(t["ask"] - t["bid"])
    sortie = []
    for cle in ordre:
        s = seaux[cle]
        sp = sorted(s["spreads"])
        sortie.append({"ts": cle, "o": s["o"], "h": s["h"], "l": s["l"],
                       "c": s["c"], "spread": sp[len(sp) // 2]})
    return sortie


def telecharger(symbole: str, debut: datetime, fin: datetime, sortie: Path):
    sortie.parent.mkdir(parents=True, exist_ok=True)
    heure, total, heures, vides = debut, 0, 0, 0
    with open(sortie, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts", "o", "h", "l", "c", "spread"])
        while heure < fin:
            ticks = telecharger_heure(symbole, heure)
            heures += 1
            if ticks:
                for b in ticks_vers_m1(ticks):
                    w.writerow([b["ts"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                                f"{b['o']:.6f}", f"{b['h']:.6f}",
                                f"{b['l']:.6f}", f"{b['c']:.6f}",
                                f"{b['spread']:.6f}"])
                    total += 1
            else:
                vides += 1
            if heures % 168 == 0:
                print(f"  {heure:%Y-%m-%d}  ·  {total:>8} bougies M1 écrites")
            heure += timedelta(hours=1)
    print(f"\n{total} bougies M1 écrites dans {sortie}")
    print(f"{heures} heures parcourues, dont {vides} vides (week-ends et jours fériés)")
    return total


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        print("Exemple : python3 telecharger.py EURUSD 2025-01-01 2025-12-31")
        sys.exit(1)
    symbole = sys.argv[1].upper()
    if symbole not in ECHELLE:
        print(f"Symbole inconnu. Disponibles : {', '.join(ECHELLE)}")
        sys.exit(1)
    debut = datetime.fromisoformat(sys.argv[2]).replace(tzinfo=UTC)
    fin = datetime.fromisoformat(sys.argv[3]).replace(tzinfo=UTC)
    dest = Path(__file__).resolve().parent / "data" / f"{symbole}_M1.csv"
    jours = (fin - debut).days
    print(f"Téléchargement {symbole} du {debut:%Y-%m-%d} au {fin:%Y-%m-%d}")
    print(f"{jours} jours ≈ {jours * 24} requêtes. Compter environ "
          f"{jours * 24 // 60} minutes.\n")
    telecharger(symbole, debut, fin, dest)


if __name__ == "__main__":
    main()
