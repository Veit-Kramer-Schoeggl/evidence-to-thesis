# Prüfliste festlegen

<sub>🚶 machst du selbst · 🤖 erledigt Claude Code für dich · 💻 erledigt ein Programm von selbst</sub>

**Worum es geht:** Bevor du die erste Arbeit auswertest, legst du fest, worauf
du bei jeder Arbeit achtest. Diese Punkte bilden die Prüfliste, die in jeder
Auswertung oben steht. Der Wächter verlangt sie von jeder Auswertung, die auf
„geprüft“ steht.

Die Prüfliste des Kits ist ein Vorschlag für empirische Studien. Deine Arbeit
braucht vielleicht andere Punkte: Eine qualitative Studie hat keine
Endpunkte, eine Übersichtsarbeit braucht eine Bewertung ihrer Suche, eine
technische Arbeit eher Punkte zu Software oder Messgeräten.

## So gehst du vor

1. 🚶 **Den Vorschlag ansehen.** Die Prüfliste steht in
   [`vorlagen/auswertung.md`](../vorlagen/auswertung.md), zwischen den
   Kommentarzeilen `pruefliste:start` und `pruefliste:ende`.
2. 🚶 **Überlegen, was deine Arbeit braucht.** Drei Fragen helfen:
   - Was muss ich von jeder Arbeit wissen, bevor ich sie verwenden darf? Etwa
     das Studiendesign, die Stichprobe, die Messmethode.
   - Was geht bei Arbeiten meines Fachs typischerweise schief? Etwa Verzerrung,
     eine fehlende Vergleichsgruppe, eine sehr kleine Stichprobe.
   - Was muss ich später wiederfinden? Etwa die Fundstelle jeder Zahl oder
     wofür ich die Arbeit brauche.
3. 🤖 🚶 **Mit Claude Code besprechen.**
   > „Hier ist meine Fragestellung. Welche Prüfpunkte schlägst du für die
   > Auswertung vor, mit Begründung? Was aus dem Vorschlag des Kits brauche ich
   > nicht?“

   Claude Code zeigt Optionen, du entscheidest.
4. 🤖 **Eintragen.** Jeder Punkt ist eine Zeile in der Form
   `- [ ] **Name** was zu tun ist`. Den fett gesetzten Namen sucht der Wächter
   in jeder Auswertung; halte ihn kurz.
5. 🤖 **Die Pflichtabschnitte anpassen.** Der Kommentar `pflichtabschnitte:`
   darunter nennt die Überschriften, die jede Auswertung haben muss. Ändere
   ihn, wenn du Abschnitte umbenennst oder streichst.
6. 🤖 🚶 **Festhalten.** Die Prüfliste ist eine Weichenstellung. Sie bekommt einen
   Eintrag in [`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md): welche Punkte du
   gestrichen oder ergänzt hast, und warum. Siehe
   [5 · Entscheidung](5-entscheidung.md).
7. 💻 **Prüfen.**
   > „Prüfe, ob die Vorlage und der Wächter zusammenpassen.“

   Claude Code lässt dann die Tests und den Wächter laufen.

## Mögliche Prüfpunkte je nach Art der Studien

Vorschläge, keine Pflicht. Für die Bewertung der Qualität nennt die Vorlage
anerkannte Checklisten wie AMSTAR 2, RoB 2 oder die Newcastle-Ottawa-Skala.

| Art der Studien | mögliche Prüfpunkte |
|---|---|
| Kohorten- und Fall-Kontroll-Studien | Exposition und Vergleich, Endpunkte, Verzerrung (Störgrößen, Umkehrkausalität), Überlappung der Kohorten |
| randomisierte Studien | Zufallszuteilung und Verblindung, Abbrüche, Auswertung nach Zuteilung |
| Übersichtsarbeiten und Metaanalysen | Suche (Datenbanken, Zeitraum), Qualitätsbewertung der eingeschlossenen Studien, Unterschiede zwischen den Studien, Doppelzählung |
| qualitative Studien | Stichprobe und Kontext, Erhebung, Auswertung, Rolle der Forschenden |
| Mess- und Validierungsstudien | Gerät und Messort, Vergleichsmethode, Bedingungen, Fehler je Bedingung |
| technische Arbeiten und Software | Version und Verfügbarkeit, Testdaten, Nachvollziehbarkeit |

## Wenn du die Prüfliste später änderst

- **Ein neuer Punkt:** Der Wächter nennt jede Auswertung, der er fehlt, bei
  „in Arbeit“ als Hinweis, bei „geprüft“ als Fehler. So geht der Punkt in
  keiner Auswertung verloren.
- **Ein Punkt passt bei einer einzelnen Arbeit nicht:** „entfällt“ mit Grund
  dahinter schreiben und abhaken.
- **Festhalten:** als datierten Nachtrag zum Eintrag in
  [`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md).

Weiter: [1 · Recherche](1-recherche.md) · siehe auch
[2 · Auswertung](2-auswertung.md) · zurück zur [Übersicht](../README.md)
