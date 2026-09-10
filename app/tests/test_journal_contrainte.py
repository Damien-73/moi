from __future__ import annotations
import random, sys, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forexlab import contrainte, journal

UTC = timezone.utc


def trades_synthetiques(n=120, graine=1, decalage_h=0, revanche=False):
    rng = random.Random(graine)
    # Le marché est ouvert de 8 h à 20 h UTC ; le relevé du courtier les
    # affiche décalées de `decalage_h`. Le décalage doit survivre au passage
    # d'un jour à l'autre, sinon on ne teste rien.
    base = (8 + decalage_h) % 24
    ts = datetime(2026, 1, 5, 0, 0, tzinfo=UTC) + timedelta(hours=8 + decalage_h)
    out, dernier_r = [], 0.0
    for i in range(n):
        heure_utc = (ts.hour - decalage_h) % 24
        if ts.weekday() >= 5 or not (8 <= heure_utc <= 20):
            jour = ts.date() + timedelta(days=1)
            ts = datetime(jour.year, jour.month, jour.day, tzinfo=UTC) + \
                timedelta(hours=8 + decalage_h)
            while ts.weekday() >= 5:
                ts += timedelta(days=1)
        risque = 0.0020
        if revanche and dernier_r < 0:
            risque = 0.0040                      # il double après une perte
        gagne = rng.random() < 0.45
        r = rng.uniform(0.9, 1.6) if gagne else -1.0
        out.append({"symbole": "EURUSD", "sens": 1, "entree_ts": ts,
                    "sortie_ts": ts + timedelta(hours=3),
                    "entree": 1.1000, "sortie": 1.1000 + r * risque,
                    "volume": 1.0, "stop": 1.1000 - risque, "objectif": None})
        dernier_r = r
        ts += timedelta(hours=rng.choice([2, 4, 6]))
    return out


class TestImportEtRisque(unittest.TestCase):
    def test_normalisation_symbole(self):
        for s in ("EURUSD.pro", "EURUSDm", "EUR/USD", "EURUSD#", "eurusd_raw"):
            self.assertEqual(journal.normaliser_symbole(s), "EURUSD")

    def test_risque_depuis_stop(self):
        t = trades_synthetiques(60)
        self.assertEqual(journal.reconstruire_risque(t), "stop_declare")
        self.assertTrue(all(x["risque"] for x in t))

    def test_risque_estime_sans_stop(self):
        t = trades_synthetiques(60)
        for x in t:
            x["stop"] = None
        methode = journal.reconstruire_risque(t)
        self.assertEqual(methode, "risque_estime")
        self.assertTrue(all(x["risque"] for x in t))

    def test_decalage_horaire_detecte(self):
        """Sans cette correction, l'analyse horaire est fausse de 2 à 3 heures."""
        t = trades_synthetiques(400, decalage_h=3)
        d, fiable = journal.detecter_decalage(t)
        self.assertTrue(fiable, "le décalage aurait dû être jugé fiable")
        self.assertIn(d, (2, 3, 4), f"décalage détecté {d}, attendu ~3")

    def test_decalage_non_fiable_demande_confirmation(self):
        d, fiable = journal.detecter_decalage(trades_synthetiques(25))
        self.assertFalse(fiable, "trop peu de semaines : ne jamais deviner en silence")


