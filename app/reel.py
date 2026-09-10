"""Exécution sur données de marché RÉELLES.

    python3 reel.py

Source : jeu EUR/USD horaire embarqué dans le paquet `backtesting` (données
histdata.com), 5 000 bougies, avril 2017 – février 2018.

DEUX DÉGRADATIONS ASSUMÉES ET MARQUÉES, à ne jamais oublier en lisant les
chiffres produits :

  1. Pas de données M1. La résolution intra-bougie se fait donc en H1 au lieu
     de M1. Quand objectif et invalidation tombent dans la même bougie, la
     règle conservatrice compte une INVALIDATION : avec des bougies 60 fois
     plus grossières, ce cas devient fréquent et les résultats sont
     PESSIMISTES. Le taux d'ambiguïté est publié.

  2. Pas de bid/ask. Le spread est estimé, non mesuré. Toute détection issue
     de ce jeu doit être marquée `spread_estime` (SPEC-DONNEES-REFERENCE §3).
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from datetime import timedelta, timezone
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

from forexlab import (agregation, backtest, contrainte, export, pipeline,
                      rapport, registre, stats)
import verificateur

UTC = timezone.utc


def charger_reel():
    from backtesting.test import EURUSD
    out = []
    for ts, r in EURUSD.iterrows():
        t = ts.to_pydatetime().replace(tzinfo=UTC)
        out.append({"ts": t, "o": float(r["Open"]), "h": float(r["High"]),
                    "l": float(r["Low"]), "c": float(r["Close"])})
    out.sort(key=lambda b: b["ts"])
    return out


def agreger_depuis_h1(h1, unite):
    """Agrège des bougies H1 réelles. `complete` est jugé sur le nombre de H1."""
    attendu = {"H4": 4, "D1": 24}[unite]
    agg = agregation.agreger(h1, unite)
    for b in agg:
        b["complete"] = b["minutes"] >= 0.75 * attendu
    return agg


def titre(t):
    print(f"\n{t}\n" + "─" * max(len(t), 72))


def bloc(nom, s):
    if not s["publiable"]:
        print(f"   {nom:<26} données insuffisantes — {s['n']} sur 100")
        return
    print(f"   {nom:<26} {s['esperance']:+.3f} R ± {s['ic95']:.3f}   "
          f"n={s['n']:>5}   atteint {s.get('atteint', 0):.0%}   "
          f"ambigu {s['ambigu']:.0%}   [{s['statut']}]")


def main():
    titre("Données réelles EUR/USD")
    h1 = charger_reel()
    print(f"   {len(h1)} bougies H1 · du {h1[0]['ts']:%Y-%m-%d} au {h1[-1]['ts']:%Y-%m-%d}")
    amplitude = max(b["h"] for b in h1) - min(b["l"] for b in h1)
    print(f"   amplitude de la période : {amplitude * 1e4:.0f} pips")
    print("   ⚠ résolution en H1 faute de M1 → résultats PESSIMISTES")
    print("   ⚠ spread ESTIMÉ faute de bid/ask")

    h4 = agreger_depuis_h1(h1, "H4")
    d1 = agreger_depuis_h1(h1, "D1")
    print(f"   {len(h4)} bougies H4 · {len(d1)} journalières")

    titre("Chaîne complète — détection sur H4, résolution sur H1")
    ranges, lignes = pipeline.executer("EURUSD", "H4", h4, h1, d1, d1,
                                       catalogue=True)
    annoncees = [l for l in lignes if l.statut == "annoncee"]
    ecartees = [l for l in lignes if l.statut == "ecartee"]
    print(f"   {len(ranges)} ranges · {len(lignes)} détections "
          f"→ {len(annoncees)} annoncées, {len(ecartees)} écartées")
    print("\n   Par figure")
    for f, n in Counter(l.figure for l in lignes).most_common():
        print(f"      {n:>5}  {f}")
    print("\n   Motifs de rejet")
    for m, n in Counter(l.motif_rejet for l in ecartees).most_common():
        print(f"      {n:>5}  {m}")

    def agr(sel, cible="methode"):
        rs = [l.issues[cible]["r_net"] for l in sel if l.issues.get(cible)]
        res = [l.issues[cible]["resultat"] for l in sel if l.issues.get(cible)]
        amb = sum(1 for l in sel if l.issues.get(cible) and l.issues[cible]["ambigu_m1"])
        return stats.agregat(rs, res, amb)

    sa, se, st = agr(annoncees), agr(ecartees), agr(lignes)

    titre("Résultats nets — spread, glissement et portage déduits")
    bloc("annoncées", sa)
    bloc("écartées (témoin)", se)
    bloc("toutes", st)
    print("\n   Par objectif")
    for c, nom in (("methode", "projection figure"), ("1r5", "1,5 R"), ("2r", "2 R")):
        bloc(nom, agr(lignes, c))

    titre("Classement corrigé du test multiple")
    series = {}
    for cle in sorted({(l.figure, l.methode) for l in lignes}):
        series[cle[1]] = agr([l for l in lignes if (l.figure, l.methode) == cle])
    cl = stats.classement(series)
    print(f"   {cl['series_publiables']} séries publiables sur {cl['series_testees']} testées")
    for l in cl["lignes"]:
        print(f"   {l['nom']:<26} {l['esperance']:+.3f} R ± {l['ic95']:.3f}  "
              f"n={l['n']:>5}  {'significatif' if l['significatif'] else ''}")
    if not cl["lignes"]:
        print("   aucune série n'atteint 100 occurrences")

    titre("Backtest honnête — verdict")
    dec = backtest.rapport_decision(lignes, cl["series_testees"])
    if dec["verdict"] == "insuffisant":
        print(f"   échantillon insuffisant : {dec['n']} détections")
    else:
        print(f"   espérance nette {dec['esperance']:+.3f} R sur {dec['n']} détections")
        d = dec["deflate"]
        if d.get("suffisant"):
            print(f"   Sharpe {d['sharpe']:+.3f} · seuil test multiple "
                  f"{d['sharpe_seuil']:.3f} ({d['essais']} séries)")
            print(f"   Sharpe déflaté {d['dsr']:.1%} "
                  f"{'significatif' if d['significatif'] else '— NON significatif'}")
        wf = dec["walk_forward"]
        if wf.get("suffisant"):
            print(f"   séquentiel : calibré {wf['esperance_calibree']:+.3f} R → "
                  f"hors échantillon {wf['esperance_hors_echantillon']:+.3f} R")
            print(f"   seuils par pli : {', '.join(f'{s:.2f}' for s in wf['seuils'])}"
                  f" ({'stables' if wf['seuil_stable'] else 'INSTABLES'})")
        else:
            print(f"   séquentiel : {wf.get('raison', 'échantillon insuffisant')}")
        print(f"\n   VERDICT : {dec['verdict'].upper()}")
        print(f"   {dec['conduite']}")

    titre("Registre et vérification indépendante")
    ch = registre.Chaine()
    seaux = defaultdict(list)
    for l in lignes:
        seaux[l.entree_ts.replace(minute=0, second=0, microsecond=0)].append(l.empreinte)
    for k in sorted(seaux):
        ch.ajouter(k, seaux[k])
    f = export.exporter(lignes, ch, ICI / "data" / "registre_reel.json")
    v = verificateur.verifier(f)
    print(f"   {v['cycles']} cycles · {v['detections']} détections · "
          f"{'✓ conforme' if v['valide'] else '✗ ' + '; '.join(v['erreurs'])}")

    site = rapport.ecrire(ICI / "data" / "site_reel", lignes, sa, se, cl, v)
    print(f"   écrans : {site.relative_to(ICI)}/index.html")

    titre("Rappel")
    print("   Résolution H1 et spread estimé : ces chiffres sont PESSIMISTES")
    print("   et approximatifs. Ils orientent une décision, ils ne prouvent rien.")


if __name__ == "__main__":
    main()
