# Literatur

Ein Ordner je Thema, also etwa je Teilfrage deiner Arbeit. Für ein Teilthema
legst du darin einen Unterordner an; er ist genauso aufgebaut. Ein Beispiel:

```
literatur/
└── schlaf/
    ├── schlaf.md                      Sammeldokument: Kurzfassung, Stand, Was sich abzeichnet, Fragen
    ├── Mustermann2020_auswertung.md   eine Auswertung je gelesener Arbeit, mit Prüfliste
    ├── pdf/                           die Volltexte, nicht im Repository
    │   └── Mustermann2020.pdf
    └── studienabbruch/                ein Unterordner für ein Teilthema
        ├── studienabbruch.md          sein Sammeldokument
        ├── Musterfrau2022_auswertung.md
        └── pdf/
```

Anlegen lässt du das am einfachsten von Claude Code („Lege ein Thema schlaf
an“), oder du gibst die Befehle selbst ein:

```bash
python3 tools/neu.py kategorie schlaf
python3 tools/neu.py kategorie schlaf/studienabbruch
python3 tools/neu.py auswertung schlaf Mustermann2020
```

Volltext, Auswertung und Literaturangabe tragen denselben Namen, den
Zitierschlüssel aus [`literatur.bib`](../literatur.bib). Mehr dazu in
[1 · Recherche](../ablauf/1-recherche.md), [2 · Auswertung](../ablauf/2-auswertung.md)
und [4 · Sammeldokumente](../ablauf/4-sammeldokumente.md).
