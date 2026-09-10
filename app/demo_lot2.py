"""Démonstration de bout en bout des lots 2, 3 et 4.

    cd app && python3 demo_lot2.py

Génère un historique réaliste, exécute la chaîne complète — détection,
score, résolution en M1, coûts, registre — et affiche ce que le produit
montrerait réellement.
"""
from __future__ import annotations

import math
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from forexlab import agregation, determinisme, pipeline, registre
from forexlab.calendrier import marche_ouvert

UTC = timezone.utc


def historique(mois=8, graine=3):
    """M1 réaliste : dérive lente, cycles de volatilité, ATR horaire de 8-12 pips."""
    rng = random.Random(graine)
    ts = datetime(2026, 1, 4, 22, 0, tzinfo=UTC)
    fin = ts + timedelta(days=30 * mois)
    prix, out, i = 1.1000, [], 0
    while ts < fin:
        if marche_ouvert(ts):
            vol = 0.000055 * (1.0 + 0.6 * math.sin(2 * math.pi * i / 8000))
            derive = 0.0000006 * math.sin(2 * math.pi * i / 40000)
            o = prix
            c = prix + derive + rng.gauss(0, vol)
            h = max(o, c) + abs(rng.gauss(0, vol * 0.6))
            l = min(o, c) - abs(rng.gauss(0, vol * 0.6))
            out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
            prix = c
            i += 1
        ts += timedelta(minutes=1)
    return out


def titre(t):
    print(f"\n{t}\n" + "─" * max(len(t), 68))


def bloc_stat(nom, s):
    if not s["publiable"]:
        print(f"   {nom:<26} données insuffisantes — {s['n']} sur 100 nécessaires")
        return
    print(f"   {nom:<26} {s['esperance']:+.3f} R  ± {s['ic95']:.3f}"
          f"   n={s['n']:>5}   atteint {s['atteint']:.0%}   [{s['statut']}]")


