"""Tests du décodeur Dukascopy, sans accès réseau.

On fabrique un fichier bi5 synthétique et on vérifie le décodage.
Le téléchargement lui-même n'est pas testable ici : le réseau est fermé.
"""
from __future__ import annotations

import lzma
import struct
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import telecharger

UTC = timezone.utc


def bi5_synthetique(ticks):
    brut = b"".join(struct.pack(">IIIff", ms, ask, bid, 1.0, 1.0)
                    for ms, ask, bid in ticks)
    return lzma.compress(brut, format=lzma.FORMAT_ALONE)


class TestDecodeur(unittest.TestCase):
    def setUp(self):
        self.heure = datetime(2025, 6, 2, 10, 0, tzinfo=UTC)

    def test_adresse_mois_indexe_a_zero(self):
        """Piège Dukascopy : janvier s'écrit 00, décembre 11."""
        u = telecharger.adresse("EURUSD", datetime(2025, 1, 15, 9, tzinfo=UTC))
        self.assertIn("/2025/00/15/09h_ticks.bi5", u)
        u = telecharger.adresse("EURUSD", datetime(2025, 12, 1, 0, tzinfo=UTC))
        self.assertIn("/2025/11/01/00h_ticks.bi5", u)

    def test_decodage_prix_et_horodatage(self):
        brut = bi5_synthetique([(0, 110125, 110115), (60000, 110130, 110121)])
        ticks = telecharger.decoder(brut, "EURUSD", self.heure)
        self.assertEqual(len(ticks), 2)
        self.assertAlmostEqual(ticks[0]["bid"], 1.10115, places=9)
        self.assertAlmostEqual(ticks[0]["ask"], 1.10125, places=9)
        self.assertEqual(ticks[1]["ts"], self.heure + timedelta(minutes=1))

    def test_echelle_yen(self):
        brut = bi5_synthetique([(0, 151250, 151230)])
        t = telecharger.decoder(brut, "USDJPY", self.heure)[0]
        self.assertAlmostEqual(t["bid"], 151.230, places=6)

    def test_fichier_vide_et_corrompu(self):
        self.assertEqual(telecharger.decoder(b"", "EURUSD", self.heure), [])
        self.assertEqual(telecharger.decoder(b"pas du lzma", "EURUSD", self.heure), [])

    def test_agregation_m1_et_spread_median(self):
        brut = bi5_synthetique([
            (0, 110125, 110115), (10000, 110140, 110130),
            (30000, 110100, 110090), (60000, 110160, 110150)])
        m1 = telecharger.ticks_vers_m1(telecharger.decoder(brut, "EURUSD", self.heure))
        self.assertEqual(len(m1), 2)
        b = m1[0]
        self.assertAlmostEqual(b["o"], 1.101200, places=6)
        self.assertAlmostEqual(b["h"], 1.101350, places=6)
        self.assertAlmostEqual(b["l"], 1.100950, places=6)
        self.assertAlmostEqual(b["c"], 1.100950, places=6)
        self.assertAlmostEqual(b["spread"], 0.00010, places=7)

    def test_coherence_ohlc(self):
        brut = bi5_synthetique([(i * 1000, 110120 + i, 110110 + i) for i in range(50)])
        for b in telecharger.ticks_vers_m1(telecharger.decoder(brut, "EURUSD", self.heure)):
            self.assertLessEqual(b["l"], b["o"])
            self.assertLessEqual(b["o"], b["h"])
            self.assertLessEqual(b["l"], b["c"])
            self.assertLessEqual(b["c"], b["h"])
            self.assertGreater(b["spread"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
