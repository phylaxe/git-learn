---
title: "Commits vergleichen"
level: beginner
order: 7
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Hallo Welt' > hallo.txt"
  - cmd: "git add hallo.txt"
  - cmd: "git commit -m 'Erste Version'"
  - cmd: "echo 'Hallo schöne Welt' > hallo.txt"

task: |
  Die Datei hallo.txt wurde verändert. Schau dir den Unterschied
  mit `git diff` an. Stage dann die Datei mit `git add` und prüfe
  den Unterschied erneut mit `git diff --staged`. Erstelle am Ende
  einen Commit mit deinen Änderungen.

hints:
  - "`git diff` zeigt Änderungen im Working Directory"
  - "`git diff --staged` zeigt Änderungen in der Staging Area"
  - "Vergiss nicht, am Ende einen Commit zu erstellen"

solution: |
  git diff
  git add hallo.txt
  git diff --staged
  git commit -m "Text aktualisiert"

validation:
  - type: commit_count
    expected: 2
  - type: working_tree_clean
    expected: true
---

## Commits vergleichen

Mit `git diff` kannst du sehen, was sich seit dem letzten Commit
verändert hat. Das ist besonders nützlich, bevor du Änderungen
stagen oder committen willst.

- `git diff` zeigt Änderungen, die noch **nicht gestagt** sind
- `git diff --staged` zeigt Änderungen, die **bereits gestagt** sind

### Was du lernst
- Wie du mit `git diff` Änderungen im Working Directory siehst
- Wie du mit `git diff --staged` gestagete Änderungen prüfst
- Den Unterschied zwischen unstaged und staged Änderungen
