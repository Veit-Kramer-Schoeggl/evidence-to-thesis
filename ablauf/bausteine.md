# Die Bausteine und wozu sie da sind

<sub>🚶 machst du selbst · 🤖 erledigt Claude Code für dich · 💻 erledigt ein Programm von selbst</sub>

Das Kit hat einige Dateien und Programme, die auf den ersten Blick nach
Aufwand aussehen. Jeder Baustein löst ein Problem, das bei Abschlussarbeiten
immer wieder auftritt. Hier steht je Baustein, was er ist, wozu er da ist und
was hineinkommt.

| Baustein | wozu, in einem Satz |
|---|---|
| [Der Hook](#der-hook) 💻 | startet die Prüfung vor jedem Commit von selbst, damit sie nie vergessen wird |
| [Der Wächter](#der-wächter) 💻 | findet mechanische Fehler, bevor sie sich festsetzen |
| [Die Tests](#die-tests) 💻 | prüfen den Wächter und die Programme selbst |
| [Das Zahlenregister](#das-zahlenregister) 🤖 🚶 | eine Stelle für jede Zahl, die aus einer Studie weiterwandert |
| [Die Literaturliste](#die-literaturliste) 💻 | richtige Literaturangaben, ein Kurzname je Arbeit für alles |
| [Die Rechercheprotokolle](#die-rechercheprotokolle) 🚶 🤖 | machen deine Suche wiederholbar |
| [Die Beschaffungsliste](#die-beschaffungsliste) 🚶 | trennt „noch nicht versucht“ von „nicht zu bekommen“ |
| [Die Sammeldokumente](#die-sammeldokumente) 🤖 🚶 | alles zu einem Thema an einem Ort |
| [Die Entscheidungen](#die-entscheidungen) 🚶 🤖 | beantworten später die Frage „Warum so?“ |
| [Der Stand](#der-stand) 🤖 🚶 | der Wiedereinstieg nach jeder Pause |
| [Das KI-Protokoll](#das-ki-protokoll) 🤖 🚶 | der Nachweis, wofür du KI eingesetzt und was du geprüft hast |
| [Die Arbeitsregeln für Claude Code](#die-arbeitsregeln-für-claude-code) 🚶 | woran sich der Assistent in deinem Repository hält |
| [Die Vorlagen](#die-vorlagen) 🚶 | gleicher Aufbau, damit nichts vergessen wird |
| [Die Merkliste](#die-merkliste) 🚶 🤖 | sammelt, was in den Text soll, bevor du schreibst |
| [Die Linkprüfung](#die-linkprüfung) 💻 | hält die Verweise zwischen den Dokumenten gültig |

Git und GitHub erklärt [Bei jedem Schritt](bei-jedem-schritt.md#git-ist-pflicht).

## Der Hook

**Was:** ein kleines Skript, das Git vor jedem Commit von selbst startet,
[`tools/hooks/pre-commit`](../tools/hooks/pre-commit). Du schaltest es einmal
ein, siehe [0 · Einrichten](0-einrichten.md#schritt-4--dein-eigenes-repository-anlegen).

**Wozu:** Die Prüfung läuft immer, auch wenn du müde bist oder es eilig hast.
Vergessen kannst du sie nicht.

**Was er tut:** Er startet den Wächter und danach die Tests. Schlägt einer
fehl, speichert Git nichts, und du siehst, was fehlt.

## Der Wächter

**Was:** das Prüfprogramm [`tools/pruefe.py`](../tools/pruefe.py).

**Wozu:** Er findet mechanische Fehler, bevor sie sich festsetzen: eine Zahl
ohne Fundstelle im Register, einen vergessenen Punkt der Prüfliste, eine
geprüfte Auswertung ohne Link im Sammeldokument, einen Volltext mit falschem
Namen, einen Link ins Leere.

**Was er nicht kann:** Inhalte beurteilen. Ob eine Zahl richtig abgelesen ist,
prüfst du selbst, siehe
[Nichts blind übernehmen](ki-und-plagiat.md#3-nichts-blind-übernehmen).

## Die Tests

**Was:** kleine Programme im Ordner `tests/`, die die Werkzeuge selbst prüfen.

**Wozu:** Wer prüft den Wächter? Die Tests. Sie stellen sicher, dass der
Wächter Fehler wirklich findet und dass Vorlagen und Wächter zusammenpassen.
Änderst du eine Vorlage oder ein Programm, zeigen sie sofort, ob dabei etwas
kaputtgegangen ist.

**Beispiele:** „Eine Auswertung aus der Vorlage besteht den Wächter.“ „Ein
Link ins Leere wird gefunden.“ „Eine Zahl ohne Fundstelle im Register wird
gemeldet.“

**Für eigene Rechnungen** gibt es Tests mit festen Sollwerten, siehe
[3 · Modell](3-modell.md).

## Das Zahlenregister

**Was:** die Datei [`data/register.yaml`](../data/register.yaml), eine Liste
aller Zahlen aus Studien, die du weiterverwendest. Jeder Eintrag nennt die
Studie, ihre Auswertung, die Zahl, ihre Fundstelle, den Status und die
Belastbarkeit.

**Wozu:**

- **Eine Stelle für jede Zahl.** Text und Rechnung nehmen die Zahl von dort,
  nicht aus dem Gedächtnis oder einer Notiz.
- **Rückverfolgbar.** Zu jeder Zahl im Text findest du schnell Seite und
  Tabelle im Original.
- **Belastbarkeit sichtbar.** Zahlen aus schwachen Studien fallen auf, bevor
  sie in eine Rechnung wandern.
- **Eine Korrektur, eine Stelle.** Findest du einen Lesefehler, änderst du ihn
  einmal, und überall gilt der richtige Wert.

**Was hineinkommt,** zum Beispiel:

- Effektmaße wie Odds Ratio, Hazard Ratio oder relatives Risiko, jeweils mit
  Konfidenzintervall;
- Mittelwerte und Streuungen;
- Häufigkeiten und Anteile;
- Stichprobengrößen;
- Kosten;
- Kennwerte der Messgenauigkeit wie Sensitivität und Spezifität;
- Umrechnungsfaktoren aus Studien.

**Was nicht hineinkommt:** eigene Annahmen, denn sie haben keine Fundstelle;
sie gehören mit Begründung nach [`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md).
Auch Zahlen, die nur in einer Auswertung stehen und nirgends weiterwandern,
brauchen keinen Eintrag.

**Ein Eintrag,** als erfundenes Beispiel mit Platzhaltern statt Zahlen:

```yaml
eintraege:
  - id: Mustermann2020-abbruch
    schluessel: Mustermann2020
    auswertung: literatur/schlaf/Mustermann2020_auswertung.md
    status: geprüft
    belastbarkeit: eingeschränkt
    werte:
      - name: Odds Ratio für Studienabbruch, viel gegen wenig Schlaf
        wert: 0.XX
        ki95: [0.XX, 0.XX]
        fundstelle: "Tab. N, S. N"
```

Die Auswertung nennt die Kennung dann in ihrer Zeile **Register:**, also
`Mustermann2020-abbruch`. Der Wächter prüft, dass beide aufeinander zeigen und
jeder Wert eine Fundstelle hat.

**Wahlweise:** Rechnet deine Arbeit nicht und verwendet sie nur wenige Zahlen,
reicht die Fundstelle in der Auswertung. Das Register lohnt sich, sobald
Zahlen weiterwandern.

## Die Literaturliste

**Was:** die Datei [`literatur.bib`](../literatur.bib).

**Wozu:** Die Angaben kommen über die DOI aus Crossref, statt abgetippt zu
werden; so stimmen Namen, Jahre und Titel. Jede Arbeit bekommt einen
Kurznamen, den Zitierschlüssel. Er verbindet Volltext, Auswertung, Register
und Text. LaTeX und pandoc lesen die Datei direkt.

**Was hineinkommt:** jede Arbeit aus deinen Rechercheprotokollen, eingetragen
von [`tools/doi2bib.py`](../tools/doi2bib.py).

## Die Rechercheprotokolle

**Was:** je Suche eine Datei in `notes/recherche/`, angelegt aus
[`vorlagen/rechercheprotokoll.md`](../vorlagen/rechercheprotokoll.md).

**Wozu:** Deine Suche bleibt wiederholbar. Im Methodenteil kannst du genau
sagen, wo, wann und wie du gesucht hast. Die Zeichen hinter den DOIs zeigen
deinen Fortschritt.

**Was hineinkommt:** Datum, Werkzeug, Filter, die Suchanfrage wörtlich, die
Treffer mit DOI und die nicht aufgenommenen Treffer mit Grund.

## Die Beschaffungsliste

**Was:** die Datei
[`notes/recherche/beschaffung.yaml`](../notes/recherche/beschaffung.yaml).

**Wozu:** Sie trennt „noch nicht versucht“ von „nicht zu bekommen“. Der Grund
steht dabei. So kannst du in der Diskussion belegen, welche Arbeiten dir
fehlten und warum.

**Was hineinkommt:** der Zitierschlüssel, der Grund, wann und worüber du es
versucht hast.

## Die Sammeldokumente

**Was:** je Thema eine Datei, siehe
[4 · Sammeldokumente](4-sammeldokumente.md).

**Wozu:** Alles zu einem Thema steht an einem Ort: die Kurzfassung, der Stand
aller Arbeiten, was sich abzeichnet, die offenen Fragen. Keine Frage
verschwindet still.

## Die Entscheidungen

**Was:** die Datei [`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md).

**Wozu:** Wer später fragt „Warum so?“, du selbst, deine Betreuung oder die
Prüfung, findet die Antwort mit Begründung und mit den Optionen, die du nicht
gewählt hast.

**Was hineinkommt,** zum Beispiel: was an KI-Nutzung erlaubt ist (als ersten
Eintrag), die Fragestellung, die Methode, die Ein- und Ausschlusskriterien der
Suche, die Prüfliste, Annahmen in Rechnungen, die Gliederung.

## Der Stand

**Was:** die Datei [`STAND.md`](../STAND.md).

**Wozu:** Nach einer Pause weißt du sofort, wo du stehst. Claude Code liest
hier zuerst.

**Was hineinkommt:** worum es geht, was erledigt ist, offene Entscheidungen,
nächste Schritte, was noch zu beschaffen ist.

## Das KI-Protokoll

**Was:** die Datei [`KI-PROTOKOLL.md`](../KI-PROTOKOLL.md).

**Wozu:** Deine Hochschule verlangt, dass du KI-Nutzung offenlegst. Das
Protokoll sammelt laufend, was du dafür brauchst, und belegt, was du selbst
geprüft hast. Mehr in
[KI, Plagiat und Eidesstattliche Erklärung](ki-und-plagiat.md).

**Was hineinkommt:** je Arbeitsgang der Auftrag, was die KI getan hat, was du
geprüft hast und was in die Arbeit geht.

## Die Arbeitsregeln für Claude Code

**Was:** die Datei [`CLAUDE.md`](../CLAUDE.md). Claude Code liest sie beim
Start jeder Sitzung.

**Wozu:** Sie legt fest, wie der Assistent in deinem Repository arbeitet: keine
Zahl ohne Fundstelle, erst Optionen, dann Ausführung, alles protokollieren.

**Was hineinkommt:** Die Grundregeln lässt du stehen. Eigene Regeln ergänzt du,
etwa die Sprache deiner Arbeit oder Begriffe, die immer gleich heißen sollen.

## Die Vorlagen

**Was:** die Dateien in `vorlagen/`, siehe
[README, „Vorlagen anpassen“](../README.md#vorlagen-anpassen).

**Wozu:** Gleicher Aufbau macht Auswertungen vergleichbar und erinnert an alles
Wichtige. Die Vorlagen sind Vorschläge; die Prüfliste passt du an deine Arbeit
an, siehe [Prüfliste festlegen](pruefliste-festlegen.md).

## Die Merkliste

**Was:** die Datei [`notes/merkliste.md`](../notes/merkliste.md).

**Wozu:** Was dir beim Lesen für den Text auffällt, sammelst du hier, nach
Kapiteln, bevor du schreibst. Was du bewusst nicht machst, steht unter
„Zurückgestellt“, damit es nicht immer wieder aufkommt.

## Die Linkprüfung

**Was:** das Programm [`tools/verweise.py`](../tools/verweise.py); der Wächter
ruft es bei jedem Commit auf.

**Wozu:** Die Dokumente verweisen aufeinander. Benennst du eine Datei um oder
löschst einen Abschnitt, findet die Linkprüfung jeden Verweis, der danach ins
Leere zeigt.

Zurück zur [Übersicht](../README.md)
