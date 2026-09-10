"""Vérificateur public — SPEC-LOT3 §7.

    python3 verificateur.py data/registre.json

Programme autonome qui ne dépend d'aucun service de l'éditeur. Il recalcule
les empreintes, les racines de Merkle et la continuité de la chaîne à partir
du seul jeu de données publié.

C'est ce programme qui transforme une affirmation en preuve. S'il ne peut pas
être exécuté par un tiers sur une machine vierge, tout l'argumentaire du
produit s'effondre.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forexlab import registre

UTC = timezone.utc


def _instant(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def verifier(chemin: Path):
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)

    dets = data["detections"]
    cycles = data["cycles"]
    erreurs = []

    # 1 — empreinte de chaque détection, recalculée depuis ses champs
    mauvaises = 0
    for d in dets:
        attendue = registre.feuille(
            version=d["version"], symbole=d["symbole"], unite=d["unite"],
            sens=d["sens"], entree_ts=_instant(d["entree_ts"]),
            entree=d["entree"], invalidation=d["invalidation"],
            objectif_methode=d["objectif_methode"], objectif_1r5=d["objectif_1r5"],
            objectif_2r=d["objectif_2r"], horizon=d["horizon"],
            score_points=d["score_points"], score_max=d["score_max"],
            statut=d["statut"], motif_rejet=d["motif_rejet"])
        if attendue != d["empreinte"]:
            mauvaises += 1
    if mauvaises:
        erreurs.append(f"{mauvaises} empreintes de détection incorrectes")

    # 2 — racines de Merkle et continuité de la chaîne
    precedente = registre.ZERO
    for c in cycles:
        if registre.racine_merkle(c["feuilles"]) != c["racine"]:
            erreurs.append(f"racine incorrecte au cycle {c['numero']}")
            break
        if registre.tete(precedente, c["racine"], c["numero"],
                         _instant(c["horodatage"]), len(c["feuilles"])) != c["tete"]:
            erreurs.append(f"chaîne rompue au cycle {c['numero']}")
            break
        precedente = c["tete"]

    # 3 — toute détection doit appartenir à un cycle
    dans_cycles = {f for c in cycles for f in c["feuilles"]}
    orphelines = [d for d in dets if d["empreinte"] not in dans_cycles]
    if orphelines:
        erreurs.append(f"{len(orphelines)} détections absentes de la chaîne")

    # 4 — les écartées doivent être dans la chaîne au même titre que les annoncées
    ecartees = [d for d in dets if d["statut"] == "ecartee"]
    ec_chainees = sum(1 for d in ecartees if d["empreinte"] in dans_cycles)
    if ecartees and ec_chainees != len(ecartees):
        erreurs.append("des configurations écartées manquent à la chaîne")

    # 5 — numérotation continue, aucun cycle manquant
    numeros = [c["numero"] for c in cycles]
    if numeros != list(range(len(cycles))):
        erreurs.append("numérotation des cycles discontinue")

    return {
        "detections": len(dets),
        "annoncees": sum(1 for d in dets if d["statut"] == "annoncee"),
        "ecartees": len(ecartees),
        "cycles": len(cycles),
        "cycles_vides": sum(1 for c in cycles if not c["feuilles"]),
        "figures": Counter(d["figure"] for d in dets),
        "erreurs": erreurs,
        "valide": not erreurs,
    }


def main():
    chemin = Path(sys.argv[1] if len(sys.argv) > 1 else "data/registre.json")
    if not chemin.exists():
        print(f"Fichier absent : {chemin}")
        sys.exit(1)
    r = verifier(chemin)
    print(f"Vérification de {chemin}\n")
    print(f"  {r['detections']:>7} détections  "
          f"({r['annoncees']} annoncées, {r['ecartees']} écartées)")
    print(f"  {r['cycles']:>7} cycles        ({r['cycles_vides']} vides, ancrés quand même)")
    print(f"  {len(r['figures']):>7} figures\n")
    controles = [
        "empreintes de détection recalculées",
        "racines de Merkle recalculées",
        "chaîne des têtes continue",
        "toute détection appartient à un cycle",
        "configurations écartées présentes dans la chaîne",
        "numérotation des cycles continue",
    ]
    for c in controles:
        print(f"  {'✓' if r['valide'] else '·'} {c}")
    if r["erreurs"]:
        print("\n  ÉCHEC :")
        for e in r["erreurs"]:
            print(f"    ✗ {e}")
        sys.exit(1)
    print("\n  ✓ Registre conforme. Recalculé intégralement, sans accès à l'éditeur.")


if __name__ == "__main__":
    main()
