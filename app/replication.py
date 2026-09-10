"""Réplication sur plusieurs jeux de données INDÉPENDANTS.

    python3 replication.py

Un résultat obtenu sur une seule période peut être un accident. Le répéter sur
des périodes différentes, issues de sources différentes, est la seule façon de
savoir si le verdict tient.

CE QU'ON NE FAIT PAS : concaténer les jeux. Mélanger des sources de prix
distinctes violerait la règle du cahier des charges §15 — publier la source
retenue et n'en jamais changer. On exécute séparément, on compare les verdicts.
"""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

from forexlab import agregation, backtest, pipeline, stats

UTC = timezone.utc


def lire_mt4(chemin):
    """Format d'export MetaTrader : AAAA.MM.JJ,HH:MM,O,H,L,C,V (sans en-tête)."""
    out = []
    with open(chemin, newline="", encoding="utf-8", errors="ignore") as f:
        for r in csv.reader(f):
            if len(r) < 6:
                continue
            try:
                ts = datetime.strptime(f"{r[0]} {r[1]}", "%Y.%m.%d %H:%M").replace(tzinfo=UTC)
                o, h, l, c = (float(x) for x in r[2:6])
            except ValueError:
                continue
            if l <= min(o, c) and max(o, c) <= h:
                out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
    out.sort(key=lambda b: b["ts"])
    return out


def lire_paquet():
    from backtesting.test import EURUSD
    return [{"ts": t.to_pydatetime().replace(tzinfo=UTC), "o": float(r["Open"]),
             "h": float(r["High"]), "l": float(r["Low"]), "c": float(r["Close"])}
            for t, r in EURUSD.iterrows()]


def agreger_h1(h1, unite):
    attendu = {"H4": 4, "D1": 24}[unite]
    agg = agregation.agreger(h1, unite)
    for b in agg:
        b["complete"] = b["minutes"] >= 0.75 * attendu
    return agg


def executer(nom, h1):
    h4, d1 = agreger_h1(h1, "H4"), agreger_h1(h1, "D1")
    _, lignes = pipeline.executer("EURUSD", "H4", h4, h1, d1, d1, catalogue=True)

    def agr(sel, cible="methode"):
        rs = [l.issues[cible]["r_net"] for l in sel if l.issues.get(cible)]
        res = [l.issues[cible]["resultat"] for l in sel if l.issues.get(cible)]
        amb = sum(1 for l in sel if l.issues.get(cible) and l.issues[cible]["ambigu_m1"])
        return stats.agregat(rs, res, amb)

    series = {}
    for cle in sorted({(l.figure, l.methode) for l in lignes}):
        series[cle[1]] = agr([l for l in lignes if (l.figure, l.methode) == cle])
    cl = stats.classement(series)
    dec = backtest.rapport_decision(lignes, cl["series_testees"])
    s = agr(lignes)
    return {
        "nom": nom, "bougies": len(h1),
        "debut": h1[0]["ts"], "fin": h1[-1]["ts"],
        "detections": len(lignes),
        "annoncees": sum(1 for l in lignes if l.statut == "annoncee"),
        "esperance": s.get("esperance"), "ic95": s.get("ic95"), "n": s["n"],
        "verdict": dec["verdict"],
        "dsr": dec.get("deflate", {}).get("dsr"),
        "wf": dec.get("walk_forward", {}),
    }


def main():
    jeux = []
    for nom, chemin in (("GitHub · petewerner · 2013", "EURUSD_H1_2013.csv"),
                        ("GitHub · tapy · 2019", "EURUSD_H1_2019.csv")):
        p = ICI / "data" / chemin
        if p.exists():
            jeux.append((nom, lire_mt4(p)))
    try:
        jeux.append(("paquet backtesting · 2017-18", lire_paquet()))
    except Exception:
        pass

    print("RÉPLICATION — mêmes règles, périodes et sources indépendantes\n")
    resultats = []
    for nom, h1 in jeux:
        if len(h1) < 500:
            print(f"  {nom} : trop court ({len(h1)} bougies), ignoré")
            continue
        r = executer(nom, h1)
        resultats.append(r)
        print(f"  {r['nom']:<30} {r['bougies']:>5} H1 · "
              f"{r['debut']:%Y-%m} → {r['fin']:%Y-%m}")

    print("\n" + "─" * 78)
    print(f"{'jeu':<30}{'détections':>11}{'espérance':>12}{'IC 95%':>10}{'verdict':>12}")
    print("─" * 78)
    for r in resultats:
        e = f"{r['esperance']:+.3f} R" if r["esperance"] is not None else "—"
        ic = f"±{r['ic95']:.3f}" if r["ic95"] is not None else "—"
        print(f"{r['nom']:<30}{r['detections']:>11}{e:>12}{ic:>10}{r['verdict']:>12}")
    print("─" * 78)

    print("\nValidation séquentielle — ce qui survit hors échantillon")
    for r in resultats:
        wf = r["wf"]
        if wf.get("suffisant"):
            print(f"  {r['nom']:<30} calibré {wf['esperance_calibree']:+.3f} R "
                  f"→ hors échantillon {wf['esperance_hors_echantillon']:+.3f} R")
        else:
            print(f"  {r['nom']:<30} échantillon insuffisant "
                  f"({wf.get('n', 0)} détections)")

    verdicts = {r["verdict"] for r in resultats}
    annoncees = sum(r["annoncees"] for r in resultats)
    print(f"\nVerdicts obtenus : {', '.join(sorted(verdicts))}")
    print(f"Configurations annoncées, tous jeux confondus : {annoncees}")
    if verdicts <= {"nul", "negatif"}:
        print("\nAucun jeu ne fait ressortir d'avantage. Le résultat se répète sur des")
        print("périodes et des sources différentes : ce n'est pas un accident de")
        print("période. Il reste que chaque échantillon est trop petit pour conclure")
        print("à l'ABSENCE d'avantage — seulement qu'aucun ne ressort.")


if __name__ == "__main__":
    main()
