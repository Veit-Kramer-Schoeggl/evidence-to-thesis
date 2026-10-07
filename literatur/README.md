# Literatur

Ein Unterordner je Kategorie, also je Teilfrage der Arbeit:

```
literatur/
└── <kategorie>/
    ├── <kategorie>.md               Sammeldokument: Kurzfassung, Stand, Was sich abzeichnet, Fragen
    ├── <Schlüssel>_auswertung.md     eine Auswertung je gelesener Arbeit, mit Prüfliste
    └── pdf/                          Volltexte, nicht versioniert (.gitignore)
```

Anlegen mit:

```bash
python3 tools/neu.py kategorie <kategorie>
python3 tools/neu.py auswertung <kategorie> <Schlüssel>
```

Der Zitierschlüssel kommt aus `literatur.bib` (`tools/doi2bib.py`); Volltext,
Auswertung und Bibliografie tragen denselben Namen.
