# Backlog

Was es in der Bachelorarbeit, aus der dieses Kit stammt, schon gibt, bisher
aber nur für diese eine Arbeit gebaut ist. Das sind Ideen für spätere
Fassungen des Kits, ohne Zusage und ohne Reihenfolge. Wünsche und Vorschläge
gern als Issue.

In deinem eigenen Repository kannst du diese Datei löschen.

## Rechnen mit Zahlen aus der Literatur

Wie man dabei vorgeht, beschreibt schon [3 · Modell](ablauf/3-modell.md); die
Werkzeuge dafür fehlen noch:

- **Ein Rechenprogramm mit einer Liste seiner Eingabewerte.** Jeder
  Eingabewert verweist auf seinen Eintrag im Zahlenregister. Der Wächter weist
  Werte zurück, deren Quelle als „nicht belastbar“ eingestuft ist.
- **Ergebnisse, die sich selbst in den Text schreiben.** Das Rechenprogramm
  setzt seine Ergebnisse in markierte Stellen der Dokumente, dazu die
  wichtigsten Zahlen für die Kurzfassung. Niemand schreibt sie von Hand ab.
  Die Regel steht schon in [`CLAUDE.md`](CLAUDE.md), Regel 6; es fehlen ein
  kleines Hilfsprogramm und eine Prüfung, ob die Stellen noch zum Programm
  passen.
- **Tests mit festen Sollwerten** für die eigene Rechnung, nicht nur für die
  Werkzeuge.
- **Robustheitsrechnungen:** jede Annahme einmal an den Rändern ihrer Spanne,
  als Tabelle aus demselben Programm.
- **Die Rechenschritte als eigenes Dokument** mit Diagramm, damit sich die
  Rechnung ohne das Programm nachvollziehen lässt.

## Abbildungen

- **Abbildungen nur aus Programmen**, jede mit einem Fingerabdruck der
  verwendeten Zahlen. Ändert sich eine Zahl, meldet der Wächter jede Abbildung,
  die sie noch alt zeigt.

## Register und Übersichten

- **Feste Wortlisten je Merkmal** im Register, etwa für Endpunkt,
  Adjustierung, Datenbasis, Definition des Zielmerkmals und Messgüte. Der
  Wächter lässt nur Werte aus der Liste zu, damit gleiche Dinge gleich heißen.
- **Belastbarkeit mit Gründen aus einem Katalog**, abgeglichen mit der
  Adjustierung.
- **Übersichtstabellen, die aus dem Register entstehen** (Vergleich,
  Endpunkte, Adjustierung), vom Wächter auf Aktualität geprüft.
- **Eigene Prüflisten je Art der Quelle**, gewählt nach Ordner, etwa für
  Begriffsquellen oder Studien zur Messgenauigkeit.
- **Feinere Status und ein Zweck aus einer festen Liste**, etwa „Abstract“,
  „Volltext“, „geprüft“. Das hilft, wenn ein Repository zwei Arbeiten trägt.

## Recherche und KI

- **Recherche mit KI-Suchdiensten** wie Consensus: wie Treffer übernommen
  werden (Literaturangaben über Crossref, Exporte nur auf dem eigenen Rechner)
  und was davon ins Protokoll gehört.
- **Prüfdurchgänge mit mehreren KI-Agenten** in Claude Code: Mehrere Agenten
  prüfen Auswertungen oder ziehen Bilanz über alle offenen Fragen, ein weiterer
  prüft ihre Befunde nach.
- **Gegenprüfung durch ein zweites KI-Modell:** ein Prüfauftrag für ein
  anderes Modell, mit den Unterlagen, die es dafür braucht.
- **Anfragen nach Daten** bei Behörden oder bei Autorinnen und Autoren, mit
  Stand und Antwort.

## Dokumentation

- **„Der Weg einer Zahl“:** ein Dokument, das zeigt, wie eine Zahl von der
  Quelle über Register und Rechnung in den Text kommt, mit allen Prüfstellen.
- **Eine Begriffsliste** für Arbeiten, die in einer anderen Sprache geschrieben
  werden als die Notizen: festgelegte Übersetzungen und Wortregeln.
