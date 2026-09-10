"""Ce que les écrans AFFIRMENT doit être vrai.

Ces tests existent parce que 93 tests verts coexistaient avec une interface qui
mentait : chaque carte annonçait la détection comme « ancrée » alors qu'aucun
ancrage externe n'est en service. Générer un fichier n'est pas le tester.
"""
from __future__ import annotations

import html
import re
import sys
import unittest
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forexlab import rapport, stats
from forexlab.pipeline import Ligne

UTC = timezone.utc


def ligne(i, statut="annoncee", motif=""):
    ts = datetime(2026, 3, 1, tzinfo=UTC) + timedelta(hours=i)
    return Ligne("EURUSD", "H1", "range", "R1a", 1, ts, 1.10, 1.09, 1.12,
                 1.115, 1.12, 8, 10, 0.8, statut, motif, {"zone": {}},
                 {"methode": {"resultat": "atteint", "r_net": 0.9,
                              "r_brut": 1.0, "ambigu_m1": False}}, f"{i:064x}")


def texte(fichier):
    s = fichier.read_text(encoding="utf-8")
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)))


class _Structure(HTMLParser):
    def __init__(self):
        super().__init__(); self.pile = []; self.erreurs = []
        self.orphelins = {"meta", "link", "br", "hr", "img", "input"}

    def handle_starttag(self, t, a):
        if t not in self.orphelins:
            self.pile.append(t)

    def handle_endtag(self, t):
        if not self.pile:
            self.erreurs.append(f"</{t}> sans ouverture")
        elif self.pile[-1] != t:
            self.erreurs.append(f"</{t}> alors que <{self.pile[-1]}> est ouvert")
        else:
            self.pile.pop()


class TestEcrans(unittest.TestCase):
    def _generer(self, dossier, lignes, ancre):
        sa = stats.agregat([0.1] * 150, ["atteint"] * 150)
        se = stats.agregat([-0.2] * 300, ["invalide"] * 300)
        cl = {"lignes": [], "series_testees": 18, "series_publiables": 0}
        integ = {"cycles": 12, "cycles_vides": 1, "detections": len(lignes),
                 "valide": True, "ancre": ancre}
        return rapport.ecrire(dossier, lignes, sa, se, cl, integ)

    def test_jamais_ancree_sans_ancrage(self):
        """Le défaut réel : l'interface affirmait un ancrage inexistant."""
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(5)], ancre=False)
            for f in site.glob("*.html"):
                t = texte(f)
                self.assertNotIn("ancrée chez trois tiers", t,
                                 f"{f.name} affirme un ancrage qui n'existe pas")
            self.assertIn("non encore ancrés", texte(site / "integrite.html"))
            self.assertIn("non opposable", texte(site / "integrite.html"))

    def test_ancrage_affirme_seulement_s_il_existe(self):
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(5)], ancre=True)
            self.assertIn("ancrée chez trois tiers", texte(site / "index.html"))

    def test_aucune_annoncee_le_dit_au_lieu_de_montrer_des_ecartees(self):
        with TemporaryDirectory() as d:
            lignes = [ligne(i, "ecartee", "score_insuffisant") for i in range(5)]
            site = self._generer(d, lignes, ancre=False)
            t = texte(site / "index.html")
            self.assertIn("Aucune configuration", t)
            self.assertNotIn("R1a", t, "l'accueil ne doit pas lister d'écartées")

    def test_avertissement_de_risque_sur_toutes_les_pages(self):
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(3)], ancre=False)
            for f in site.glob("*.html"):
                self.assertIn("performances passées", texte(f), f.name)
                self.assertIn("ne constitue pas un conseil", texte(f), f.name)

    def test_vocabulaire_interdit_absent(self):
        """Les cinq interdits du cahier des charges §22."""
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(3)], ancre=False)
            for f in site.glob("*.html"):
                t = texte(f).lower()
                for mot in ("achetez", "vendez", "prenez ce trade",
                            "recommandé pour vous", "garanti", "profit assuré"):
                    self.assertNotIn(mot, t, f"{f.name} contient « {mot} »")

    def test_html_bien_forme(self):
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(3)], ancre=False)
            for f in site.glob("*.html"):
                v = _Structure(); v.feed(f.read_text(encoding="utf-8"))
                self.assertEqual(v.erreurs, [], f.name)
                self.assertEqual([t for t in v.pile if t not in ("html", "body")],
                                 [], f"{f.name} : balises non fermées")

    def test_nombre_de_series_testees_affiche(self):
        """Un lecteur doit pouvoir juger de l'ampleur du test multiple."""
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(3)], ancre=False)
            self.assertIn("18 séries testées", texte(site / "figures.html"))

    def test_aucun_chiffre_sans_comparaison(self):
        """Toute espérance affichée doit porter son terme de comparaison."""
        with TemporaryDirectory() as d:
            site = self._generer(d, [ligne(i) for i in range(3)], ancre=False)
            for f in ("index.html", "ecartees.html"):
                t = texte(site / f)
                self.assertTrue("témoin" in t.lower() or "Annoncées" in t,
                                f"{f} affiche un chiffre sans comparaison")


if __name__ == "__main__":
    unittest.main(verbosity=2)
