# Beispiel: eine fertige Auswertung

So kann eine Auswertung aussehen, wenn sie fertig ist. Sie folgt der Vorlage
[`vorlagen/auswertung.md`](../vorlagen/auswertung.md) und zeigt, wie tief man
liest: welche Punkte hineingehören, wie jede Zahl belegt wird und wo die
Fallen einer Studie liegen.

> **Was hier echt ist und was nicht.**
> - **Echt** ist die Studie: Chudasama et al. 2019, *BMC Medicine*, frei
>   lizenziert (CC BY). Jede Zahl ist am Volltext geprüft; die Seitenangaben
>   folgen dem PDF des Verlags (Seite 1 bis 13).
> - **Erfunden** ist die Arbeit, für die ausgewertet wird. Angenommen ist eine
>   Abschlussarbeit mit der Frage: *Wie viele Lebensjahre bringt Bewegung im
>   mittleren Alter?*
> - **Kästen „Warum so?“** erklären, worauf es an einer Stelle ankommt. In
>   deinen eigenen Auswertungen schreibst du sie nicht.
>
> Die Datei liegt bewusst nicht unter `literatur/`: Dort hält der Wächter sie
> für deine eigene Literatur.

---

# Chudasama2019 — Bewegung, Mehrfacherkrankung und Lebenserwartung, UK Biobank

> Kategorie *Bewegung und Lebenserwartung* · aus der Vorlage `vorlagen/auswertung.md`

