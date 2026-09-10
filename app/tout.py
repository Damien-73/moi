"""Chaîne complète, de la donnée aux écrans.

    python3 tout.py              # données synthétiques, pour voir
    python3 tout.py EURUSD H1    # données réelles téléchargées

Produit : les statistiques, le registre exporté, la vérification par un tiers,
et les quatre écrans publics dans data/site/.
"""
from __future__ import annotations

import math
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

from forexlab import (agregation, contrainte, export, pipeline, rapport,
                      registre, stats)
from forexlab.calendrier import marche_ouvert
import verificateur

UTC = timezone.utc


def historique(mois=10, graine=3):
    rng = random.Random(graine)
    ts = datetime(2026, 1, 4, 22, 0, tzinfo=UTC)
    fin = ts + timedelta(days=30 * mois)
    prix, out, i = 1.1000, [], 0
    while ts < fin:
        if marche_ouvert(ts):
            vol = 0.000055 * (1 + 0.6 * math.sin(2 * math.pi * i / 8000))
            o = prix
            c = prix + 0.0000006 * math.sin(2 * math.pi * i / 40000) + rng.gauss(0, vol)
            out.append({"ts": ts, "o": o, "h": max(o, c) + abs(rng.gauss(0, vol * .6)),
                        "l": min(o, c) - abs(rng.gauss(0, vol * .6)), "c": c})
            prix = c
            i += 1
        ts += timedelta(minutes=1)
    return out


def titre(t):
    print(f"\n{t}\n" + "─" * max(len(t), 70))


