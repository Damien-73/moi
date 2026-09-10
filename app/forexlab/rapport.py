"""Génération des écrans — SPEC-ECRANS et SPEC-DESIGN.

Règles appliquées, non négociables :
  · un seul chiffre par écran, toujours avec son terme de comparaison ;
  · chiffres tabulaires partout — sans eux les colonnes ne s'alignent pas
    et le produit perd instantanément son air sérieux ;
  · encodage BLEU / ORANGE, jamais rouge/vert : environ 8 % des hommes ont
    une déficience de perception du rouge et du vert, ce qui serait un défaut
    fonctionnel dans un produit dont la valeur tient à la lecture de résultats ;
  · les issues défavorables au même rang que les favorables, jamais repliées.
"""
from __future__ import annotations

import html
from pathlib import Path

CSS = """
:root{
  --fond:#FAF9F7; --surface:#FFFFFF; --texte:#16181D; --second:#5F6570;
  --bord:#E6E3DE; --accent:#1F4FD8; --favorable:#1F6FEB; --defavorable:#C2621A;
  --neutre:#8A8F98;
}
@media (prefers-color-scheme:dark){
  :root{--fond:#0E0F11;--surface:#17181B;--texte:#EDEDEF;--second:#9BA1AC;
        --bord:#26282D;--accent:#5B85F5;--favorable:#5B85F5;--defavorable:#D98A4A;}
}
*{box-sizing:border-box}
body{margin:0;background:var(--fond);color:var(--texte);
  font:16px/1.55 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-variant-numeric:tabular-nums;}
.page{max-width:1180px;margin:0 auto;padding:32px 24px 96px}
header{display:flex;gap:24px;align-items:baseline;flex-wrap:wrap;
  border-bottom:1px solid var(--bord);padding-bottom:16px;margin-bottom:32px}
h1{font-size:22px;margin:0;font-weight:600;letter-spacing:-.01em}
nav a{color:var(--second);text-decoration:none;margin-right:16px;font-size:14px}
nav a:hover,nav a.actif{color:var(--accent)}
.chiffre{font-size:52px;font-weight:600;letter-spacing:-.02em;line-height:1.05}
.libelle{color:var(--second);font-size:15px;margin-top:4px}
.comparaison{color:var(--second);font-size:13px;margin-top:12px;
  border-top:1px solid var(--bord);padding-top:12px}
.tetiere{display:flex;gap:64px;flex-wrap:wrap;margin-bottom:40px}
.carte{background:var(--surface);border:1px solid var(--bord);border-radius:8px;
  padding:16px 18px;margin-bottom:12px}
.ligne1{display:flex;justify-content:space-between;gap:16px;align-items:baseline;
  flex-wrap:wrap}
.titre{font-weight:600}
.etat{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--second)}
.niveaux{color:var(--second);font-size:14px;margin-top:8px}
.pied{color:var(--second);font-size:12px;margin-top:12px;
  border-top:1px solid var(--bord);padding-top:10px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.fav{color:var(--favorable)} .def{color:var(--defavorable)} .neu{color:var(--neutre)}
table{border-collapse:collapse;width:100%;font-size:15px}
th{text-align:left;color:var(--second);font-weight:500;font-size:13px;
  border-bottom:1px solid var(--bord);padding:8px 10px}
td{padding:9px 10px;border-bottom:1px solid var(--bord)}
tr:hover td{background:var(--surface)}
.num{text-align:right}
.insuffisant{color:var(--second);font-style:italic}
.avert{background:var(--surface);border:1px solid var(--bord);border-left:3px solid var(--defavorable);
  border-radius:6px;padding:12px 16px;color:var(--second);font-size:13px;margin-top:48px}
.motif{color:var(--defavorable);font-size:14px;margin-top:8px}
"""

NAV = [("index.html", "Registre"), ("ecartees.html", "Écartées"),
       ("figures.html", "Figures"), ("integrite.html", "Preuve")]

