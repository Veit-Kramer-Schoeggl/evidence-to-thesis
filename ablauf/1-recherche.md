# 1 · Recherche

**Worum es geht:** Arbeiten zu deinem Thema finden, festhalten, wie du gesucht
hast, und die Volltexte auf legalem Weg beschaffen.

**Was am Ende da ist:**

- je Suche ein Rechercheprotokoll in `notes/recherche/`,
- die Literaturangaben in [`literatur.bib`](../literatur.bib),
- die Volltexte in `literatur/<thema>/pdf/`, nur auf deinem Rechner.

Jeden Schritt kann Claude Code für dich erledigen. Die Sätze in
Anführungszeichen sind Beispiele, wie du darum bittest. Darunter steht der
Befehl, den Claude Code dann ausführt; du kannst ihn auch selbst eingeben.

## 1. Ein Thema anlegen

Ein Thema ist ein Ordner unter `literatur/`, etwa einer je Teilfrage deiner
Arbeit. Im Kit heißt so ein Ordner *Kategorie*. Für ein Teilthema legst du
darin einen Unterordner an; er ist genauso aufgebaut.

> „Lege ein Thema schlaf an und darin ein Teilthema studienabbruch.“

```bash
python3 tools/neu.py kategorie schlaf
python3 tools/neu.py kategorie schlaf/studienabbruch
```

Jedes Thema bekommt dabei sein Sammeldokument, etwa `literatur/schlaf/schlaf.md`.

## 2. Ein Rechercheprotokoll anlegen

Ins Protokoll kommt, womit, wann und wie du gesucht hast, die Suchanfrage
wörtlich. So kann jede Person deine Suche wiederholen.

> „Lege ein Rechercheprotokoll für die Suche in PubMed zum Thema schlaf an.“

```bash
python3 tools/neu.py protokoll pubmed-schlaf schlaf
```

Die Zeile **Ablage:** oben im Protokoll sagt, in welches Thema die Treffer
gehören.

## 3. Suchen

Wo du suchst, hängt vom Fach ab: in Fachdatenbanken wie PubMed, CINAHL oder
Scopus, in Google Scholar, mit KI-Suchdiensten wie Consensus oder Elicit oder
in den Literaturverzeichnissen guter Arbeiten.

> **Vorsicht bei KI-Suchdiensten.** Sie fassen Studien manchmal falsch
> zusammen oder nennen Angaben, die so nicht im Text stehen. Nimm ihre
> Treffer als Hinweis. Zahlen übernimmst du erst aus dem Volltext.

## 4. Treffer eintragen

Je Treffer eine Zeile in der Tabelle „Treffer“ des Protokolls, die DOI ganz
vorne. Die DOI ist die dauerhafte Kennung eines Artikels. Sie steht meist oben
auf der Seite des Artikels und beginnt mit `10.`.

## 5. Literaturangaben holen

> „Hol die Literaturangaben zu allen DOIs im Protokoll.“

```bash
python3 tools/doi2bib.py --file notes/recherche/2026-10-pubmed-schlaf.md
```

Das Programm fragt zu jeder DOI die offiziellen Angaben ab: Autorinnen und
Autoren, Titel, Jahr, Zeitschrift. Es trägt sie in [`literatur.bib`](../literatur.bib) ein. Jede
Arbeit bekommt dabei einen Kurznamen, den *Zitierschlüssel*, zum Beispiel
`Mustermann2020`. Unter diesem Namen liegen später auch ihr Volltext und ihre
Auswertung.

## 6. Volltexte holen

> „Hol die frei verfügbaren Volltexte für das Thema schlaf.“

```bash
python3 tools/holpdf.py --kategorie schlaf --file notes/recherche/2026-10-pubmed-schlaf.md
```

Das Programm lädt nur Fassungen, die legal frei verfügbar sind (Open Access).
Dafür braucht es einmal deine E-Mail-Adresse, siehe
[0 · Einrichten, Schritt 6](0-einrichten.md#schritt-6--volltexte-automatisch-holen-wahlweise).
Alles andere holst du über den Zugang deiner Hochschulbibliothek. Speichere
die Datei unter dem Zitierschlüssel, also als
`literatur/schlaf/pdf/Mustermann2020.pdf`.

Bekommst du einen Volltext nicht, trag ihn mit Grund in
[`notes/recherche/beschaffung.yaml`](../notes/recherche/beschaffung.yaml) ein. Dann ist klar, warum er fehlt, und der
Wächter mahnt ihn nicht mehr als vergessen an.

**Volltexte kommen nie ins Repository.** Sie sind urheberrechtlich geschützt.
Die Ordner `pdf/` sind deshalb davon ausgenommen.

## 7. Den Stand nachziehen

> „Zieh den Stand nach.“

```bash
python3 tools/status.py
```

Das Programm setzt hinter jede DOI im Protokoll ein Zeichen: `·` fehlt noch,
📄 Volltext da, ✅ ausgewertet, ⛔ nicht zu bekommen. Dieselbe Übersicht
schreibt es in die Tabelle „Stand“ des Sammeldokuments. Dort steht bei jeder
Arbeit, deren Volltext noch fehlt, die DOI als Link: anklicken und holen.

## Woran der Wächter dich erinnert

- ein Protokoll ohne Zeile **Ablage:**,
- eine DOI ohne Literaturangabe in [`literatur.bib`](../literatur.bib),
- ein Volltext mit falschem Namen, am falschen Ort oder mit fremdem Inhalt;
  den Inhalt prüft er, wenn `pdftotext` installiert ist,
- veraltete Zeichen im Protokoll.

Bei jedem Lauf nennt er außerdem, welche Volltexte noch fehlen.

Weiter: [2 · Auswertung](2-auswertung.md) · zurück zur [Übersicht](../README.md)
