# 3 · Modell (wahlweise)

**Worum es geht:** Manche Arbeiten rechnen selbst. Sie schätzen zum Beispiel
Kosten, rechnen ein Ergebnis auf eine andere Gruppe um oder fassen Zahlen
aus mehreren Studien zusammen. Dieser Schritt beschreibt, wie so eine
Rechnung nachvollziehbar bleibt. Rechnet deine Arbeit nicht, überspringst du
ihn.

**Was am Ende da ist:** ein Rechenprogramm im Ordner `analysis/`, seine
Ergebnisse an markierten Stellen deiner Dokumente und eine Beschreibung der
Rechenschritte.

## Die Regeln

1. **Zahlen hinein nur mit Fundstelle.** Jeder Eingabewert kommt aus dem
   Zahlenregister [`data/register.yaml`](../data/register.yaml), also aus
   einer Auswertung mit Seite oder Tabelle, oder ist ausdrücklich als Annahme
   gekennzeichnet.
2. **Gerechnet wird in einem Programm,** nicht von Hand und nicht in einer
   Tabellenkalkulation. Ein Programm rechnet beim nächsten Mal genauso, und
   jede Änderung steht im Git-Verlauf. Claude Code schreibt dir das Programm,
   meist in Python, und erklärt es Schritt für Schritt.
3. **Ergebnisse schreibt das Programm selbst in den Text.** Es setzt sie
   zwischen zwei Kommentarzeilen wie `<!-- ergebnis:start -->` und
   `<!-- ergebnis:ende -->`, etwa in die Kurzfassung des Sammeldokuments.
   Diese Stellen änderst du nie von Hand; rechnet das Programm neu, stimmen sie
   wieder. So steht es auch in Regel 6 von [`CLAUDE.md`](../CLAUDE.md).
4. **Abbildungen entstehen aus dem Programm,** nicht durch Abmalen oder
   Nachbauen von Hand.
5. **Annahmen offenlegen und durchspielen.** Jede Annahme steht im Programm
   mit Begründung. Dazu rechnest du sie einmal am oberen und am unteren Rand
   ihrer möglichen Werte, damit du siehst, wie stark das Ergebnis an ihr hängt.
6. **Tests mit festen Sollwerten.** Ein kleiner Test prüft, ob das Programm
   für bekannte Eingaben das bekannte Ergebnis liefert. Ändert sich später
   etwas am Programm, fällt ein Fehler sofort auf.
7. **Die Rechenschritte beschreiben,** in einem eigenen Dokument in
   `analysis/`: was jeder Schritt tut, warum, und woher seine Zahlen kommen.
   So lässt sich die Rechnung auch ohne das Programm nachvollziehen.

> „Ich möchte aus den Zahlen im Register die Kosten je Person schätzen. Schlag
> mir vor, wie wir das Programm aufbauen, und zeig mir die Annahmen, die ich
> entscheiden muss.“

Die Annahmen sind Weichenstellungen: Sie kommen mit Begründung nach
[`ENTSCHEIDUNGEN.md`](../ENTSCHEIDUNGEN.md), siehe
[5 · Entscheidung](5-entscheidung.md).

## Was das Kit dafür noch nicht mitbringt

Werkzeuge für diesen Schritt gibt es bisher nur in der Arbeit, aus der das Kit
stammt; sie stehen im [`BACKLOG.md`](../BACKLOG.md). Bis dahin baut Claude Code
sie dir nach den Regeln oben.

Weiter: [4 · Sammeldokumente](4-sammeldokumente.md) · zurück zur [Übersicht](../README.md)
