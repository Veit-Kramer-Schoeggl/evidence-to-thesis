# 5 · Schreiben

**Worum es geht:** aus dem Gesammelten den Text machen, und zwar in einem
Format, das Git versionieren kann.

## LaTeX oder Markdown, nicht Word

Bei Textdateien zeigt Git Zeile für Zeile, was sich wann geändert hat. Eine
Word-Datei ist dagegen gepackt: Git sieht nur, dass sie sich geändert hat,
nicht was. Deshalb schreibst du deine Arbeit als Text, in LaTeX oder in
Markdown. Beide Formate lesen Menschen und Programme gleichermaßen, und Claude
Code kann in beiden schreiben und prüfen.

| | LaTeX | Markdown |
|---|---|---|
| passt, wenn | deine Hochschule eine LaTeX-Vorlage hat, du Formeln brauchst oder das Layout genau steuern willst | du einfach schreiben willst |
| Datei | `arbeit/arbeit.tex` | `arbeit/arbeit.md` |
| zitieren | `\cite{Mustermann2020}` | `[@Mustermann2020]` oder `[@Mustermann2020, S. 5]` |
| daraus wird | ein PDF | eine Word-Datei oder ein PDF, mit dem Programm pandoc |

## Word und PDF sind nur Ausgaben

Du erzeugst sie aus dem Text, gibst sie ab oder schickst sie deiner Betreuung.
Von Hand bearbeitest du sie nicht: Jede Änderung machst du im Text und
erzeugst die Ausgabe neu. Ausgaben gehören nach `arbeit/ausgabe/`; dieser
Ordner ist vom Repository ausgenommen.

Kommentiert deine Betreuung in einer Word-Datei, überträgst du die Änderungen
in den Text. Claude Code kann dir die Kommentare dafür auflisten.

### Aus Markdown eine Word-Datei machen

Dafür gibt es das freie Programm pandoc. Einmal installieren:

- Windows: `winget install --source winget --exact --id JohnMacFarlane.Pandoc`
- macOS: `brew install pandoc`
- Linux: `sudo apt install pandoc`. Für das Zitieren brauchst du pandoc ab
  Version 2.11; ist die Fassung deines Systems älter, hilft
  [pandoc.org/installing.html](https://pandoc.org/installing.html).

Dann erzeugt dieser Befehl die Word-Datei, mit Literaturverzeichnis:

```bash
pandoc arbeit/arbeit.md --citeproc --bibliography=literatur.bib -o arbeit/ausgabe/arbeit.docx
```

Hast du die Word-Vorlage deiner Hochschule, nimmt pandoc deren Schriften und
Abstände:

```bash
pandoc arbeit/arbeit.md --citeproc --bibliography=literatur.bib --reference-doc=arbeit/vorlage.docx -o arbeit/ausgabe/arbeit.docx
```

Den Zitierstil, etwa APA, legst du mit einer CSL-Datei fest. Passende Dateien
gibt es im [Zotero-Stilverzeichnis](https://www.zotero.org/styles); du gibst
sie mit `--csl=arbeit/apa.csl` an.

### Aus LaTeX ein PDF machen

Dafür brauchst du eine LaTeX-Installation, etwa TeX Live (Linux, Windows),
MiKTeX (Windows) oder MacTeX (macOS). Welche zur Vorlage deiner Hochschule
passt, klärt Claude Code mit dir.

> „Erzeuge mir aus arbeit.tex ein PDF in arbeit/ausgabe.“

## Zahlen im Text

Zahlen schreibst du nicht aus dem Gedächtnis, sondern aus der Auswertung mit
ihrer Fundstelle oder aus dem Zahlenregister. Ergebnisse eigener Rechnungen
überträgt am besten das Rechenskript selbst, siehe Regel 6 in [`CLAUDE.md`](../CLAUDE.md).

## Vorher: die Merkliste

Was dir beim Lesen für den Text auffällt, sammelst du vorher in
[`notes/merkliste.md`](../notes/merkliste.md), nach Kapiteln geordnet, mit Fundstelle.

Zurück zur [Übersicht](../README.md) · siehe auch [Bei jedem Schritt](bei-jedem-schritt.md)
