# KI, Plagiat und Eidesstattliche Erklärung

<sub>🚶 machst du selbst · 🤖 erledigt Claude Code für dich · 💻 erledigt ein Programm von selbst</sub>

**Lies das vor allem anderen.** Dieses Kit arbeitet mit einem KI-Assistenten.
Ob und wie du KI in deiner Arbeit verwenden darfst, entscheidet nicht das Kit,
sondern deine Hochschule und deine Betreuung.

## 1. Vorher klären: Darfst du mit KI arbeiten, und wie?

1. 🚶 **Lies die Regeln deiner Hochschule:** den Leitfaden deines Studiengangs
   zum wissenschaftlichen Arbeiten, die Richtlinie zur guten
   wissenschaftlichen Praxis und den Text der Eidesstattlichen Erklärung, die
   du mit deiner Arbeit unterschreibst.
2. 🚶 **Frag deine Betreuung,** ob und wofür sie KI in deiner Arbeit erlaubt: zum
   Suchen, Zusammenfassen, Rechnen, Programmieren, für Textentwürfe oder nur
   zum sprachlichen Glätten.
3. 🚶 **Halte die Antwort fest,** als ersten Eintrag in
   [`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md): was erlaubt ist, was nicht und
   wie du es offenlegst, mit Quelle und Datum, etwa „E-Mail der Betreuung vom
   …“.
4. 🚶 **Ist KI nicht erlaubt,** ist dieses Kit nicht das richtige Werkzeug für
   deine Arbeit.

> **Beispiel: FH JOANNEUM, Institut eHealth.** Stand: „Leitfaden für
> wissenschaftliche Arbeiten bei GEB und EHT“, Version 2.0 vom Oktober 2024,
> und die LaTeX-Vorlage für Abschlussarbeiten, Fassung 2024-05.
> - **Zitieren von KI (Leitfaden, Abschnitt 6.3):** Erzeugt die KI Wissen oder
>   inhaltliche Passagen, zitierst du sie nach APA. Übersetzt sie nur oder
>   verbessert sie den Stil, entfällt das Zitat; das erläuterst du allenfalls
>   im Methodenteil.
> - **Eidesstattliche Erklärung (Vorlage):** Du erklärst unter anderem, alle
>   verwendeten Hilfsmittel in der Methodendarstellung oder einem Verzeichnis
>   deklariert zu haben, ausdrücklich auch KI-Assistenzsysteme wie Chatbots,
>   und ihre Verwendung bei den entsprechenden Textstellen angegeben zu haben.
> - **Prüfung:** Laut Erklärung kann die Arbeit auf Plagiate und auf Texte
>   fremder Herkunft geprüft werden, von Menschen (Ghostwriting) wie von
>   KI-Systemen. Abschlussarbeiten werden mit Plagiatssoftware geprüft
>   (Leitfaden, Abschnitt 6).
> - **Folgen:** Eine wahrheitswidrige Erklärung kann laut Erklärung zu einer
>   negativen Beurteilung, zur nachträglichen Aberkennung des Titels und zu
>   Strafverfolgung führen.
>
> Diese Zusammenfassung ersetzt die Dokumente nicht. Maßgeblich ist ihre
> jeweils gültige Fassung.

## 2. Was als Plagiat gilt

- **Ein Plagiat** ist, fremde Formulierungen, Ideen oder Ergebnisse als eigene
  auszugeben, ohne die Quelle zu nennen. Das gilt für Texte von Menschen und
  ebenso für KI-Texte, die du nicht offenlegst.
- **KI-Text kann fremden Text enthalten.** Ein Sprachmodell kann Formulierungen
  wiedergeben, die es beim Training gesehen hat, ohne die Quelle zu nennen.
  Übernimmst du so einen Satz, übernimmst du womöglich ein Plagiat, ohne es zu
  merken.
- **Frühere Fassungen zählen mit.** Plagiatssoftware findet auch öffentliche
  Entwürfe deiner eigenen Arbeit. Deshalb ist dein Repository privat.

## 3. Nichts blind übernehmen

Jede Zusammenfassung, jede Auswertung und jeden Textentwurf von Claude Code
liest du ganz, bevor du etwas davon übernimmst. Warum:

- **KI macht Fehler, die überzeugend klingen.** Sie liest die falsche Zeile
  einer Tabelle ab, verwechselt Vergleichsgruppen, schreibt einer Studie
  Aussagen zu, die nicht darin stehen, oder nennt Quellen, die es nicht gibt.
  Der Text liest sich trotzdem flüssig und sicher.
- **Du trägst die Verantwortung.** Mit der Eidesstattlichen Erklärung stehst
  du für jeden Satz und jede Zahl ein, nicht die KI.
- **Du musst es erklären können.** Betreuung und Prüfung fragen, warum etwas
  so ist. Was du nur übernommen hast, kannst du nicht verteidigen.
- **Die Arbeit soll zeigen, was du kannst.** Die KI hilft dir dabei; sie
  ersetzt dein Verständnis nicht.

🚶 So gehst du vor:

1. Jede Zusammenfassung und jeden Entwurf ganz lesen.
2. Jede Zahl am Original prüfen: die genannte Seite oder Tabelle aufschlagen
   und vergleichen.
3. Bei jeder Aussage fragen: Steht das wirklich so in der Quelle?
4. Im [KI-Protokoll](../KI-PROTOKOLL.md) vermerken, was du geprüft hast und
   mit welchem Ergebnis.
5. Was du nicht prüfen konntest, als „zu prüfen“ kennzeichnen statt
   übernehmen.

## 4. Was du dem KI-Dienst gibst

Was Claude Code liest, schickt es zur Verarbeitung an die Server von
Anthropic. Kläre deshalb vorher:

- **Volltexte:** ob die Lizenzen deiner Bibliothek oder der Verlage erlauben,
  Artikel so zu verarbeiten.
- **Daten über Personen:** Interviews, Fragebögen oder Gesundheitsdaten gehören
  nicht ungefragt in einen KI-Dienst. Kläre das mit deiner Betreuung und mit
  der Stelle für Datenschutz deiner Hochschule.

## 5. Offenlegen

- [`KI-PROTOKOLL.md`](../KI-PROTOKOLL.md) sammelt laufend, was du offenlegen
  musst; die Vorlage dazu ist
  [`vorlagen/ki-protokoll-eintrag.md`](../vorlagen/ki-protokoll-eintrag.md).
- Wie du offenlegst, im Methodenteil, in einem Verzeichnis oder mit Zitat an
  der Textstelle, bestimmt der Leitfaden deiner Hochschule.
- Am Ende übernimmst du daraus die Angaben in deine Arbeit.

Weiter: [0 · Einrichten](0-einrichten.md) · siehe auch
[Bei jedem Schritt](bei-jedem-schritt.md#das-ki-protokoll) · zurück zur
[Übersicht](../README.md)