def main():
    reel = len(sys.argv) > 1
    if reel:
        import analyser
        symbole, unite = sys.argv[1].upper(), (sys.argv[2] if len(sys.argv) > 2 else "H1")
        chemin = ICI / "data" / f"{symbole}_M1.csv"
        if not chemin.exists():
            print(f"Fichier absent : {chemin}\n"
                  f"Lance : python3 telecharger.py {symbole} 2025-01-01 2025-07-01")
            sys.exit(1)
        m1, grille = analyser.charger(chemin)
    else:
        symbole, unite, grille = "EURUSD", "H1", None
        titre("Données synthétiques (aucun fichier réel fourni)")
        m1 = historique()

    bougies = agregation.agreger(m1, unite)
    uts = agregation.agreger(m1, {"H1": "H4", "H4": "D1", "D1": "D1"}[unite])
    d1 = agregation.agreger(m1, "D1")
    print(f"{len(m1)} bougies M1 · {len(bougies)} {unite} · "
          f"du {m1[0]['ts']:%Y-%m-%d} au {m1[-1]['ts']:%Y-%m-%d}")

    titre("1. Catalogue complet — détection, score, résolution, coûts")
    ranges, lignes = pipeline.executer(symbole, unite, bougies, m1, uts, d1,
                                       grille=grille, catalogue=True)
    annoncees = [l for l in lignes if l.statut == "annoncee"]
    ecartees = [l for l in lignes if l.statut == "ecartee"]
    print(f"{len(lignes)} détections → {len(annoncees)} annoncées, "
          f"{len(ecartees)} écartées et conservées")
    print("\nPar figure")
    for f, n in Counter(l.figure for l in lignes).most_common():
        print(f"   {n:>6}  {f}")

    def agr(sel, cible="methode"):
        rs = [l.issues[cible]["r_net"] for l in sel if l.issues.get(cible)]
        res = [l.issues[cible]["resultat"] for l in sel if l.issues.get(cible)]
        amb = sum(1 for l in sel if l.issues.get(cible) and l.issues[cible]["ambigu_m1"])
        return stats.agregat(rs, res, amb)

    sa, se = agr(annoncees), agr(ecartees)

    titre("2. Résultats nets — aucune statistique servie seule")
    for nom, s in (("annoncées", sa), ("écartées (témoin)", se), ("toutes", agr(lignes))):
        if s["publiable"]:
            print(f"   {nom:<22} {s['esperance']:+.3f} R ± {s['ic95']:.3f}  "
                  f"n={s['n']:>5}  atteint {s.get('atteint', 0):.0%}  "
                  f"ambigu {s['ambigu']:.1%}  [{s['statut']}]")
        else:
            print(f"   {nom:<22} données insuffisantes — {s['n']} sur 100")
    if sa["publiable"] and se["publiable"]:
        c = stats.comparer(sa, se)
        print(f"\n   Écart annoncées − témoin : "
              f"{c['comparaison']['ecart']:+.3f} R "
              f"({'significatif' if c['comparaison']['ecart_significatif'] else 'non significatif'})")

    titre("3. Classement des figures, corrigé du test multiple")
    series = {}
    for cle in sorted({(l.figure, l.methode) for l in lignes}):
        sel = [l for l in lignes if (l.figure, l.methode) == cle]
        series[f"{cle[1]}"] = agr(sel)
    cl = stats.classement(series)
    print(f"   {cl['series_publiables']} séries publiables sur "
          f"{cl['series_testees']} testées")
    for l in cl["lignes"][:12]:
        print(f"   {l['nom']:<28} {l['esperance']:+.3f} R ± {l['ic95']:.3f}"
              f"  n={l['n']:>5}  {'significatif' if l['significatif'] else ''}")
    if not cl["lignes"]:
        print("   aucune série n'atteint 100 occurrences")

    titre("4. Mode contrainte — probabilité de réussite d'un examen")
    jours = contrainte.journees(lignes)
    sim = contrainte.simuler(jours, simulations=4000)
    if sim["suffisant"]:
        print(f"   {sim['probabilite']:.1%} ± {sim['ic95']:.1%}  "
              f"(perte {sim['type_perte']}, risque {sim['risque']:.2%})")
        print(f"   échec par perte totale {sim['echec_perte_totale']:.0%} · "
              f"par perte journalière {sim['echec_perte_jour']:.0%} · "
              f"délai dépassé {sim['echec_delai']:.0%}")
        b = contrainte.balayage_risque(jours, simulations=1200)
        print("\n   Probabilité selon le risque par trade")
        print("   " + "".join(f"{o['risque']:>7.2%}" for o in b["courbe"]))
        print("   " + "".join(f"{(o['probabilite'] or 0):>7.0%}" for o in b["courbe"]))
        print(f"   optimum à {b['optimum']['risque']:.2%} — "
              f"la courbe n'est pas monotone")
    else:
        print(f"   historique insuffisant : {sim['journees']} journées sur 60")

    titre("5. Registre, export et vérification par un tiers")
    chaine = registre.Chaine()
    par_cycle = defaultdict(list)
    for l in lignes:
        par_cycle[l.entree_ts.replace(minute=0, second=0, microsecond=0)].append(l.empreinte)
    for cle in sorted(par_cycle):
        chaine.ajouter(cle, par_cycle[cle])
    fichier = export.exporter(lignes, chaine, ICI / "data" / "registre.json")
    print(f"   registre exporté : {fichier.relative_to(ICI)}")
    v = verificateur.verifier(fichier)
    print(f"   vérification indépendante : "
          f"{'✓ conforme' if v['valide'] else '✗ ' + '; '.join(v['erreurs'])}")
    print(f"   {v['cycles']} cycles · {v['detections']} détections · "
          f"{len(v['figures'])} figures")

    titre("6. Écrans")
    site = rapport.ecrire(ICI / "data" / "site", lignes, sa, se, cl, v)
    for f in sorted(site.glob("*.html")):
        print(f"   {f.relative_to(ICI)}")
    print(f"\n   Ouvre {(site / 'index.html').relative_to(ICI)} dans ton navigateur.")

    if not reel:
        print("\n⚠ Données SYNTHÉTIQUES. Pour de vrais chiffres :")
        print("   python3 telecharger.py EURUSD 2025-01-01 2025-07-01")
        print("   python3 tout.py EURUSD H1")


if __name__ == "__main__":
    main()
