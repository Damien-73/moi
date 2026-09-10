"""Tests des lots 2, 3 et 4. python3 app/tests/test_lot2.py"""
from __future__ import annotations

import random
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from forexlab import (agregation, calendrier_eco, couts, determinisme, indicateurs,
                      niveaux, pipeline, pivots, range_v1, registre, resolution, score)

UTC = timezone.utc


def m1_serie(n=40000, graine=11, depart=1.1000):
    """Marche aléatoire M1 reproductible, heures d'ouverture seulement."""
    from forexlab.calendrier import marche_ouvert
    rng = random.Random(graine)
    ts = datetime(2026, 1, 4, 22, 0, tzinfo=UTC)
    prix, out = depart, []
    while len(out) < n:
        if marche_ouvert(ts):
            o = prix
            c = prix + rng.gauss(0, 0.00025)
            h = max(o, c) + abs(rng.gauss(0, 0.00012))
            l = min(o, c) - abs(rng.gauss(0, 0.00012))
            out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
            prix = c
        ts += timedelta(minutes=1)
    return out


class TestCouts(unittest.TestCase):
    def test_portage_toujours_penalise_par_la_marge(self):
        """Quel que soit le sens, la marge du courtier est prélevée."""
        p = couts.portage_journalier("EURUSD", 1, 1.10)
        m = couts.portage_journalier("EURUSD", -1, 1.10)
        differentiel = couts.TAUX_COURT["EUR"] - couts.TAUX_COURT["USD"]
        attendu_achat = (differentiel - 0.010) / 360 * 1.10
        self.assertAlmostEqual(p, attendu_achat, places=12)
        self.assertAlmostEqual(m, (-differentiel - 0.010) / 360 * 1.10, places=12)
        self.assertLess(p + m, 0, "la marge doit rendre la somme des deux sens négative")

    def test_mercredi_compte_triple(self):
        # mardi 12:00 UTC -> jeudi 12:00 UTC : passe par mardi 17h NY et mercredi 17h NY
        d = datetime(2026, 3, 10, 12, 0, tzinfo=UTC)
        f = datetime(2026, 3, 12, 12, 0, tzinfo=UTC)
        total = couts.portage_total("EURUSD", 1, 1.10, d, f)
        unite = couts.portage_journalier("EURUSD", 1, 1.10)
        self.assertAlmostEqual(total / unite, 4.0, places=9,
                               msg="1 jour + mercredi triple = 4 unités")

    def test_spread_elargi_au_roulement(self):
        normal = couts.spread("EURUSD", datetime(2026, 3, 10, 14, 0, tzinfo=UTC))
        roul = couts.spread("EURUSD", datetime(2026, 3, 10, 21, 30, tzinfo=UTC))
        self.assertGreater(roul, 3 * normal)


class TestResolution(unittest.TestCase):
    @staticmethod
    def bougie(ts, o, h, l, c):
        return {"ts": ts, "o": o, "h": h, "l": l, "c": c}

    def setUp(self):
        self.t0 = datetime(2026, 3, 10, 12, 0, tzinfo=UTC)

    def test_objectif_atteint(self):
        m1 = [self.bougie(self.t0 + timedelta(minutes=i), 1.10, 1.1030, 1.0995, 1.10)
              for i in range(1, 6)]
        i = resolution.resoudre(m1, "EURUSD", 1, self.t0, 1.1000, 1.0980, 1.1020,
                                self.t0 + timedelta(minutes=10))
        self.assertEqual(i.resultat, "atteint")
        self.assertFalse(i.ambigu_m1)

    def test_invalidation_avant_objectif(self):
        m1 = [self.bougie(self.t0 + timedelta(minutes=1), 1.10, 1.1005, 1.0975, 1.098),
              self.bougie(self.t0 + timedelta(minutes=2), 1.098, 1.1030, 1.098, 1.102)]
        i = resolution.resoudre(m1, "EURUSD", 1, self.t0, 1.1000, 1.0980, 1.1020,
                                self.t0 + timedelta(minutes=10))
        self.assertEqual(i.resultat, "invalide")

    def test_regle_conservatrice_sur_bougie_ambigue(self):
        """Les deux touchés dans la même bougie M1 : TOUJOURS invalidation."""
        m1 = [self.bougie(self.t0 + timedelta(minutes=1), 1.10, 1.1030, 1.0975, 1.10)]
        i = resolution.resoudre(m1, "EURUSD", 1, self.t0, 1.1000, 1.0980, 1.1020,
                                self.t0 + timedelta(minutes=10))
        self.assertEqual(i.resultat, "invalide")
        self.assertTrue(i.ambigu_m1)

    def test_sans_issue(self):
        m1 = [self.bougie(self.t0 + timedelta(minutes=i), 1.10, 1.1005, 1.0995, 1.10)
              for i in range(1, 4)]
        i = resolution.resoudre(m1, "EURUSD", 1, self.t0, 1.1000, 1.0980, 1.1020,
                                self.t0 + timedelta(minutes=3))
        self.assertEqual(i.resultat, "sans_issue")

    def test_net_toujours_inferieur_au_brut(self):
        m1 = [self.bougie(self.t0 + timedelta(minutes=1), 1.10, 1.1030, 1.0995, 1.10)]
        i = resolution.resoudre(m1, "EURUSD", 1, self.t0, 1.1000, 1.0980, 1.1020,
                                self.t0 + timedelta(minutes=10))
        self.assertLess(i.r_net, i.r_brut, "les frais doivent toujours dégrader le résultat")

    def test_vente_symetrique(self):
        m1 = [self.bougie(self.t0 + timedelta(minutes=1), 1.10, 1.1005, 1.0975, 1.098)]
        i = resolution.resoudre(m1, "EURUSD", -1, self.t0, 1.1000, 1.1020, 1.0980,
                                self.t0 + timedelta(minutes=10))
        self.assertEqual(i.resultat, "atteint")


