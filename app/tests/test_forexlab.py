"""Tests du lot 1. Lancer avec :  python3 -m unittest discover -s app/tests -v"""
from __future__ import annotations

import random
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from forexlab import agregation, calendrier, determinisme, indicateurs, pivots, stockage

UTC = timezone.utc


def serie(n=800, graine=42, depart=1.1000):
    """Marche aléatoire reproductible, en M1, à partir d'un dimanche 22:00 UTC."""
    rng = random.Random(graine)
    ts = datetime(2026, 1, 4, 22, 0, tzinfo=UTC)
    prix, out = depart, []
    for _ in range(n):
        pas = rng.gauss(0, 0.0004)
        o = prix
        c = prix + pas
        h = max(o, c) + abs(rng.gauss(0, 0.0002))
        l = min(o, c) - abs(rng.gauss(0, 0.0002))
        out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
        prix, ts = c, ts + timedelta(minutes=1)
    return out


class TestCalendrier(unittest.TestCase):
    def test_bascule_17h_new_york(self):
        # 21:59 UTC en janvier = 16:59 New York -> journée du jour même
        self.assertEqual(calendrier.jour_negociation(datetime(2026, 1, 5, 21, 59, tzinfo=UTC)), "2026-01-05")
        # 22:00 UTC = 17:00 New York -> journée suivante
        self.assertEqual(calendrier.jour_negociation(datetime(2026, 1, 5, 22, 0, tzinfo=UTC)), "2026-01-06")

    def test_changement_heure(self):
        """En été, 17:00 New York = 21:00 UTC. La bascule doit suivre le fuseau,
        pas un décalage figé. C'est le test qui casse les implémentations naïves."""
        self.assertEqual(calendrier.jour_negociation(datetime(2026, 7, 6, 20, 59, tzinfo=UTC)), "2026-07-06")
        self.assertEqual(calendrier.jour_negociation(datetime(2026, 7, 6, 21, 0, tzinfo=UTC)), "2026-07-07")

    def test_h4_aligne_sur_la_journee(self):
        """Une bougie H4 ne doit jamais chevaucher deux journées de négociation."""
        for jour in ("2026-01-06", "2026-07-07"):
            ouverture = calendrier.ouverture_jour(jour)
            for k in range(6):
                t = ouverture + timedelta(hours=4 * k, minutes=1)
                self.assertEqual(calendrier.debut_bougie(t, "H4"),
                                 ouverture + timedelta(hours=4 * k))
                self.assertEqual(calendrier.jour_negociation(t), jour)

    def test_marche_ferme_le_weekend(self):
        self.assertFalse(calendrier.marche_ouvert(datetime(2026, 1, 10, 12, 0, tzinfo=UTC)))  # samedi
        self.assertTrue(calendrier.marche_ouvert(datetime(2026, 1, 7, 12, 0, tzinfo=UTC)))    # mercredi


class TestIndicateurs(unittest.TestCase):
    def setUp(self):
        self.b = serie(400)
        self.h = [x["h"] for x in self.b]
        self.l = [x["l"] for x in self.b]
        self.c = [x["c"] for x in self.b]

    def test_atr_amorcage_et_valeurs(self):
        a = indicateurs.atr(self.h, self.l, self.c, 14)
        self.assertTrue(all(v is None for v in a[:14]))
        self.assertIsNotNone(a[14])
        self.assertTrue(all(v > 0 for v in a[14:]))

    def test_atr_reference_calculee_a_la_main(self):
        h = [10, 11, 12, 11, 12]; l = [9, 10, 10, 9, 10]; c = [9.5, 10.5, 11, 10, 11.5]
        a = indicateurs.atr(h, l, c, 2)
        # TR : [_, 1.5, 2.0, 2.0, 2.0]  -> amorçage (1.5+2.0)/2 = 1.75
        self.assertAlmostEqual(a[2], 1.75, places=10)
        self.assertAlmostEqual(a[3], (1 * 1.75 + 2.0) / 2, places=10)

    def test_ema_est_une_moyenne_au_depart(self):
        v = [1, 2, 3, 4, 5, 6]
        e = indicateurs.ema(v, 3)
        self.assertIsNone(e[1])
        self.assertAlmostEqual(e[2], 2.0)          # (1+2+3)/3
        self.assertAlmostEqual(e[3], 0.5 * 4 + 0.5 * 2.0)

    def test_rsi_borne(self):
        r = indicateurs.rsi(self.c, 14)
        self.assertTrue(all(0 <= v <= 100 for v in r[14:]))

    def test_rsi_hausse_continue_vaut_100(self):
        self.assertAlmostEqual(indicateurs.rsi(list(range(1, 40)), 14)[-1], 100.0)

    def test_adx_positif(self):
        a = indicateurs.adx(self.h, self.l, self.c, 14)
        self.assertTrue(any(v is not None for v in a))
        self.assertTrue(all(v >= 0 for v in a if v is not None))


