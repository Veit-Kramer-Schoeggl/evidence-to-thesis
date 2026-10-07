#!/usr/bin/env python3
"""Tote Verweise in allen Markdown-Dateien finden.

Geprüft wird jeder relative Link `[Text](pfad)`, jedes Bild `![…](pfad)` und
jeder HTML-Link `<a href="pfad">`,
auch Links ab dem Hauptordner (`/pfad`, so lesen GitHub und VS Code sie):
Gibt es die Datei, und — bei `pfad#anker` oder `#anker` — gibt es in der
Zieldatei eine Überschrift oder ein `<a id>` mit diesem Anker? Anker werden
gebildet wie auf GitHub (Kleinschreibung, Satzzeichen weg, Leerzeichen zu
Bindestrichen, Dubletten mit -1, -2 …).

Nicht geprüft: Links nach außen (http, mailto), alles in Codeblöcken oder
Inline-Code, der Ordner vorlagen/ (Platzhalter) und fehlende Ziele in einem
pdf/-Ordner, weil Volltexte nicht versioniert sind.

    python3 tools/verweise.py         # Liste der toten Verweise

Eingebunden in tools/pruefe.py, läuft also vor jedem Commit. Anlass aus der
Praxis: Ein Skript setzte in vielen Auswertungsköpfen einen kaputten Link, und
nur ein Linktest fand ihn.
"""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUSGENOMMEN = {".git", "node_modules", "__pycache__", "vorlagen"}   # Vorlagen enthalten Platzhalter

LINK = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
ANKER_ID = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"")
HTML_LINK = re.compile(r"<a\s+[^>]*href=\"([^\"]+)\"", re.I)   # etwa im klickbaren Ordnerbaum (<pre>)


def ohne_code(text: str) -> str:
    """Codeblöcke und Inline-Code durch Leerzeilen/Leerraum ersetzen (Zeilen bleiben erhalten)."""
    zeilen, im_block = [], False
    for z in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", z):
            im_block = not im_block
            zeilen.append("")
            continue
        zeilen.append("" if im_block else re.sub(r"`[^`]*`", "", z))
    return "\n".join(zeilen)


def slug(ueberschrift: str) -> str:
    """Anker einer Überschrift wie auf GitHub."""
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", ueberschrift)   # Links → Text
    t = t.replace("`", "").replace("*", "").strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def anker(text: str) -> set[str]:
    gefunden: set[str] = set()
    zaehler: dict[str, int] = {}
    for z in ohne_code(text).split("\n"):
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", z)
        if m:
            s = slug(m.group(1))
            n = zaehler.get(s, 0)
            gefunden.add(s if n == 0 else f"{s}-{n}")
            zaehler[s] = n + 1
    gefunden.update(ANKER_ID.findall(text))
    return gefunden


def md_dateien(wurzel: Path) -> list[Path]:
    return sorted(p for p in wurzel.rglob("*.md") if not AUSGENOMMEN & set(p.relative_to(wurzel).parts))


def pruefen(wurzel: Path = REPO) -> list[tuple[str, str]]:
    """Alle toten Verweise als (Datei, Meldung)."""
    fehler: list[tuple[str, str]] = []
    anker_cache: dict[Path, set[str]] = {}

    def anker_von(p: Path) -> set[str]:
        if p not in anker_cache:
            anker_cache[p] = anker(p.read_text(encoding="utf-8"))
        return anker_cache[p]

    for md in md_dateien(wurzel):
        text = md.read_text(encoding="utf-8")
        wo = str(md.relative_to(wurzel))
        for nr, zeile in enumerate(ohne_code(text).split("\n"), 1):
            for ziel in [m.group(1) for m in LINK.finditer(zeile)] + HTML_LINK.findall(zeile):
                if re.match(r"^[a-z][a-z0-9+.-]*:", ziel, re.I):   # http:, mailto: …
                    continue
                pfad, _, frag = ziel.partition("#")
                pfad = urllib.parse.unquote(pfad)
                if pfad.startswith("/"):                  # ab dem Hauptordner, wie auf GitHub
                    datei = (wurzel / pfad.lstrip("/")).resolve()
                else:
                    datei = (md.parent / pfad).resolve() if pfad else md
                try:
                    datei.relative_to(wurzel.resolve())
                except ValueError:
                    fehler.append((wo, f"Zeile {nr}: „{ziel}“ zeigt aus dem Repository hinaus"))
                    continue
                if not datei.exists():
                    if "pdf" in Path(pfad).parts:      # Volltexte sind nicht versioniert
                        continue
                    fehler.append((wo, f"Zeile {nr}: „{ziel}“ — Datei gibt es nicht"))
                    continue
                if frag and datei.suffix == ".md":
                    frag = urllib.parse.unquote(frag)
                    if frag not in anker_von(datei):
                        fehler.append((wo, f"Zeile {nr}: Anker „#{frag}“ fehlt in {datei.relative_to(wurzel.resolve())}"))
    return fehler


def main() -> int:
    fehler = pruefen()
    for wo, was in fehler:
        print(f"{wo}: {was}")
    print(f"{len(fehler)} tote(r) Verweis(e).")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