class TestRange(unittest.TestCase):
    def setUp(self):
        self.m1 = m1_serie(40000)
        self.h1 = agregation.agreger(self.m1, "H1")
        h = [b["h"] for b in self.h1]; l = [b["l"] for b in self.h1]
        c = [b["c"] for b in self.h1]
        self.atrs = indicateurs.atr(h, l, c, 14)
        self.pivots = pivots.detecter_pivots(h, l, self.atrs)

    def test_detection_produit_des_ranges(self):
        rgs, dets = range_v1.detecter(self.h1, self.pivots, self.atrs)
        self.assertGreater(len(rgs), 0, "aucun range détecté sur 40 000 minutes")
        self.assertGreater(len(dets), 0)

    def test_bornes_coherentes_et_figees(self):
        rgs, _ = range_v1.detecter(self.h1, self.pivots, self.atrs)
        for r in rgs:
            self.assertGreater(r.borne_haute, r.borne_basse)
            self.assertGreaterEqual(r.hauteur, range_v1.P["HAUTEUR_MIN"] * r.atr - 1e-12)
            self.assertLessEqual(r.hauteur, range_v1.P["HAUTEUR_MAX"] * r.atr + 1e-12)

    def test_risque_toujours_strictement_positif(self):
        _, dets = range_v1.detecter(self.h1, self.pivots, self.atrs)
        for d in dets:
            self.assertGreater(abs(d.entree - d.invalidation), 0)
            self.assertNotEqual(d.objectif, d.entree)

    def test_sens_coherent_avec_les_niveaux(self):
        _, dets = range_v1.detecter(self.h1, self.pivots, self.atrs)
        for d in dets:
            if d.sens > 0:
                self.assertLess(d.invalidation, d.entree)
                self.assertGreater(d.objectif, d.entree)
            else:
                self.assertGreater(d.invalidation, d.entree)
                self.assertLess(d.objectif, d.entree)