AVERT = ("Les performances passées ne préjugent pas des performances futures. "
         "70 à 85 % des comptes de particuliers perdent de l'argent sur les contrats "
         "financiers. Ce service fournit des analyses statistiques impersonnelles "
         "et ne constitue pas un conseil en investissement.")


def _e(x):
    return html.escape(str(x))


def _page(titre, actif, corps):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (u, ' class="actif"' if u == actif else "", t)
        for u, t in NAV)
    return (f"<!doctype html><html lang=fr><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{_e(titre)}</title><style>{CSS}</style></head><body><div class=page>"
            f"<header><h1>Registre prospectif</h1><nav>{nav}</nav></header>"
            f"{corps}<div class=avert>{AVERT}</div></div></body></html>")


def _tetiere(chiffre, libelle, comparaison):
    return (f"<div class=tetiere><div><div class=chiffre>{chiffre}</div>"
            f"<div class=libelle>{libelle}</div>"
            f"<div class=comparaison>{comparaison}</div></div></div>")


def _issue(l):
    i = l.issues.get("methode")
    if not i:
        return '<span class=neu>non résolue</span>'
    if i["resultat"] == "atteint":
        return f'<span class=fav>objectif atteint · {i["r_net"]:+.2f} R net</span>'
    if i["resultat"] == "invalide":
        return f'<span class=def>invalidée · {i["r_net"]:+.2f} R net</span>'
    return f'<span class=neu>sans issue · {i["r_net"]:+.2f} R net</span>'


def _carte(l, montrer_motif=False):
    etat = "ANNONCÉE" if l.statut == "annoncee" else "ÉCARTÉE"
    sens = "achat" if l.sens > 0 else "vente"
    c = [f"<div class=carte><div class=ligne1>"
         f"<span class=titre>{_e(l.symbole)} · {_e(l.unite)} · {_e(l.methode)}</span>"
         f"<span class=etat>{etat} · {l.score_normalise:.0%}</span></div>"
         f"<div class=niveaux>{sens} · entrée {l.entree:.5f} · "
         f"invalidation {l.invalidation:.5f} · objectif {l.objectif:.5f}</div>"
         f"<div class=niveaux>{_issue(l)}</div>"]
    if montrer_motif and l.motif_rejet:
        c.append(f"<div class=motif>Motif : {_e(l.motif_rejet)}</div>")
    c.append(f"<div class=pied>publiée {l.entree_ts:%Y-%m-%d %H:%M} UTC · "
             f"empreinte {l.empreinte[:16]}… · ancrée</div></div>")
    return "".join(c)


def _stat(s, temoin=None):
    if not s["publiable"]:
        return (f"<span class=insuffisant>données insuffisantes — "
                f"{s['n']} sur 100 nécessaires</span>")
    t = ""
    if temoin and temoin.get("publiable"):
        t = f" · témoin {temoin['esperance']:+.3f} R"
    return f"{s['esperance']:+.3f} R ± {s['ic95']:.3f} · n = {s['n']}{t}"


