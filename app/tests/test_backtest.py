"""Le backtest doit être capable de se contredire lui-même."""
from __future__ import annotations

import random
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forexlab import backtest
from forexlab.pipeline import Ligne

UTC = timezone.utc


def lignes(n=1200, graine=1, score_predictif=True, esperance=0.0):
    """Si `score_predictif`, un score élevé donne réellement un meilleur R."""
    rng = random.Random(graine)
    out = []
    for i in range(n):
        s = rng.random()
        biais = (s - 0.5) * 0.6 if score_predictif else 0.0
        r = rng.gauss(esperance + biais, 1.0)
        out.append(Ligne("EURUSD", "H1", "range", "R1a", 1,
                         datetime(2026, 1, 1, tzinfo=UTC) + timedelta(hours=i),
                         1.1, 1.09, 1.12, 1.115, 1.12, int(s * 10), 10, s,
                         "annoncee", "", {},
                         {"methode": {"r_net": r, "r_brut": r,
                                      "resultat": "atteint" if r > 0 else "invalide",
                                      "ambigu_m1": False}}, f"{i:064x}"))
    return out


class TestSharpeDeflate(unittest.TestCase):
    def test_un_seul_essai_laisse_passer_un_vrai_effet(self):
        rng = random.Random(7)
        rs = [rng.gauss(0.25, 1.0) for _ in range(800)]
        d = backtest.sharpe_deflate(rs, essais=1)
        self.assertTrue(d["significatif"], f"DSR={d['dsr']:.3f}")

    def test_le_meme_effet_ne_survit_pas_a_mille_essais(self):
        """Tester 1 000 séries fait ressortir la meilleure par construction."""
        rng = random.Random(7)
        rs = [rng.gauss(0.06, 1.0) for _ in range(800)]
        seul = backtest.sharpe_deflate(rs, essais=1)
        multiple = backtest.sharpe_deflate(rs, essais=1000)
        self.assertGreater(seul["dsr"], multiple["dsr"])
        self.assertFalse(multiple["significatif"],
                         "un effet faible ne doit pas survivre à 1 000 essais")

    def test_seuil_croit_avec_le_nombre_d_essais(self):
        rs = [0.1] * 200
        a = backtest.sharpe_deflate(rs, essais=10)["sharpe_seuil"]
        b = backtest.sharpe_deflate(rs, essais=500)["sharpe_seuil"]
        self.assertGreater(b, a)

    def test_echantillon_trop_court_refuse(self):
        self.assertFalse(backtest.sharpe_deflate([0.1] * 5, essais=1)["suffisant"])


class TestWalkForward(unittest.TestCase):
    def test_score_predictif_generalise(self):
        wf = backtest.walk_forward(lignes(1500, graine=2, score_predictif=True))
        self.assertTrue(wf["suffisant"])
        self.assertLess(wf["degradation"], 0.25,
                        "un score réellement prédictif doit généraliser")
        self.assertGreater(wf["esperance_hors_echantillon"], 0.0)

    def test_score_de_bruit_se_degrade_hors_echantillon(self):
        """Calibré, le seuil a l'air bon ; hors échantillon, il ne vaut rien.

        C'est exactement le mécanisme du surajustement, et le test doit le voir.
        """
        bruit = backtest.walk_forward(lignes(1500, graine=3, score_predictif=False))
        vrai = backtest.walk_forward(lignes(1500, graine=2, score_predictif=True))
        self.assertTrue(bruit["suffisant"] and vrai["suffisant"])

        # Sur du bruit, le seuil calibré FLATTE toujours.
        self.assertGreater(bruit["esperance_calibree"],
                           bruit["esperance_hors_echantillon"])

        # La dégradation ABSOLUE ne discrimine pas : un score réellement
        # prédictif part de plus haut, donc il dégrade davantage en valeur
        # absolue. Ce qui compte est ce qui SURVIT hors échantillon.
        self.assertLess(bruit["esperance_hors_echantillon"], 0.06,
                        "sur du bruit, rien ne doit survivre hors échantillon")
        self.assertGreater(vrai["esperance_hors_echantillon"], 0.10,
                           "un score prédictif doit survivre hors échantillon")

    def test_historique_insuffisant_refuse(self):
        wf = backtest.walk_forward(lignes(50))
        self.assertFalse(wf["suffisant"])


class TestRapportDecision(unittest.TestCase):
    def test_verdict_negatif(self):
        r = backtest.rapport_decision(
            lignes(800, graine=4, score_predictif=False, esperance=-0.20), 18)
        self.assertEqual(r["verdict"], "negatif")
        self.assertIn("coûte réellement", r["conduite"])

    def test_verdict_nul_bascule_sur_le_comparatif(self):
        r = backtest.rapport_decision(
            lignes(800, graine=5, score_predictif=False, esperance=0.0), 18)
        self.assertEqual(r["verdict"], "nul")
        self.assertIn("comparatif", r["conduite"])

    def test_effet_fort_mais_beaucoup_d_essais_reste_prudent(self):
        """Même un bon chiffre ne doit pas passer « positif » s'il sort
        d'un très grand nombre d'essais non déclarés."""
        r = backtest.rapport_decision(
            lignes(800, graine=6, score_predictif=False, esperance=0.05), 5000)
        self.assertIn(r["verdict"], ("nul", "negatif"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