class TestRegistre(unittest.TestCase):
    def test_merkle_et_preuve_inclusion(self):
        f = [registre.feuille(version="range.v1", symbole="EURUSD", unite="H4",
                              sens=1, entree_ts=datetime(2026, 3, i + 1, tzinfo=UTC),
                              entree=1.1 + i / 10000, invalidation=1.09, objectif_methode=1.12,
                              objectif_1r5=1.115, objectif_2r=1.12, horizon=20,
                              score_points=8, score_max=10, statut="annoncee")
             for i in range(7)]
        r = registre.racine_merkle(f)
        for i in range(7):
            p = registre.preuve_inclusion(f, i)
            self.assertTrue(registre.verifier_inclusion(f[i], p, r))

    def test_feuille_sensible_au_dernier_chiffre(self):
        base = dict(version="range.v1", symbole="EURUSD", unite="H4", sens=1,
                    entree_ts=datetime(2026, 3, 1, tzinfo=UTC), invalidation=1.09,
                    objectif_methode=1.12, objectif_1r5=1.115, objectif_2r=1.12, horizon=20,
                    score_points=8, score_max=10, statut="annoncee")
        a = registre.feuille(entree=1.10000, **base)
        b = registre.feuille(entree=1.10001, **base)
        self.assertNotEqual(a, b)

    def test_zeros_de_queue_sans_effet(self):
        base = dict(version="range.v1", symbole="EURUSD", unite="H4", sens=1,
                    entree_ts=datetime(2026, 3, 1, tzinfo=UTC), invalidation=1.09,
                    objectif_methode=1.12, objectif_1r5=1.115, objectif_2r=1.12, horizon=20,
                    score_points=8, score_max=10, statut="annoncee")
        self.assertEqual(registre.feuille(entree=1.1, **base),
                         registre.feuille(entree=1.10000000, **base))

    def test_chaine_detecte_une_reecriture(self):
        ch = registre.Chaine()
        for k in range(5):
            ch.ajouter(datetime(2026, 3, 1, k, tzinfo=UTC), [f"{k}" * 64])
        self.assertTrue(ch.verifier()[0])
        ch.cycles[2].feuilles[0] = "f" * 64          # falsification
        ok, msg = ch.verifier()
        self.assertFalse(ok)
        self.assertIn("2", msg)

    def test_cycle_vide_est_ancre(self):
        ch = registre.Chaine()
        c = ch.ajouter(datetime(2026, 3, 1, tzinfo=UTC), [])
        self.assertEqual(len(c.feuilles), 0)
        self.assertTrue(ch.verifier()[0])


class TestScoreEtPipeline(unittest.TestCase):
    def setUp(self):
        self.m1 = m1_serie(40000)
        self.h1 = agregation.agreger(self.m1, "H1")
        self.h4 = agregation.agreger(self.m1, "H4")
        self.d1 = agregation.agreger(self.m1, "D1")

    def _executer(self, bougies=None):
        return pipeline.executer("EURUSD", "H1", bougies or self.h1, self.m1,
                                 self.h4, self.d1)

    def test_chaine_complete(self):
        rgs, lignes = self._executer()
        self.assertGreater(len(lignes), 0)
        for l in lignes:
            self.assertIn(l.statut, ("annoncee", "ecartee"))
            self.assertEqual(len(l.empreinte), 64)
            self.assertTrue((l.statut == "ecartee") == bool(l.motif_rejet))

    def test_ecartees_conservees_avec_motif(self):
        """Le groupe témoin est l'argument central : rien n'est supprimé."""
        _, lignes = self._executer()
        ecartees = [l for l in lignes if l.statut == "ecartee"]
        self.assertGreater(len(ecartees), 0)
        for l in ecartees:
            self.assertTrue(l.motif_rejet)
            self.assertIsInstance(l.detail, dict)

    def test_critere_zone_neutralise_pour_le_range(self):
        _, lignes = self._executer()
        self.assertTrue(lignes[0].detail["zone"].get("neutralise"))

    def test_score_normalise_borne(self):
        _, lignes = self._executer()
        for l in lignes:
            self.assertGreaterEqual(l.score_normalise, 0.0)
            self.assertLessEqual(l.score_normalise, 1.0)
            self.assertLessEqual(l.score_points, l.score_max)

    def test_filtre_dur_calendrier(self):
        """Une annonce macro dans l'horizon écarte la détection."""
        _, base = self._executer()
        cible = base[0]
        cal = calendrier_eco.Calendrier([
            calendrier_eco.Evenement(cible.entree_ts, "USD", "taux_directeur")])
        _, avec = pipeline.executer("EURUSD", "H1", self.h1, self.m1,
                                    self.h4, self.d1, calendrier=cal)
        touchee = [l for l in avec if l.entree_ts == cible.entree_ts][0]
        self.assertIn("evenement_macro", touchee.motif_rejet)
        self.assertEqual(touchee.statut, "ecartee")

    def test_trois_objectifs_resolus(self):
        _, lignes = self._executer()
        for l in lignes[:50]:
            self.assertEqual(set(l.issues), {"methode", "1r5", "2r"})

    def test_statistiques_sous_seuil_non_publiables(self):
        _, lignes = self._executer()
        s = pipeline.statistiques(lignes[:40])
        self.assertFalse(s["publiable"])
        self.assertEqual(s["statut"], "insuffisant")

    def test_point_in_time_chaine_complete(self):
        """Le test décisif : les empreintes ne doivent pas dépendre du futur."""
        coupure = len(self.h1) * 2 // 3
        tronque = self.h1[:coupure]
        fin = tronque[-1]["ts"]
        m1_tronque = [b for b in self.m1 if b["ts"] <= fin]

        _, ref = pipeline.executer("EURUSD", "H1", tronque, m1_tronque,
                                   self.h4, self.d1)
        # Les deux listes doivent être filtrées IDENTIQUEMENT : une détection
        # sur la dernière bougie a une entrée postérieure à la coupure.
        emp_ref = [l.empreinte for l in ref if l.entree_ts <= fin]

        aberrantes = determinisme.donnees_aberrantes(tronque, facteur=10.0, nombre=400)
        _, avec = pipeline.executer("EURUSD", "H1", tronque + aberrantes,
                                    m1_tronque, self.h4, self.d1)
        emp_avec = [l.empreinte for l in avec if l.entree_ts <= fin]

        self.assertEqual(emp_ref, emp_avec[:len(emp_ref)],
                         "fuite d'information future dans la chaîne complète")




