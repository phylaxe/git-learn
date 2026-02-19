---
title: "Zwischen Welten wechseln"
level: intermediate
order: 2
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Hauptprogramm' > main.py"
  - cmd: "git add main.py"
  - cmd: "git commit -m 'Add main.py'"
  - cmd: "git branch feature"

task: |
  Der Branch `feature` existiert bereits.
  Wechsle auf den Branch `feature`, erstelle dort eine neue Datei
  `feature.txt` mit dem Inhalt "Neues Feature", und committe sie.

hints:
  - "Mit `git switch` oder `git checkout` kannst du den Branch wechseln"
  - "Erstelle die Datei und nutze `git add` + `git commit` wie gewohnt"
  - "git switch feature && echo 'Neues Feature' > feature.txt && git add feature.txt && git commit -m 'Add feature'"

solution: |
  git switch feature
  echo "Neues Feature" > feature.txt
  git add feature.txt
  git commit -m "Add feature"

validation:
  - type: branch_active
    expected: "feature"
  - type: file_exists
    path: "feature.txt"
  - type: commit_count
    expected: 3
  - type: working_tree_clean
    expected: true
---

## Zwischen Welten wechseln

Einen Branch zu erstellen ist nur der erste Schritt. Um darauf zu arbeiten,
musst du dorthin wechseln. Git bietet dafür zwei Befehle:

### git switch vs. git checkout

| Befehl | Beschreibung |
|--------|-------------|
| `git switch <branch>` | Moderner Befehl zum Branch-Wechsel (seit Git 2.23) |
| `git checkout <branch>` | Klassischer Befehl (funktioniert immer noch) |
| `git switch -c <branch>` | Branch erstellen UND wechseln |
| `git checkout -b <branch>` | Dasselbe, klassische Variante |

Der Befehl `git switch` wurde eingeführt, weil `git checkout` zu viele
verschiedene Aufgaben hatte und verwirrend war. Für das Wechseln zwischen
Branches ist `git switch` heute der empfohlene Befehl.

### Was passiert beim Wechseln?

Wenn du den Branch wechselst, passiert Folgendes:
1. Git aktualisiert den **HEAD-Zeiger** auf den neuen Branch
2. Dein **Working Directory** wird an den Stand des neuen Branches angepasst
3. Die **Staging Area** wird zurückgesetzt

### Was du lernst
- Wie du mit `git switch` zwischen Branches wechselst
- Wie du auf einem Branch arbeitest und Commits erstellst
- Den Unterschied zwischen `git switch` und `git checkout`
