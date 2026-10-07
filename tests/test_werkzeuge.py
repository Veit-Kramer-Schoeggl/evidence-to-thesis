"""Tests der Werkzeuge: Vorlagen und Wächter passen zusammen, Linkprüfung, DOI-Erkennung, Zitierschlüssel."""

import contextlib
import importlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

pruefe = importlib.import_module("pruefe")
verweise = importlib.import_module("verweise")
doi2bib = importlib.import_module("doi2bib")
neu = importlib.import_module("neu")

VORLAGE_AUSWERTUNG = (REPO / "vorlagen" / "auswertung.md").read_text(encoding="utf-8")
VORLAGE_SAMMEL = (REPO / "vorlagen" / "sammeldokument.md").read_text(encoding="utf-8")


def auswertung_aus_vorlage(status: str = "in Arbeit", abgehakt: bool = False, zweck: str = "Methoden") -> str:
    text = (VORLAGE_AUSWERTUNG.replace("<Schlüssel>", "Muster2020").replace("<Kategorie>", "thema")
            .replace("<Datum>", "2026-01-01").replace("<Titel>", "Titel").replace("<DOI>", "10.1000/x"))
    text = text.replace("Zweck **<wofür die Arbeit gebraucht wird, z. B. Methoden, Diskussion>**", f"Zweck **{zweck}**")
    text = text.replace("Status: **in Arbeit**", f"Status: **{status}**")
    if abgehakt:
        text = text.replace("- [ ] ", "- [x] ")
    return text


