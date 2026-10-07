# 4 · Sammeldokumente

<sub>🚶 machst du selbst · 🤖 erledigt Claude Code für dich · 💻 erledigt ein Programm von selbst</sub>

**Worum es geht:** je Thema an einer Stelle zusammentragen, was die
Auswertungen ergeben, was offen ist und was in deine Arbeit kommt.

**Wo:** `literatur/<thema>/<thema>.md`. Die Datei entsteht mit dem Thema,
siehe [1 · Recherche](1-recherche.md).

## Die Teile

| Abschnitt | was hineinkommt |
|---|---|
| Kurzfassung | der Stand des Themas in wenigen Absätzen, verständlich ohne den Rest |
| Stand | alle Arbeiten des Themas mit Zeichen und DOI; schreibt [`tools/status.py`](../tools/status.py) selbst |
| Was sich abzeichnet | je geprüfter Auswertung die Kernaussage mit Link |
| Fragen | jede Frage mit Kennung (F1, F2 …), bis sie beantwortet oder entschieden ist |

Die Vorlage [`vorlagen/sammeldokument.md`](../vorlagen/sammeldokument.md) zeigt zu jedem Teil Optionen und ein
Beispiel. Fest ist nur der Abschnitt „Was sich abzeichnet“: Dort sucht der
Wächter die Links auf geprüfte Auswertungen.

💻 Die Tabelle „Stand“ schreibt ein Programm; 🤖 Kurzfassung und Befunde
entwirft Claude Code; 🚶 du prüfst sie.

## Was sich bewährt hat

- **Nichts verschwindet still.** Eine erledigte Frage bekommt einen Befund
  und bleibt stehen.
- **Die Kurzfassung nachziehen,** sobald sich etwas Wichtiges ändert, mit
  Datum.
- **Keine Zahl aus einer eigenen Rechnung abschreiben.** Verweise auf die
  Rechnung.
- **Erkenntnisse hierher, nicht in neue Dateien.** So bleibt alles zu einem
  Thema an einem Ort.

> „Fasse den Stand des Themas schlaf in der Kurzfassung zusammen.“
> Claude Code entwirft, du prüfst.

Weiter: [5 · Entscheidung](5-entscheidung.md) · zurück zur [Übersicht](../README.md)
