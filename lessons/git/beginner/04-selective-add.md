---
title: "Selektiv stagen"
level: beginner
order: 4
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'init' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Datei A' > a.txt"
  - cmd: "echo 'Datei B' > b.txt"
  - cmd: "echo 'Datei C' > c.txt"

task: |
  Es wurden drei neue Dateien erstellt: a.txt, b.txt und c.txt.
  Stage nur a.txt und c.txt -- b.txt soll NICHT gestaged werden.
  So lernst du, gezielt einzelne Dateien für einen Commit vorzubereiten.

hints:
  - "Du kannst `git add` mit einzelnen Dateinamen aufrufen"
  - "Du kannst mehrere Dateien auf einmal angeben: `git add datei1 datei2`"
  - "git add a.txt c.txt"

solution: |
  git add a.txt c.txt

validation:
  - type: file_exists
    path: a.txt
  - type: file_exists
    path: b.txt
  - type: file_exists
    path: c.txt
  - type: staging_area_empty
    expected: false
  - type: working_tree_clean
    expected: false
---

## Selektiv stagen

Eine der grossen Stärken von Git ist, dass du nicht alle Änderungen
auf einmal committen musst. Du kannst gezielt auswählen, welche
Dateien in den nächsten Commit aufgenommen werden sollen.

Das ist besonders nützlich, wenn du an mehreren Dingen gleichzeitig
gearbeitet hast und saubere, thematisch getrennte Commits erstellen
möchtest.

### Was du lernst
- Wie du gezielt einzelne Dateien mit `git add <datei>` stagen kannst
- Warum selektives Stagen für saubere Commits wichtig ist
- Dass ungestaged Dateien als "untracked" angezeigt werden
