# Recherche: <Thema>

**Ablage:** [`literatur/<Kategorie>/`](../../literatur/<Kategorie>/) — Volltexte nach `pdf/`, Auswertungen daneben

> **So ist diese Vorlage gemeint.** Sie ist ein Vorschlag. Fest sind nur zwei
> Dinge, weil die Werkzeuge sie lesen:
> - die Zeile **Ablage:** oben;
> - eine Kennung am Anfang jeder Trefferzeile.
>
> Die Kennung ist eine DOI, oder `isbn:`, `hdl:` bzw. `url:` bei Arbeiten ohne
> DOI. Die Blöcke **Optionen** und **Beispiel** kommen beim Ausfüllen weg; die
> Beispiele sind erfunden.

**Datum:** <Datum> · **Werkzeug:** <womit gesucht wurde> · **Filter:** <welche, oder „keine“>

> **Optionen für das Werkzeug**
> - eine Fachdatenbank, etwa PubMed, CINAHL, Scopus oder ERIC;
> - Google Scholar;
> - ein KI-Suchdienst, etwa Consensus oder Elicit;
> - Handsuche in Literaturverzeichnissen und über „zitiert von“;
> - ein Hinweis der Betreuung.
>
> Je Werkzeug ein eigenes Protokoll, oder alle in einem mit je einem Abschnitt.

**Suchanfragen, wörtlich:**

1. `<Suchanfrage>`

> **Beispiel:** `("sleep duration" OR "sleep length") AND ("academic performance" OR dropout) AND student*`

**Anlass.** Welche Frage deiner Arbeit diese Suche beantworten soll.

> Urteile hier beruhen auf Abstracts. Zahlen werden erst aus dem Volltext
> übernommen, in der Auswertung, mit Fundstelle.

## Treffer

Eine Kennung je Zeile, am Zeilenanfang der Tabelle. `tools/doi2bib.py --file`
holt die Bibliografie, `tools/holpdf.py --file` die frei verfügbaren
Volltexte. `tools/status.py` setzt hinter jede Kennung den Stand:

| Zeichen | Stand |
|---|---|
| `·` | steht aus |
| `📄` | Volltext da |
| `✅` | ausgewertet |
| `⛔` | nicht beschaffbar, Grund in `beschaffung.yaml` |

| DOI | Studie | Warum sie zählt |
|---|---|---|

> **Optionen:** weitere Spalten nach Bedarf, etwa Design, Land oder
> Stichprobe; die Kennung bleibt vorne. Bei einer systematischen Suche hältst
> du zusätzlich die Zahlen je Schritt fest (gefunden, gesichtet,
> aufgenommen), etwa für ein Flussdiagramm nach PRISMA 2020.
>
> **Beispiel:** `| <DOI> | Mustermann 2020, Kohorte | einzige Studie mit Verwaltungsdaten statt Selbstauskunft |`

## Nicht aufgenommen

| Studie | Grund |
|---|---|

> **Beispiel:** `| Mustermann 2019 | untersucht Schulkinder, nicht Studierende |`
