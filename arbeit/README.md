# Die Arbeit selbst

Hier schreibst du den Text deiner Arbeit, als **LaTeX** (`.tex`) oder als
**Markdown** (`.md`). Nicht in Word: Bei einer Word-Datei kann Git nicht
zeigen, was sich geändert hat. Warum das zählt, steht in
[Bei jedem Schritt](../ablauf/bei-jedem-schritt.md#git-ist-pflicht).

**Word und PDF sind nur Ausgaben.** Du erzeugst sie aus dem Text in den Ordner
`arbeit/ausgabe/`. Dieser Ordner ist vom Repository ausgenommen; du
bearbeitest nur den Text. Wie das geht, steht in
[5 · Schreiben](../ablauf/5-schreiben.md).

**Vorlagen der Hochschule sind nicht enthalten.** Hol sie dir über die
offiziellen Kanäle deines Studiengangs und leg sie hier ab. Ob sie in ein
öffentliches Repository dürfen, klärst du mit deiner Hochschule; dein eigenes
Repository ist ohnehin privat.

**Die Literaturliste** liegt im Hauptordner als
[`literatur.bib`](../literatur.bib):

- LaTeX: `\bibliography{../literatur}` mit BibTeX oder
  `\addbibresource{../literatur.bib}` mit biblatex.
- Markdown: pandoc mit `--citeproc --bibliography=literatur.bib`; zitiert wird
  mit `[@Schlüssel]`.

**Zahlen** kommen nicht von Hand in den Text, sondern aus den Auswertungen,
dem Zahlenregister [`data/register.yaml`](../data/register.yaml) oder aus den
Ergebnisblöcken deiner eigenen Rechnungen.
