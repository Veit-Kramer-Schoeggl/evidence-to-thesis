#!/usr/bin/env python3
"""Bearbeitungsstand in den Rechercheprotokollen fortschreiben.

Setzt hinter jede DOI in notes/recherche/*.md ein Statuszeichen:

    ·   Volltext steht aus
    ⛔  Volltext derzeit nicht beschaffbar — mit Grund in notes/recherche/beschaffung.yaml
    📄  Volltext liegt unter literatur/<kategorie>/pdf/<Schlüssel>.pdf (oder .xml)
    ✅  ausgewertet, es gibt literatur/<kategorie>/<Schlüssel>_auswertung.md

Dazu schreibt es in jedes Sammeldokument literatur/<kategorie>/<kategorie>.md, das die
Marken <!-- stand:start --> und <!-- stand:ende --> trägt, die Tabelle „Stand“: jede
Arbeit aus den Protokollen, deren Ablage diese Kategorie ist, mit Zeichen, Titel und
DOI. Fehlt der Volltext noch, lässt sich die Arbeit über die DOI gleich holen.

    python3 tools/status.py            # Status aktualisieren
    python3 tools/status.py --check    # nur berichten, nichts schreiben

Der Status wird nie von Hand gepflegt, sondern aus dem Dateibestand abgeleitet.
So kann er nicht veralten.

Quellen ohne DOI (WHO-Berichte, Gesetze, Bücher) stehen als `hdl:…` oder
`isbn:…` am Zeilenanfang — genau so, ohne Leer- und Trennzeichen.
tools/doi2bib.py und tools/holpdf.py übergehen solche Zeilen; hier und in
tools/bestand.py zählen sie wie eine DOI (kennung_aus_zeile).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIB = REPO / "literatur.bib"
LITERATUR = REPO / "literatur"
RECHERCHE = REPO / "notes" / "recherche"
BESCHAFFUNG = RECHERCHE / "beschaffung.yaml"

FEHLT, PDF_DA, AUSGEWERTET, NICHT_BESCHAFFBAR = "·", "📄", "✅", "⛔"
# Was als Volltext zählt. Word-Dateien kommen als Autorenmanuskript aus Repositorien vor.
VOLLTEXT_ENDUNGEN = (".pdf", ".xml", ".doc", ".docx")
SYMBOLE = {FEHLT, PDF_DA, AUSGEWERTET, NICHT_BESCHAFFBAR}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doi2bib import doi_aus_zeile  # noqa: E402


def doi_zu_schluessel() -> dict[str, str]:
    if not BIB.exists():
        return {}
    out = {}
    for eintrag in re.split(r"(?=@\w+\s*\{)", BIB.read_text(encoding="utf-8")):
        k = re.match(r"@\w+\s*\{\s*([^,\s]+)", eintrag)
        d = re.search(r"(?i)\bdoi\s*=\s*[{\"]([^}\"]+)", eintrag)
        if k and d:
            out[d.group(1).strip().lower()] = k.group(1)
    return out


# ── Kennungen ohne DOI ──────────────────────────────────
# Berichte von WHO, Behörden oder Kommissionen tragen oft keine DOI, sondern
# eine ISBN oder ein Handle. In den Protokollen stehen sie wie eine DOI am
# Zeilenanfang: `isbn:9789241565042` oder `hdl:10665/186463`. In literatur.bib
# stehen sie im Feld isbn= oder als Handle-Adresse im Feld url=
# (…/handle/10665/186463 oder hdl.handle.net/10665/186463). Berichte ohne
# DOI, ISBN und Handle (Jagger 2014, REVES-Leitfaden) stehen als `url:` mit
# der Adresse aus dem Feld url= — ohne Schema, klein.
_KENNUNG = re.compile(r"^[\s|\-*+>]*(isbn|hdl|url):\s*(\S+)", re.IGNORECASE)
_HANDLE_IN_URL = re.compile(r"(?:/handle/|hdl\.handle\.net/)(\d+/[^\s/\"}]+)")


def kennung_norm(art: str, wert: str) -> str:
    """Einheitliche Schreibweise, klein: `isbn:` nur Ziffern (und x), `hdl:` wie gedruckt."""
    art = art.lower()
    wert = wert.strip().rstrip(".,;:|)")
    if art == "isbn":
        return "isbn:" + re.sub(r"[^0-9Xx]", "", wert).lower()
    if art == "url":
        wert = re.sub(r"^https?://", "", wert, flags=re.IGNORECASE).rstrip("/")
    return f"{art}:{wert.lower()}"


def kennung_aus_zeile(line: str) -> str:
    """DOI oder Kennung (isbn:, hdl:) am Zeilenanfang; sonst leerer String."""
    doi = doi_aus_zeile(line)
    if doi:
        return doi
    m = _KENNUNG.match(line)
    return kennung_norm(m.group(1), m.group(2)) if m else ""


def kennung_zu_schluessel() -> dict[str, str]:
    """DOI oder Kennung (klein) -> Zitierschlüssel; aus doi=, isbn= und url= in literatur.bib."""
    out = doi_zu_schluessel()
    if not BIB.exists():
        return out
    for eintrag in re.split(r"(?=@\w+\s*\{)", BIB.read_text(encoding="utf-8")):
        k = re.match(r"@\w+\s*\{\s*([^,\s]+)", eintrag)
        if not k:
            continue
        isbn = re.search(r"(?i)\bisbn\s*=\s*[{\"]([^}\"]+)", eintrag)
        if isbn and re.search(r"\d", isbn.group(1)):
            out[kennung_norm("isbn", isbn.group(1))] = k.group(1)
        url = re.search(r"(?i)\burl\s*=\s*[{\"]([^}\"]+)", eintrag)
        if url:
            h = _HANDLE_IN_URL.search(url.group(1))
            if h:
                out[kennung_norm("hdl", h.group(1))] = k.group(1)
            out[kennung_norm("url", url.group(1).strip())] = k.group(1)
    return out


def bib_titel() -> dict[str, str]:
    """Zitierschlüssel → Titel aus literatur.bib."""
    if not BIB.exists():
        return {}
    out = {}
    for eintrag in re.split(r"(?=@\w+\s*\{)", BIB.read_text(encoding="utf-8")):
        k = re.match(r"@\w+\s*\{\s*([^,\s]+)", eintrag)
        t = re.search(r"\btitle\s*=\s*\{(.+?)\}\s*,\s*\w+\s*=", eintrag, re.S)
        if k and t:
            out[k.group(1)] = t.group(1)
    return out


def ablage_ordner(text: str) -> Path | None:
    """Der Ablageordner aus dem Kopf eines Protokolls: **Ablage:** `literatur/...`"""
    m = re.search(r"^\*\*Ablage:\*\*.*?(literatur/[^`)\]\s]+)", text, re.MULTILINE)
    return (REPO / m.group(1).rstrip("/")) if m else None


def vorhandene_volltexte() -> dict[str, Path]:
    """Schlüssel → Datei. Volltexte liegen in pdf/-Unterordnern; .xml zählt mit
    (JATS-Volltext, z. B. Salway2023)."""
    return {p.stem: p for endung in VOLLTEXT_ENDUNGEN
            for p in LITERATUR.glob(f"**/pdf/*{endung}")}


def ausgewertete() -> dict[str, Path]:
    """Schlüssel → Auswertungsdatei."""
    return {p.name[: -len("_auswertung.md")]: p
            for p in LITERATUR.glob("**/*_auswertung.md")}


def nicht_beschaffbar() -> tuple[dict[str, str], list[str]]:
    """Schlüssel → Grund aus notes/recherche/beschaffung.yaml, dazu Formfehler."""
    if not BESCHAFFUNG.exists():
        return {}, []
    import yaml  # type: ignore
    daten = yaml.safe_load(BESCHAFFUNG.read_text(encoding="utf-8")) or {}
    out, fehler = {}, []
    for e in daten.get("nicht_beschaffbar") or []:
        k = e.get("schluessel")
        if not k:
            fehler.append(f"Eintrag ohne `schluessel`: {e}")
        elif not e.get("grund"):
            fehler.append(f"`{k}`: kein `grund` — ohne Grund ist ‚nicht beschaffbar‘ nicht von ‚vergessen‘ zu unterscheiden")
        else:
            wann = f" ({e['versucht_am']})" if e.get("versucht_am") else ""
            out[k] = f"{e['grund']}{wann}"
    return out, fehler


def symbol(key: str | None, volltexte, fertig, gesperrt=()) -> str:
    if key and key in fertig:
        return AUSGEWERTET
    if key and key in volltexte:
        return PDF_DA
    if key and key in gesperrt:
        return NICHT_BESCHAFFBAR
    return FEHLT


def zeile_setzen(line: str, doi: str, zeichen: str) -> str:
    """Zeichen hinter die DOI setzen, in derselben Zelle.

    Bewusst keine eigene Tabellenspalte: Die Zeile beginnt weiterhin mit der
    DOI, tools/doi2bib.py und tools/holpdf.py lesen sie unverändert, und die
    Tabellenbreite bleibt, wie sie ist.
    """
    muster = re.compile(re.escape(doi) + r"(?:\s*(?:" + "|".join(map(re.escape, SYMBOLE)) + r"))?")
    return muster.sub(f"{doi} {zeichen}", line, count=1)


# ── Die Tabelle „Stand“ im Sammeldokument ──
STAND_START, STAND_ENDE = "<!-- stand:start -->", "<!-- stand:ende -->"
STAND_REIHENFOLGE = {AUSGEWERTET: 0, PDF_DA: 1, FEHLT: 2, NICHT_BESCHAFFBAR: 3}


def kennung_als_link(kennung: str) -> str:
    """DOI oder Kennung so, dass man sie anklicken oder kopieren kann."""
    if kennung.startswith("10."):
        return f"[{kennung}](https://doi.org/{kennung.replace('(', '%28').replace(')', '%29')})"
    art, _, wert = kennung.partition(":")
    if art == "hdl":
        return f"[{kennung}](https://hdl.handle.net/{wert})"
    if art == "url":
        return f"<https://{wert}>"
    return kennung


def stand_tabellen(keys, pdfs, fertig, gesperrt) -> dict[Path, str]:
    """Sammeldokument → Tabelle aller Arbeiten seiner Kategorie, aus den Protokollen mit Ablage."""
    titel = bib_titel()
    je_ordner: dict[Path, dict[str, tuple[str | None, str]]] = {}
    for pfad in sorted(RECHERCHE.glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        ordner = ablage_ordner(text)
        if ordner is None:
            continue
        for line in text.splitlines():
            kennung = kennung_aus_zeile(line)
            if kennung:
                key = keys.get(kennung.lower())
                je_ordner.setdefault(ordner, {}).setdefault(key or kennung.lower(), (key, kennung))
    out = {}
    for ordner, eintraege in je_ordner.items():
        zeilen = []
        for key, kennung in eintraege.values():
            z = symbol(key, pdfs, fertig, gesperrt)
            if key and key in fertig:
                arbeit = f"[{key}]({Path(os.path.relpath(fertig[key], ordner)).as_posix()})"
            else:
                arbeit = key or "noch nicht in literatur.bib"
            name = " ".join((titel.get(key or "", "")).split()).replace("|", "\\|")
            zeilen.append((STAND_REIHENFOLGE[z], (key or kennung).lower(),
                           f"| {z} | {arbeit} | {name} | {kennung_als_link(kennung)} |"))
        out[ordner / f"{ordner.name}.md"] = "\n".join(
            ["| | Arbeit | Titel | DOI |", "|---|---|---|---|"] + [z for *_, z in sorted(zeilen)])
    return out


def stand_setzen(text: str, tabelle: str) -> str:
    """Die Tabelle zwischen die Marken setzen; ohne Marken bleibt der Text, wie er ist."""
    a, e = text.find(STAND_START), text.find(STAND_ENDE)
    if a < 0 or e < a:
        return text
    return text[: a + len(STAND_START)] + "\n" + tabelle + "\n" + text[e:]


def datei_aktualisieren(pfad: Path, keys: dict[str, str], pdfs, fertig, gesperrt,
                        schreiben: bool) -> list[tuple[str, str]]:
    zeilen = pfad.read_text(encoding="utf-8").splitlines()
    bericht: list[tuple[str, str]] = []
    for i, line in enumerate(zeilen):
        doi = kennung_aus_zeile(line)
        if not doi:
            continue
        key = keys.get(doi.lower())
        z = symbol(key, pdfs, fertig, gesperrt)

        zeilen[i] = zeile_setzen(line, doi, z)
        bericht.append((key or doi, z))
    if schreiben:
        pfad.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    return bericht


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="nur berichten, nichts schreiben")
    args = ap.parse_args()

    keys, pdfs, fertig = kennung_zu_schluessel(), vorhandene_volltexte(), ausgewertete()
    gesperrt, _ = nicht_beschaffbar()
    gesamt = {FEHLT: 0, PDF_DA: 0, AUSGEWERTET: 0, NICHT_BESCHAFFBAR: 0}

    for pfad in sorted(RECHERCHE.glob("*.md")):
        bericht = datei_aktualisieren(pfad, keys, pdfs, fertig, gesperrt, schreiben=not args.check)
        if not bericht:
            continue
        print(f"\n{pfad.relative_to(REPO)}")
        for key, z in bericht:
            print(f"  {z}  {key}")
            gesamt[z] += 1

    for sammel, tabelle in stand_tabellen(keys, pdfs, fertig, gesperrt).items():
        if not sammel.exists():
            continue
        alt = sammel.read_text(encoding="utf-8")
        neu = stand_setzen(alt, tabelle)
        if neu != alt:
            print(f"\n{sammel.relative_to(REPO)}: Tabelle „Stand“ {'veraltet' if args.check else 'nachgezogen'}")
            if not args.check:
                sammel.write_text(neu, encoding="utf-8")

    print(f"\n{AUSGEWERTET} ausgewertet: {gesamt[AUSGEWERTET]}   "
          f"{PDF_DA} Volltext da: {gesamt[PDF_DA]}   {FEHLT} steht aus: {gesamt[FEHLT]}   "
          f"{NICHT_BESCHAFFBAR} nicht beschaffbar: {gesamt[NICHT_BESCHAFFBAR]}")
    if args.check:
        print("--check: nichts geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
