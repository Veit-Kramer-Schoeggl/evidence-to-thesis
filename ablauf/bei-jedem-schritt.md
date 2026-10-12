# Bei jedem Schritt: Git, Wächter, KI-Protokoll

<sub>🚶 machst du selbst · 🤖 erledigt Claude Code für dich · 💻 erledigt ein Programm von selbst</sub>

Drei Dinge begleiten jeden Schritt von der Recherche bis zum Text.

## Git ist Pflicht

**Was Git macht.** Git speichert jeden Stand deiner Arbeit, mit Datum und
einer kurzen Notiz, was sich geändert hat und warum. Ein gespeicherter Stand
heißt *Commit*. Mit *Push* lädst du deine Commits zu GitHub hoch; dort liegt
eine Sicherung.

**Warum es bei einer wissenschaftlichen Arbeit Pflicht ist.** Gute
wissenschaftliche Praxis verlangt, dass nachvollziehbar dokumentiert ist, wie
ein Ergebnis zustande kam. Im Kodex der Deutschen Forschungsgemeinschaft heißt
es dazu (Leitlinie 12, „Dokumentation“): Wissenschaftlerinnen und
Wissenschaftler „dokumentieren alle für das Zustandekommen eines
Forschungsergebnisses relevanten Informationen so nachvollziehbar, wie dies im
betroffenen Fachgebiet erforderlich und angemessen ist, um das Ergebnis
überprüfen und bewerten zu können“
([DFG-Kodex](https://wissenschaftliche-integritaet.de/kodex/)). Was deine
Hochschule im Einzelnen verlangt, steht in ihren eigenen Richtlinien zur
guten wissenschaftlichen Praxis.

Mit Git hast du das nebenbei:

- **Nachvollziehbar:** Zu jeder Zahl siehst du, wann sie dazukam und wann sie
  sich geändert hat.
- **Umkehrbar:** Du kannst zu jedem früheren Stand zurück.
- **Belegbar:** Der Verlauf zeigt, dass du deine Arbeit Schritt für Schritt
  selbst erarbeitet hast, auch dort, wo eine KI geholfen hat.
- **Gesichert:** Geht dein Rechner kaputt, fehlt höchstens die Arbeit seit dem
  letzten Push.

### Im Alltag

- Nach jedem abgeschlossenen Arbeitsschritt ein Commit, mit einer Notiz, was
  sich geändert hat und warum.
- Am Ende jeder Sitzung ein Push.
- 🤖 Claude Code erledigt beides: „Speichere den Stand mit Git und lade ihn hoch.“

Wer es selbst machen will:

```bash
git status                                   # was hat sich geändert?
git add -A                                   # alle Änderungen vormerken
git commit -m "Mustermann 2020 ausgewertet"  # Stand speichern, mit Notiz
git push                                     # zu GitHub hochladen
git log --oneline                            # die letzten Stände ansehen
```

### Was ins Repository gehört und was nicht

🚶 Du entscheidest, was gespeichert wird; 💻 Git hält sich dabei an die Datei
[`.gitignore`](../.gitignore); 🤖 Claude Code trägt neue Ausnahmen für dich ein.

**Die Datei `.gitignore`** liegt im Hauptordner. Jede Zeile nennt eine Datei,
einen Ordner oder ein Muster, das Git nicht speichern soll. Diese Dateien
bleiben auf deinem Rechner, kommen aber in keinen Commit und nicht zu GitHub.

| gehört ins Repository | gehört nicht hinein und steht deshalb in `.gitignore` |
|---|---|
| der Text deiner Arbeit (`.tex`, `.md`) | Volltexte (`literatur/**/pdf/`): urheberrechtlich geschützt |
| Auswertungen, Sammeldokumente, Rechercheprotokolle | Word- und PDF-Ausgaben (`arbeit/ausgabe/`): entstehen aus dem Text |
| Zahlenregister, Literaturliste, Beschaffungsliste | Exporte aus Suchdiensten (`notes/recherche/exporte/`): Lizenz verbietet die Weitergabe |
| Entscheidungen, Stand, KI-Protokoll, Merkliste | Zugangsdaten in einer Datei `.env` |
| Programme, Tests und Vorlagen | Zwischendateien von LaTeX (`*.aux`, `*.log` …) und Python (`__pycache__/`) |
| Abbildungen, die deine Programme erzeugen | Einstellungen von Editor und System (`.idea/`, `.vscode/`, `.DS_Store`) |

**Nie ins Repository, auch nicht in ein privates:**

- Passwörter, Zugangsschlüssel und deine E-Mail-Adresse;
- Daten über Personen, etwa Interviews oder Gesundheitsdaten, solange die
  Regeln deiner Hochschule das nicht ausdrücklich erlauben.

**Eine Ausnahme ergänzen:** eine neue Zeile in `.gitignore`, etwa
`interviews/` für einen ganzen Ordner oder `*.docx` für alle Word-Dateien. Ein
`!` davor nimmt eine Datei wieder auf, etwa `!arbeit/vorlage.docx`.

> „Nimm den Ordner interviews in die .gitignore auf.“

**Prüfen, was gespeichert würde:** `git status` zeigt alle geänderten Dateien,
die Git speichern würde. Warum eine Datei fehlt, zeigt
`git check-ignore -v <datei>`.

**Schon gespeichert?** `.gitignore` wirkt nur für Dateien, die noch nicht im
Repository sind. Ist etwas versehentlich hineingeraten, bitte Claude Code, es
herauszunehmen. War es ein Passwort oder ein Zugangsschlüssel, ändere es
sofort: Im Verlauf steht es weiterhin, und nach einem Push auch bei GitHub.

## Der Wächter

💻 Läuft von selbst. Wozu es Hook, Wächter und Tests gibt, erklärt
[Die Bausteine](bausteine.md#der-hook).

Vor jedem Commit startet Git den Wächter, das Programm [`tools/pruefe.py`](../tools/pruefe.py), und
danach die Tests. Findet er einen Fehler, hält er den Commit auf und sagt,
was fehlt. Bei Entwürfen im Status „in Arbeit“ gibt er nur Hinweise.

Er prüft:

- die Auswertungen: Kopf, Prüfliste, Pflichtabschnitte und, bei „geprüft“,
  den Link im Sammeldokument;
- das Zahlenregister: eine Fundstelle bei jeder Zahl;
- den Bestand: Protokolle, Volltexte und Auswertungen passen zusammen;
- die Links: keiner zeigt ins Leere.

Er merkt nicht, wenn du beim Abschreiben zwei Ziffern vertauschst, eine
Vergleichsgruppe falsch verstehst oder ein Sammeldokument inhaltlich nicht
mehr stimmt. Dafür sind die Prüfliste und dein eigener Blick da.

Im Notfall erzwingt `git commit --no-verify` einen Commit trotz Fehler. Das ist
dann eine bewusste Entscheidung; schreib den Grund in die Commit-Notiz.

## Das KI-Protokoll

🤖 Claude Code schreibt den Eintrag, 🚶 du ergänzt, was du geprüft hast.

Nach jedem Arbeitsgang mit KI kommt ein Eintrag in [`KI-PROTOKOLL.md`](../KI-PROTOKOLL.md), nach der
Vorlage [`vorlagen/ki-protokoll-eintrag.md`](../vorlagen/ki-protokoll-eintrag.md). Er hält fest:

- den Auftrag,
- das Werkzeug mit Version, bei Claude Code auch das Modell,
- was die KI getan hat,
- was du selbst am Original geprüft hast,
- was davon in deine Arbeit geht.

Claude Code schreibt den Eintrag am Ende eines Arbeitsgangs; du ergänzt, was
du selbst geprüft hast.

Was an KI-Nutzung erlaubt ist und wie du sie offenlegst, regelt der Leitfaden
deiner Hochschule. Das Protokoll hilft dir, ihn einzuhalten, ersetzt ihn aber
nicht; siehe [KI, Plagiat und Eidesstattliche Erklärung](ki-und-plagiat.md).

## Nichts blind übernehmen

🚶 Jede Zusammenfassung, jede Auswertung und jeden Entwurf von Claude Code liest
du ganz und prüfst jede Zahl am Original. KI macht Fehler, die überzeugend
klingen, und die Verantwortung für deine Arbeit trägst du. Warum das so
wichtig ist und wie du vorgehst, steht unter
[Nichts blind übernehmen](ki-und-plagiat.md#3-nichts-blind-übernehmen).

Zurück zur [Übersicht](../README.md)
