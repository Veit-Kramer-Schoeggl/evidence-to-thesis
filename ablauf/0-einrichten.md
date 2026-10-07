# 0 · Einrichten

Einmal am Anfang. Danach hast du:

- ein Konto bei GitHub und eines bei Claude,
- Git, Python, das GitHub-Programm `gh` und Claude Code auf deinem Rechner,
- dein eigenes, privates Repository mit dem Kit.

Du brauchst kein Vorwissen. Jeder Befehl steht unten in einem eigenen Feld.
Auf GitHub erscheint rechts oben an jedem Feld ein Symbol zum Kopieren. Füge
den Befehl ins Terminal ein und drück die Eingabetaste.

> **Das Terminal öffnen.** Das Terminal ist ein Fenster, in das du Befehle
> eingibst.
> - **Windows:** Starttaste drücken, „PowerShell“ tippen, „Windows PowerShell“ öffnen.
> - **macOS:** Befehlstaste und Leertaste, „Terminal“ tippen, Eingabetaste.
> - **Linux:** meist Strg + Alt + T.
>
> **Einfügen:** unter Windows mit Rechtsklick oder Strg + V, unter macOS mit
> Befehlstaste + V, unter Linux mit Strg + Umschalt + V.

## Schritt 1 · Konten anlegen

### GitHub

GitHub hebt dein Repository im Internet auf. Das ist deine Sicherung, und du
kannst damit an mehreren Rechnern arbeiten.

