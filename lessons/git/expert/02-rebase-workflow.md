---
title: "Rebase Workflow"
level: expert
order: 2
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Basis' > projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'Infrastruktur' >> projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Infrastruktur aufgebaut'"
  - cmd: "git checkout -b feature/api"
  - cmd: "echo 'API Endpunkt' > api.txt"
  - cmd: "git add api.txt"
  - cmd: "git commit -m 'API Endpunkt erstellt'"
  - cmd: "git checkout master"
  - cmd: "echo 'Sicherheitsupdate' >> projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Sicherheitsupdate eingespielt'"

task: |
  Die Situation: Auf `master` gibt es 3 Commits (inkl. einem neuen Sicherheitsupdate).
  Der Branch `feature/api` wurde nach dem 2. Commit abgezweigt und hat 1 eigenen Commit.

  Das Problem: `feature/api` basiert auf einem alten Stand von `master`. Bevor du
  den Feature Branch mergst, sollst du ihn per Rebase auf den neuesten Stand bringen.

  1. Wechsle auf `feature/api`
  2. Rebase den Branch auf `master` (damit der Feature-Commit auf dem neuesten
     master-Stand aufbaut)
  3. Wechsle zurück auf `master`
  4. Merge `feature/api` in `master` (das wird ein Fast-Forward Merge)

  Am Ende soll `master` genau 4 Commits haben und eine lineare Geschichte.

hints:
  - "Mit `git rebase master` auf dem Feature Branch bringst du ihn auf den neuesten Stand"
  - "Nach dem Rebase hat `feature/api` die gleiche Basis wie `master` – der Merge wird ein Fast-Forward"
  - |
    git checkout feature/api
    git rebase master
    git checkout master
    git merge feature/api

solution: |
  git checkout feature/api
  git rebase master
  git checkout master
  git merge feature/api

validation:
  - type: branch_active
    expected: "master"
  - type: working_tree_clean
    expected: true
  - type: commit_count
    expected: 4
---

## Rebase Workflow

Während `git merge` zwei Branches zusammenführt und dabei die parallele
Geschichte erhält, sorgt `git rebase` für eine **lineare Geschichte**. Das
ist besonders in Teams wichtig, wo viele Feature Branches parallel existieren.

### Merge vs. Rebase

**Mit Merge** (nicht-linear):
```
master:  A → B → D ──→ M (Merge-Commit)
              ↘       ↗
feature:       C ────
```

**Mit Rebase** (linear):
```
master:  A → B → D
                  ↘
feature:           C' (rebased)

Nach Fast-Forward Merge:
master:  A → B → D → C'
```

### Der Rebase Workflow

1. Auf dem Feature Branch arbeiten
2. Vor dem Merge: `git rebase master` auf dem Feature Branch ausführen
3. Zurück auf `master` wechseln
4. `git merge feature` → ergibt automatisch einen Fast-Forward Merge

### Wie Rebase funktioniert

`git rebase master` nimmt alle Commits deines Feature Branches und wendet
sie **nacheinander** auf der Spitze von `master` an. Dabei werden neue
Commits mit neuen Hashes erstellt (C wird zu C').

### Die goldene Rebase-Regel

> **Rebase niemals Commits, die bereits gepusht und von anderen verwendet werden.**

Rebase ändert die Commit-Hashes. Wenn andere auf den alten Commits aufbauen,
führt das zu Chaos.

### Was du lernst
- Wie `git rebase` eine lineare Geschichte erzeugt
- Den Rebase-then-Merge Workflow
- Warum ein Fast-Forward Merge nach Rebase möglich ist
- Die goldene Rebase-Regel