def main():
    titre("1. Historique")
    m1 = historique()
    h1 = agregation.agreger(m1, "H1")
    h4 = agregation.agreger(m1, "H4")
    d1 = agregation.agreger(m1, "D1")
    print(f"   {len(m1):>7} bougies M1   ·   {len(h1)} H1   ·   {len(h4)} H4   ·   {len(d1)} D1")
    print(f"   du {m1[0]['ts']:%Y-%m-%d} au {m1[-1]['ts']:%Y-%m-%d}")

    titre("2. Chaîne complète — détection, score, résolution, coûts")
    ranges, lignes = pipeline.executer("EURUSD", "H1", h1, m1, h4, d1)
    annoncees = [l for l in lignes if l.statut == "annoncee"]
    ecartees = [l for l in lignes if l.statut == "ecartee"]
    print(f"   {len(ranges):>5} ranges constitués")
    print(f"   {len(lignes):>5} détections   →   {len(annoncees)} annoncées"
          f"   ·   {len(ecartees)} écartées et conservées")

    motifs = {}
    for l in ecartees:
        motifs[l.motif_rejet] = motifs.get(l.motif_rejet, 0) + 1
    print("\n   Motifs de rejet")
    for m, n in sorted(motifs.items(), key=lambda x: -x[1]):
        print(f"     {n:>5}  {m}")

    titre("3. Résultats — nets de spread, glissement et portage")
    print("   Objectif de la méthode")
    bloc_stat("toutes détections", pipeline.statistiques(lignes))
    bloc_stat("annoncées", pipeline.statistiques(annoncees))
    bloc_stat("écartées (groupe témoin)", pipeline.statistiques(ecartees))
    print("\n   Objectifs à ratio fixe, sur les annoncées")
    bloc_stat("objectif 1,5 R", pipeline.statistiques(annoncees, "1r5"))
    bloc_stat("objectif 2 R", pipeline.statistiques(annoncees, "2r"))

    print("\n   Par méthode (objectif de la méthode)")
    for m in ("R1a", "R1b", "R2", "R3"):
        bloc_stat(m, pipeline.statistiques([l for l in lignes if l.methode == m]))

    sa = pipeline.statistiques(annoncees)
    se = pipeline.statistiques(ecartees)
    if sa["publiable"] and se["publiable"]:
        print(f"\n   Écart annoncées − témoin : {sa['esperance'] - se['esperance']:+.3f} R")
    else:
        print("\n   Écart annoncées − témoin : non publiable, échantillon insuffisant")

    titre("4. Distribution des scores — le seuil d'annonce est-il atteignable ?")
    from collections import Counter
    dist = Counter(round(l.score_normalise * 10) for l in lignes)
    for k in sorted(dist):
        barre = "█" * max(1, dist[k] * 40 // max(dist.values()))
        print(f"   {k * 10:>3}% {barre} {dist[k]}")
    atteint = sum(n for k, n in dist.items() if k >= 7)
    print(f"\n   Détections atteignant le seuil de 70 % : {atteint} sur {len(lignes)}")
    print("   Le seuil initial de 0,70 est une valeur posée a priori. Le cahier")
    print("   des charges (§31, point 6) impose de le CALIBRER SUR LES DONNÉES,")
    print("   après 400 occurrences. Cette distribution est la mesure qui servira.")

    titre("5. Une détection, telle que l'utilisateur la verrait")
    ex = annoncees[0] if annoncees else lignes[0]
    print(f"   EUR/USD · H1 · Range {ex.methode} · "
          f"{'ANNONCÉE' if ex.statut == 'annoncee' else 'ÉCARTÉE'} · "
          f"{ex.score_normalise:.0%}  ({ex.score_points}/{ex.score_max})")
    print(f"   {ex.entree_ts:%Y-%m-%d %H:%M} UTC   sens {'achat' if ex.sens > 0 else 'vente'}")
    print(f"   entrée {ex.entree:.5f}   invalidation {ex.invalidation:.5f}"
          f"   objectif {ex.objectif:.5f}")
    print("   détail du score")
    for k, v in ex.detail.items():
        if v.get("neutralise"):
            print(f"     {k:<14} —  neutralisé : contenu dans la définition du range")
        else:
            print(f"     {k:<14} {str(v.get('points')):>3}   {v.get('mesure','')}")
    iss = ex.issues["methode"]
    if iss:
        print(f"   issue : {iss['resultat']}   "
              f"{iss['r_brut']:+.2f} R brut   →   {iss['r_net']:+.2f} R net")
        print(f"   coûts : spread {iss['cout_spread']:.6f}"
              f"   glissement {iss['cout_glissement']:.6f}"
              f"   portage {iss['cout_portage']:.6f}")

    titre("6. Registre — arbre de Merkle et chaîne")
    chaine = registre.Chaine()
    par_cycle = {}
    for l in lignes:
        cle = l.entree_ts.replace(minute=0, second=0, microsecond=0)
        par_cycle.setdefault(cle, []).append(l.empreinte)
    for cle in sorted(par_cycle):
        chaine.ajouter(cle, par_cycle[cle])
    ok, msg = chaine.verifier()
    print(f"   {len(chaine.cycles)} cycles horaires · {len(lignes)} feuilles")
    print(f"   vérification : {'✓' if ok else '✗'} {msg}")
    print(f"   tête de chaîne : {chaine.derniere_tete[:48]}…")

    c0 = chaine.cycles[0]
    preuve = registre.preuve_inclusion(c0.feuilles, 0)
    valide = registre.verifier_inclusion(c0.feuilles[0], preuve, c0.racine)
    print(f"   preuve d'inclusion d'une détection : {len(preuve)} empreintes, "
          f"{'✓ vérifiée' if valide else '✗ invalide'}")

    original = chaine.cycles[0].feuilles[0]
    chaine.cycles[0].feuilles[0] = "0" * 64
    ok2, msg2 = chaine.verifier()
    chaine.cycles[0].feuilles[0] = original
    print(f"   falsification d'une feuille : {'✓ détectée' if not ok2 else '✗ NON DÉTECTÉE'}"
          f" — {msg2}")

    titre("7. Test point-in-time sur la chaîne complète")
    coupure = len(h1) * 2 // 3
    tronque = h1[:coupure]
    fin = tronque[-1]["ts"]
    m1t = [b for b in m1 if b["ts"] <= fin]
    _, ref = pipeline.executer("EURUSD", "H1", tronque, m1t, h4, d1)
    aberr = determinisme.donnees_aberrantes(tronque, facteur=10.0, nombre=500)
    _, avec = pipeline.executer("EURUSD", "H1", tronque + aberr, m1t, h4, d1)
    e_ref = [l.empreinte for l in ref if l.entree_ts <= fin]
    e_avec = [l.empreinte for l in avec if l.entree_ts <= fin]
    sain = e_ref == e_avec[:len(e_ref)]
    print(f"   {len(e_ref)} détections recalculées avec 500 bougies aberrantes"
          f" collées après la coupure")
    print(f"   {'✓ aucune ne change — aucune fuite d information future' if sain else '✗ FUITE DÉTECTÉE'}")

    titre("Conclusion")
    print("   La chaîne complète tourne : bougie M1 → range → score → résolution")
    print("   intra-bougie → coûts nets → empreinte → arbre de Merkle → chaîne.")
    print("   Les configurations écartées sont conservées avec leur motif.")
    print("   Les résultats sont nets de spread, de glissement et de portage.")
    print("\n   Ce que ces chiffres ne sont PAS : une preuve d'avantage.")
    print("   Ils portent sur des données synthétiques, et un backtest ne")
    print("   démontre rien. Seul le registre prospectif le fera.")
    if not sain:
        sys.exit(1)


if __name__ == "__main__":
    main()