1. Öffne [github.com/signup](https://github.com/signup).
2. Gib deine E-Mail-Adresse ein, wähle ein Passwort und einen Benutzernamen.
3. Gib den Code ein, den GitHub dir per E-Mail schickt.
4. Fragt GitHub nach einem Plan, reicht „Free“.

### Claude

Claude Code ist der KI-Assistent, mit dem du im Kit arbeitest. Er braucht ein
Claude-Konto mit einem bezahlten Abo.

1. Öffne [claude.ai](https://claude.ai) und registriere dich mit deiner
   E-Mail-Adresse oder einem Google-Konto.
2. Bestätige deine Adresse mit dem Code oder Link aus der E-Mail.
3. Schließ ein Abo ab, das Claude Code enthält, also mindestens **Pro**
   (siehe Tabelle). Die aktuellen Preise stehen auf
   [claude.com/pricing](https://claude.com/pricing).

#### Welcher Plan welche Modelle erlaubt

Claude gibt es in vier Modellfamilien: Haiku, Sonnet, Opus und Fable. Stand
der Tabelle: 7. Oktober 2026.

| Plan | Claude Code | Haiku | Sonnet | Opus | Fable |
|---|---|---|---|---|---|
| Free | nein | ja | ja | nein | nein |
| Pro | ja | ja | ja | ja | nur gegen Aufpreis |
| Max (5x oder 20x) | ja | ja | ja | ja | ja, bis zur Hälfte des Wochenkontingents |
| Team, Standard-Platz | ja | ja | ja | ja | nur gegen Aufpreis |
| Team, Premium-Platz | ja | ja | ja | ja | ja, bis zur Hälfte des Wochenkontingents |
| Enterprise | ja | ja | ja | ja | je nach Vertrag |
| Console (Bezahlung nach Verbrauch) | ja | ja | ja | ja | ja, zu den API-Preisen |

- **„Nur gegen Aufpreis“** heißt: Fable zählt nicht zum Kontingent des Abos.
  Du bezahlst es mit zusätzlich gekauftem Nutzungsguthaben.
- **Max** bietet laut Preisseite fünf- oder zwanzigmal so viel Nutzung je
  Fünf-Stunden-Fenster wie Pro.
- **Für das Kit reicht Pro** (unsere Empfehlung). Ein größerer Plan lohnt
  sich, wenn du oft an die Nutzungsgrenze stößt.

Quellen: die [Preisseite](https://claude.com/pricing), gelesen am
7. Oktober 2026; der Hilfeartikel
[„Claude Fable models on your plan“](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan),
Stand 2. September 2026; die Claude-Code-Dokumentation
[„Advanced setup“](https://code.claude.com/docs/en/setup), dort steht, dass
der Free-Plan kein Claude Code enthält. Pläne und Modelle ändern sich; im
Zweifel gilt die Preisseite.

## Schritt 2 · Programme installieren

Wähl dein Betriebssystem. Füge die Befehle **einzeln** ein und warte jeweils,
bis das Terminal wieder bereit ist.

<details>
<summary><b>Windows</b> (Windows 10 ab Version 1809, oder Windows 11)</summary>

In der PowerShell, nacheinander: Git, das GitHub-Programm, Python, Claude Code.

```powershell
winget install --id Git.Git -e --source winget
```

```powershell
winget install --id GitHub.cli --source winget
```

```powershell
winget install 9NQ7512CXL7T -e --accept-package-agreements --disable-interactivity
```

```powershell
irm https://claude.ai/install.ps1 | iex
```

Danach **das PowerShell-Fenster schließen und ein neues öffnen**. Erst dann
findet Windows die neuen Programme; ein neuer Reiter reicht nicht.

Zum Schluss das Python-Paket, das die Prüfprogramme brauchen. Ist noch kein
Python da, installiert Windows es dabei selbst:

```powershell
py -m pip install pyyaml
```

Kennt die PowerShell den Befehl `winget` nicht, installier im Microsoft Store
die App „App-Installer“ und versuch es noch einmal.

</details>

<details>
<summary><b>macOS</b> (macOS 13 oder neuer)</summary>

Im Terminal. Zuerst die Entwicklerwerkzeuge von Apple. Sie bringen Git und
Python mit. Es öffnet sich ein Fenster: „Installieren“ klicken und warten.

```bash
xcode-select --install
```

Dann Homebrew, ein Programm, das andere Programme installiert. Es fragt nach
dem Passwort deines Mac. Beim Tippen siehst du nichts; das ist normal.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Nur auf einem Mac mit Apple-Chip zusätzlich diese Zeile. Ob du einen hast,
siehst du im Apfelmenü unter „Über diesen Mac“: Dort steht „Chip Apple M…“.

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"
```

Dann das GitHub-Programm, Claude Code und das Python-Paket für die
Prüfprogramme:

```bash
brew install gh
```

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

```bash
python3 -m pip install --user pyyaml
```

Zum Schluss das Terminal schließen und neu öffnen.

</details>

<details>
<summary><b>Linux</b> (Ubuntu ab 22.04, Debian ab 12)</summary>

```bash
sudo apt update && sudo apt install -y git gh python3 python3-yaml curl
```

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Danach das Terminal schließen und neu öffnen. Auf älteren Versionen fehlt
`gh` in der Paketliste; dann hilft
[die Anleitung von GitHub](https://github.com/cli/cli/blob/trunk/docs/install_linux.md).

</details>

**Prüfen, ob alles da ist** (auf allen Systemen). Jeder Befehl sollte eine
Versionsnummer zeigen:

```bash
git --version
```

```bash
gh --version
```

```bash
claude --version
```

Meldet einer „nicht gefunden“, hilft meist: Terminal schließen und neu öffnen.

## Schritt 3 · Mit GitHub verbinden

```bash
gh auth login --hostname github.com --git-protocol https --web
```

Das Programm zeigt einen Code aus acht Zeichen. Drück die Eingabetaste, gib
den Code im Browser ein und bestätige mit „Authorize“. Dann noch:

```bash
gh auth setup-git
```

Damit verwendet auch Git diese Anmeldung.

## Schritt 4 · Dein eigenes Repository anlegen

Ein Repository ist dein Projektordner mit seinem ganzen Verlauf. Deines
entsteht aus diesem Kit und ist **privat**: Nur du siehst es. Öffentliche
Entwürfe könnte jede Person lesen, und Plagiatssoftware fände sie später als
Treffer zu deiner eigenen Arbeit.

Statt `meine-arbeit` kannst du jeden Namen ohne Leerzeichen nehmen. Ändere ihn
dann in allen drei Befehlen.

```bash
gh repo create meine-arbeit --template Veit-Kramer-Schoeggl/evidence-to-thesis --private
```

```bash
gh repo clone meine-arbeit
```

```bash
cd meine-arbeit
```

Der Ordner `meine-arbeit` liegt dort, wo das Terminal gerade war, meist in
deinem Benutzerordner. Jetzt den Wächter einschalten; ab dann prüft er vor
jedem Commit:

```bash
git config core.hooksPath tools/hooks
```

> **Ohne Befehle geht es auch:** Auf der Seite des Kits auf GitHub „Use this
> template“ → „Create a new repository“ wählen, Namen eingeben, „Private“
> wählen, „Create repository“. Danach weiter mit `gh repo clone`.

## Schritt 5 · Claude Code starten

Im Ordner deines Repositorys:

```bash
claude
```

Beim ersten Start öffnet sich der Browser: Melde dich mit deinem
Claude-Konto an. Danach liest Claude Code die Arbeitsregeln aus [`CLAUDE.md`](../CLAUDE.md).
Schreib als Erstes:

> Prüfe, ob das Kit vollständig eingerichtet ist, und erkläre mir kurz den Ablauf.

Claude Code lässt dann die Tests und den Wächter laufen und sagt dir, was noch
fehlt.

> **Lieber mit Fenstern als im Terminal?** Claude Code gibt es auch als
> Erweiterung für VS Code und als Desktop-App mit einem Reiter „Code“. Beide
> lesen dieselbe [`CLAUDE.md`](../CLAUDE.md). Anleitungen:
> [VS Code](https://code.claude.com/docs/en/vs-code),
> [Desktop-App](https://code.claude.com/docs/en/desktop-quickstart).

## Schritt 6 · Volltexte automatisch holen (wahlweise)

[`tools/holpdf.py`](../tools/holpdf.py) fragt beim Dienst Unpaywall nach Volltexten, die legal frei
verfügbar sind. Unpaywall verlangt dafür eine E-Mail-Adresse. Sie steht nur
auf deinem Rechner, nie im Repository. Setz deine Adresse statt
`deine@adresse.at` ein:

- **Windows** (PowerShell):

  ```powershell
  [Environment]::SetEnvironmentVariable("UNPAYWALL_EMAIL", "deine@adresse.at", "User")
  ```

- **macOS:**

  ```bash
  echo 'export UNPAYWALL_EMAIL=deine@adresse.at' >> ~/.zprofile
  ```

- **Linux:**

  ```bash
  echo 'export UNPAYWALL_EMAIL=deine@adresse.at' >> ~/.bashrc
  ```

Danach das Terminal neu öffnen.

Wahlweise auch `pdftotext`: Damit prüft der Wächter, ob in jeder PDF-Datei die
richtige Arbeit steckt. Unter macOS `brew install poppler`, unter Linux
`sudo apt install poppler-utils`.

## Schritt 7 · Die Prüfliste festlegen

Bevor du die erste Arbeit auswertest, legst du fest, worauf du bei jeder Arbeit
achtest. Wie das geht und welche Prüfpunkte zu welcher Art von Studien passen,
steht in [Prüfliste festlegen](pruefliste-festlegen.md).

> „Hier ist meine Fragestellung. Welche Prüfpunkte schlägst du für die
> Auswertung vor?“

## Wenn etwas nicht klappt

- **`claude` wird nicht gefunden:** Terminal schließen und neu öffnen. Hilft
  das nicht, steht die Lösung in der Anleitung von Anthropic,
  [„Troubleshoot installation“](https://code.claude.com/docs/en/troubleshoot-install).
- **Sobald Claude Code läuft,** frag es einfach. Es kann dir bei jedem
  weiteren Schritt helfen und Fehlermeldungen erklären.

Weiter: [1 · Recherche](1-recherche.md) · zurück zur [Übersicht](../README.md)
