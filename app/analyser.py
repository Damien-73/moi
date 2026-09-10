"""Exécute la chaîne complète sur les données réelles téléchargées.

    python3 analyser.py EURUSD H1

Utilise le spread RÉEL contenu dans le fichier : les résultats ne sont donc
pas marqués « spread estimé » (SPEC-DONNEES-REFERENCE §3).
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from forexlab import agregation, couts, pipeline, registre

UTC = timezone.utc


def charger(chemin: Path):
    """Lit le CSV produit par telecharger.py. Retourne (bougies, grille de spread)."""
    bougies, spreads = [], defaultdict(list)
    with open(chemin, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ts = datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            bougies.append({"ts": ts, "o": float(r["o"]), "h": float(r["h"]),
                            "l": float(r["l"]), "c": float(r["c"])})
            if r.get("spread"):
                spreads[couts.creneau(ts)].append(float(r["spread"]))
    grille = {c: sorted(v)[len(v) // 2] for c, v in spreads.items() if v}
    return bougies, grille


def bloc(nom, s):
    if not s["publiable"]:
        print(f"   {nom:<28} données insuffisantes — {s['n']} sur 100")
        return
    print(f"   {nom:<28} {s['esperance']:+.3f} R ± {s['ic95']:.3f}"
          f"   n={s['n']:>5}   atteint {s['atteint']:.0%}"
          f"   ambigu {s['ambigu']:.1%}   [{s['statut']}]")


def main():
    symbole = (sys.argv[1] if len(sys.argv) > 1 else "EURUSD").upper()
    unite = (sys.argv[2] if len(sys.argv) > 2 else "H1").upper()
    chemin = Path(__file__).resolve().parent / "data" / f"{symbole}_M1.csv"
    if not chemin.exists():
        print(f"Fichier absent : {chemin}")
        print(f"Lance d'abord :  python3 telecharger.py {symbole} 2024-01-01 2025-12-31")
        sys.exit(1)

    print(f"Chargement de {chemin.name}")
    m1, grille = charger(chemin)
    if not m1:
        print("Fichier vide.")
        sys.exit(1)
    print(f"   {len(m1)} bougies M1 · du {m1[0]['ts']:%Y-%m-%d} au {m1[-1]['ts']:%Y-%m-%d}")

    if grille:
        vals = sorted(grille.values())
        pip = 0.01 if symbole.endswith("JPY") else 0.0001
        print(f"   spread réel : médian {vals[len(vals) // 2] / pip:.2f} pips, "
              f"min {vals[0] / pip:.2f}, max {vals[-1] / pip:.2f}  "
              f"({len(grille)} créneaux horaires)")
    else:
        print("   ⚠ aucun spread dans le fichier : le modèle par défaut sera utilisé,")
        print("     et les résultats devront être marqués « spread estimé »")

    bougies = agregation.agreger(m1, unite)
    uts = agregation.agreger(m1, {"H1": "H4", "H4": "D1", "D1": "D1"}[unite])
    d1 = agregation.agreger(m1, "D1")
    print(f"   {len(bougies)} bougies {unite}")

    print("\nExécution de la chaîne…")
    ranges, lignes = pipeline.executer(
        symbole, unite, bougies, m1, uts, d1,
        pas_rond=0.50 if symbole.endswith("JPY") else 0.0050, grille=grille or None)

    annoncees = [l for l in lignes if l.statut == "annoncee"]
    ecartees = [l for l in lignes if l.statut == "ecartee"]
    print(f"\n{len(ranges)} ranges · {len(lignes)} détections "
          f"→ {len(annoncees)} annoncées, {len(ecartees)} écartées")

    print("\nMotifs de rejet")
    for m, n in Counter(l.motif_rejet for l in ecartees).most_common():
        print(f"   {n:>6}  {m}")

    print("\nRésultats nets — objectif de la méthode")
    bloc("toutes", pipeline.statistiques(lignes))
    bloc("annoncées", pipeline.statistiques(annoncees))
    bloc("écartées (témoin)", pipeline.statistiques(ecartees))

    print("\nPar méthode")
    for m in ("R1a", "R1b", "R2", "R3"):
        bloc(m, pipeline.statistiques([l for l in lignes if l.methode == m]))

    print("\nPar objectif, sur toutes les détections")
    for cible, nom in (("methode", "projection figure"), ("1r5", "1,5 R"), ("2r", "2 R")):
        bloc(nom, pipeline.statistiques(lignes, cible))

    print("\nPar tranche de score")
    tranches = defaultdict(list)
    for l in lignes:
        tranches[min(int(l.score_normalise * 10) // 2 * 2, 8)].append(l)
    for k in sorted(tranches):
        bloc(f"score {k * 10}-{k * 10 + 19} %", pipeline.statistiques(tranches[k]))

    print("\nDistribution des scores")
    dist = Counter(round(l.score_normalise * 10) for l in lignes)
    if dist:
        mx = max(dist.values())
        for k in sorted(dist):
            print(f"   {k * 10:>3}% {'█' * max(1, dist[k] * 40 // mx)} {dist[k]}")

    chaine = registre.Chaine()
    par_cycle = defaultdict(list)
    for l in lignes:
        par_cycle[l.entree_ts.replace(minute=0, second=0, microsecond=0)].append(l.empreinte)
    for cle in sorted(par_cycle):
        chaine.ajouter(cle, par_cycle[cle])
    ok, msg = chaine.verifier()
    print(f"\nRegistre : {len(chaine.cycles)} cycles · {'✓' if ok else '✗'} {msg}")
    print(f"Tête de chaîne : {chaine.derniere_tete}")

    print("\n⚠ Ces chiffres sont un BACKTEST. Ils orientent une décision ;")
    print("  ils ne prouvent rien à personne. Seul le registre prospectif le fera.")


if __name__ == "__main__":
    main()
