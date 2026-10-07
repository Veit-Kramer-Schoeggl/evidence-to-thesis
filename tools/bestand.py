#!/usr/bin/env python3
"""Bestandsprüfung: Protokolle, Volltexte, Auswertungen und Beschaffung.

Gleicht vier Quellen gegeneinander ab:

    notes/recherche/*.md            was wir haben wollen (DOI- oder Kennungszeilen, Ablageordner)
    literatur/**/pdf/*.pdf|.xml     was wir haben
    literatur/**/*_auswertung.md    was ausgewertet ist
    notes/recherche/beschaffung.yaml  was derzeit nicht beschaffbar ist, mit Grund

Wird von tools/pruefe.py vor jedem Commit aufgerufen, lässt sich aber auch
allein laufen lassen:

    python3 tools/bestand.py
    python3 tools/bestand.py --umbenennen   # fast richtig benannte Volltexte korrigieren


Fehler blockieren den Commit. Hinweise blockieren nicht, werden aber bei jedem
Lauf genannt — vor allem jeder Volltext, der noch aussteht, getrennt von denen,
die ausdrücklich als nicht beschaffbar vermerkt sind. So ist immer klar, warum
etwas fehlt.

Volltexte sind nicht versioniert. Auf einem Rechner ohne Volltexte ist
„laut Protokoll vorhanden, hier nicht" deshalb nur ein Hinweis, kein Fehler.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LITERATUR = REPO / "literatur"
RECHERCHE = REPO / "notes" / "recherche"
BESCHAFFUNG = RECHERCHE / "beschaffung.yaml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from status import (AUSGEWERTET, FEHLT, NICHT_BESCHAFFBAR, PDF_DA, VOLLTEXT_ENDUNGEN,  # noqa: E402
                    ausgewertete, kennung_aus_zeile, kennung_zu_schluessel,
                    nicht_beschaffbar, symbol, vorhandene_volltexte)


@dataclass
class Zeile:
    protokoll: Path
    doi: str
    schluessel: str | None
    zeichen: str | None            # das Zeichen, das gerade hinter der DOI steht


@dataclass
class Befund:
    fehler: list[tuple[str, str]] = field(default_factory=list)
    umbenennen: list[tuple[Path, Path]] = field(default_factory=list)
    steht_aus: dict[str, list[str]] = field(default_factory=dict)
    nicht_beschaffbar: list[str] = field(default_factory=list)
    anderswo: list[str] = field(default_factory=list)
    hinweise: list[str] = field(default_factory=list)

    def fehlt(self, wo: str, was: str) -> None:
        self.fehler.append((wo, was))


def grob(name: str) -> str:
    """Für den Abgleich fast richtiger Dateinamen: ohne Akzente, Groß-/Kleinschreibung,
    Leer- und Sonderzeichen. „Mañas2022", „Saint-Maurice2020", „Paluch 2021" →
    manas2022, saintmaurice2020, paluch2021."""
    ohne = unicodedata.normalize("NFKD", name)
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in ohne if not unicodedata.combining(c)).lower())


def grober(name: str) -> str:
    """Zusätzlich die deutsche Umschrift einebnen: „Hoechsmann" und „Höchsmann"
    (Schlüssel „Hochsmann") landen beide bei „hochsmann"."""
    return re.sub(r"([aou])e", r"\1", grob(name))


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def ablage(protokoll: Path, text: str) -> Path | None:
    """Der Ablageordner steht im Kopf: **Ablage:** `literatur/...`"""
    m = re.search(r"^\*\*Ablage:\*\*.*?(literatur/[^`)\]\s]+)", text, re.MULTILINE)
    return (REPO / m.group(1).rstrip("/")) if m else None


def zeilen_lesen(protokoll: Path, keys: dict[str, str]) -> list[Zeile]:
    out = []
    for z in protokoll.read_text(encoding="utf-8").splitlines():
        doi = kennung_aus_zeile(z)          # DOI oder hdl:/isbn:
        if not doi:
            continue
        rest = z[z.find(doi) + len(doi):].lstrip()
        zeichen = next((s for s in (FEHLT, PDF_DA, AUSGEWERTET, NICHT_BESCHAFFBAR)
                        if rest.startswith(s)), None)
        out.append(Zeile(protokoll, doi, keys.get(doi.lower()), zeichen))
    return out


# ── Inhalt gegen Titel ──
# Anlass aus der Praxis: Unter einem richtig benannten PDF lag mehrmals eine andere
# Arbeit — der Dateiname stimmte, der Inhalt nicht.

def bib_titel() -> dict[str, str]:
    """Zitierschlüssel → Titel aus literatur.bib."""
    bib = REPO / "literatur.bib"
    if not bib.exists():
        return {}
    out = {}
    for eintrag in re.split(r"(?=@\w+\s*\{)", bib.read_text(encoding="utf-8")):
        k = re.match(r"@\w+\s*\{\s*([^,\s]+)", eintrag)
        t = re.search(r"\btitle\s*=\s*\{(.+?)\}\s*,\s*\w+\s*=", eintrag, re.S)
        if k and t:
            out[k.group(1)] = t.group(1)
    return out


def woerter(text: str) -> list[str]:
    """Kleinbuchstaben ohne Akzente, Silbentrennung am Zeilenende aufgehoben."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.findall(r"[a-z0-9]+", text)


def laengster_lauf(titel: list[str], text: list[str]) -> int:
    """Längste Folge von Titelwörtern, die im Text genauso zusammenhängend steht."""
    stellen: dict[str, list[int]] = {}
    for i, w in enumerate(text):
        stellen.setdefault(w, []).append(i)
    best = 0
    for s in range(len(titel)):
        for j in stellen.get(titel[s], ()):
            n = 0
            while s + n < len(titel) and j + n < len(text) and titel[s + n] == text[j + n]:
                n += 1
            best = max(best, n)
    return best


def titel_passt(titel: str, text: str) -> bool:
    """Mindestens sechs Titelwörter am Stück, bei kurzen Titeln die Hälfte.

    Die Schwelle hat sich in der Praxis bewährt: Richtige Volltexte erreichen
    sieben und mehr Wörter am Stück, falsch abgelegte deutlich weniger.
    """
    tw = woerter(titel)
    if not tw:
        return True
    return laengster_lauf(tw, woerter(text)) >= min(6, -(-len(tw) // 2))


def pdf_text(datei: Path, seiten: int = 2) -> str | None:
    """Text der ersten Seiten; None, wenn pdftotext fehlt."""
    import subprocess
    try:
        r = subprocess.run(["pdftotext", "-l", str(seiten), str(datei), "-"],
                           capture_output=True, text=True, timeout=30)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return r.stdout


# Zweite Stufe: Einmal lag eine andere Arbeit unter dem richtigen Namen, deren Titel
# mit denselben sieben Wörtern begann. Die Titelprüfung ließ sie durch, die DOI
# nicht. Richtige Volltexte tragen ihre DOI oder gar keine.
DOI_MUSTER = re.compile(r"10\.\d{4,9}/[^\s\"<>]+")


def doi_norm(s: str) -> str:
    """Nur Kleinbuchstaben und Ziffern — übersteht Zeilenumbrüche und
    verlorene Trennstriche („bjsports-2018-\n100493")."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def fremde_doi(doi: str, text: str) -> str | None:
    """Die erste DOI im Text, wenn der Text DOIs trägt, aber nicht die eigene;
    sonst None (eigene gefunden, oder gar keine DOI im Text)."""
    if doi_norm(doi) in doi_norm(text):
        return None
    m = DOI_MUSTER.search(text)
    return m.group(0).rstrip(".,;)") if m else None


def pruefe_inhalt(datei: Path, titel: str | None, b: "Befund", doi: str | None = None) -> None:
    """Steht im Volltext wirklich die Arbeit, deren Schlüssel er trägt?"""
    if not (titel or doi) or datei.suffix.lower() != ".pdf":
        return
    text = pdf_text(datei)
    if text is None:
        if not any("pdftotext" in h for h in b.hinweise):
            b.hinweise.append("pdftotext fehlt — Inhalt der Volltexte nicht gegen die Titel geprüft")
        return
    if len(text.strip()) < 300:
        # Ein Umschlag ohne Text (Berichte, Bücher — der WHO-Weltbericht 2015
        # trägt auf Seite 1 sechs Wörter): weiter hinten nachsehen, bevor die
        # Datei als Scan gilt. Ein echter Scan bleibt auch auf sechs Seiten leer.
        text = pdf_text(datei, seiten=6) or text
    # Ein Scan mit bloßer Kopfzeile je Seite (Fries 1980 als Faksimile im
    # WHO-Bulletin) hat Zeichen, aber kaum Wörter — deshalb Wörter zählen.
    if len(woerter(text)) < 150:
        b.hinweise.append(f"{rel(datei)}: ohne Textebene (Scan?) — Titel nicht prüfbar, von Hand ansehen")
        return
    if doi and (fremd := fremde_doi(doi, text)):
        b.fehlt(rel(datei), f"trägt die DOI {fremd}, nicht {doi} aus literatur.bib — "
                            f"liegt unter diesem Namen eine andere Arbeit?")
        return
    if titel and not titel_passt(titel, text):
        kurz = titel if len(titel) <= 90 else titel[:87] + "…"
        b.fehlt(rel(datei), f"Inhalt passt nicht zum Titel in literatur.bib („{kurz}“) — "
                            f"liegt unter diesem Namen eine andere Arbeit?")


def pruefe_bestand() -> Befund:
    b = Befund()
    keys = kennung_zu_schluessel()
    bib_keys = set(keys.values())
    volltexte = vorhandene_volltexte()           # Schlüssel → Pfad
    titel = bib_titel()
    # nur echte DOIs — die Inhaltsprüfung sucht sie im Volltext; hdl:, isbn:, url: nicht
    doi_je_key = {v: d for d, v in keys.items() if d.startswith("10.")}
    fertig = ausgewertete()                       # Schlüssel → Pfad
    gesperrt, register_fehler = nicht_beschaffbar()
    for was in register_fehler:
        b.fehlt(rel(BESCHAFFUNG), was)

    # ── Protokolle lesen ────────────────────────────────────────────────
    ordner_je_key: dict[str, set[Path]] = {}      # nur aus Protokollen mit Ablage
    in_protokoll: set[str] = set()                 # aus allen Protokollen
    alle_zeilen: list[Zeile] = []
    for p in sorted(RECHERCHE.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        zeilen = zeilen_lesen(p, keys)
        if not zeilen:
            continue
        ordner = ablage(p, text)
        if ordner is None:
            b.fehlt(rel(p), "Kopf ohne `**Ablage:** literatur/…` — wohin gehören die Volltexte?")
        elif not ordner.is_dir():
            b.fehlt(rel(p), f"Ablageordner {rel(ordner)} existiert nicht")
        for z in zeilen:
            alle_zeilen.append(z)
            if z.schluessel is None:
                b.fehlt(rel(p), f"DOI {z.doi} ohne Bibliografieeintrag — "
                                f"`python3 tools/doi2bib.py {z.doi}`, dann den Titel prüfen")
            else:
                in_protokoll.add(z.schluessel)
                if ordner is not None:
                    ordner_je_key.setdefault(z.schluessel, set()).add(ordner)

    # ── Volltexte: richtig benannt, eingetragen, am richtigen Ort ───────
    for datei in sorted(LITERATUR.glob("**/*")):
        if not datei.is_file() or datei.suffix.lower() == ".md":
            continue
        # Erzeugte Abbildungen der Sammeldokumente: nur in abb/, nur Bildformate
        if datei.parent.name == "abb" and datei.suffix.lower() in (".png", ".svg"):
            continue
        if datei.suffix.lower() not in VOLLTEXT_ENDUNGEN:
            b.fehlt(rel(datei), f"unerwarteter Dateityp ‚{datei.suffix}‘ — Volltexte als "
                                f"{', '.join(VOLLTEXT_ENDUNGEN)} in pdf/, Abbildungen als .png/.svg in abb/, sonst nur Markdown")
            continue
        if datei.parent.name != "pdf":
            b.fehlt(rel(datei), "Volltext gehört in den Unterordner pdf/")
            continue
        k = datei.stem
        if k not in bib_keys:
            gemeint = ([x for x in bib_keys if grob(x) == grob(k)]
                       or [x for x in bib_keys if grober(x) == grober(k)])
            if len(gemeint) == 1:
                ziel = datei.with_name(gemeint[0] + datei.suffix)
                b.umbenennen.append((datei, ziel))
                b.fehlt(rel(datei), f"fast richtig benannt — gemeint ist `{gemeint[0]}`; "
                                    f"`python3 tools/bestand.py --umbenennen`")
            else:
                b.fehlt(rel(datei), "Dateiname ist kein Zitierschlüssel aus literatur.bib — "
                                    "falsch benannt oder nicht eingetragen")
        elif k not in in_protokoll:
            b.fehlt(rel(datei), "Volltext steht in keinem Rechercheprotokoll")
        elif k in ordner_je_key and datei.parent.parent not in ordner_je_key[k]:
            soll = ", ".join(rel(o) + "/pdf/" for o in sorted(ordner_je_key[k]))
            b.fehlt(rel(datei), f"liegt im falschen Ordner — laut Protokoll gehört er nach {soll}")
        if k in bib_keys:
            pruefe_inhalt(datei, titel.get(k), b, doi_je_key.get(k))

    # ── Auswertungen: eingetragen und am richtigen Ort ──────────────────
    for k, pfad in sorted(fertig.items()):
        if k not in in_protokoll:
            b.fehlt(rel(pfad), "Auswertung zu einer Arbeit, die in keinem Rechercheprotokoll steht")
        elif k in ordner_je_key and pfad.parent not in ordner_je_key[k]:
            b.fehlt(rel(pfad), "Auswertung liegt nicht im Ablageordner ihres Protokolls")

    # ── Beschaffungsregister gegen den Bestand ──────────────────────────
    for k, grund in gesperrt.items():
        if k in volltexte:
            b.fehlt(rel(BESCHAFFUNG), f"`{k}` ist als nicht beschaffbar vermerkt, "
                                      f"der Volltext liegt aber vor — Eintrag entfernen")
        if k not in in_protokoll:
            b.fehlt(rel(BESCHAFFUNG), f"`{k}` steht in keinem Rechercheprotokoll")

    # ── Statuszeichen in den Protokollen, und was fehlt ─────────────────
    gesehen: set[str] = set()
    for z in alle_zeilen:
        k = z.schluessel
        soll = symbol(k, volltexte, fertig, gesperrt)
        ist = z.zeichen
        wo = rel(z.protokoll)
        # Auswertungen sind versioniert: dort streng in beide Richtungen.
        # Volltexte nicht: „📄, aber hier nicht vorhanden" ist nur ein Hinweis.
        if ist == PDF_DA and soll in (FEHLT, NICHT_BESCHAFFBAR):
            b.anderswo.append(f"{k}  ({wo})")
        elif ist != soll:
            b.fehlt(wo, f"{k or z.doi}: Zeichen „{ist or 'keins'}\", richtig wäre „{soll}\" — "
                        f"`python3 tools/status.py`")
        if k is None or k in gesehen:
            continue
        gesehen.add(k)
        if k in gesperrt:
            b.nicht_beschaffbar.append(f"{k}: {gesperrt[k]}")
        elif k not in volltexte and k not in fertig:
            b.steht_aus.setdefault(z.protokoll.stem, []).append(k)
    return b


def ausgeben(b: Befund, datei=sys.stdout) -> None:
    if b.steht_aus:
        n = sum(len(v) for v in b.steht_aus.values())
        print(f"\n· {n} Volltext(e) stehen aus:", file=datei)
        for prot, ks in b.steht_aus.items():
            print(f"      {prot}: {', '.join(ks)}", file=datei)
    if b.nicht_beschaffbar:
        print(f"\n⛔ {len(b.nicht_beschaffbar)} derzeit nicht beschaffbar:", file=datei)
        for z in b.nicht_beschaffbar:
            print(f"      {z}", file=datei)
    if b.hinweise:
        print(f"\n△ {len(b.hinweise)} Hinweis(e) zum Inhalt der Volltexte:", file=datei)
        for z in b.hinweise:
            print(f"      {z}", file=datei)
    if b.anderswo:
        print(f"\n○ {len(b.anderswo)} laut Protokoll vorhanden, auf diesem Rechner nicht "
              f"(Volltexte getrennt übertragen):", file=datei)
        for z in b.anderswo:
            print(f"      {z}", file=datei)


if __name__ == "__main__":
    befund = pruefe_bestand()
    if "--umbenennen" in sys.argv:
        for alt, neu in befund.umbenennen:
            if neu.exists():
                print(f"✗ {rel(neu)} gibt es schon — {rel(alt)} bleibt, bitte von Hand klären")
                continue
            alt.rename(neu)
            print(f"✓ {rel(alt)} → {neu.name}")
        befund = pruefe_bestand()
    for wo, was in befund.fehler:
        print(f"✗ {wo}\n      {was}", file=sys.stderr)
    ausgeben(befund)
    sys.exit(1 if befund.fehler else 0)
