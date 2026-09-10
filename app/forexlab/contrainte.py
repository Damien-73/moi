"""Mode contrainte — SPEC-LOT11.

Répond à « cette approche survit-elle à une limite de perte de 5 % par jour ? »,
et non à « est-elle rentable ? ». Ce sont deux questions différentes, et la
seconde ne se déduit pas de la première.

POINT TECHNIQUE DÉCISIF : le rééchantillonnage se fait par JOURNÉE COMPLÈTE,
jamais par trade isolé. Tirer des trades indépendamment détruit le regroupement
journalier — dont dépend entièrement la limite de perte quotidienne — et la
corrélation entre positions simultanées. Un tirage indépendant SOUS-ESTIME
massivement la probabilité de rupture.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict


def journees(lignes, cible="methode"):
    """Regroupe les résultats en journées de négociation, ordre conservé.

    Chaque journée porte la liste ordonnée de ses R nets et de ses excursions
    défavorables, nécessaires pour évaluer le pire point de la journée.
    """
    seaux = defaultdict(list)
    for l in lignes:
        iss = l.issues.get(cible) if hasattr(l, "issues") else l.get(cible)
        if not iss:
            continue
        jour = l.entree_ts.date() if hasattr(l, "entree_ts") else l["entree_ts"].date()
        seaux[jour].append((iss["r_net"], iss.get("excursion_def", 0.0)))
    return [seaux[j] for j in sorted(seaux)]


def simuler(jours, objectif=0.10, perte_jour=0.05, perte_totale=0.10,
            type_perte="suiveuse", risque=0.01, duree_max=30,
            simulations=10000, graine=0):
    """Retourne la probabilité de réussite et la répartition des causes d'échec."""
    if not jours:
        return {"suffisant": False, "journees": 0}
    if len(jours) < 60:
        return {"suffisant": False, "journees": len(jours), "manquant": 60 - len(jours)}

    rng = random.Random(graine)
    reussites = ech_total = ech_jour = ech_delai = 0
    durees, pires = [], []

    for _ in range(simulations):
        capital, sommet, pire = 1.0, 1.0, 0.0
        issue = None
        for jour_index in range(duree_max):
            debut_jour = capital
            for r_net, exc_def in rng.choice(jours):
                # pire point atteint pendant le trade, avant sa clôture
                flottant = capital * (1 + risque * min(exc_def, 0.0))
                seuil = ((sommet if type_perte == "suiveuse" else 1.0)
                         * (1 - perte_totale))
                if flottant <= seuil:
                    issue = "total"
                    break
                capital *= (1 + risque * r_net)
                sommet = max(sommet, capital)
                pire = max(pire, 1 - capital / sommet)
                if capital <= ((sommet if type_perte == "suiveuse" else 1.0)
                               * (1 - perte_totale)):
                    issue = "total"
                    break
            if issue:
                break
            if capital <= debut_jour * (1 - perte_jour):
                issue = "jour"
                break
            if capital >= 1.0 + objectif:
                issue = "reussite"
                durees.append(jour_index + 1)
                break
        pires.append(pire)
        if issue == "reussite":
            reussites += 1
        elif issue == "total":
            ech_total += 1
        elif issue == "jour":
            ech_jour += 1
        else:
            ech_delai += 1

    p = reussites / simulations
    ic = 1.96 * math.sqrt(p * (1 - p) / simulations)
    durees.sort()
    pires.sort()
    return {
        "suffisant": True, "journees": len(jours),
        "probabilite": p, "ic95": ic,
        "echec_perte_totale": ech_total / simulations,
        "echec_perte_jour": ech_jour / simulations,
        "echec_delai": ech_delai / simulations,
        "duree_mediane": durees[len(durees) // 2] if durees else None,
        "pire_perte_mediane": pires[len(pires) // 2],
        "type_perte": type_perte, "risque": risque,
    }


def balayage_risque(jours, risques=None, **kw):
    """La sortie la plus utile du module : la courbe n'est PAS monotone.

    En dessous de l'optimum on n'atteint pas l'objectif dans le temps imparti ;
    au-dessus on franchit la limite avant. L'optimum se situe presque toujours
    bien plus bas que ce que les traders utilisent.
    """
    risques = risques or [0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.025, 0.03]
    kw.pop("risque", None)
    out = []
    for r in risques:
        s = simuler(jours, risque=r, **kw)
        out.append({"risque": r, "probabilite": s.get("probabilite"),
                    "suffisant": s.get("suffisant", False)})
    valides = [o for o in out if o["probabilite"] is not None]
    optimum = max(valides, key=lambda o: o["probabilite"]) if valides else None
    # Si l'espérance est négative, la courbe ne redescend pas : seule la
    # variance peut atteindre l'objectif, donc « l'optimum » est au risque
    # maximal. Le présenter comme un optimum serait décrire un pari comme une
    # méthode (SPEC-LOT11 §7).
    rs = [r for j in jours for r, _ in j]
    esperance = sum(rs) / len(rs) if rs else 0.0
    pari = esperance <= 0
    return {"courbe": out, "optimum": None if pari else optimum,
            "esperance": esperance, "pari": pari,
            "avertissement": (
                f"Espérance nette de cette sélection : {esperance:+.3f} R. "
                "Aucune taille de position ne rend cette approche viable. "
                "La probabilité augmente avec le risque parce que seule la "
                "chance peut atteindre l'objectif : ce n'est pas une "
                "recommandation, c'est la description d'un pari.") if pari else None}
