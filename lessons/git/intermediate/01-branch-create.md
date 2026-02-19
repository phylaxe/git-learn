---
title: "Parallele Welten"
level: intermediate
order: 1
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Erste Funktion' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Add app.py'"

task: |
  Du hast ein Repository mit zwei Commits auf dem master-Branch.
  Erstelle einen neuen Branch namens `feature`, aber wechsle NICHT dorthin.
  Du sollst danach immer noch auf `master` sein.

hints:
  - "Ein Branch ist nur ein Zeiger auf einen bestimmten Commit"
  - "Mit `git branch <name>` erstellst du einen neuen Branch, ohne dorthin zu wechseln"
  - "git branch feature"

solution: |
  git branch feature

validation:
  - type: branch_exists
    expected: "feature"
  - type: branch_active
    expected: "master"
---

## Parallele Welten

Branches sind eines der mächtigsten Konzepte in Git. Ein Branch ist im
Grunde nur ein leichtgewichtiger Zeiger auf einen bestimmten Commit.
Wenn du einen neuen Branch erstellst, sagst du Git: „Hier möchte ich
parallel weiterarbeiten, ohne den Hauptzweig zu stören."

### Warum Branches?

Stell dir vor, du arbeitest an einem Projekt und willst ein neues Feature
ausprobieren. Ohne Branches müsstest du direkt auf dem Hauptzweig arbeiten –
und wenn etwas schiefgeht, ist dein stabiler Code in Gefahr.

Mit Branches kannst du:
- **Neue Features** isoliert entwickeln
- **Bugfixes** separat bearbeiten
- **Experimente** durchführen, ohne den Hauptzweig zu gefährden

### Wichtige Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `git branch` | Alle lokalen Branches anzeigen |
| `git branch <name>` | Neuen Branch erstellen (ohne zu wechseln) |
| `git branch -v` | Branches mit letztem Commit anzeigen |

### Was du lernst
- Was ein Branch in Git ist
- Wie du mit `git branch` einen neuen Branch erstellst
- Dass das Erstellen eines Branches nicht automatisch dorthin wechselt
