---
title: "Visueller Ueberblick"
level: beginner
order: 8
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Projekt Start' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'Erste Funktion' > feature.txt"
  - cmd: "git add feature.txt"
  - cmd: "git commit -m 'Erste Funktion hinzugefuegt'"
  - cmd: "echo 'Dokumentation' > docs.txt"
  - cmd: "git add docs.txt"
  - cmd: "git commit -m 'Dokumentation erstellt'"
  - cmd: "git checkout -b feature-branch"
  - cmd: "echo 'Neue Funktion' > neue-funktion.txt"
  - cmd: "git add neue-funktion.txt"
  - cmd: "git commit -m 'Neue Funktion auf Branch'"

task: |
  Erstelle einen Git-Alias namens 'tree', der den Befehl
  `log --oneline --graph --all` ausfuehrt. Nutze dann `git tree`
  um die Branch-Struktur deines Repositories visuell anzuzeigen.

hints:
  - "Einen Alias erstellst du mit `git config alias.name 'befehl'`"
  - "Der vollstaendige Befehl: `git config alias.tree 'log --oneline --graph --all'`"
  - "Danach kannst du `git tree` verwenden"

solution: |
  git config alias.tree "log --oneline --graph --all"
  git tree

validation:
  - type: config_value
    key: "alias.tree"
    expected: "log --oneline --graph --all"
---

## Visueller Ueberblick

Wenn dein Projekt mehrere Branches hat, wird es schnell
unuebersichtlich. Mit `git log --oneline --graph --all` bekommst
du eine visuelle Darstellung aller Branches und Commits.

Da dieser Befehl sehr lang ist, kannst du einen **Git-Alias**
erstellen. Ein Alias ist eine Abkuerzung fuer einen laengeren
Git-Befehl.

### Was du lernst
- Wie du mit `git log --oneline --graph --all` Branches visualisierst
- Wie du mit `git config alias.name 'befehl'` einen Alias erstellst
- Wie Aliases deinen Workflow beschleunigen
