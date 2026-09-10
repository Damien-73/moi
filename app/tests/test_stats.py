import math, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forexlab import stats


class TestAgregat(unittest.TestCase):
    def test_sous_seuil_non_publiable(self):
        s = stats.agregat([0.1] * 99)
        self.assertFalse(s["publiable"])
        self.assertEqual(s["manquant"], 1)
        self.assertEqual(s["statut"], "insuffisant")

    def test_seuils(self):
        self.assertEqual(stats.agregat([0.1] * 100)["statut"], "provisoire")
        self.assertEqual(stats.agregat([0.1] * 400)["statut"], "établi")

    def test_intervalle_confiance(self):
        rs = [1.0, -1.0] * 200
        s = stats.agregat(rs)
        self.assertAlmostEqual(s["esperance"], 0.0, places=9)
        self.assertAlmostEqual(s["ic95"], 1.96 * 1.0 / math.sqrt(400), places=3)


class TestCorrectionTestsMultiples(unittest.TestCase):
    def test_series_de_bruit_pur_ne_ressortent_pas(self):
        """144 séries de bruit : sans correction, environ 7 seraient « significatives »."""
        import random
        rng = random.Random(4)
        series = {f"s{i}": stats.agregat([rng.gauss(0, 1) for _ in range(300)])
                  for i in range(144)}
        brutes = sum(1 for s in series.values() if stats.p_valeur(s) < 0.05)
        bh = stats.benjamini_hochberg(series)
        corriges = sum(1 for v in bh.values() if v["significatif"])
        self.assertGreater(brutes, 2, "il devrait y avoir des faux positifs bruts")
        self.assertLessEqual(corriges, 1, f"{corriges} faux positifs après correction")

    def test_vrai_effet_survit_a_la_correction(self):
        import random
        rng = random.Random(5)
        series = {f"bruit{i}": stats.agregat([rng.gauss(0, 1) for _ in range(300)])
                  for i in range(50)}
        series["vrai"] = stats.agregat([rng.gauss(0.35, 1) for _ in range(600)])
        bh = stats.benjamini_hochberg(series)
        self.assertTrue(bh["vrai"]["significatif"])


class TestComparaisonObligatoire(unittest.TestCase):
    def test_absence_de_temoin_refusee(self):
        s = stats.agregat([0.1] * 200)
        with self.assertRaises(ValueError):
            stats.comparer(s, None)

    def test_ecart_calcule(self):
        a = stats.agregat([0.2] * 200)
        t = stats.agregat([-0.2] * 200)
        c = stats.comparer(a, t)
        self.assertAlmostEqual(c["comparaison"]["ecart"], 0.4, places=9)

    def test_sous_seuil_pas_de_chiffre(self):
        c = stats.comparer(stats.agregat([0.1] * 30), stats.agregat([0.0] * 200))
        self.assertFalse(c["publiable"])
        self.assertNotIn("valeur", c)
        self.assertIn("30 sur 100", c["message"])


class TestClassement(unittest.TestCase):
    def test_nombre_de_series_testees_affiche(self):
        series = {f"s{i}": stats.agregat([0.1 * i] * 150) for i in range(1, 6)}
        c = stats.classement(series)
        self.assertEqual(c["series_testees"], 5)
        self.assertEqual([l["nom"] for l in c["lignes"]][0], "s5")


if __name__ == "__main__":
    unittest.main(verbosity=2)
