# Backlog

Was es in der Bachelorarbeit, aus der dieses Kit stammt, schon gibt, bisher
aber nur für diese eine Arbeit gebaut ist. Das sind Kandidaten für spätere
Fassungen des Kits, ohne Zusage und ohne Reihenfolge. Wünsche und Ideen gern
als Issue.

In deinem eigenen Repository kannst du diese Datei löschen.

## Rechnen mit Zahlen aus der Literatur

- **Rechenskript mit Parameterdatei.** Die Eingabewerte stehen in einer
  YAML-Datei, jeder mit Verweis auf seinen Registereintrag. Der Wächter weist
  Werte zurück, deren Quelle als „nicht belastbar“ eingestuft ist.
- **Erzeugte Blöcke.** Das Skript schreibt seine Ergebnisse selbst in
  markierte Blöcke im Text (`<!-- name:start -->` … `<!-- name:ende -->`),
  dazu einen Block mit den Kernzahlen für die Kurzfassung. Die Regel steht
  schon in `CLAUDE.md`. Es fehlen ein kleines Hilfsmodul und eine Prüfung, ob
  die Blöcke noch zum Skript passen.
- **Tests mit festen Sollwerten** für die eigene Rechnung, nicht nur für die
  Werkzeuge.
- **Sensitivitätsrechnungen** aus demselben Skript: jede Annahme einmal an
  den Rändern ihrer Spanne, als erzeugte Tabelle.
- **Rechenschritte** als eigenes Dokument mit Diagramm, damit sich die
  Rechnung ohne den Code nachvollziehen lässt.

## Abbildungen

- **Abbildungen nur aus Skripten** (`tools/abb_*.py`), jede mit einem
  Fingerabdruck der verwendeten Zahlen. Der Wächter meldet jede Abbildung,
  deren Zahlen sich seither geändert haben.

## Register und Übersichten

- **Festes Vokabular je Merkmal** im Register, etwa für Endpunkt,
  Adjustierung, Datenbasis, Definition des Zielmerkmals und Messgüte. Der
  Wächter lässt nur Werte aus dem Vokabular zu.
- **Belastbarkeit mit Gründen aus einem Katalog**, abgeglichen mit der
  Adjustierung.
- **Erzeugte Übersichtstabellen** aus dem Register (Vergleich, Endpunkte,
  Adjustierung), vom Wächter auf Aktualität geprüft.
- **Eigene Prüflisten je Quellenart**, gewählt nach Ordner, etwa für
  Konzeptquellen oder Studien zur Messgüte.
- **Feinere Status und ein Zweck aus festem Vokabular**, etwa „Abstract“,
  „Volltext“, „geprüft“. Das hilft, wenn ein Repository zwei Arbeiten trägt.

## Recherche und KI

- **Recherche mit KI-Suchdiensten** wie Consensus: wie Treffer übernommen
  werden (Metadaten über Crossref, Exporte nur lokal) und was davon ins
  Protokoll gehört.
- **Prüfdurchgänge mit Hilfsagenten** in Claude Code: Mehrere Agenten prüfen
  Auswertungen oder ziehen Bilanz über alle offenen Fragen. Ein weiterer
  prüft ihre Befunde gegen.
- **Gegenprüfung durch ein zweites Modell:** ein Prüfauftrag für ein anderes
  KI-Modell, mit den Unterlagen, die es dafür braucht.
- **Anfragen nach Daten** bei Behörden oder bei Autorinnen und Autoren, mit
  Stand und Antwort.

## Dokumentation

- **„Der Weg einer Zahl“:** ein Dokument, das zeigt, wie eine Zahl von der
  Quelle über Register und Rechnung in den Text kommt, mit allen Prüfstellen.
- **Begriffsliste** für Arbeiten, die in einer anderen Sprache geschrieben
  werden als die Notizen: festgelegte Übersetzungen und Wortregeln.
