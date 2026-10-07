#!/usr/bin/env python3
"""Der Wächter: prüft vor jedem Commit, ob Auswertungen, Register und Bestand zusammenpassen.

    python3 tools/pruefe.py            # alles prüfen
    python3 tools/pruefe.py --leise    # nur Fehler ausgeben

Rückgabewert 0 heißt alles in Ordnung, 1 heißt mindestens ein Fehler. Der Hook
tools/hooks/pre-commit ruft dieses Skript und danach die Tests auf.

Geprüft wird:

  je Auswertung   Kopfzeile mit Status, Pflichtabschnitte, Prüfliste vollständig;
                  bei Status „geprüft" zusätzlich Zweck eingetragen, alle Punkte
                  abgehakt und die Auswertung im Sammeldokument unter „Was sich
                  abzeichnet" verlinkt
  Register        data/register.yaml (optional): jeder Eintrag mit Zitierschlüssel
                  in literatur.bib, Rückverweis auf eine bestehende Auswertung,
                  Fundstelle bei jedem Wert, Belastbarkeit aus festem Katalog
  Querverweis     jede ID in der `**Register:**`-Zeile einer Auswertung steht im
                  Register und zeigt auf genau diese Auswertung zurück
  Bestand         Protokolle, Volltexte, Auswertungen, Beschaffung (tools/bestand.py)
  Verweise        kein toter relativer Link in allen Markdown-Dateien (tools/verweise.py)

Ein Commit lässt sich im Notfall mit `git commit --no-verify` erzwingen. Das ist
dann eine bewusste Entscheidung, keine Unachtsamkeit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LITERATUR = REPO / "literatur"
REGISTER = REPO / "data" / "register.yaml"
BIB = REPO / "literatur.bib"

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Die Prüfliste, EINMAL festgelegt. Jede Auswertung führt jeden Punkt, erkannt am fett
# gesetzten Anfang. Wer hier einen Punkt ergänzt, bekommt vom Wächter jede Datei genannt,
# der er noch fehlt; so geht er in keinem einzelnen Kopf verloren.
PRUEFLISTE = [
    "Design und Qualität",
    "Exposition und Vergleich",
    "Endpunkte",
    "Ergebnisse",
    "Übertragung",
    "Verzerrung",
    "Belastbarkeit",
    "Vorbehalt",
    "Register",
    "Sammeldokument",
    "Aufgeworfene Fragen",
    "Zweck",
]
PFLICHTABSCHNITTE = [
    "Fragestellung",
    "Design und Qualität",
    "Ergebnisse",
    "Stärken",
    "Schwächen",
    "Was wir daraus nehmen",
]
STATUS = {"in Arbeit", "geprüft"}
BELASTBARKEIT = {"tragend", "eingeschränkt", "nicht belastbar"}


class Bericht:
    def __init__(self) -> None:
        self.fehler: list[tuple[str, str]] = []
        self.hinweise: list[str] = []
        self.geprueft = 0

    def fehlt(self, wo: str, was: str) -> None:
        self.fehler.append((wo, was))


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def bib_schluessel(bib: Path = BIB) -> set[str]:
    if not bib.exists():
        return set()
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib.read_text(encoding="utf-8")))


def register_laden(pfad: Path = REGISTER) -> list[dict]:
    if not pfad.exists():
        return []
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.exit("PyYAML fehlt:  pip install -r requirements.txt")
    daten = yaml.safe_load(pfad.read_text(encoding="utf-8")) or {}
    return list(daten.get("eintraege") or [])


def register_ids(text: str) -> list[str] | None:
    """IDs aus der Zeile `**Register:** `a` · `b``; None, wenn es keine solche Zeile gibt."""
    m = re.search(r"^>?\s*\*\*Register:\*\*(.*)$", text, re.MULTILINE)
    if not m:
        return None
    return re.findall(r"`([^`]+)`", m.group(1))


def pruefe_auswertung(pfad: Path, register: dict[str, dict], b: Bericht) -> None:
    wo = rel(pfad)
    text = pfad.read_text(encoding="utf-8")
    b.geprueft += 1

    # ── Kopfzeile ───────────────────────────────────────────────────────
    m_status = re.search(r"Status: \*\*([^*]+)\*\*", text)
    status = m_status.group(1).strip() if m_status else None
    if status not in STATUS:
        b.fehlt(wo, f"Kopfzeile braucht `Status: **in Arbeit**` oder `Status: **geprüft**` (gefunden: {status!r})")
    m_zweck = re.search(r"Zweck \*\*([^*]+)\*\*", text)
    if not m_zweck or m_zweck.group(1).strip().startswith("<"):
        if status == "geprüft":
            b.fehlt(wo, "Kopfzeile ohne ausgefüllten `Zweck **…**` (wofür wird die Arbeit gebraucht?)")
        else:
            b.hinweise.append(f"{wo}: Zweck noch nicht eingetragen")

    # ── Pflichtabschnitte ───────────────────────────────────────────────
    ueberschriften = [u.lower() for u in re.findall(r"^##+ +(.+?)\s*$", text, re.MULTILINE)]
    for pflicht in PFLICHTABSCHNITTE:
        if not any(pflicht.lower() in u for u in ueberschriften):
            b.fehlt(wo, f"Abschnitt „{pflicht}\" fehlt")

    # ── Prüfliste ───────────────────────────────────────────────────────
    kaestchen = re.findall(r"^- \[( |x|X)\] +(.+?)\s*$", text, re.MULTILINE)
    if not kaestchen:
        b.fehlt(wo, "keine Prüfliste im Kopf (Vorlage: vorlagen/auswertung.md)")
    else:
        vorhanden = {m.group(1) for m in (re.match(r"\*\*(.+?)\*\*", t) for _, t in kaestchen) if m}
        for punkt in PRUEFLISTE:
            if not any(v.startswith(punkt) for v in vorhanden):
                b.fehlt(wo, f"Prüflistenpunkt fehlt ganz: **{punkt}**")
        offen = [t for h, t in kaestchen if h == " "]
        if status == "geprüft":
            for t in offen:
                b.fehlt(wo, f"Status „geprüft\", aber Prüflistenpunkt offen: {t}")
        elif offen:
            b.hinweise.append(f"{wo}: in Arbeit, {len(offen)} Prüflistenpunkt(e) offen")

    # ── Sammeldokument: greift es die Auswertung auf? ───────────────────
    if status == "geprüft":
        sammel = pfad.parent / f"{pfad.parent.name}.md"
        if not sammel.exists():
            b.fehlt(wo, f"Sammeldokument {rel(sammel)} fehlt (Vorlage: vorlagen/sammeldokument.md)")
        else:
            s = sammel.read_text(encoding="utf-8")
            abschnitt = re.search(r"^## Was sich abzeichnet\s*$(.*?)(?=^## |\Z)", s, re.MULTILINE | re.DOTALL)
            if not abschnitt:
                b.fehlt(wo, f"{sammel.name} hat keinen Abschnitt „Was sich abzeichnet\"")
            elif not re.search(r"\(" + re.escape(pfad.name) + r"[)#]", abschnitt.group(1)):
                b.fehlt(wo, f"„Was sich abzeichnet\" in {sammel.name} verweist nicht auf diese Auswertung")

    # ── Querverweis zum Register ────────────────────────────────────────
    ids = register_ids(text)
    if ids is None:
        b.fehlt(wo, "keine `**Register:**`-Zeile (IDs in Backticks, oder „keine“)")
        return
    for rid in ids:
        e = register.get(rid)
        if e is None:
            b.fehlt(wo, f"Register-ID `{rid}` steht nicht in data/register.yaml")
        elif e.get("auswertung") != wo:
            b.fehlt(wo, f"`{rid}` verweist auf „{e.get('auswertung')}\" statt zurück auf diese Datei")
    for rid, e in register.items():
        if e.get("auswertung") == wo and rid not in ids:
            b.fehlt(wo, f"`{rid}` zeigt hierher, steht aber nicht in der `**Register:**`-Zeile")


def pruefe_register(eintraege: list[dict], schluessel: set[str], b: Bericht) -> dict[str, dict]:
    wo = rel(REGISTER)
    out: dict[str, dict] = {}
    for i, e in enumerate(eintraege):
        rid = e.get("id")
        if not rid:
            b.fehlt(wo, f"Eintrag {i + 1} ohne `id`")
            continue
        if rid in out:
            b.fehlt(wo, f"`{rid}` doppelt")
        out[rid] = e
        if e.get("schluessel") not in schluessel:
            b.fehlt(wo, f"`{rid}`: Zitierschlüssel {e.get('schluessel')!r} fehlt in literatur.bib (tools/doi2bib.py)")
        ausw = e.get("auswertung")
        if not ausw or not (REPO / ausw).exists():
            b.fehlt(wo, f"`{rid}`: Auswertung {ausw!r} gibt es nicht")
        if e.get("status") not in STATUS:
            b.fehlt(wo, f"`{rid}`: Status muss „in Arbeit\" oder „geprüft\" sein")
        if e.get("belastbarkeit") not in BELASTBARKEIT:
            b.fehlt(wo, f"`{rid}`: Belastbarkeit muss eine von {sorted(BELASTBARKEIT)} sein")
        for w in e.get("werte") or []:
            if w.get("wert") is not None and not str(w.get("fundstelle") or "").strip():
                b.fehlt(wo, f"`{rid}`: Wert „{w.get('name')}\" ohne Fundstelle")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leise", action="store_true", help="nur Fehler ausgeben")
    args = ap.parse_args()

    b = Bericht()
    register = pruefe_register(register_laden(), bib_schluessel(), b)
    for pfad in sorted(LITERATUR.glob("**/*_auswertung.md")):
        pruefe_auswertung(pfad, register, b)

    import verweise
    for wo, was in verweise.pruefen(REPO):
        b.fehlt(wo, was)

    from bestand import pruefe_bestand, ausgeben as bestand_ausgeben
    bestand = pruefe_bestand()
    for wo, was in bestand.fehler:
        b.fehlt(wo, was)

    if b.fehler:
        print(f"\n✗ {len(b.fehler)} Mangel/Mängel:\n", file=sys.stderr)
        letzte = None
        for wo, was in b.fehler:
            if wo != letzte:
                print(f"  {wo}", file=sys.stderr)
                letzte = wo
            print(f"      {was}", file=sys.stderr)
        print("\n  Im Notfall: git commit --no-verify\n", file=sys.stderr)
        return 1

    if not args.leise:
        print(f"✓ {b.geprueft} Auswertung(en), {len(register)} Registereinträge, Verweise und Bestand stimmen.")
        for h in b.hinweise:
            print(f"  ○ {h}")
    bestand_ausgeben(bestand)
    return 0


if __name__ == "__main__":
    sys.exit(main())
