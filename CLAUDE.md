# Arbeitsregeln für den KI-Assistenten

Diese Datei liest Claude Code beim Start jeder Sitzung; das Kit ist für Claude
Code gebaut. Sie gilt für alles in diesem Repository. Passe sie an deine Arbeit
an, aber lass die Grundregeln stehen.

## Grundregeln

1. **Keine Zahl ohne Fundstelle.** Jede Zahl im Repository trägt ihre Herkunft:
   Quelle mit Seite, Tabelle oder Abbildung, oder ausdrücklich „eigene Rechnung“,
   „Annahme“ oder „zu prüfen“. Erfundene oder geschätzte Zahlen ohne diese
   Kennzeichnung sind verboten, auch als Beispiel.
2. **Nur aus dem Volltext zitieren.** Zahlen und Aussagen aus Abstracts oder aus
   Suchdiensten gelten als Hinweis, nicht als Beleg. Übernommen wird erst nach
   der Auswertung des Volltexts.
3. **Metadaten aus Crossref.** Autorinnen, Autoren und Jahr nie aus einem
   Suchdienst übernehmen, sondern über [`tools/doi2bib.py`](tools/doi2bib.py).
4. **Erst Optionen, dann Ausführung.** Bei Weichenstellungen (Methode, Quelle,
   Gliederung, Annahme) zeigt der Assistent die Optionen mit Vor- und Nachteilen
   und eine Empfehlung. Entscheiden tut die Person, die die Arbeit schreibt.
   Die Entscheidung kommt mit Begründung nach [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md).
5. **Erkenntnisse in die Sammeldokumente.** Ergebnisse, Bilanzen und neue
   Fragen gehören in das Sammeldokument der Kategorie
   (`literatur/<kategorie>/<kategorie>.md`), nicht in neue Einzeldateien.
6. **Zahlen aus eigenen Rechnungen nicht von Hand übertragen.** Ein Skript
   schreibt seine Ergebnisse selbst in markierte Blöcke
   (`<!-- name:start -->` … `<!-- name:ende -->`). Diese Blöcke nie von Hand
   ändern; Texte verweisen auf sie.
7. **Volltexte nur aus legalen Quellen.** Offene Fassungen über
   [`tools/holpdf.py`](tools/holpdf.py), alles andere über den Zugang der Hochschulbibliothek.
   Volltexte werden nie versioniert (`literatur/**/pdf/` steht in `.gitignore`).
8. **Nichts still ändern.** Ältere Entscheidungen und Statusvermerke bleiben
   stehen und bekommen einen datierten Nachtrag („Nachgezogen <Datum>: …“).
9. **KI-Einsatz protokollieren.** Nach jedem Arbeitsgang ein Eintrag in
   [`KI-PROTOKOLL.md`](KI-PROTOKOLL.md) (Vorlage: [`vorlagen/ki-protokoll-eintrag.md`](vorlagen/ki-protokoll-eintrag.md)): was die KI
   gemacht hat und was am Original geprüft wurde.
10. **Wächter nicht umgehen.** Commits laufen durch [`tools/pruefe.py`](tools/pruefe.py) und die
    Tests. `git commit --no-verify` nur bewusst, mit Grund im Protokoll.
11. **Git ist Pflicht.** Nach jedem abgeschlossenen Arbeitsschritt ein Commit
    mit einer Notiz, was sich geändert hat und warum. Am Ende jeder Sitzung
    pushen, wenn die Person nichts anderes sagt. Nie Volltexte, Ausgaben der
    Arbeit oder persönliche Daten committen.
12. **Der Text der Arbeit ist LaTeX oder Markdown.** Er entsteht in `arbeit/`
    als `.tex` oder `.md`. Word und PDF sind Ausgaben nach `arbeit/ausgabe/`:
    nie die Quelle, nie von Hand bearbeitet.

## Datenschutz

- Die eigene E-Mail-Adresse steht nur in der Umgebungsvariable
  `UNPAYWALL_EMAIL` und geht nur an Unpaywall. Sie kommt in keine Datei des
  Repositorys und an keinen anderen Dienst.
- Keine personenbezogenen Daten Dritter ins Repository.
- Exporte aus Suchdiensten mit eingeschränkter Lizenz bleiben lokal.

## Einrichten

Bittet die Person darum, etwa mit „Prüfe, ob das Kit eingerichtet ist“, geh so
vor und erkläre jeden Schritt in einem Satz:

1. Python finden: `python3`, sonst `python` oder `py`; nötig ist Version 3.9
   oder neuer.
2. PyYAML prüfen (`<python> -c "import yaml"`) und, wenn es fehlt,
   installieren. Windows: `py -m pip install pyyaml`. macOS:
   `python3 -m pip install --user pyyaml`. Linux (Ubuntu, Debian):
   `sudo apt install python3-yaml`; dieser Befehl braucht das Passwort der
   Person, also bitte sie, ihn selbst einzugeben.
3. Den Wächter einschalten: `git config core.hooksPath tools/hooks`.
4. Tests und Wächter laufen lassen:
   `<python> -m unittest discover -s tests -t .` und `<python> tools/pruefe.py`.
5. Fragen, ob Volltexte automatisch geholt werden sollen. Dann erklären, wie
   die Person `UNPAYWALL_EMAIL` setzt ([`ablauf/0-einrichten.md`](ablauf/0-einrichten.md), Schritt 6).
   Die Adresse nie selbst in eine Datei schreiben.
6. Mit der Person [`STAND.md`](STAND.md), Abschnitt 1, ausfüllen: Fragestellung, Abgabe,
   Umfang, Betreuung.

## Ablauf, kurz

Einrichten → Recherche (`notes/recherche/`) → Volltext (`literatur/<kategorie>/pdf/`) →
Auswertung mit Prüfliste (`literatur/<kategorie>/<Schlüssel>_auswertung.md`) →
wahlweise Modell (`analysis/`) → Sammeldokument → Entscheidung
([`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md)) → Text (`arbeit/`).
Den Stand und die nächsten Schritte hält [`STAND.md`](STAND.md) fest. Die Anleitung zu
jedem Schritt steht in `ablauf/`, die Übersicht im README.

**Vorlagen sind Vorschläge.** Beim Ausfüllen einer Vorlage schlägt der
Assistent die Optionen vor, die zur Arbeit passen, statt jeden Abschnitt
schematisch zu füllen. Die Blöcke **Optionen** und **Beispiel** kommen nach
dem Ausfüllen weg. Fest ist nur, was die Werkzeuge lesen (README, Abschnitt
„Vorlagen anpassen“).

## Sprache und Stil

- **Einfach erklären.** Die Person ist vielleicht keine Informatikerin und kein
  Informatiker. Erkläre Fachwörter aus der Informatik (Commit, Terminal, Pfad,
  Umgebungsvariable …) beim ersten Gebrauch in einem Satz. Sag, was ein Befehl
  tut, bevor du ihn ausführst. Technische Schritte erledigst du selbst, statt
  sie der Person aufzutragen, soweit deine Berechtigungen das erlauben.
- Geschlechtergerecht formulieren.
- Knapp, in ganzen Sätzen, ohne Füllwörter.
- Fachbegriffe einheitlich verwenden; eine Begriffsliste lohnt sich, sobald
  die Arbeit in einer anderen Sprache geschrieben wird als die Notizen.
