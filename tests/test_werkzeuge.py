"""Tests der Werkzeuge: Vorlagen und Wächter passen zusammen, angelegte Dateien, Linkprüfung, DOI-Erkennung,
Zitierschlüssel."""

from __future__ import annotations

import contextlib
import importlib
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

pruefe = importlib.import_module("pruefe")
verweise = importlib.import_module("verweise")
doi2bib = importlib.import_module("doi2bib")
neu = importlib.import_module("neu")
status = importlib.import_module("status")

VORLAGE_AUSWERTUNG = (REPO / "vorlagen" / "auswertung.md").read_text(encoding="utf-8")
VORLAGE_SAMMEL = (REPO / "vorlagen" / "sammeldokument.md").read_text(encoding="utf-8")


def auswertung_aus_vorlage(status: str = "in Arbeit", abgehakt: bool = False, zweck: str = "Methoden") -> str:
    text = (VORLAGE_AUSWERTUNG.replace("<Schlüssel>", "Muster2020").replace("<Kategorie>", "thema")
            .replace("<Datum>", "2026-01-01").replace("<Titel>", "Titel").replace("<DOI>", "10.1000/x"))
    text = re.sub(r"Zweck \*\*<[^*]*>\*\*", f"Zweck **{zweck}**", text, count=1)
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

    def test_pruefliste_kommt_aus_der_vorlage(self):
        self.assertEqual((pruefe.PRUEFLISTE, pruefe.PFLICHTABSCHNITTE), pruefe.aus_vorlage())
        self.assertTrue(pruefe.PRUEFLISTE)
        for punkt in pruefe.PRUEFLISTE:
            self.assertIn(f"**{punkt}**", VORLAGE_AUSWERTUNG)

    def test_entwurf_mit_fehlendem_abschnitt_nur_hinweis(self):
        text = auswertung_aus_vorlage().replace("## Stärken", "## Gut gemacht")
        b = self.befund(text)
        self.assertEqual(b.fehler, [])
        self.assertTrue(any("Stärken" in h for h in b.hinweise))
        b = self.befund(auswertung_aus_vorlage("geprüft", abgehakt=True).replace("## Stärken", "## Gut gemacht"))
        self.assertTrue(any("Stärken" in was for _, was in b.fehler))

    def test_beispiel_in_inline_code_zaehlt_nicht_als_link(self):
        sammel = VORLAGE_SAMMEL.replace("## Was sich abzeichnet\n",
                                        "## Was sich abzeichnet\n\n`- [Muster 2020](Muster2020_auswertung.md)`\n")
        b = self.befund(auswertung_aus_vorlage("geprüft", abgehakt=True), sammel)
        self.assertTrue(any("verweist nicht auf diese Auswertung" in was for _, was in b.fehler))

    def test_register_querverweis(self):
        text = auswertung_aus_vorlage().replace("> **Register:** keine", "> **Register:** `Muster2020-a`")
        self.datei.write_text(text, encoding="utf-8")
        b = pruefe.Bericht()
        pruefe.pruefe_auswertung(self.datei, {}, b)
        self.assertTrue(any("steht nicht in data/register.yaml" in was for _, was in b.fehler))
        b = pruefe.Bericht()
        pruefe.pruefe_auswertung(self.datei, {"Muster2020-a": {"auswertung": pruefe.rel(self.datei)}}, b)
        self.assertEqual(b.fehler, [])


class EigeneVorlage(unittest.TestCase):
    """Wer die Prüfliste oder die Pflichtabschnitte in der Vorlage ändert, ändert, was der Wächter verlangt."""

    def lesen(self, text: str) -> tuple[list[str], list[str]]:
        with tempfile.TemporaryDirectory() as d:
            pfad = Path(d) / "auswertung.md"
            pfad.write_text(text, encoding="utf-8")
            return pruefe.aus_vorlage(pfad)

    def test_eigene_punkte_und_abschnitte(self):
        liste, abschnitte = self.lesen(
            "<!-- pflichtabschnitte: Frage, Befund -->\n<!-- pruefliste:start -->\n"
            "- [ ] **Messinstrument** validiert\n- [ ] **Überlappung** geprüft\n<!-- pruefliste:ende -->\n")
        self.assertEqual(liste, ["Messinstrument", "Überlappung"])
        self.assertEqual(abschnitte, ["Frage", "Befund"])

    def test_ohne_marken_gelten_die_standardlisten(self):
        self.assertEqual(self.lesen("# Nur Text\n"),
                         (pruefe.PRUEFLISTE_STANDARD, pruefe.PFLICHTABSCHNITTE_STANDARD))

    def test_leere_pruefliste_heisst_keine(self):
        liste, _ = self.lesen("<!-- pruefliste:start -->\n<!-- pruefliste:ende -->\n")
        self.assertEqual(liste, [])


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

    def test_links_ab_dem_hauptordner(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w / "ENTSCHEIDUNGEN.md").write_text("# E\n", encoding="utf-8")
            (w / "tief" / "tiefer").mkdir(parents=True)
            (w / "tief" / "tiefer" / "a.md").write_text("[gut](/ENTSCHEIDUNGEN.md) [tot](/FEHLT.md)\n", encoding="utf-8")
            fehler = verweise.pruefen(w)
        self.assertEqual(len(fehler), 1)
        self.assertIn("/FEHLT.md", fehler[0][1])

    def test_html_links_im_ordnerbaum(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w / "ziel.md").write_text("## Abschnitt\n", encoding="utf-8")
            (w / "README.md").write_text('<pre>\n├── <a href="ziel.md#abschnitt">ziel.md</a>\n'
                                         '├── <a href="fehlt.md">fehlt.md</a>\n</pre>\n', encoding="utf-8")
            fehler = verweise.pruefen(w)
        self.assertEqual(len(fehler), 1)
        self.assertIn("fehlt.md", fehler[0][1])

    def test_anker_wie_github(self):
        self.assertEqual(verweise.slug("Was sich abzeichnet"), "was-sich-abzeichnet")


