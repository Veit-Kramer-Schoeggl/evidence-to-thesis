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

### Was nicht ins Repository gehört

- Volltexte, weil sie urheberrechtlich geschützt sind; die Ordner `pdf/` sind
  ausgenommen.
- Word- und PDF-Ausgaben deiner Arbeit; der Ordner `arbeit/ausgabe/` ist
  ausgenommen.
- Passwörter, deine E-Mail-Adresse und Daten über andere Personen.
- Exporte aus Suchdiensten, deren Lizenz die Weitergabe verbietet; dafür gibt
  es den ausgenommenen Ordner `notes/recherche/exporte/`.

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
