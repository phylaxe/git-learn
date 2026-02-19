---
title: "Konflikte lösen"
level: intermediate
order: 6
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Willkommen bei meinem Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Feature-Version des Projekts' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Update README on feature'"
  - cmd: "git checkout master"
  - cmd: "echo 'Master-Version des Projekts' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Update README on master'"

task: |
  Sowohl `master` als auch `feature` haben die Datei `README.md` unterschiedlich geändert.
  Wenn du `feature` in `master` mergst, entsteht ein Konflikt.

  Führe den Merge durch, löse den Konflikt in `README.md`
  (wähle den Inhalt, den du behalten möchtest, und entferne die Konfliktmarker),
  und schliesse den Merge mit einem Commit ab.

hints:
  - "Starte mit `git merge feature` – Git wird den Konflikt melden"
  - "Öffne README.md und entferne die Zeilen mit <<<<<<, ======, >>>>>> – behalte den gewünschten Inhalt"
  - "git merge feature && echo 'Finale Version' > README.md && git add README.md && git commit -m 'Resolve merge conflict'"

solution: |
  git merge feature
  echo "Finale Version" > README.md
  git add README.md
  git commit -m "Resolve merge conflict"

validation:
  - type: working_tree_clean
    expected: true
  - type: merge_commit
  - type: branch_active
    expected: "master"
---

## Konflikte lösen

Merge-Konflikte gehören zum Alltag der Softwareentwicklung. Sie entstehen,
wenn zwei Branches die **gleiche Stelle** in der **gleichen Datei**
unterschiedlich verändert haben. Git kann dann nicht automatisch entscheiden,
welche Version korrekt ist.

### Wann entstehen Konflikte?

Ein Konflikt entsteht, wenn:
1. Zwei Branches die **gleiche Zeile** einer Datei ändern
2. Ein Branch eine Datei löscht, die der andere verändert hat

Ein Konflikt entsteht **nicht**, wenn:
- Zwei Branches verschiedene Dateien ändern
- Zwei Branches verschiedene Stellen derselben Datei ändern

### Konfliktmarker verstehen

Git markiert die Konfliktstellen in der Datei:

```
<<<<<<< HEAD
Master-Version des Projekts
=======
Feature-Version des Projekts
>>>>>>> feature
```

- **`<<<<<<< HEAD`**: Anfang des Konflikts – dein aktueller Branch (master)
- **`=======`**: Trennung zwischen den beiden Versionen
- **`>>>>>>> feature`**: Ende des Konflikts – der eingemergte Branch

### Konflikt lösen – Schritt für Schritt

1. **Merge starten**: `git merge feature`
2. **Konflikte finden**: `git status` zeigt betroffene Dateien
3. **Datei bearbeiten**: Konfliktmarker entfernen, gewünschten Inhalt behalten
4. **Datei stagen**: `git add README.md`
5. **Merge abschliessen**: `git commit`

### Was du lernst
- Wann und warum Merge-Konflikte entstehen
- Wie du Konfliktmarker liest und interpretierst
- Wie du einen Konflikt Schritt für Schritt löst
