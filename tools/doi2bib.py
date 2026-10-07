#!/usr/bin/env python3
"""DOIs zu BibTeX-Einträgen für literatur.bib.

Holt die Metadaten über die offizielle DOI-Content-Negotiation
(https://doi.org mit Accept: application/x-bibtex), vergibt einen
einheitlichen Zitierschlüssel (NachnameJahr) und hängt neue Einträge an
die gemeinsame Bibliografie an. Vorhandene Schlüssel und DOIs werden
übersprungen, nichts wird überschrieben.

    python3 tools/doi2bib.py 10.1000/182 10.1000/183
    python3 tools/doi2bib.py --file dois.txt
    python3 tools/doi2bib.py --file dois.txt --dry-run

In der Datei steht eine DOI je Zeile, jeweils am Zeilenanfang. Listen- und
Tabellenzeichen davor sind erlaubt, der Rest der Zeile ist frei. So lässt sich
dieselbe Datei als schlichte Liste oder als Markdown-Tabelle führen. Zeilen,
die nicht mit einer DOI beginnen, werden übergangen - eine DOI, die nur in
einer Anmerkung erwähnt wird, kommt also nicht versehentlich mit.

Die Metadaten der Verlage sind nicht immer sauber. Jeder neue Eintrag ist
gegen die Quelle zu prüfen, bevor er zitiert wird (README, Abschnitt „Regeln“).

Optional: THESIS_KONTAKT (etwa die URL des eigenen GitHub-Profils) wird als
Kontakt in der Kennung der Abfragen mitgeschickt. Eine E-Mail-Adresse braucht
dieses Werkzeug nicht.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIB = REPO / "literatur.bib"
# Kennung der Abfragen, ohne E-Mail-Adresse: Der „polite pool" von Crossref bringt bei
# den wenigen Abfragen einer Abschlussarbeit keinen messbaren Vorteil.
KONTAKT = os.environ.get("THESIS_KONTAKT", "").strip()
UA = f"evidence-to-thesis/1.0 ({KONTAKT})" if KONTAKT else "evidence-to-thesis/1.0"


def fetch_bibtex(doi: str, timeout: int = 30) -> str:
    """Rohen BibTeX-Eintrag für eine DOI holen."""
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/:()<>-._")
    req = urllib.request.Request(
        url, headers={"Accept": "application/x-bibtex; charset=utf-8", "User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8").strip()


def field(entry: str, name: str) -> str:
    """Ein Feld aus einem BibTeX-Eintrag lesen, geschweifte Klammern zählend."""
    m = re.search(rf"\b{name}\s*=\s*", entry, re.IGNORECASE)
    if not m:
        return ""
    i = m.end()
    if i < len(entry) and entry[i] == "{":
        depth, out = 0, []
        for ch in entry[i:]:
            if ch == "{":
                depth += 1
                if depth == 1:
                    continue
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            out.append(ch)
        return "".join(out).strip()
    m2 = re.match(r'"([^"]*)"|([^,\n}]*)', entry[i:])
    return (m2.group(1) or m2.group(2) or "").strip() if m2 else ""


# Zeichen, die sich nicht in Grundbuchstabe plus Akzent zerlegen lassen
_SONDERZEICHEN = str.maketrans({
    "ø": "o", "Ø": "O", "æ": "ae", "Æ": "Ae", "œ": "oe", "Œ": "Oe",
    "ß": "ss", "đ": "d", "Đ": "D", "ł": "l", "Ł": "L", "ı": "i", "ð": "d", "þ": "th",
})


def first_surname(authors: str) -> str:
    """Nachnamen der erstgenannten Person bestimmen, als ASCII-Schlüsselteil.

    Akzente werden transliteriert, nicht verworfen: aus Rodríguez-Gutiérrez
    wird RodriguezGutierrez, nicht Rodrguezgutirrez.
    """
    first = re.split(r"\s+and\s+", authors.strip())[0] if authors.strip() else ""
    if not first:
        return "Anon"
    surname = first.split(",")[0] if "," in first else first.split()[-1]
    surname = re.sub(r"\\[a-zA-Z]+\s*", "", surname)          # TeX-Makros
    surname = surname.translate(_SONDERZEICHEN)
    surname = unicodedata.normalize("NFKD", surname)           # é -> e + Akzent
    surname = "".join(c for c in surname if not unicodedata.combining(c))
    roh = [t for t in re.split(r"[-\s']+", surname) if t]
    # Führende Initialen verwerfen: manche Verlage schreiben "H.K. Montoye,
    # Alexander" statt "Montoye, Alexander H.K.". Initialen erkennt man an
    # durchgehender Großschreibung bei höchstens drei Buchstaben - Namensteile
    # wie "van", "del" oder "de" sind kleingeschrieben und bleiben erhalten.
    initial = re.compile(r"^(?:[A-Z]\.?){1,3}$")
    while len(roh) > 1 and initial.match(roh[0]):
        roh.pop(0)
    teile = [re.sub(r"[^A-Za-z]", "", t) for t in roh]
    return "".join(t.capitalize() for t in teile if t) or "Anon"


def make_key(entry: str, taken: set[str]) -> str:
    """Zitierschlüssel NachnameJahr vergeben, bei Kollision mit Suffix."""
    year = re.sub(r"\D", "", field(entry, "year"))[:4] or "0000"
    base = f"{first_surname(field(entry, 'author'))}{year}"
    if base not in taken:
        return base
    for suffix in "abcdefghijklmnopqrstuvwxyz":
        if f"{base}{suffix}" not in taken:
            return f"{base}{suffix}"
    raise RuntimeError(f"Zu viele Kollisionen für {base}")


def rekey(entry: str, key: str) -> str:
    return re.sub(r"^(@\w+\s*\{)[^,]*", lambda m: m.group(1) + key, entry, count=1)


# Eine Zeile steuert nur dann eine DOI bei, wenn sie MIT der DOI beginnt -
# nach optionalen Listen- oder Tabellenzeichen. Damit funktionieren einfache
# Listen ebenso wie Markdown-Tabellen, während DOIs, die bloß im Fließtext
# einer Anmerkung vorkommen, nicht versehentlich mitgelesen werden.
_ZEILENANFANG = re.compile(
    r"^[\s|\-*+>]*(?:https?://(?:dx\.)?doi\.org/|doi:)?(10\.\d{4,9}/\S+)",
    re.IGNORECASE,
)


def doi_aus_zeile(line: str) -> str:
    """DOI am Anfang einer Zeile herauslösen, sonst leerer String."""
    m = _ZEILENANFANG.match(line)
    if not m:
        return ""
    return m.group(1).rstrip(".,;:|)")


def read_dois(args: argparse.Namespace) -> list[str]:
    raw: list[str] = list(args.dois)
    if args.file:
        raw += Path(args.file).read_text(encoding="utf-8").splitlines()
    out, seen = [], set()
    for line in raw:
        doi = doi_aus_zeile(line)
        if doi and doi.lower() not in seen:
            seen.add(doi.lower())
            out.append(doi)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="*", help="DOIs, durch Leerzeichen getrennt")
    ap.add_argument("--file", help="Datei mit einer DOI je Zeile")
    ap.add_argument("--out", default=str(BIB), help=f"Zieldatei (Vorgabe: {BIB})")
    ap.add_argument("--dry-run", action="store_true", help="nur anzeigen, nichts schreiben")
    args = ap.parse_args()

    dois = read_dois(args)
    if not dois:
        ap.error("keine DOIs angegeben")

    out_path = Path(args.out)
    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    taken = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", existing))
    have_dois = {d.lower() for d in re.findall(r"(?i)\bdoi\s*=\s*[{\"]([^}\"]+)", existing)}

    added, skipped, failed = [], [], []
    for doi in dois:
        if doi.lower() in have_dois:
            skipped.append((doi, "DOI steht bereits in der Datei"))
            continue
        try:
            entry = fetch_bibtex(doi)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            failed.append((doi, str(exc)))
            continue
        if not entry.startswith("@"):
            failed.append((doi, "keine BibTeX-Antwort erhalten"))
            continue
        key = make_key(entry, taken)
        taken.add(key)
        have_dois.add(doi.lower())
        added.append((doi, key, rekey(entry, key), field(entry, "title")))
        time.sleep(0.5)  # höflich gegenüber dem Dienst

    for doi, key, _, title in added:
        print(f"  neu       {key:<20} {title[:60]}")
    for doi, why in skipped:
        print(f"  übersprungen {doi}  ({why})")
    for doi, why in failed:
        print(f"  FEHLER    {doi}  ({why})", file=sys.stderr)

    if added and not args.dry_run:
        with out_path.open("a", encoding="utf-8") as fh:
            for _, _, entry, _ in added:
                fh.write("\n" + entry + "\n")
        print(f"\n{len(added)} Eintrag/Einträge an {out_path} angehängt.")
        print("Bitte gegen die Quelle prüfen, bevor zitiert wird (README, „Regeln“).")
    elif args.dry_run:
        print("\n--dry-run: nichts geschrieben.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
