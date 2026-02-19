---
title: "Die Staging Area"
level: beginner
order: 3
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Neue Zeile' >> README.md"

task: |
  Die Datei README.md wurde bereits verändert.
  Nutze `git add`, um die Änderung in die Staging Area zu übernehmen.
  Erstelle dann einen Commit mit einer passenden Nachricht.

hints:
  - "Die Staging Area ist der Bereich zwischen Working Directory und Repository"
  - "Mit `git add <datei>` fügst du Änderungen zur Staging Area hinzu"
  - "git add README.md && git commit -m 'Add neue Zeile'"

solution: |
  git add README.md
  git commit -m "Add neue Zeile"

validation:
  - type: commit_count
    expected: 2
  - type: working_tree_clean
    expected: true
---

## Die Staging Area

Die Staging Area (auch "Index" genannt) ist ein zentrales Konzept in Git.
Sie ist ein Zwischenbereich, in dem du Änderungen sammelst, bevor du
sie mit einem Commit dauerhaft speicherst.

Der Workflow sieht so aus:
1. Du änderst Dateien im **Working Directory**
2. Du fügst Änderungen mit `git add` zur **Staging Area** hinzu
3. Du speicherst mit `git commit` einen Snapshot im **Repository**

### Was du lernst
- Was die Staging Area ist und wozu sie dient
- Wie du mit `git add` Änderungen stagen kannst
- Den Drei-Bereiche-Workflow von Git