def serie_construite(profil, n=600, graine=0, base=1.1000):
    """Séries de référence annotées à la main — SPEC-LOT2 §8.3.

    'range'    : le prix oscille entre deux bornes nettes
    'tendance' : hausse franche et continue, aucun range ne doit être détecté
    'bruit'    : marche aléatoire pure
    """
    import math
    rng = random.Random(graine)
    ts = datetime(2026, 1, 5, 0, 0, tzinfo=UTC)
    out, prix = [], base
    for i in range(n):
        # Niveaux de bruit calibrés sur la réalité : l'ATR horaire d'EUR/USD
        # vaut 8 à 12 pips. Un générateur trop lisse produirait un ATR de 4 pips
        # et testerait le détecteur sur un marché qui n'existe pas.
        if profil == "range":
            centre = base + 0.0022 * math.sin(2 * math.pi * i / 45)
            prix += (centre - prix) * 0.30 + rng.gauss(0, 0.00045)
        elif profil == "tendance":
            prix += 0.00075 + rng.gauss(0, 0.00040)
        else:
            prix += rng.gauss(0, 0.00060)
        o = prix
        c = prix + rng.gauss(0, 0.00025)
        h = max(o, c) + abs(rng.gauss(0, 0.00020))
        l = min(o, c) - abs(rng.gauss(0, 0.00020))
        out.append({"ts": ts, "o": o, "h": h, "l": l, "c": c})
        prix = c
        ts += timedelta(hours=1)
    return out


class TestJeuDeReference(unittest.TestCase):
    """Le détecteur doit trouver ce qui existe et ne rien inventer."""

    @staticmethod
    def _detecter(bougies):
        h = [b["h"] for b in bougies]; l = [b["l"] for b in bougies]
        c = [b["c"] for b in bougies]
        atrs = indicateurs.atr(h, l, c, 14)
        ps = pivots.detecter_pivots(h, l, atrs)
        return range_v1.detecter(bougies, ps, atrs)[0]

    def test_trouve_les_ranges_construits(self):
        trouves = sum(1 for g in range(10)
                      if self._detecter(serie_construite("range", graine=g)))
        self.assertGreaterEqual(trouves, 8,
                                f"seulement {trouves}/10 ranges construits détectés")

    def test_n_invente_pas_de_range_en_tendance(self):
        inventes = sum(1 for g in range(10)
                       if self._detecter(serie_construite("tendance", graine=100 + g)))
        self.assertLessEqual(inventes, 1,
                             f"{inventes}/10 ranges inventés sur des tendances franches")

    def test_bornes_proches_des_bornes_reelles(self):
        rgs = self._detecter(serie_construite("range", graine=7))
        self.assertTrue(rgs)
        r = rgs[0]
        # amplitude construite : ±0,0022 autour de 1,1000, plus le bruit
        self.assertAlmostEqual(r.borne_haute, 1.1022, delta=0.0022)
        self.assertAlmostEqual(r.borne_basse, 1.0978, delta=0.0022)
        self.assertGreater(r.hauteur, 0.0025)


if __name__ == "__main__":
    unittest.main(verbosity=2)