class TestMesures(unittest.TestCase):
    def test_detecte_le_dimensionnement_de_revanche(self):
        t = trades_synthetiques(200, graine=3, revanche=True)
        journal.reconstruire_risque(t)
        m = journal.mesures(t)
        self.assertLess(m["revanche"], -0.15,
                        "la corrélation risque/résultat précédent doit être négative")
        cles = [c.get("cle") for c in journal.constats(m)]
        self.assertIn("revanche", cles)

    def test_pas_de_faux_diagnostic_sur_un_journal_sain(self):
        t = trades_synthetiques(200, graine=4, revanche=False)
        journal.reconstruire_risque(t)
        m = journal.mesures(t)
        self.assertGreater(m["revanche"], -0.15)

    def test_au_plus_trois_constats(self):
        t = trades_synthetiques(200, graine=5, revanche=True)
        journal.reconstruire_risque(t)
        self.assertLessEqual(len(journal.constats(journal.mesures(t))), 3)

    def test_sous_le_seuil_aucun_diagnostic(self):
        t = trades_synthetiques(20)
        journal.reconstruire_risque(t)
        c = journal.constats(journal.mesures(t))
        self.assertEqual(len(c), 1)
        self.assertIn("30", c[0]["detail"])

    def test_serie_de_pertes_attendue_calculee(self):
        t = trades_synthetiques(200, graine=6)
        journal.reconstruire_risque(t)
        m = journal.mesures(t)
        self.assertGreater(m["serie_pertes_attendue"], 3)


def jours_synthetiques(n=200, esperance=0.0, graine=2):
    rng = random.Random(graine)
    out = []
    for _ in range(n):
        jour = []
        for _ in range(rng.choice([1, 2, 3])):
            gagne = rng.random() < 0.45
            r = rng.uniform(0.9, 1.6) if gagne else -1.0
            jour.append((r + esperance, min(0.0, -abs(rng.gauss(0, 0.4)))))
        out.append(jour)
    return out


class TestContrainte(unittest.TestCase):
    def test_historique_insuffisant_refuse(self):
        s = contrainte.simuler(jours_synthetiques(40), simulations=200)
        self.assertFalse(s["suffisant"])
        self.assertEqual(s["manquant"], 20)

    def test_probabilite_bornee_et_causes_totalisent_un(self):
        s = contrainte.simuler(jours_synthetiques(), simulations=2000)
        self.assertTrue(0 <= s["probabilite"] <= 1)
        total = (s["probabilite"] + s["echec_perte_totale"]
                 + s["echec_perte_jour"] + s["echec_delai"])
        self.assertAlmostEqual(total, 1.0, places=6)

    def test_suiveuse_plus_severe_que_statique(self):
        j = jours_synthetiques()
        stat = contrainte.simuler(j, type_perte="statique", simulations=3000)
        suiv = contrainte.simuler(j, type_perte="suiveuse", simulations=3000)
        self.assertGreaterEqual(stat["probabilite"], suiv["probabilite"],
                                "la perte suiveuse ne laisse aucun coussin s'accumuler")

    def test_risque_eleve_deplace_la_cause_d_echec(self):
        """À faible risque on échoue par DÉLAI ; à fort risque, par PERTE.

        C'est le mécanisme qui rend la courbe non monotone : affirmer
        « moins de risque, plus de réussite » serait faux.
        """
        j = jours_synthetiques()
        faible = contrainte.simuler(j, risque=0.005, simulations=3000)
        fort = contrainte.simuler(j, risque=0.03, simulations=3000)
        self.assertGreater(faible["echec_delai"], fort["echec_delai"])
        self.assertGreater(fort["echec_perte_totale"], faible["echec_perte_totale"],
                           "3 % de risque doit faire sauter le compte plus souvent")

    def test_courbe_non_monotone_avec_optimum(self):
        b = contrainte.balayage_risque(jours_synthetiques(esperance=0.06),
                                       simulations=1500)
        self.assertFalse(b["pari"])
        self.assertIsNotNone(b["optimum"])
        probs = [o["probabilite"] for o in b["courbe"]]
        self.assertLess(probs[-1], max(probs),
                        "la probabilité doit chuter aux risques élevés")

    def test_esperance_negative_ne_donne_pas_d_optimum(self):
        """Avec une espérance négative, « l'optimum » est au risque maximal :
        seule la variance peut atteindre l'objectif. Présenter cela comme un
        optimum décrirait un pari comme une méthode."""
        b = contrainte.balayage_risque(jours_synthetiques(esperance=-0.20),
                                       simulations=1200)
        self.assertTrue(b["pari"])
        self.assertIsNone(b["optimum"])
        self.assertIn("pari", b["avertissement"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
