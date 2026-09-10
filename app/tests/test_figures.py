"""Jeu de référence des figures — SPEC-FIGURES.

Chaque figure est construite à la main, puis on vérifie qu'elle est trouvée.
On vérifie aussi qu'aucune n'est inventée sur du bruit pur.
"""
from __future__ import annotations

import random
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forexlab import figures, indicateurs, pivots

UTC = timezone.utc
BRUIT = 0.00012


def construire(points, n_par_segment=12, graine=1, avant=320, palier=3):
    """Fabrique une série passant exactement par une suite de niveaux imposés.

    Chaque sommet est TENU sur `palier` bougies : sans cela, l'extrême retenu
    par le ZigZag dépend du bruit et deux creux censés être au même niveau
    se retrouvent à plusieurs pips l'un de l'autre. Le générateur doit produire
    des figures nettes, sinon il teste autre chose que ce qu'il prétend.
    """
    rng = random.Random(graine)
    ts = datetime(2026, 1, 5, tzinfo=UTC)
    serie = []

    def ajoute(cible, bruit=BRUIT):
        nonlocal ts
        o = serie[-1]["c"] if serie else cible
        c = cible + rng.gauss(0, bruit)
        h = max(o, c) + abs(rng.gauss(0, bruit))
        l = min(o, c) - abs(rng.gauss(0, bruit))
        serie.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
        ts += timedelta(hours=1)

    prix = points[0]
    for _ in range(avant):                       # amorçage : fixe l'ATR
        prix += rng.gauss(0, 0.00035)
        ajoute(prix, 0.00012)
    decalage = serie[-1]["c"] - points[0]

    for i, (a, b) in enumerate(zip(points, points[1:])):
        for k in range(1, n_par_segment + 1):
            ajoute(a + (a and 0) + (b - a) * k / n_par_segment + decalage)
        if i < len(points) - 2:                  # tenir le sommet atteint
            for _ in range(palier):
                ajoute(b + decalage, BRUIT * 0.4)
    return serie


def outils(serie):
    h = [b["h"] for b in serie]; l = [b["l"] for b in serie]; c = [b["c"] for b in serie]
    atrs = indicateurs.atr(h, l, c, 14)
    return atrs, pivots.detecter_pivots(h, l, atrs), indicateurs.ema(c, 20), indicateurs.ema(c, 50)


class TestFiguresConstruites(unittest.TestCase):
    def _noms(self, dets):
        return {d.figure for d in dets}

    def test_double_creux(self):
        # creux, rebond, creux au même niveau, cassure de l'encolure
        s = construire([1.1000, 1.0900, 1.1010, 1.0900, 1.1080], graine=2)
        atrs, ps, _, _ = outils(s)
        d = figures.double_extreme(s, ps, atrs, 1)
        self.assertTrue(d, "double creux construit non détecté")
        self.assertTrue(all(x.figure == "double_creux" for x in d))

    def test_double_sommet(self):
        s = construire([1.1000, 1.1100, 1.0990, 1.1100, 1.0920], graine=3)
        atrs, ps, _, _ = outils(s)
        self.assertTrue(figures.double_extreme(s, ps, atrs, -1))

    def test_ete_inversee_deux_variantes(self):
        # épaule, creux, tête plus basse, creux, épaule, cassure
        s = construire([1.1000, 1.0930, 1.1000, 1.0860, 1.1005, 1.0935, 1.1090],
                       graine=4)
        atrs, ps, _, _ = outils(s)
        d = figures.epaule_tete_epaule(s, ps, atrs, 1)
        self.assertTrue(d, "ETE inversée construite non détectée")
        variantes = {x.methode.split(".")[1] for x in d}
        self.assertEqual(variantes, {"large", "serree"},
                         "les deux invalidations doivent être mesurées séparément")
        larges = [x for x in d if "large" in x.methode]
        serrees = [x for x in d if "serree" in x.methode]
        self.assertLess(abs(serrees[0].entree - serrees[0].invalidation),
                        abs(larges[0].entree - larges[0].invalidation),
                        "l'invalidation serrée doit donner un risque plus faible")

    def test_triangle_ascendant(self):
        # sommets alignés, creux croissants, puis cassure
        s = construire([1.0900, 1.1000, 1.0930, 1.1002, 1.0960, 1.1001, 1.1070],
                       graine=5)
        atrs, ps, _, _ = outils(s)
        self.assertTrue(figures.triangle(s, ps, atrs, 1),
                        "triangle ascendant construit non détecté")

    def test_cassure_niveau(self):
        s = construire([1.1000, 1.0940, 1.1000, 1.0945, 1.1002, 1.0950, 1.1080],
                       graine=6)
        atrs, ps, _, _ = outils(s)
        self.assertTrue(figures.cassure_niveau(s, ps, atrs, 1))


class TestPasDInvention(unittest.TestCase):
    def test_bruit_pur_produit_peu_de_figures(self):
        """Sur une marche aléatoire, le catalogue ne doit pas s'emballer."""
        rng = random.Random(99)
        ts = datetime(2026, 1, 5, tzinfo=UTC)
        prix, s = 1.10, []
        for _ in range(1200):
            o = prix
            c = prix + rng.gauss(0, 0.0006)
            s.append({"ts": ts, "o": o, "h": max(o, c) + 0.0002,
                      "l": min(o, c) - 0.0002, "c": c})
            prix = c
            ts += timedelta(hours=1)
        atrs, ps, e20, e50 = outils(s)
        dets = figures.toutes(s, ps, atrs, e20, e50)
        par_barreau = len(dets) / max(1, len(s) - figures.C["AMORCAGE"])
        self.assertLess(par_barreau, 0.5,
                        f"{len(dets)} détections sur {len(s)} bougies : trop permissif")

    def test_toutes_les_detections_sont_coherentes(self):
        s = construire([1.1000, 1.0900, 1.1010, 1.0900, 1.1080], graine=7)
        atrs, ps, e20, e50 = outils(s)
        for d in figures.toutes(s, ps, atrs, e20, e50):
            self.assertGreater(abs(d.entree - d.invalidation), 0)
            self.assertGreater((d.objectif - d.entree) * d.sens, 0,
                               f"{d.methode} : objectif du mauvais côté")
            self.assertLess((d.invalidation - d.entree) * d.sens, 0,
                            f"{d.methode} : invalidation du mauvais côté")

    def test_neutralisations_declarees(self):
        """Chaque figure déclare les critères que sa construction satisfait."""
        self.assertIn("tendance", figures.NEUTRALISES["drapeau"])
        self.assertIn("tendance", figures.NEUTRALISES["pullback_tendance"])
        self.assertIn("zone", figures.NEUTRALISES["double_creux"])
        self.assertEqual(figures.NEUTRALISES["ete"], ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