class Doi(unittest.TestCase):
    def test_doi_am_zeilenanfang_einer_tabelle(self):
        self.assertEqual(doi2bib.doi_aus_zeile("| 10.1000/182 · | Muster 2020 | Grund |"), "10.1000/182")
        self.assertEqual(doi2bib.doi_aus_zeile("Anmerkung zu 10.1000/182"), "")

    def test_zitierschluessel(self):
        eintrag = "@article{x, author={Müller, Anna and Huber, Ben}, title={T}, year={2020}, doi={10.1/x}}"
        self.assertEqual(doi2bib.make_key(eintrag, set()), "Muller2020")
        self.assertEqual(doi2bib.make_key(eintrag, {"Muller2020"}), "Muller2020a")


def neu_aufrufen(wurzel: Path, *argumente: str) -> None:
    """tools/neu.py in einem Wegwerf-Ordner aufrufen, ohne status.py im echten Repository."""
    alt = (neu.REPO, neu.BIB)
    neu.REPO, neu.BIB = wurzel, wurzel / "literatur.bib"
    try:
        with mock.patch.object(neu, "status_nachziehen", lambda: None), \
                mock.patch.object(sys, "argv", ["neu.py", *argumente]), \
                contextlib.redirect_stdout(io.StringIO()):
            neu.main()
    finally:
        neu.REPO, neu.BIB = alt


ROOT_LINK = re.compile(r"\]\((/[^)#\s]+)")


def stellvertreter_fuer_hauptordner(wurzel: Path) -> None:
    """Vorlagen verlinken Dateien ab dem Hauptordner (/CLAUDE.md …). Im Wegwerf-Ordner
    stehen dafür leere Stellvertreter, aber nur für Ziele, die es im Kit wirklich gibt."""
    for md in list(wurzel.glob("**/*.md")):
        for ziel in ROOT_LINK.findall(md.read_text(encoding="utf-8")):
            echt, platz = REPO / ziel.lstrip("/"), wurzel / ziel.lstrip("/")
            if echt.exists() and not platz.exists():
                platz.parent.mkdir(parents=True, exist_ok=True)
                platz.write_text("", encoding="utf-8")


