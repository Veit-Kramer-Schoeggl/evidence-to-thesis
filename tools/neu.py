#!/usr/bin/env python3
"""Neue Dateien aus den Vorlagen anlegen, mit den richtigen Namen am richtigen Ort.

    python3 tools/neu.py kategorie <name>                 # literatur/<name>/<name>.md
    python3 tools/neu.py auswertung <kategorie> <Schlüssel>  # literatur/<kategorie>/<Schlüssel>_auswertung.md
    python3 tools/neu.py protokoll <name> [<kategorie>]   # notes/recherche/<JJJJ-MM>-<name>.md

Mit --knapp kommen die Hilfeblöcke der Vorlage nicht mit: die Zitatblöcke, die mit
**So ist diese Vorlage gemeint.**, **Optionen** oder **Beispiel** beginnen.

    python3 tools/neu.py --knapp auswertung <kategorie> <Schlüssel>

Der Zitierschlüssel muss in literatur.bib stehen (tools/doi2bib.py legt ihn an).
Bestehende Dateien werden nie überschrieben.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VORLAGEN = REPO / "vorlagen"
BIB = REPO / "literatur.bib"

# Ein Hilfeblock ist ein Zitatblock, dessen erste Zeile mit **So ist …**, **Optionen …** oder
# **Beispiel …** beginnt; er reicht bis zur ersten Zeile ohne „>“, dazu die Leerzeile danach.
HILFE = re.compile(r"^> \*\*(?:So ist|Optionen|Beispiel)[^\n]*(?:\n>[^\n]*)*\n?\n?", re.MULTILINE)


def bib_eintrag(schluessel: str) -> str | None:
    if not BIB.exists():
        return None
    for eintrag in re.split(r"(?=@\w+\s*\{)", BIB.read_text(encoding="utf-8")):
        if re.match(r"@\w+\s*\{\s*" + re.escape(schluessel) + r"\s*,", eintrag):
            return eintrag
    return None


def feld(eintrag: str, name: str) -> str:
    m = re.search(r"\b" + name + r"\s*=\s*\{(.+?)\}\s*,\s*\w+\s*=", eintrag, re.S) or \
        re.search(r"\b" + name + r"\s*=\s*\{(.+?)\}\s*\}?\s*$", eintrag, re.S)
    return " ".join(m.group(1).split()) if m else ""


def ohne_hilfe(text: str) -> str:
    """Die Vorlage ohne ihre Hilfeblöcke (Optionen, Beispiele, Lesehinweis)."""
    return re.sub(r"\n{3,}", "\n\n", HILFE.sub("", text)).rstrip() + "\n"


def status_nachziehen() -> None:
    """Statuszeichen in den Rechercheprotokollen gleich nachziehen (tools/status.py)."""
    import subprocess
    subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "status.py")], check=False,
                   stdout=subprocess.DEVNULL)


def vorlage(name: str, knapp: bool) -> str:
    text = (VORLAGEN / name).read_text(encoding="utf-8")
    return ohne_hilfe(text) if knapp else text


def schreiben(ziel: Path, text: str) -> None:
    if ziel.exists():
        sys.exit(f"{ziel.relative_to(REPO)} gibt es schon; nichts überschrieben.")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")
    print(f"angelegt: {ziel.relative_to(REPO)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("art", choices=["kategorie", "auswertung", "protokoll"])
    ap.add_argument("namen", nargs="+")
    ap.add_argument("--knapp", action="store_true", help="ohne die Blöcke Optionen und Beispiel anlegen")
    a = ap.parse_args()
    heute = dt.date.today().isoformat()

    if a.art == "kategorie":
        name = a.namen[0]
        text = vorlage("sammeldokument.md", a.knapp)
        schreiben(REPO / "literatur" / name / f"{name}.md",
                  text.replace("<Kategorie>", name).replace("<Datum>", heute))
    elif a.art == "auswertung":
        if len(a.namen) != 2:
            sys.exit("Aufruf: python3 tools/neu.py auswertung <kategorie> <Schlüssel>")
        kategorie, schluessel = a.namen
        eintrag = bib_eintrag(schluessel)
        if eintrag is None:
            sys.exit(f"{schluessel} steht nicht in literatur.bib. Erst: python3 tools/doi2bib.py <DOI>")
        text = vorlage("auswertung.md", a.knapp)
        text = (text.replace("<Schlüssel>", schluessel).replace("<Datum>", heute).replace("<Kategorie>", kategorie)
                    .replace("<Titel>", feld(eintrag, "title") or "<Titel>")
                    .replace("<DOI>", feld(eintrag, "doi") or "<DOI>"))
        schreiben(REPO / "literatur" / kategorie / f"{schluessel}_auswertung.md", text)
        status_nachziehen()
        if not (REPO / "literatur" / kategorie / f"{kategorie}.md").exists():
            print(f"Hinweis: Sammeldokument fehlt noch:  python3 tools/neu.py kategorie {kategorie}")
    else:
        name = a.namen[0]
        kategorie = a.namen[1] if len(a.namen) > 1 else name
        text = vorlage("rechercheprotokoll.md", a.knapp)
        schreiben(REPO / "notes" / "recherche" / f"{heute[:7]}-{name}.md",
                  text.replace("<Thema>", name).replace("<Datum>", heute).replace("<Kategorie>", kategorie))
    return 0


if __name__ == "__main__":
    sys.exit(main())
