# <Schlüssel> — <worum es geht, in einem Satz>

> Kategorie [<Kategorie>](<Kategorie>.md) · aus der Vorlage `vorlagen/auswertung.md`

📄 [Volltext](pdf/<Schlüssel>.pdf) · 🔗 [doi:<DOI>](https://doi.org/<DOI>)
· Zweck **<wofür du die Arbeit brauchst>** · Status: **in Arbeit** · angelegt <Datum>

> **Register:** keine

*Titel laut Bibliografie:* <Titel>

> **So ist diese Vorlage gemeint.** Sie ist ein Vorschlag: Übernimm, was dir
> hilft, und streich den Rest. Die Blöcke **Optionen** und **Beispiel** helfen
> beim Ausfüllen und kommen danach weg; [`tools/neu.py`](/tools/neu.py) mit `--knapp` legt die
> Datei gleich ohne sie an. Die Beispiele sind erfunden und zeigen nur die
> Form. Zahlen darin sind Platzhalter (`<n>`, `0,XX`, `S. N`).
>
> Fest ist nur, was der Wächter liest:
> - die Kopfzeile mit Zweck und Status;
> - die Zeile **Register:**;
> - die Prüfliste zwischen den Kommentarzeilen `pruefliste:start` und
>   `pruefliste:ende`, die in der Vorschau unsichtbar sind;
> - die Pflichtabschnitte im Kommentar darunter.
>
> Prüfliste und Pflichtabschnitte nimmt er aus `vorlagen/auswertung.md`.
> Änderst du sie dort, prüft er ab dann nach deiner Fassung.

<!-- pflichtabschnitte: Fragestellung, Design und Qualität, Ergebnisse, Stärken, Schwächen, Was wir daraus nehmen -->

> **Optionen für den Kopf**
> - **Zweck:** wofür du die Arbeit brauchst, etwa ein Kapitel deiner
>   Gliederung, „Methoden“, „Hintergrund“, „Vergleichswert“ oder „nur gelesen“.
> - **Status:** „in Arbeit“, solange du liest. Der Wächter nennt dann nur
>   Hinweise. „geprüft“, sobald die Prüfliste abgehakt und die Auswertung im
>   Sammeldokument verlinkt ist. Ab dann verlangt er alles.
> - **Register:** „keine“, oder die Kennungen aus [`data/register.yaml`](/data/register.yaml), jede in
>   schrägen Hochkommas wie `` `Mustermann2020-a` ``,
>   sobald Zahlen dieser Arbeit in eine Rechnung oder in den Text wandern.
>
> **Beispiel:** Zweck „Kapitel 2, Hintergrund“, Status „in Arbeit“,
> Register „keine“.

### Prüfliste — vor der Zusammenfassung abzuarbeiten

<!-- pruefliste:start -->
- [ ] **Design und Qualität** ausgewiesen: Studientyp, Stichprobe, Nachbeobachtung, Qualitätsbewertung
- [ ] **Exposition und Vergleich** wörtlich benannt: wer gegen wen verglichen wird und wie gemessen
- [ ] **Endpunkte** ausgewiesen: alle berichteten genannt, der ausgewertete benannt, Definition vermerkt
- [ ] **Ergebnisse** mit Seiten- oder Tabellenangabe bei jeder Zahl
- [ ] **Übertragung** auf die eigene Fragestellung versucht, Annahmen offengelegt oder Hindernis benannt
- [ ] **Verzerrung** geprüft: Adjustierung, Störgrößen, Umkehrkausalität
- [ ] **Belastbarkeit** eingestuft: tragend, eingeschränkt oder nicht belastbar, mit Gründen
- [ ] **Vorbehalt** vermerkt, wo eine Zahl nicht direkt mit anderen vergleichbar ist
- [ ] **Register** nachgezogen, wenn Zahlen weiterverwendet werden, sonst „keine“
- [ ] **Sammeldokument** nachgezogen: „Was sich abzeichnet“ verweist auf diese Auswertung
- [ ] **Aufgeworfene Fragen** im Fragenteil des Sammeldokuments nachgetragen
- [ ] **Zweck** gesetzt: wofür die Arbeit gebraucht wird
<!-- pruefliste:ende -->

> **Optionen für die Prüfliste**
> - **So lassen:** Die Punkte oben passen für die meisten empirischen Arbeiten.
> - **Kürzen:** Punkte, die für deine Quellen nie passen, streichst du in
>   `vorlagen/auswertung.md`, etwa „Endpunkte“ bei theoretischen Arbeiten.
> - **Ergänzen:** eigene Punkte im selben Format (`- [ ] **Name** …`), etwa
>   **Überlappung** (stützen sich mehrere Arbeiten auf dieselben Daten?) oder
>   **Messinstrument** (validiert, und für deine Zielgruppe?).
> - **Einzelfall:** Passt ein Punkt bei einer einzelnen Arbeit nicht, schreib
>   „entfällt“ mit Grund dahinter und hake ihn ab.
>
> Was du in der Vorlage änderst, verlangt der Wächter ab dann von jeder
> Auswertung: bei „geprüft“ als Fehler, bei „in Arbeit“ als Hinweis.

## Fragestellung

Was untersucht die Arbeit, und was willst du von ihr wissen?

> **Beispiel:** „Die Übersichtsarbeit fasst Kohortenstudien zur Frage
> zusammen, ob längerer Schlaf mit besserem Studienerfolg einhergeht. Uns
> interessiert, wie stark der Zusammenhang ist und ob er ab einer bestimmten
> Schlafdauer abflacht.“

## Design und Qualität

| | |
|---|---|
| Typ | |
| Stichprobe | |
| Nachbeobachtung | |
| Qualität | |

> **Optionen**
> - **Form:** Tabelle wie oben, oder ein kurzer Absatz, wenn wenig zu sagen ist.
> - **Qualität:** eine anerkannte Checkliste, passend zum Studientyp. Für
>   Übersichtsarbeiten gibt es AMSTAR 2, für randomisierte Studien RoB 2, für
>   nicht randomisierte Interventionsstudien ROBINS-I. Kohorten- und
>   Fall-Kontroll-Studien bewertest du mit der Newcastle-Ottawa-Skala,
>   qualitative Studien mit der CASP-Checkliste. Oder eine eigene Einschätzung,
>   dann mit Begründung.
>
> **Beispiel:** „Typ: Metaanalyse prospektiver Kohortenstudien. Stichprobe:
> `<n>` Studien mit zusammen `<n>` Personen (S. N). Nachbeobachtung: `<n>` bis
> `<n>` Jahre (Tab. N). Qualität: nach AMSTAR 2 niedrig, weil nur eine
> Datenbank durchsucht wurde. Das ist einer der kritischen Punkte der
> Checkliste (S. N).“

## Exposition und Vergleich

Wer wird gegen wen verglichen, und wie wurde gemessen? Hier entstehen die
meisten Missverständnisse: Zwei Studien mit verschiedenen Vergleichsgruppen
messen Verschiedenes, auch wenn ihre Zahlen ähnlich aussehen.

> **Optionen:** Bei Interventionsstudien heißt der Abschnitt „Intervention und
> Kontrolle“. Bei qualitativen Studien beschreibst du Stichprobe und Kontext.
> Wird nichts verglichen, schreibst du „entfällt“ in die Prüfliste.
>
> **Beispiel:** „Verglichen wird das oberste mit dem untersten Fünftel der
> Schlafdauer, einmal zu Beginn per Fragebogen erhoben (S. N). Die
> Vergleichsgruppe heißt also ‚wenig Schlaf‘, nicht ‚Schlafmangel‘.“

## Endpunkte

Was wurde gemessen, und welchen Endpunkt wertest du aus?

> **Optionen:** alle berichteten Endpunkte auflisten und den ausgewerteten
> markieren, oder nur den ausgewerteten mit seiner Definition nennen.
>
> **Beispiel:** „Berichtet: Notendurchschnitt und Studienabbruch.
> Ausgewertet: Studienabbruch, aus den Verwaltungsdaten der Hochschulen,
> nicht selbst angegeben (S. N).“

## Ergebnisse

Jede Zahl mit Fundstelle: Seite, Tabelle oder Abbildung.

> **Optionen:** Fließtext bei wenigen Zahlen. Bei vielen Zahlen eine Tabelle
> `| Vergleich | Wert | 95-%-KI | Fundstelle |`.
>
> **Beispiel:** „Odds Ratio 0,XX (95-%-KI 0,XX–0,XX) für Studienabbruch,
> oberstes gegen unterstes Fünftel der Schlafdauer (Tab. N, S. N).“

## Übertragung auf unsere Frage

Lässt sich das Ergebnis auf deine Frage übertragen, und welche Annahmen braucht
es dafür?

> **Beispiel:** „Die Kohorten stammen aus anderen Ländern und Hochschultypen.
> Ob der Zusammenhang auch an österreichischen Fachhochschulen gilt, ist nicht
> belegt. Wir nehmen es an und benennen das in der Diskussion (Annahme).“

## Verzerrung und Belastbarkeit

Adjustierung, Störgrößen, Umkehrkausalität; danach die Einstufung mit Gründen.

> **Optionen für die Einstufung**
> - **tragend:** Die Arbeit kann eine Aussage oder Zahl deiner Arbeit allein tragen.
> - **eingeschränkt:** verwendbar, aber mit benanntem Vorbehalt.
> - **nicht belastbar:** lesen ja, ihre Zahlen nicht verwenden.
>
> **Beispiel:** „Eingeschränkt: Schlaf nur einmal erfragt. Umkehrkausalität
> ist möglich, weil Prüfungsstress den Schlaf verkürzen kann. Adjustiert für
> Alter und Studienfach, nicht für Erwerbstätigkeit neben dem Studium (S. N).“

## Stärken

> **Beispiel:** „Große, gut beschriebene Kohorten; Endpunkt aus
> Verwaltungsdaten statt Selbstauskunft.“

## Schwächen

> **Beispiel:** „Schlafdauer nur selbst angegeben; keine Angabe, wie mit
> fehlenden Werten umgegangen wurde.“

## Was wir daraus nehmen

Nummerierte Aussagen mit Fundstelle und dem Ort, an dem sie in deiner Arbeit
landen. Danach, was du bewusst nicht übernimmst.

1. …

**Was wir nicht daraus nehmen.** …

> **Beispiel:** „1. Der Zusammenhang zeigt in allen Kohorten in dieselbe
> Richtung (Abb. N). Das stützt Entscheidung E3 und kommt in Kapitel 2. Was
> wir nicht daraus nehmen: die Zahl für Erstsemester, weil sie auf einer sehr
> kleinen Gruppe beruht (S. N).“

> **Optionen für weitere Abschnitte**
> - **Wörtliche Zitate** mit Seite, wenn du die Arbeit im Text zitieren willst.
> - **Fragen an die Arbeit**, die du der Betreuung oder den Autorinnen und
>   Autoren stellen willst.
> - **Abbildungen und Tabellen**, die du nachbauen willst, mit Fundstelle.