class TestPivots(unittest.TestCase):
    def test_confirmation_toujours_posterieure(self):
        b = serie(1500)
        h = [x["h"] for x in b]; l = [x["l"] for x in b]; c = [x["c"] for x in b]
        a = indicateurs.atr(h, l, c, 14)
        ps = pivots.detecter_pivots(h, l, a)
        self.assertGreater(len(ps), 3)
        for p in ps:
            self.assertGreater(p.confirmation, p.barreau,
                               "un pivot connu avant sa confirmation = fuite d'information future")

    def test_alternance(self):
        b = serie(1500)
        h = [x["h"] for x in b]; l = [x["l"] for x in b]; c = [x["c"] for x in b]
        ps = pivots.detecter_pivots(h, l, indicateurs.atr(h, l, c, 14))
        for x, y in zip(ps, ps[1:]):
            self.assertNotEqual(x.type, y.type)

    def test_filtre_connus_a(self):
        b = serie(1500)
        h = [x["h"] for x in b]; l = [x["l"] for x in b]; c = [x["c"] for x in b]
        ps = pivots.detecter_pivots(h, l, indicateurs.atr(h, l, c, 14))
        t = ps[len(ps) // 2].confirmation
        for p in pivots.pivots_connus(ps, t):
            self.assertLessEqual(p.confirmation, t)


class TestAgregation(unittest.TestCase):
    def test_ohlc_coherent(self):
        m1 = serie(600)
        for unite in ("H1", "H4", "D1"):
            for b in agregation.agreger(m1, unite):
                self.assertLessEqual(b["l"], b["o"])
                self.assertLessEqual(b["o"], b["h"])
                self.assertLessEqual(b["l"], b["c"])
                self.assertLessEqual(b["c"], b["h"])

    def test_h1_compte_60_minutes(self):
        m1 = serie(600)
        h1 = agregation.agreger(m1, "H1")
        pleines = [b for b in h1[1:-1]]
        self.assertTrue(all(b["minutes"] == 60 for b in pleines))

    def test_extremes_conserves(self):
        m1 = serie(600)
        d1 = agregation.agreger(m1, "D1")
        self.assertAlmostEqual(max(b["h"] for b in d1), max(b["h"] for b in m1))
        self.assertAlmostEqual(min(b["l"] for b in d1), min(b["l"] for b in m1))


class TestPointInTime(unittest.TestCase):
    """Le test le plus important du projet (SPEC-LOT2 §8.1)."""

    @staticmethod
    def chaine_de_calcul(bougies, jusqu_a):
        h = [b["h"] for b in bougies]; l = [b["l"] for b in bougies]; c = [b["c"] for b in bougies]
        a = indicateurs.atr(h, l, c, 14)
        ps = pivots.detecter_pivots(h, l, a)
        return [{"type": p.type, "barreau": p.barreau,
                 "confirmation": p.confirmation, "prix": p.prix}
                for p in ps if p.confirmation < jusqu_a]

    def test_donnees_futures_reelles_sans_effet(self):
        b = serie(1200)
        ok, ref, avec = determinisme.test_point_in_time(
            self.chaine_de_calcul, b, 800, b[800:])
        self.assertTrue(ok, f"fuite d'information future : {ref} != {avec}")

    def test_donnees_futures_aberrantes_sans_effet(self):
        """Attaque : prix multipliés par 10 après la coupure. Si un seul
        résultat antérieur change, la mise en service est bloquée."""
        b = serie(1200)
        ok, ref, avec = determinisme.test_point_in_time(
            self.chaine_de_calcul, b, 800, determinisme.donnees_aberrantes(b[:800]))
        self.assertTrue(ok, f"fuite d'information future : {ref} != {avec}")

    def test_le_harnais_detecte_bien_une_fuite(self):
        """Contre-épreuve : un calcul volontairement fautif DOIT échouer.
        Un test qui ne peut pas échouer ne prouve rien."""
        def calcul_fautif(bougies, jusqu_a):
            return [{"max_futur": max(b["h"] for b in bougies)}]  # regarde tout
        b = serie(1200)
        ok, _, _ = determinisme.test_point_in_time(
            calcul_fautif, b, 800, determinisme.donnees_aberrantes(b[:800]))
        self.assertFalse(ok, "le harnais doit détecter une fuite manifeste")


class TestSerialisation(unittest.TestCase):
    def test_decimales_sans_zeros_de_queue(self):
        self.assertEqual(determinisme._canonique(1.08120), "1.0812")
        self.assertEqual(determinisme._canonique(1.0), "1")
        self.assertEqual(determinisme._canonique(0.0), "0")

    def test_horodatage_en_z(self):
        t = datetime(2026, 3, 14, 12, 0, tzinfo=UTC)
        self.assertEqual(determinisme._canonique(t), "2026-03-14T12:00:00Z")

    def test_empreinte_stable(self):
        d = [{"a": 1.0, "b": "x"}, {"a": 2.5, "b": "y"}]
        self.assertEqual(determinisme.empreinte(d), determinisme.empreinte(list(d)))

    def test_empreinte_sensible(self):
        self.assertNotEqual(determinisme.empreinte([{"a": 1.0}]),
                            determinisme.empreinte([{"a": 1.0000001}]))


class TestStockage(unittest.TestCase):
    def test_aller_retour(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            cx = stockage.ouvrir(Path(d) / "t.db")
            m1 = serie(300)
            n = stockage.enregistrer_bougies(cx, "EURUSD", "M1", m1, "test")
            self.assertEqual(n, 300)
            relu = stockage.lire_bougies(cx, "EURUSD", "M1")
            self.assertEqual(len(relu), 300)
            self.assertEqual(relu[0]["ts"], m1[0]["ts"])
            self.assertAlmostEqual(relu[0]["c"], m1[0]["c"], places=9)

    def test_reecriture_idempotente(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            cx = stockage.ouvrir(Path(d) / "t.db")
            m1 = serie(100)
            stockage.enregistrer_bougies(cx, "EURUSD", "M1", m1, "test")
            stockage.enregistrer_bougies(cx, "EURUSD", "M1", m1, "test")
            self.assertEqual(len(stockage.lire_bougies(cx, "EURUSD", "M1")), 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