class Neu(unittest.TestCase):
    @staticmethod
    def anlegen(wurzel: Path, *knapp: str) -> list[Path]:
        """Kategorie, Protokoll und Auswertung anlegen, wie im Schnellstart."""
        (wurzel / "literatur.bib").write_text(
            "@article{Muster2020, title={Ein Titel}, doi={10.1000/x}, year={2020}}\n", encoding="utf-8")
        neu_aufrufen(wurzel, *knapp, "kategorie", "thema")
        neu_aufrufen(wurzel, *knapp, "protokoll", "suche", "thema")
        neu_aufrufen(wurzel, *knapp, "auswertung", "thema", "Muster2020")
        stellvertreter_fuer_hauptordner(wurzel)
        return sorted(p for p in wurzel.glob("**/*.md") if p.stat().st_size)

    def test_auswertung_aus_vorlage_anlegen(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            self.anlegen(w)
            text = (w / "literatur" / "thema" / "Muster2020_auswertung.md").read_text(encoding="utf-8")
        self.assertIn("# Muster2020", text)
        self.assertIn("[thema](thema.md)", text)
        self.assertIn("10.1000/x", text)

    def test_angelegte_dateien_sind_sauber(self):
        """Keine toten Links, keine Kennung aus einem Beispiel, und der Wächter hat nichts zu beanstanden."""
        for knapp in ((), ("--knapp",)):
            with self.subTest(knapp=knapp), tempfile.TemporaryDirectory() as d:
                w = Path(d)
                dateien = self.anlegen(w, *knapp)
                self.assertEqual(len(dateien), 3)
                self.assertEqual(verweise.pruefen(w), [])
                for datei in dateien:
                    for zeile in datei.read_text(encoding="utf-8").splitlines():
                        self.assertEqual(status.kennung_aus_zeile(zeile), "", f"{datei.name}: {zeile}")
                b = pruefe.Bericht()
                pruefe.pruefe_auswertung(w / "literatur" / "thema" / "Muster2020_auswertung.md", {}, b)
                self.assertEqual(b.fehler, [])

    def test_unterordner_fuer_ein_teilthema(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            self.anlegen(w)
            neu_aufrufen(w, "kategorie", "thema/teil")
            neu_aufrufen(w, "protokoll", "teilsuche", "thema/teil")
            with (w / "literatur.bib").open("a", encoding="utf-8") as f:
                f.write("@article{Muster2021, title={Zweiter Titel}, doi={10.1000/y}, year={2021}}\n")
            neu_aufrufen(w, "auswertung", "thema/teil", "Muster2021")
            stellvertreter_fuer_hauptordner(w)
            sammel = (w / "literatur" / "thema" / "teil" / "teil.md").read_text(encoding="utf-8")
            auswertung = (w / "literatur" / "thema" / "teil" / "Muster2021_auswertung.md").read_text(encoding="utf-8")
            protokoll = next((w / "notes" / "recherche").glob("*-teilsuche.md")).read_text(encoding="utf-8")
            self.assertEqual(verweise.pruefen(w), [])
        self.assertTrue(sammel.startswith("# teil — Gesamtschau"))
        self.assertIn("[teil](teil.md)", auswertung)
        self.assertIn("literatur/thema/teil/", protokoll)

    def test_links_der_vorlagen_zeigen_auf_bestehende_dateien(self):
        for vorlage in sorted((REPO / "vorlagen").glob("*.md")):
            for ziel in ROOT_LINK.findall(vorlage.read_text(encoding="utf-8")):
                self.assertTrue((REPO / ziel.lstrip("/")).exists(), f"{vorlage.name}: {ziel}")

    def test_knapp_laesst_nur_die_hilfe_weg(self):
        knapp = neu.ohne_hilfe(VORLAGE_AUSWERTUNG)
        for hilfe in ("> **So ist", "> **Optionen", "> **Beispiel"):
            self.assertNotIn(hilfe, knapp)
        for bleibt in ("> **Register:** keine", "<!-- pruefliste:start -->", "<!-- pflichtabschnitte:",
                       *(f"## {a}" for a in pruefe.PFLICHTABSCHNITTE)):
            self.assertIn(bleibt, knapp)
        self.assertEqual(neu.ohne_hilfe("Text\n\n> **Beispiel:** x\n> y\n\nWeiter\n"), "Text\n\nWeiter\n")


class StandTabelle(unittest.TestCase):
    """status.py schreibt „Stand“ ins Sammeldokument, mit DOI bei jeder Arbeit, deren Volltext fehlt."""

    def test_tabelle_im_sammeldokument(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            Neu.anlegen(w)                      # Kategorie thema, Protokoll mit Ablage thema, Auswertung Muster2020
            with (w / "literatur.bib").open("a", encoding="utf-8") as f:
                f.write("@article{Muster2021, title={Zweiter | Titel}, doi={10.1016/s2542-5196(20)30079-6}, year={2021}}\n")
            protokoll = next((w / "notes" / "recherche").glob("*.md"))
            kopf = "| DOI | Studie | Warum sie zählt |\n|---|---|---|\n"
            text = protokoll.read_text(encoding="utf-8")
            self.assertIn(kopf, text)
            text = text.replace(kopf, kopf + "| 10.1000/x | Muster 2020 | a |\n"
                                "| 10.1016/s2542-5196(20)30079-6 | Muster 2021 | b |\n"
                                "| 10.1000/neu | noch ohne Eintrag | c |\n", 1)
            protokoll.write_text(text, encoding="utf-8")
            pfade = dict(REPO=w, BIB=w / "literatur.bib", LITERATUR=w / "literatur",
                         RECHERCHE=w / "notes" / "recherche", BESCHAFFUNG=w / "notes" / "recherche" / "beschaffung.yaml")
            with mock.patch.multiple(status, **pfade):
                tabellen = status.stand_tabellen(status.kennung_zu_schluessel(), status.vorhandene_volltexte(),
                                                 status.ausgewertete(), {})
                sammel = w / "literatur" / "thema" / "thema.md"
                neu_text = status.stand_setzen(sammel.read_text(encoding="utf-8"), tabellen[sammel])
        zeilen = neu_text.split(status.STAND_START)[1].split(status.STAND_ENDE)[0].strip().splitlines()
        self.assertEqual(zeilen[2], "| ✅ | [Muster2020](Muster2020_auswertung.md) | Ein Titel | "
                                    "[10.1000/x](https://doi.org/10.1000/x) |")
        self.assertIn("| · | Muster2021 | Zweiter \\| Titel | [10.1016/s2542-5196(20)30079-6]"
                      "(https://doi.org/10.1016/s2542-5196%2820%2930079-6) |", zeilen)
        self.assertIn("| · | noch nicht in literatur.bib |  | [10.1000/neu](https://doi.org/10.1000/neu) |", zeilen)

    def test_ohne_marken_bleibt_alles(self):
        self.assertEqual(status.stand_setzen("# Text ohne Marken\n", "| x |"), "# Text ohne Marken\n")


if __name__ == "__main__":
    unittest.main()
