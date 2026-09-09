"""Démonstration de bout en bout du lot 1.

Lancer depuis le dossier `app` :   python3 demo.py

Aucune donnée réelle n'est nécessaire : le script fabrique une série
reproductible, la stocke, l'agrège, calcule les indicateurs, détecte les
pivots, puis exécute le test point-in-time.
"""
from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from forexlab import agregation, calendrier, determinisme, indicateurs, pivots, stockage

UTC = timezone.utc


def serie_synthetique(n=20000, graine=7):
    rng = random.Random(graine)
    ts = datetime(2026, 1, 4, 22, 0, tzinfo=UTC)
    prix, out = 1.1000, []
    while len(out) < n:
        if calendrier.marche_ouvert(ts):
            o = prix
            c = prix + rng.gauss(0, 0.00035)
            h = max(o, c) + abs(rng.gauss(0, 0.00018))
            l = min(o, c) - abs(rng.gauss(0, 0.00018))
            out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
            prix = c
        ts += timedelta(minutes=1)
    return out


def titre(t):
    print(f"\n{t}\n" + "─" * len(t))


def main():
    titre("1. Génération et stockage")
    m1 = serie_synthetique()
    cx = stockage.ouvrir(Path(__file__).parent / "data" / "demo.db")
    stockage.enregistrer_bougies(cx, "EURUSD", "M1", m1, "synthetique")
    print(f"   {len(m1):>7} bougies M1 stockées")
    print(f"   du {m1[0]['ts']:%Y-%m-%d %H:%M} au {m1[-1]['ts']:%Y-%m-%d %H:%M} UTC")

    titre("2. Agrégation (convention : clôture 17:00 America/New_York)")
    for unite in ("H1", "H4", "D1"):
        agg = agregation.agreger(m1, unite)
        stockage.enregistrer_bougies(cx, "EURUSD", unite, agg, "agregat")
        completes = sum(1 for b in agg if b["complete"])
        print(f"   {unite:>3} : {len(agg):>5} bougies, {completes} complètes")

    titre("3. Indicateurs sur H1")
    h1 = stockage.lire_bougies(cx, "EURUSD", "H1")
    h = [b["h"] for b in h1]; l = [b["l"] for b in h1]; c = [b["c"] for b in h1]
    a = indicateurs.atr(h, l, c, 14)
    r = indicateurs.rsi(c, 14)
    x = indicateurs.adx(h, l, c, 14)
    dispo = sum(1 for v in a if v is not None)
    print(f"   ATR calculé sur {dispo} bougies · dernière valeur {a[-1]:.6f}")
    print(f"   RSI dernier {r[-1]:.1f} · ADX dernier {x[-1]:.1f}")

    titre("4. Pivots (ZigZag à seuil ATR)")
    ps = pivots.detecter_pivots(h, l, a)
    print(f"   {len(ps)} pivots confirmés")
    if ps:
        d = [p.confirmation - p.barreau for p in ps]
        print(f"   délai de confirmation : min {min(d)}, médian {sorted(d)[len(d)//2]}, max {max(d)} bougies")
        print("   ⚠ ce délai est la raison d'être du test suivant : un pivot n'est")
        print("     PAS connu à la bougie où le graphique l'affiche.")

    titre("5. Test point-in-time — le test le plus important du projet")

    def chaine(bougies, jusqu_a):
        hh = [b["h"] for b in bougies]; ll = [b["l"] for b in bougies]
        cc = [b["c"] for b in bougies]
        aa = indicateurs.atr(hh, ll, cc, 14)
        return [{"t": p.type, "b": p.barreau, "c": p.confirmation, "p": p.prix}
                for p in pivots.detecter_pivots(hh, ll, aa) if p.confirmation < jusqu_a]

    coupure = len(h1) // 2
    ok1, ref, _ = determinisme.test_point_in_time(chaine, h1, coupure, h1[coupure:])
    ok2, _, _ = determinisme.test_point_in_time(
        chaine, h1, coupure, determinisme.donnees_aberrantes(h1[:coupure]))
    print(f"   données futures réelles      : {'✓ aucun effet' if ok1 else '✗ FUITE'}")
    print(f"   données futures aberrantes   : {'✓ aucun effet' if ok2 else '✗ FUITE'}")
    print(f"   empreinte de référence       : {ref[:32]}…")

    titre("Résultat")
    if ok1 and ok2:
        print("   Le noyau du lot 1 est sain : aucune information future ne fuit.")
        print("   C'est la condition sans laquelle tous les chiffres publiés")
        print("   plus tard seraient faux — et personne ne s'en apercevrait.")
    else:
        print("   ÉCHEC — ne pas continuer tant que ce n'est pas corrigé.")
        sys.exit(1)


if __name__ == "__main__":
    main()
