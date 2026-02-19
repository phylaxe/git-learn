---
title: "Klonen"
level: remotes
order: 1
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'print(\"Hallo Welt\")' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'App hinzugefügt'"
  - cmd: "git clone --bare . ../remote.git"
  - cmd: "git remote add origin ../remote.git"

task: |
  Du arbeitest in einem Repository, das mit einem Remote namens `origin` verbunden ist.

  Finde heraus, welche Remotes konfiguriert sind und wie die URL von `origin` lautet.
  Nutze `git remote -v` um die Details anzuzeigen.

  Übermittle dann die URL von origin mit: check "deine-antwort"

hints:
  - "Mit `git remote` siehst du die Namen aller konfigurierten Remotes"
  - "Mit `git remote -v` siehst du auch die URLs der Remotes"
  - "Die URL enthält `remote.git` – übermittle sie mit: check \"../remote.git\""

solution: |
  git remote -v
  check "../remote.git"

validation:
  - type: remote_exists
    name: "origin"
  - type: check_answer
    contains: "remote.git"
---

## Klonen

Wenn du ein bestehendes Git-Repository kopieren möchtest, nutzt du `git clone`.
Dieser Befehl erstellt eine vollständige Kopie des Repositories – inklusive der
gesamten Commit-Historie – und richtet automatisch eine Verbindung zum
Ursprungs-Repository ein.

### Was ist ein Remote?

Ein **Remote** ist ein Verweis auf ein anderes Repository, meistens auf einem
Server. Wenn du ein Repository klonst, wird das Quell-Repository automatisch
als Remote namens `origin` eingetragen.

### Grundlegende Befehle

```bash
# Repository klonen
git clone <url>

# Klonen in einen bestimmten Ordner
git clone <url> mein-ordner

# Konfigurierte Remotes anzeigen
git remote

# Remotes mit URLs anzeigen
git remote -v
```

### Bare Repositories

Ein **Bare Repository** (erstellt mit `git clone --bare`) enthält nur die
Git-Datenbank ohne Arbeitskopie. Es dient als zentraler Ablageort, auf den
mehrere Entwickler pushen und von dem sie pullen können.

### Was du lernst
- Was ein Remote ist und wie es mit `git clone` eingerichtet wird
- Wie du konfigurierte Remotes mit `git remote -v` anzeigst
- Was ein Bare Repository ist