📄 Volltext · 🔗 [doi:10.1186/s12916-019-1339-0](https://doi.org/10.1186/s12916-019-1339-0)
· Zweck **Kapitel 2, Hintergrund, und Kapitel 5, Diskussion** · Status: **geprüft** · ausgewertet 2026-09-23

> **Register:** keine

*Titel laut Bibliografie:* Physical activity, multimorbidity, and life
expectancy: a UK Biobank longitudinal study

> **Warum so?** Der Kopf sagt in einer Zeile, wofür du die Arbeit brauchst.
> Steht dort kein Zweck, liest du ohne Ziel und notierst alles. In einer
> echten Arbeit stünden bei **Register** die Kennungen der zwei Zahlen, die
> unten unter „Was wir daraus nehmen“ weiterwandern.

### Prüfliste — vor der Zusammenfassung abzuarbeiten

- [x] **Design und Qualität** ausgewiesen: Studientyp, Stichprobe, Nachbeobachtung, Qualitätsbewertung
- [x] **Exposition und Vergleich** wörtlich benannt: wer gegen wen verglichen wird und wie gemessen
- [x] **Endpunkte** ausgewiesen: alle berichteten genannt, der ausgewertete benannt, Definition vermerkt
- [x] **Ergebnisse** mit Seiten- oder Tabellenangabe bei jeder Zahl
- [x] **Übertragung** auf die eigene Fragestellung versucht, Annahmen offengelegt oder Hindernis benannt
- [x] **Verzerrung** geprüft: Adjustierung, Störgrößen, Umkehrkausalität
- [x] **Belastbarkeit** eingestuft: tragend, eingeschränkt oder nicht belastbar, mit Gründen
- [x] **Vorbehalt** vermerkt, wo eine Zahl nicht direkt mit anderen vergleichbar ist
- [x] **Register** nachgezogen, wenn Zahlen weiterverwendet werden, sonst „keine“ — *entfällt im Beispiel*
- [x] **Sammeldokument** nachgezogen: „Was sich abzeichnet“ verweist auf diese Auswertung — *entfällt im Beispiel*
- [x] **Aufgeworfene Fragen** im Fragenteil des Sammeldokuments nachgetragen — *entfällt im Beispiel*
- [x] **Zweck** gesetzt: wofür die Arbeit gebraucht wird

## Fragestellung

Die Studie fragt, wie viel Bewegung das Sterberisiko und die
Lebenserwartung bei Menschen **mit und ohne Mehrfacherkrankung** verändert,
und sie misst Bewegung dafür auf zwei Arten: per Fragebogen und per Gerät am
Handgelenk (S. 1–2).

**Für unsere Arbeit:** Sie gehört zu den wenigen Studien, die nicht nur
Risiken, sondern **gewonnene Lebensjahre** angeben, und zwar schon ab einem
Alter von 45 Jahren (S. 7).

> **Warum so?** Zwei Fragen getrennt halten: was die Studie wissen will und
> was du von ihr willst. Beides deckt sich selten. Hier ist die
> Mehrfacherkrankung das Thema der Studie, für uns nur eine Nebensache.

## Design und Qualität

| | |
|---|---|
| Typ | prospektive Kohortenstudie, UK Biobank; Eingangsuntersuchung 2006–2010, Alter 38 bis 73 Jahre (S. 2) |
| Stichprobe | 491.939 Personen in der Fragebogen-Auswertung, davon 96.622 mit Mehrfacherkrankung, also zwei oder mehr von 36 chronischen Erkrankungen (S. 1–2). In der Geräte-Teilstichprobe 95.616 Personen (S. 7) |
| Nachbeobachtung | Median 7,0 Jahre (IQR 6,3–7,6), 11.479 Todesfälle. In der Geräte-Teilstichprobe Median 6,9 Jahre mit **nur 306 Todesfällen** (S. 7) |
| Auswertung | Cox-Modelle für das Sterberisiko, beim Fragebogen in vier Stufen bis zur Adjustierung für den Lebensstil (S. 3). Lebenserwartung als Fläche unter der Überlebenskurve bis 100 Jahre, gewonnene Jahre als Differenz zweier Kurven (S. 3) |
| Qualität | eigene Einschätzung, keine formale Checkliste: großer, gut dokumentierter Fragebogenarm; der Gerätearm ist deutlich schwächer (siehe „Verzerrung“) |

> **Warum so?** Die Zahl der **Ereignisse** zählt mehr als die Zahl der
> Teilnehmenden. 95.616 Personen klingen nach viel, aber die Gerätezahlen
> beruhen auf 306 Todesfällen. Das erklärt die sehr breiten Intervalle unten.

## Exposition und Vergleich

Bewegung wird dreimal gemessen (S. 2–3):

- **Freizeitbewegung** per Fragebogen: Gehen, Heimwerken, anstrengender Sport
  und anderes in den letzten vier Wochen.
- **Gesamtbewegung** per Fragebogen: Gehen, mittlere und hohe Intensität in
  den letzten sieben Tagen.
- **Gerät:** ein Beschleunigungsmesser am Handgelenk, sieben Tage getragen.
  Eingeteilt wird nach der **mittleren Beschleunigung** in drei gleich große
  Gruppen (Terzile).

**Vergleichsgruppe ist immer die niedrigste Gruppe** (S. 3). Beim Fragebogen
ist das „unter 600 MET-Minuten pro Woche“; diese Grenze entspricht nach den
Autorinnen und Autoren der Empfehlung von 150 Minuten pro Woche (S. 2). Die
mittlere Gruppe reicht von 600 bis unter 3.000, die hohe beginnt bei 3.000.

> **Warum so?** Die Vergleichsgruppe heißt hier „weniger als die
> Empfehlung“, nicht „gar keine Bewegung“. Eine Studie, die gegen völlig
> Inaktive vergleicht, findet größere Effekte, auch wenn Bewegung genau gleich
> wirkt. Deshalb steht die Vergleichsgruppe wörtlich da.

**Eine Falle beim Gerät:** Die Studie übersetzt die Geräte-Terzile in „4, 10
und 22 Minuten zügiges Gehen am Tag“ (S. 7). Gemessen ist aber die Zeit über
einer Beschleunigungsschwelle (250 mg), nicht das Gehen. „Zehn Minuten
zügiges Gehen“ ist also eine Beschreibung der Gruppe, keine gemessene
Gehzeit.

## Endpunkte

**Ausgewertet:** Tod jeder Ursache, aus den Sterberegistern (S. 2). Daraus
abgeleitet: die Lebenserwartung ab einem bestimmten Alter (S. 3).

**Nicht Endpunkt:** Die Mehrfacherkrankung teilt die Teilnehmenden nur in
zwei Gruppen. Über Gesundheit, Pflegebedürftigkeit oder Lebensqualität sagt
die Studie nichts.

> **Warum so?** „Lebensjahre“ und „gesunde Lebensjahre“ sind verschiedene
> Endpunkte. Wer hier „gesunde Jahre“ herausliest, hat falsch gelesen.

## Ergebnisse

**Sterberisiko, Hazard Ratio, voll adjustiertes Modell**, gegen die niedrigste
Gruppe (S. 7; beim Gerät S. 1 und 7):

| Messart | Gruppe | mit Mehrfacherkrankung | ohne Mehrfacherkrankung |
|---|---|---|---|
| Freizeit | mittel | 0,75 (0,70–0,80) | 0,80 (0,76–0,85) |
| Freizeit | hoch | 0,65 (0,56–0,75) | 0,75 (0,68–0,82) |
| gesamt | mittel | 0,86 (0,79–0,93) | 0,83 (0,78–0,89) |
| gesamt | hoch | 0,78 (0,71–0,85) | 0,81 (0,76–0,87) |
| Gerät | mittel | 0,49 (0,29–0,80) | 0,40 (0,29–0,57) |
| Gerät | hoch | 0,29 (0,13–0,61) | 0,29 (0,19–0,46) |

**Gewonnene Lebensjahre mit 45 Jahren** gegen die niedrigste Gruppe
(Fragebogen S. 7, Gerät S. 7 und 9; Abb. 4 auf S. 10):

| Messart | Gruppe | mit Mehrfacherkrankung | ohne Mehrfacherkrankung |
|---|---|---|---|
| Freizeit | mittel | 3,12 (2,53–3,71) | 1,95 (1,59–2,31) |
| Freizeit | hoch | 3,55 (2,34–4,77) | 1,85 (1,19–2,50) |
| gesamt | mittel | 2,04 (1,35–2,74) | 1,79 (1,32–2,27) |
| gesamt | hoch | 2,92 (2,12–3,73) | 1,76 (1,25–2,27) |
| Gerät | mittel | 3,60 (−0,60–7,79) | 3,88 (1,79–6,00) |
| Gerät | hoch | 5,32 (−0,47–11,11) | 4,51 (2,15–6,88) |

Der Gewinn **wird mit dem Alter kleiner** (S. 7). Die Mehrfacherkrankung
selbst kostet mit 45 Jahren 5,15 Lebensjahre, mit 65 Jahren 4,54 (S. 7).

> **Warum so?** Jede Zahl hat ihre Seite, und zu jedem Schätzwert gehört sein
> Intervall. Die Intervalle tragen hier eine eigene Aussage: Beim Gerät mit
> Mehrfacherkrankung schließen sie die Null ein. Ob dort überhaupt ein Gewinn
> besteht, ist statistisch offen.

## Übertragung auf unsere Frage

- **Alter:** Die Zahlen gelten ab 45. Für jüngere Menschen sagt die Studie
  nichts; eine Übertragung wäre eine Annahme.
- **Dosis:** Fast der ganze Gewinn liegt zwischen „niedrig“ und „mittel“. Von
  „mittel“ auf „hoch“ kommt beim Fragebogen ohne Mehrfacherkrankung nichts
  dazu (1,95 gegen 1,85 Jahre, S. 7). Die Autorinnen und Autoren schreiben
  dazu „little additional benefit seen above this amount“ (S. 9).
- **Grenze:** Mit nur drei Gruppen lässt sich keine Kurve zeichnen. Die
  Aussage „ab der Empfehlung kommt kaum mehr dazu“ vergleicht zwei sehr
  breite Gruppen, 600 bis 3.000 gegen über 3.000 MET-Minuten.
- **Bevölkerung:** UK Biobank ist nicht repräsentativ, wohlhabendere Gruppen
  sind überrepräsentiert (S. 9). Für ein anderes Land ist die Übertragung eine
  Annahme, die in die Diskussion gehört.

## Verzerrung und Belastbarkeit

**Umkehrkausalität:** Wer krank ist, bewegt sich weniger und stirbt früher.
Dagegen schließt die Studie alle aus, die in den ersten **zwei Jahren**
gestorben sind (n = 2.416, S. 2). **Das gilt nur für den Fragebogen.** Im
Gerätearm war es wegen der kurzen Nachbeobachtung nicht möglich (S. 11).

**Adjustierung:** Der Fragebogenarm ist bis zum Lebensstil adjustiert, etwa
Rauchen, Alkohol, Ernährung und Sitzzeit (S. 3). Der Gerätearm nur nach Alter,
Geschlecht, Herkunft und sozialer Lage. Für den Lebensstil ging das nicht, weil
er sich bis zur Gerätemessung geändert haben kann (S. 3). Die
Geräte-Teilnehmenden waren außerdem gesünder als die übrigen (S. 9).

> **Warum so?** Hier liegt die wichtigste Lesefalle der Studie. Nebeneinander
> stehen ein Fragebogen-Wert von 0,80 und ein Geräte-Wert von 0,40. Daraus
> liest man leicht: „Der Fragebogen halbiert die Wirkung.“ Aber die beiden
> Zahlen stammen nicht aus derselben Lage. Der Gerätearm hat eine andere
> Teilstichprobe, eine schwächere Adjustierung, keine Zwei-Jahres-Sperre und
> 306 statt 11.479 Todesfälle. Ein Teil des Unterschieds kann also aus der
> Messung kommen, ein Teil aus diesen Unterschieden. Trennen lässt sich das
> mit der Studie nicht.

**Belastbarkeit:**
- **Fragebogenarm: tragend** für die Größenordnung „rund 2 Lebensjahre ab 45
  für die Empfehlung“. Er ist groß und gegen Umkehrkausalität abgesichert;
  vorsichtig bleibt man wegen der Selbstauskunft.
- **Gerätearm: eingeschränkt.** Er taugt nur als Hinweis auf die Richtung,
  nicht als Einzelzahl: wenige Ereignisse, keine Sperrfrist, schwächere
  Adjustierung.

## Stärken

- Groß, und sie gibt **Jahre** an statt nur Risiken (S. 3, 7).
- Zwei Jahre Sperrfrist gegen Umkehrkausalität im Fragebogenarm (S. 2).
- Drei Messarten in derselben Kohorte, also ein seltener Vergleich von
  Fragebogen und Gerät, mit den Vorbehalten oben.

## Schwächen

- Nur drei Gruppen: keine Aussage über die Form der Dosis-Wirkungs-Kurve.
- Der Gerätearm ruht auf 306 Todesfällen; zwei der Intervalle schließen die
  Null ein (S. 7).
- „Minuten zügiges Gehen“ ist keine gemessene Gehzeit (S. 7). *Selbst
  bemerkt.*
- **Ein Intervall ist in sich widersprüchlich:** Die Mehrfacherkrankung
  kostet „5.15 (95% CI 4.78, 5.14)“ Jahre (S. 7). Die Obergrenze liegt unter
  dem Schätzwert; das ist vermutlich ein Druckfehler. *Selbst bemerkt.*

> **Warum so?** „Selbst bemerkt“ trennt deine Kritik von der Kritik, die die
> Autorinnen und Autoren selbst üben. Beides ist erlaubt, aber man muss sehen
> können, von wem was stammt.

## Was wir daraus nehmen

1. **Die Größenordnung:** Wer mit 45 Jahren die Bewegungsempfehlung erfüllt,
   gewinnt im Vergleich zu weniger Aktiven im Mittel rund **2 Lebensjahre**
   ohne Mehrfacherkrankung und rund **3** mit Mehrfacherkrankung
   (Freizeitbewegung, 1,95 und 3,12 Jahre, S. 7). Das kommt in Kapitel 2.
2. **Die Kränkeren gewinnen mehr** (3,12 gegen 1,95 Jahre, S. 7). Das kommt in
   die Diskussion, Kapitel 5.
3. **Über der Empfehlung kommt wenig dazu** (S. 7, 9), mit dem Vorbehalt der
   nur drei Gruppen. Das kommt in Kapitel 2, als Hinweis, nicht als Kurve.

**Was wir nicht daraus nehmen.**
- Keine Kurvenform: Dafür reichen drei Gruppen nicht.
- Keine „gesunden Jahre“: Der Endpunkt ist der Tod.
- Keine Einzelzahl aus dem Gerätearm.
- Nicht den Satz „der Fragebogen halbiert die Wirkung“, weil die beiden Arme
  nicht vergleichbar sind (siehe „Verzerrung“).

> **Warum so?** Was du *nicht* übernimmst, ist genauso wichtig wie das, was du
> übernimmst. Hier steht, welche naheliegenden Schlüsse du bewusst nicht
> ziehst. Das schützt dich später beim Schreiben, wenn du die Studie nur noch
> aus der Erinnerung kennst.

---

Zurück zu [2 · Auswertung](2-auswertung.md) · zur Vorlage [`vorlagen/auswertung.md`](../vorlagen/auswertung.md) · zur [Übersicht](../README.md)
