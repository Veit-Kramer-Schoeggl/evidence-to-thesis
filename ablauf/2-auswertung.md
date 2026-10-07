# 2 · Auswertung

**Worum es geht:** jede Arbeit genau lesen und festhalten, was sie zeigt, wie
verlässlich sie es zeigt und was du für deine Arbeit daraus nimmst. Jede Zahl
bekommt ihre Fundstelle.

**Was am Ende da ist:** je Arbeit eine Datei
`literatur/<thema>/<Zitierschlüssel>_auswertung.md`.

## 1. Die Auswertung anlegen

> „Lege die Auswertung für Mustermann2020 im Thema schlaf an.“

```bash
python3 tools/neu.py auswertung schlaf Mustermann2020
```

Die Datei entsteht aus der Vorlage [`vorlagen/auswertung.md`](../vorlagen/auswertung.md). Jeder Abschnitt
bietet dort Optionen und ein erfundenes Beispiel. Kennst du die Vorlage
schon, lässt `--knapp` diese Hilfen weg:

```bash
python3 tools/neu.py --knapp auswertung schlaf Mustermann2020
```

## 2. Lesen und ausfüllen

- **Prüfliste:** oben in der Datei, Punkt für Punkt abarbeiten und abhaken.
- **Fundstelle:** bei jeder Zahl Seite, Tabelle oder Abbildung.
- **Belastbarkeit:** einstufen als tragend, eingeschränkt oder nicht belastbar,
  mit Gründen.
- **Status:** „in Arbeit“, solange du liest. „geprüft“, wenn alles abgehakt
  ist und die Auswertung im Sammeldokument verlinkt ist.

Claude Code kann aus dem Volltext eine erste Fassung schreiben. **Prüf dann
jede Zahl selbst im PDF** und vermerke das im KI-Protokoll. KI-Assistenten
lesen manchmal die falsche Zeile einer Tabelle ab oder verwechseln
Vergleichsgruppen.

## 3. Das Zahlenregister (wahlweise)

Wandert eine Zahl in eine eigene Rechnung oder in deinen Text, trag sie in
[`data/register.yaml`](../data/register.yaml) ein, mit Fundstelle. Die Auswertung nennt ihre Kennung
dann in der Zeile **Register:**. So findest du später zu jeder Zahl im Text
heraus, woher sie stammt.

## 4. Ins Sammeldokument übertragen

Die Kernaussage kommt mit Link ins Sammeldokument des Themas, unter „Was sich
abzeichnet“. Fragen, die beim Lesen entstanden sind, kommen in dessen
Fragenteil. Mehr dazu in [3 · Sammeldokument](3-sammeldokument.md).

## Woran der Wächter dich erinnert

- bei „in Arbeit“ nur mit Hinweisen: was noch offen ist;
- bei „geprüft“ mit Fehlern, die den Commit aufhalten: jeder Punkt der
  Prüfliste abgehakt, der Zweck eingetragen, der Link im Sammeldokument
  gesetzt, jede Kennung aus der Zeile **Register:** im Register vorhanden.

Die Prüfliste kannst du an deine Arbeit anpassen, siehe
[README, „Vorlagen anpassen“](../README.md#vorlagen-anpassen).

Weiter: [3 · Sammeldokument](3-sammeldokument.md) · zurück zur [Übersicht](../README.md)