def ecrire(dossier, lignes, stats_annoncees, stats_ecartees, classement,
           integrite):
    """Produit les quatre écrans publics."""
    d = Path(dossier)
    d.mkdir(parents=True, exist_ok=True)
    annoncees = [l for l in lignes if l.statut == "annoncee"]
    ecartees = [l for l in lignes if l.statut == "ecartee"]

    # Écran 1 — registre en direct
    if stats_annoncees["publiable"]:
        chiffre = f'{stats_annoncees["esperance"]:+.3f} R'
        lib = "espérance nette des configurations annoncées"
    else:
        chiffre = f'{len(annoncees)}'
        lib = "configurations annoncées"
    comp = (f"Groupe témoin : {_stat(stats_ecartees)}"
            f" &nbsp;·&nbsp; {len(lignes)} détections conservées, "
            f"{len(ecartees)} écartées")
    corps = _tetiere(chiffre, lib, comp)
    corps += "<p class=libelle>Chaque détection est publiée avant que son issue soit connue. Les échecs figurent au même rang que les réussites.</p>"
    corps += "".join(_carte(l) for l in (annoncees or lignes)[:40])
    (d / "index.html").write_text(_page("Registre", "index.html", corps), encoding="utf-8")

    # Écran 3 — écartées, le groupe témoin
    ec = _stat(stats_ecartees)
    if stats_ecartees["publiable"] and stats_annoncees["publiable"]:
        ecart = stats_annoncees["esperance"] - stats_ecartees["esperance"]
        comp = (f"Annoncées : {stats_annoncees['esperance']:+.3f} R "
                f"(n = {stats_annoncees['n']}) &nbsp;·&nbsp; écart {ecart:+.3f} R")
        chiffre = f'{stats_ecartees["esperance"]:+.3f} R'
    else:
        comp = f"Annoncées : {_stat(stats_annoncees)}"
        chiffre = f"{len(ecartees)}"
    corps = _tetiere(chiffre, "espérance nette des configurations écartées", comp)
    corps += "<p class=libelle>Nous conservons et publions ce que nous écartons. Sans ce groupe témoin, la valeur du filtrage serait indémontrable.</p>"
    corps += "".join(_carte(l, True) for l in ecartees[:40])
    (d / "ecartees.html").write_text(_page("Écartées", "ecartees.html", corps),
                                     encoding="utf-8")

    # Écran 4 — classement des figures, corrigé
    lignes_tab = "".join(
        f"<tr><td>{_e(l['nom'])}</td><td class=num>{l['n']}</td>"
        f"<td class=num>{l['esperance']:+.3f}</td>"
        f"<td class=num>± {l['ic95']:.3f}</td>"
        f"<td class=num>{'oui' if l['significatif'] else 'non'}</td></tr>"
        for l in classement["lignes"])
    corps = _tetiere(f"{classement['series_publiables']}",
                     "séries publiables",
                     f"{classement['series_testees']} séries testées · "
                     f"correction de tests multiples appliquée (Benjamini-Hochberg)")
    corps += ("<table><tr><th>Figure et méthode</th><th class=num>n</th>"
              "<th class=num>espérance nette</th><th class=num>IC 95 %</th>"
              "<th class=num>significatif</th></tr>" + lignes_tab + "</table>")
    corps += ("<p class=libelle>Le nombre de séries testées est affiché : sans lui, "
              "un lecteur ne peut pas juger de l'ampleur du test multiple.</p>")
    (d / "figures.html").write_text(_page("Figures", "figures.html", corps),
                                    encoding="utf-8")

    # Écran 5 — preuve et intégrité
    corps = _tetiere(f"{integrite['cycles']}", "cycles ancrés",
                     f"{integrite['detections']} détections · "
                     f"{integrite['cycles_vides']} cycles vides, ancrés quand même")
    corps += "<table><tr><th>Contrôle</th><th>Résultat</th></tr>"
    for c in ["Empreintes de détection recalculées",
              "Racines de Merkle recalculées",
              "Chaîne des têtes continue",
              "Toute détection appartient à un cycle",
              "Configurations écartées présentes dans la chaîne",
              "Numérotation des cycles continue"]:
        v = ("<span class=fav>conforme</span>" if integrite["valide"]
             else "<span class=def>à vérifier</span>")
        corps += f"<tr><td>{c}</td><td>{v}</td></tr>"
    corps += "</table>"
    corps += ("<p class=libelle>Téléchargez le jeu de données et le vérificateur, "
              "puis exécutez <code>python3 verificateur.py registre.json</code>. "
              "Il recalcule tout sans accès à nos serveurs. "
              "Toute divergence confirmée sera publiée.</p>")
    (d / "integrite.html").write_text(_page("Preuve", "integrite.html", corps),
                                      encoding="utf-8")
    return d
