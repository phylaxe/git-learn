---
title: "Selektives Staging"
level: expert
order: 5
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Version 1' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'App erstellt'"
  - cmd: "echo 'Version 2 mit Bugfix' > app.py"
  - cmd: "echo 'Notizen für später' > notizen.txt"

task: |
  Das Repository hat einen Commit. Danach wurden zwei Änderungen gemacht:
  - `app.py` wurde modifiziert (Bugfix)
  - `notizen.txt` wurde neu erstellt (noch nicht fertig)

  In der professionellen Entwicklung committet man nicht einfach alles auf einmal.
  Stattdessen erstellt man **gezielte Commits**, die jeweils eine logische Einheit bilden.

  Deine Aufgabe:
  1. Stage **nur** die Datei `app.py` (nicht `notizen.txt`)
  2. Committe mit der Nachricht "Bugfix in app.py"

  Die Datei `notizen.txt` soll als ungetrackte Datei im Arbeitsverzeichnis bleiben.

hints:
  - "Mit `git add <datei>` kannst du gezielt einzelne Dateien stagen"
  - "Verwende `git status`, um zu prüfen, dass nur `app.py` in der Staging Area ist"
  - |
    git add app.py
    git commit -m 'Bugfix in app.py'

solution: |
  git add app.py
  git commit -m "Bugfix in app.py"

validation:
  - type: commit_count
    expected: 2
  - type: commit_message
    contains: "Bugfix"
  - type: working_tree_clean
    expected: false
---

## Selektives Staging

Im Alltag hast du oft mehrere Änderungen im Arbeitsverzeichnis, die aber
nicht alle in denselben Commit gehören. Ein guter Workflow bedeutet:
**Ein Commit = eine logische Änderung.**

### Gezielte Commits erstellen

```bash
# Nur bestimmte Dateien stagen
git add bugfix.py
git commit -m "Kritischen Bug behoben"

# Weitere Dateien separat committen
git add feature.py tests/test_feature.py
git commit -m "Neues Feature mit Tests"
```

### Interaktives Staging mit git add -p

Für fortgeschrittene Kontrolle gibt es `git add -p` (Patch-Modus). Damit
kannst du sogar **einzelne Abschnitte** innerhalb einer Datei stagen:

```bash
git add -p app.py
```

Git zeigt dir jeden geänderten Abschnitt (Hunk) und fragt:
- **y** – Diesen Abschnitt stagen
- **n** – Überspringen
- **s** – In kleinere Abschnitte aufteilen
- **e** – Manuell bearbeiten

### Warum selektives Staging wichtig ist

- **Saubere Geschichte**: Jeder Commit erzählt eine klare Geschichte
- **Einfacheres Review**: Reviewer verstehen gezielte Commits besser
- **Besseres Debugging**: Mit `git bisect` findest du Fehler schneller,
  wenn Commits klein und fokussiert sind
- **Einfacheres Rückgängigmachen**: Einzelne Commits lassen sich leichter
  reverten als grosse „Alles auf einmal"-Commits

### Nützliche Befehle

```bash
# Status prüfen: Was ist gestaged, was nicht?
git status

# Nur gestagte Änderungen anzeigen
git diff --staged

# Datei aus der Staging Area entfernen (nicht löschen!)
git restore --staged datei.txt
```

### Was du lernst
- Wie du mit `git add <datei>` gezielt einzelne Dateien stagst
- Warum gezielte Commits besser sind als „git add ."
- Wie `git add -p` für noch feinere Kontrolle sorgt
