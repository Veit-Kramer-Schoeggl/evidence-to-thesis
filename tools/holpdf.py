#!/usr/bin/env python3
"""Frei verfügbare Volltexte zu DOIs herunterladen.

Fragt Unpaywall, ob zu einer DOI eine legale Open-Access-Fassung existiert,
und lädt sie nach literatur/<kategorie>/pdf/<Zitierschlüssel>.pdf. Der Schlüssel
wird aus literatur.bib gelesen, damit PDF, Bibliografieeintrag und
Auswertung denselben Namen tragen.

    python3 tools/holpdf.py --kategorie <kategorie> --file notes/recherche/<protokoll>.md
    python3 tools/holpdf.py --kategorie <kategorie> 10.1000/182
    python3 tools/holpdf.py --kategorie <kategorie> --file ... --dry-run

Was hinter einer Bezahlschranke liegt, wird NICHT beschafft, sondern am Ende
aufgelistet. Diese Volltexte holst du über den Zugang deiner Hochschulbibliothek.

Unpaywall verlangt eine E-Mail-Adresse. Sie kommt aus der Umgebungsvariable
UNPAYWALL_EMAIL und geht nur an Unpaywall, nicht an Verlage oder Repositorien:

    export UNPAYWALL_EMAIL=deine@adresse
"""

from __future__ import annotations

import argparse
import os
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIB = REPO / "literatur.bib"
LITERATUR = REPO / "literatur"
MAIL = os.environ.get("UNPAYWALL_EMAIL", "").strip()   # nur für die Anfrage bei Unpaywall
KONTAKT = os.environ.get("THESIS_KONTAKT", "").strip()
UA = f"evidence-to-thesis/1.0 ({KONTAKT})" if KONTAKT else "evidence-to-thesis/1.0"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doi2bib import doi_aus_zeile  # noqa: E402  gleiche Zeilenerkennung wie dort


def bib_schluessel() -> dict[str, str]:
    """DOI (klein) -> Zitierschlüssel aus literatur.bib."""
    if not BIB.exists():
        return {}
    text = BIB.read_text(encoding="utf-8")
    out = {}
    for eintrag in re.split(r"(?=@\w+\s*\{)", text):
        m_key = re.match(r"@\w+\s*\{\s*([^,\s]+)", eintrag)
        m_doi = re.search(r"(?i)\bdoi\s*=\s*[{\"]([^}\"]+)", eintrag)
        if m_key and m_doi:
            out[m_doi.group(1).strip().lower()] = m_key.group(1)
    return out


def unpaywall(doi: str, timeout: int = 25) -> dict:
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAIL}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def kandidaten(info: dict) -> list[tuple[str, str]]:
    """Alle Open-Access-Fundorte, Repositorien zuerst.

    Verlagsseiten wehren automatisierte Zugriffe oft mit 403 ab, obwohl der
    Artikel frei ist. PubMed Central und institutionelle Repositorien geben
    dieselbe Fassung ohne Hürde heraus, deshalb stehen sie vorn.
    """
    orte = list(info.get("oa_locations") or [])
    best = info.get("best_oa_location")
    if best and best not in orte:
        orte.insert(0, best)
    rang = {"repository": 0, "publisher": 1}
    orte.sort(key=lambda o: rang.get(o.get("host_type"), 2))
    out: list[tuple[str, str]] = []
    for o in orte:
        host = o.get("host_type", "?")
        for u in (o.get("url_for_pdf"), o.get("url")):
            if u and not any(u == v for v, _ in out):
                out.append((u, host))
    return out


def europepmc(doi: str, timeout: int = 25) -> list[tuple[str, str]]:
    """Fundorte über Europe PMC, das maschinellen Zugriff ausdrücklich erlaubt.

    Viele frei verfügbare Artikel sind beim Verlag mit 403 geschützt, liegen
    aber in PubMed Central. Europe PMC liefert dieselbe Fassung über eine
    dokumentierte Schnittstelle.
    """
    q = urllib.parse.urlencode({"query": f'DOI:"{doi}"', "format": "json", "pageSize": 1})
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{q}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            treffer = json.load(resp)["resultList"]["result"]
    except Exception:
        return []
    if not treffer:
        return []
    t = treffer[0]
    out = []
    if t.get("pmcid"):
        out.append((f"https://www.ebi.ac.uk/europepmc/webservices/rest/{t['pmcid']}/fullTextPDF", "europepmc"))
        out.append((f"https://pmc.ncbi.nlm.nih.gov/articles/{t['pmcid']}/pdf/", "pmc"))
    return out


