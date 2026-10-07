#!/usr/bin/env python3
"""Neue Dateien aus den Vorlagen anlegen, mit den richtigen Namen am richtigen Ort.

    python3 tools/neu.py kategorie <name>                 # literatur/<name>/<name>.md
    python3 tools/neu.py auswertung <kategorie> <Schlüssel>  # literatur/<kategorie>/<Schlüssel>_auswertung.md
    python3 tools/neu.py protokoll <name> [<kategorie>]   # notes/recherche/<JJJJ-MM>-<name>.md

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
    a = ap.parse_args()
    heute = dt.date.today().isoformat()

    if a.art == "kategorie":
        name = a.namen[0]
        text = (VORLAGEN / "sammeldokument.md").read_text(encoding="utf-8")
        schreiben(REPO / "literatur" / name / f"{name}.md",
                  text.replace("<Kategorie>", name).replace("<Datum>", heute))
    elif a.art == "auswertung":
        if len(a.namen) != 2:
            sys.exit("Aufruf: python3 tools/neu.py auswertung <kategorie> <Schlüssel>")
        kategorie, schluessel = a.namen
        eintrag = bib_eintrag(schluessel)
        if eintrag is None:
            sys.exit(f"{schluessel} steht nicht in literatur.bib. Erst: python3 tools/doi2bib.py <DOI>")
        text = (VORLAGEN / "auswertung.md").read_text(encoding="utf-8")
        text = (text.replace("<Schlüssel>", schluessel).replace("<Datum>", heute).replace("<Kategorie>", kategorie)
                    .replace("<Titel>", feld(eintrag, "title") or "<Titel>")
                    .replace("<DOI>", feld(eintrag, "doi") or "<DOI>"))
        schreiben(REPO / "literatur" / kategorie / f"{schluessel}_auswertung.md", text)
        import subprocess                       # Statuszeichen in den Protokollen gleich nachziehen
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "status.py")], check=False,
                       stdout=subprocess.DEVNULL)
        if not (REPO / "literatur" / kategorie / f"{kategorie}.md").exists():
            print(f"Hinweis: Sammeldokument fehlt noch:  python3 tools/neu.py kategorie {kategorie}")
    else:
        name = a.namen[0]
        kategorie = a.namen[1] if len(a.namen) > 1 else name
        text = (VORLAGEN / "rechercheprotokoll.md").read_text(encoding="utf-8")
        schreiben(REPO / "notes" / "recherche" / f"{heute[:7]}-{name}.md",
                  text.replace("<Thema>", name).replace("<Datum>", heute).replace("<Kategorie>", kategorie))
    return 0


if __name__ == "__main__":
    sys.exit(main())