class VorlageUndWaechter(unittest.TestCase):
    """Eine Auswertung aus der Vorlage muss den Wächter bestehen, sobald sie ausgefüllt ist."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name) / "thema"
        self.ordner.mkdir()
        self.datei = self.ordner / "Muster2020_auswertung.md"

    def tearDown(self):
        self.tmp.cleanup()

    def befund(self, text: str, sammel: str | None = None) -> pruefe.Bericht:
        self.datei.write_text(text, encoding="utf-8")
        if sammel is not None:
            (self.ordner / "thema.md").write_text(sammel, encoding="utf-8")
        b = pruefe.Bericht()
        pruefe.pruefe_auswertung(self.datei, {}, b)
        return b

    def test_vorlage_in_arbeit_ist_ohne_fehler(self):
        b = self.befund(auswertung_aus_vorlage())
        self.assertEqual(b.fehler, [])
        self.assertTrue(any("offen" in h for h in b.hinweise))

    def test_unausgefuellter_zweck(self):
        text = VORLAGE_AUSWERTUNG.replace("<Kategorie>", "thema")
        b = self.befund(text)                                   # in Arbeit: nur Hinweis
        self.assertEqual(b.fehler, [])
        self.assertTrue(any("Zweck" in h for h in b.hinweise))
        b = self.befund(text.replace("Status: **in Arbeit**", "Status: **geprüft**"))
        self.assertTrue(any("Zweck" in was for _, was in b.fehler))   # geprüft: Fehler

    def test_gepruefte_vorlage_mit_link_im_sammeldokument(self):
        sammel = VORLAGE_SAMMEL.replace("## Was sich abzeichnet\n",
                                        "## Was sich abzeichnet\n\n- [Muster 2020](Muster2020_auswertung.md): Kernaussage.\n")
        b = self.befund(auswertung_aus_vorlage("geprüft", abgehakt=True), sammel)
        self.assertEqual(b.fehler, [])

    def test_gepruefte_ohne_haken_und_ohne_link(self):
        b = self.befund(auswertung_aus_vorlage("geprüft"), VORLAGE_SAMMEL)
        meldungen = [was for _, was in b.fehler]
        self.assertTrue(any("Prüflistenpunkt offen" in m for m in meldungen))
        self.assertTrue(any("verweist nicht auf diese Auswertung" in m for m in meldungen))

    def test_vorlage_fuehrt_jeden_pruefpunkt(self):
        for punkt in pruefe.PRUEFLISTE:
            self.assertIn(f"**{punkt}**", VORLAGE_AUSWERTUNG)

    def test_register_querverweis(self):
        text = auswertung_aus_vorlage().replace("> **Register:** keine", "> **Register:** `Muster2020-a`")
        self.datei.write_text(text, encoding="utf-8")
        b = pruefe.Bericht()
        pruefe.pruefe_auswertung(self.datei, {}, b)
        self.assertTrue(any("steht nicht in data/register.yaml" in was for _, was in b.fehler))
        b = pruefe.Bericht()
        pruefe.pruefe_auswertung(self.datei, {"Muster2020-a": {"auswertung": pruefe.rel(self.datei)}}, b)
        self.assertEqual(b.fehler, [])


class Register(unittest.TestCase):
    def test_wert_ohne_fundstelle(self):
        b = pruefe.Bericht()
        eintrag = {"id": "X-a", "schluessel": "X2020", "auswertung": "README.md", "status": "geprüft",
                   "belastbarkeit": "tragend", "werte": [{"name": "HR", "wert": 0.5}]}
        pruefe.pruefe_register([eintrag], {"X2020"}, b)
        self.assertTrue(any("ohne Fundstelle" in was for _, was in b.fehler))

    def test_vollstaendiger_eintrag(self):
        b = pruefe.Bericht()
        eintrag = {"id": "X-a", "schluessel": "X2020", "auswertung": "README.md", "status": "geprüft",
                   "belastbarkeit": "eingeschränkt", "werte": [{"name": "HR", "wert": 0.5, "fundstelle": "Tab. 2"}]}
        pruefe.pruefe_register([eintrag], {"X2020"}, b)
        self.assertEqual(b.fehler, [])


class Verweise(unittest.TestCase):
    def test_tote_links_und_ausnahmen(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w / "a.md").write_text("# Titel\n\n[gut](b.md#unterpunkt) [tot](fehlt.md) "
                                    "[volltext](pdf/X.pdf) `[code](nirgends.md)`\n", encoding="utf-8")
            (w / "b.md").write_text("## Unterpunkt\n", encoding="utf-8")
            (w / "vorlagen").mkdir()
            (w / "vorlagen" / "v.md").write_text("[platzhalter](<Kategorie>.md)\n", encoding="utf-8")
            fehler = verweise.pruefen(w)
        self.assertEqual(len(fehler), 1)
        self.assertIn("fehlt.md", fehler[0][1])

    def test_anker_wie_github(self):
        self.assertEqual(verweise.slug("Was sich abzeichnet"), "was-sich-abzeichnet")


class Doi(unittest.TestCase):
    def test_doi_am_zeilenanfang_einer_tabelle(self):
        self.assertEqual(doi2bib.doi_aus_zeile("| 10.1186/s12966-014-0132-x · | Kelly 2014 | Grund |"),
                         "10.1186/s12966-014-0132-x")
        self.assertEqual(doi2bib.doi_aus_zeile("Anmerkung zu 10.1186/s12966-014-0132-x"), "")

    def test_zitierschluessel(self):
        eintrag = "@article{x, author={Müller, Anna and Huber, Ben}, title={T}, year={2020}, doi={10.1/x}}"
        self.assertEqual(doi2bib.make_key(eintrag, set()), "Muller2020")
        self.assertEqual(doi2bib.make_key(eintrag, {"Muller2020"}), "Muller2020a")


class Neu(unittest.TestCase):
    def test_auswertung_aus_vorlage_anlegen(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w / "literatur.bib").write_text(
                "@article{Muster2020, title={Ein Titel}, doi={10.1000/x}, year={2020}}\n", encoding="utf-8")
            alt = (neu.REPO, neu.BIB)
            neu.REPO, neu.BIB = w, w / "literatur.bib"
            try:
                sys.argv = ["neu.py", "auswertung", "thema", "Muster2020"]
                with contextlib.redirect_stdout(io.StringIO()):
                    neu.main()
            finally:
                neu.REPO, neu.BIB = alt
            text = (w / "literatur" / "thema" / "Muster2020_auswertung.md").read_text(encoding="utf-8")
        self.assertIn("# Muster2020", text)
        self.assertIn("[thema](thema.md)", text)
        self.assertIn("10.1000/x", text)


if __name__ == "__main__":
    unittest.main()
