"""Moteur statistique — SPEC-LOTS-6-15 §9.

Deux règles imposées par le code, pas par la discipline :
  1. aucun chiffre n'est renvoyé sous 100 occurrences ;
  2. aucune statistique n'est servie sans terme de comparaison.
"""
from __future__ import annotations

import math

SEUIL_PUBLIABLE = 100
SEUIL_ETABLI = 400


def agregat(rs, resultats=None, ambigus=0):
    """Agrégat élémentaire. `rs` = liste des R nets."""
    n = len(rs)
    if n == 0:
        return {"n": 0, "publiable": False, "statut": "insuffisant"}
    moy = sum(rs) / n
    var = sum((x - moy) ** 2 for x in rs) / (n - 1) if n > 1 else 0.0
    et = math.sqrt(var)
    out = {
        "n": n, "esperance": moy, "ecart_type": et,
        "ic95": 1.96 * et / math.sqrt(n),
        "publiable": n >= SEUIL_PUBLIABLE,
        "statut": ("établi" if n >= SEUIL_ETABLI
                   else "provisoire" if n >= SEUIL_PUBLIABLE else "insuffisant"),
        "manquant": max(0, SEUIL_PUBLIABLE - n),
        "ambigu": ambigus / n,
    }
    if resultats:
        out.update({
            "atteint": resultats.count("atteint") / n,
            "invalide": resultats.count("invalide") / n,
            "sans_issue": resultats.count("sans_issue") / n,
        })
    return out


def _phi(x):
    """Loi normale centrée réduite, fonction de répartition."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def p_valeur(s):
    """Test bilatéral, H0 : espérance nulle."""
    if s["n"] < 2 or s["ecart_type"] == 0:
        return 1.0
    z = s["esperance"] / (s["ecart_type"] / math.sqrt(s["n"]))
    return 2 * (1 - _phi(abs(z)))


def benjamini_hochberg(series, alpha=0.05):
    """Contrôle du taux de fausses découvertes — SPEC-LOTS-6-15 §9.3.

    `series` = {nom: agrégat}. Retourne {nom: {p, significatif, rang}}.

    Sans cette correction, tester 144 séries fait ressortir environ 7 résultats
    « significatifs » par pur hasard. Un classement sans correction ne classe
    pas des figures : il classe du bruit.
    """
    candidats = [(nom, p_valeur(s)) for nom, s in series.items() if s["publiable"]]
    m = len(candidats)
    if m == 0:
        return {}
    candidats.sort(key=lambda x: x[1])
    seuil_max, out = 0.0, {}
    for i, (nom, p) in enumerate(candidats, start=1):
        if p <= i / m * alpha:
            seuil_max = p
    for i, (nom, p) in enumerate(candidats, start=1):
        out[nom] = {"p": p, "rang": i, "m": m, "significatif": p <= seuil_max}
    return out


def comparer(serie, temoin, nom_temoin="groupe témoin"):
    """Une statistique n'est jamais servie seule (SPEC-LOTS-6-15 §9.4).

    Lève une erreur si le terme de comparaison manque : la règle est ainsi
    imposée par le code, et non laissée à la discipline de l'appelant.
    """
    if temoin is None:
        raise ValueError("terme de comparaison obligatoire")
    if not serie["publiable"]:
        return {"publiable": False, "n": serie["n"], "manquant": serie["manquant"],
                "message": f"données insuffisantes — {serie['n']} sur {SEUIL_PUBLIABLE}"}
    base = {"valeur": serie["esperance"], "ic95": serie["ic95"], "n": serie["n"],
            "statut": serie["statut"], "comparaison": {"nom": nom_temoin}}
    if temoin["publiable"]:
        ecart = serie["esperance"] - temoin["esperance"]
        # variance de la différence de deux moyennes indépendantes
        se = math.sqrt(serie["ic95"] ** 2 + temoin["ic95"] ** 2)
        base["comparaison"].update({
            "valeur": temoin["esperance"], "n": temoin["n"],
            "ecart": ecart, "ic95_ecart": se,
            "ecart_significatif": abs(ecart) > se,
        })
    else:
        base["comparaison"]["message"] = "témoin insuffisant"
    return base


def classement(series, alpha=0.05):
    """Classement corrigé. Affiche toujours le nombre de séries testées."""
    bh = benjamini_hochberg(series, alpha)
    lignes = []
    for nom, s in series.items():
        if not s["publiable"]:
            continue
        c = bh.get(nom, {})
        lignes.append({"nom": nom, "esperance": s["esperance"], "n": s["n"],
                       "ic95": s["ic95"], "p": c.get("p"),
                       "significatif": c.get("significatif", False)})
    lignes.sort(key=lambda x: -x["esperance"])
    return {"lignes": lignes, "series_testees": len(series),
            "series_publiables": len(lignes)}
