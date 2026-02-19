---
title: "Welten vereinen"
level: intermediate
order: 5
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Hauptprogramm' > main.py"
  - cmd: "git add main.py"
  - cmd: "git commit -m 'Add main.py'"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Neues Feature' > feature.py"
  - cmd: "git add feature.py"
  - cmd: "git commit -m 'Add feature'"
  - cmd: "git checkout master"

task: |
  Der Branch `feature` enthält einen zusätzlichen Commit mit der Datei `feature.py`.
  Du bist aktuell auf `master`.

  Merge den Branch `feature` in `master`, sodass die Änderungen aus `feature`
  in `master` übernommen werden.

hints:
  - "Du musst auf dem Zielbranch sein, in den du mergen willst – also auf `master`"
  - "Mit `git merge <branch>` führst du einen anderen Branch in den aktuellen zusammen"
  - "git merge feature"

solution: |
  git merge feature

validation:
  - type: branch_active
    expected: "master"
  - type: file_exists
    path: "feature.py"
  - type: commit_ancestry
    ancestor: "feature"
---

## Welten vereinen

Wenn du auf einem Branch fertig gearbeitet hast, willst du die Änderungen
zurück in den Hauptzweig bringen. Genau dafür ist `git merge` da.

### Wie funktioniert ein Merge?

Du wechselst auf den Zielbranch (z.B. `master`) und sagst Git, welchen
Branch du einmergen möchtest:

```bash
git checkout master
git merge feature
```

### Arten von Merges

Git kennt verschiedene Merge-Strategien:

#### Fast-Forward Merge
Wenn `master` seit der Erstellung des Feature-Branches keine eigenen Commits
hat, kann Git den Zeiger einfach vorspulen:

```
Vorher:  master → A → B
                        ↘
         feature →       C

Nachher: master → A → B → C ← feature
```

Es wird kein zusätzlicher Merge-Commit erstellt.

#### 3-Way Merge
Wenn beide Branches eigene Commits haben, erstellt Git einen Merge-Commit,
der beide Historien zusammenführt:

```
         A → B → D (master)
              ↘
               C (feature)

Nach merge: A → B → D → E (Merge-Commit)
                 ↘     ↗
                  C ---
```

### Was du lernst
- Wie du mit `git merge` Branches zusammenführst
- Den Unterschied zwischen Fast-Forward und 3-Way Merge
- Dass du dich vor dem Merge auf dem Zielbranch befinden musst