def lade(url: str, ziel: Path, timeout: int = 60) -> tuple[bool, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            daten = resp.read()
    except Exception as exc:  # Netzfehler, 403, Weiterleitung ins Nirgendwo
        return False, str(exc)
    if not daten.startswith(b"%PDF"):
        return False, f"Antwort ist kein PDF ({len(daten)} Bytes, beginnt mit {daten[:16]!r})"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(daten)
    return True, f"{len(daten) // 1024} kB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="*")
    ap.add_argument("--file", help="Datei mit DOIs am Zeilenanfang (auch Markdown-Tabellen)")
    ap.add_argument("--kategorie", required=True,
                    help="Ordner unter literatur/, auch verschachtelt (z. B. thema/unterthema)")
    ap.add_argument("--dry-run", action="store_true", help="nur prüfen, nichts herunterladen")
    args = ap.parse_args()
    if not MAIL:
        sys.exit("Unpaywall verlangt eine E-Mail-Adresse:  export UNPAYWALL_EMAIL=deine@adresse\n"
                 "(sie geht nur an Unpaywall, nicht an Verlage oder Repositorien)")

    dois: list[str] = list(args.dois)
    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            d = doi_aus_zeile(line)
            if d:
                dois.append(d)
    dois = list(dict.fromkeys(d.lower() for d in dois))
    if not dois:
        ap.error("keine DOIs angegeben")

    keys = bib_schluessel()
    # Volltexte liegen in einem eigenen Unterordner pdf/, damit im Kategorieordner
    # nur die Auswertungen stehen.
    ziel_ordner = LITERATUR / args.kategorie / "pdf"
    geholt, vorhanden, zahlschranke, fehler = [], [], [], []

    for doi in dois:
        key = keys.get(doi)
        if not key:
            fehler.append((doi, "kein Eintrag in literatur.bib — erst doi2bib.py laufen lassen"))
            continue
        ziel = ziel_ordner / f"{key}.pdf"
        if ziel.exists():
            vorhanden.append((key, doi))
            continue
        try:
            info = unpaywall(doi)
        except Exception as exc:
            fehler.append((doi, f"Unpaywall nicht erreichbar: {exc}"))
            continue
        orte = kandidaten(info)
        if info.get("is_oa"):
            orte = europepmc(doi) + orte   # Repositorium vor Verlagsseite
        if not info.get("is_oa") or not orte:
            zahlschranke.append((key, doi, info.get("journal_name") or "?"))
            continue
        if args.dry_run:
            quellen = ", ".join(dict.fromkeys(h for _, h in orte))
            geholt.append((key, doi, f"verfügbar über {quellen}"))
            continue
        for pdf_url, host in orte:
            ok, meldung = lade(pdf_url, ziel)
            if ok:
                geholt.append((key, doi, f"{meldung} via {host}"))
                break
            letzte = meldung
            time.sleep(0.5)
        else:
            fehler.append((doi, f"alle {len(orte)} Fundorte fehlgeschlagen, zuletzt: {letzte}"))
        time.sleep(1.0)

    if geholt:
        print(f"\nHeruntergeladen nach literatur/{args.kategorie}/pdf/ ({len(geholt)}):")
        for key, _, info in geholt:
            print(f"  {key}.pdf   {info}")
    if vorhanden:
        print(f"\nSchon vorhanden ({len(vorhanden)}):")
        for key, _ in vorhanden:
            print(f"  {key}.pdf")
    if zahlschranke:
        print(f"\nHinter Bezahlschranke, über die FH-Bibliothek zu holen ({len(zahlschranke)}):")
        for key, doi, journal in zahlschranke:
            print(f"  {key:<24} {journal[:34]:<34} https://doi.org/{doi}")
        print(f"\n  Dateien bitte als literatur/{args.kategorie}/pdf/<Schlüssel>.pdf ablegen.")
    if fehler:
        print(f"\nFehler ({len(fehler)}):", file=sys.stderr)
        for doi, warum in fehler:
            print(f"  {doi}  {warum}", file=sys.stderr)
    if args.dry_run:
        print("\n--dry-run: nichts heruntergeladen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
