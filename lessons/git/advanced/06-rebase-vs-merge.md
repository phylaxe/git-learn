---
title: "Rebase vs. Merge"
level: advanced
order: 6
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Basis' > projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Hauptentwicklung' > main.txt"
  - cmd: "git add main.txt"
  - cmd: "git commit -m 'Hauptentwicklung'"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Neues Feature' > feature.txt"
  - cmd: "git add feature.txt"
  - cmd: "git commit -m 'Feature entwickelt'"
  - cmd: "git checkout master"
  - cmd: "echo 'Weiterer Fortschritt' >> main.txt"
  - cmd: "git add main.txt"
  - cmd: "git commit -m 'Weiterer Fortschritt auf master'"

task: |
  Das Repository hat einen `master`-Branch mit 3 Commits und einen `feature`-Branch,
  der nach dem 2. Commit abgezweigt ist. Seitdem hat sich `master` weiterentwickelt.

  Deine Aufgabe:
  1. Wechsle auf den `feature`-Branch
  2. Rebase `feature` auf den aktuellen `master` (damit feature die neuesten Änderungen hat)
  3. Wechsle zurück auf `master`
  4. Merge `feature` in `master` (das sollte ein Fast-Forward sein)

  Am Ende sollst du auf `master` sein und eine saubere, lineare Geschichte haben.

hints:
  - "Beim Rebase wechselst du zuerst auf den Branch, der umgeschrieben werden soll, dann führst du `git rebase master` aus"
  - "Nach dem Rebase wechselst du auf `master` und führst `git merge feature` aus – das ergibt einen Fast-Forward-Merge"
  - "git checkout feature && git rebase master && git checkout master && git merge feature"

solution: |
  git checkout feature
  git rebase master
  git checkout master
  git merge feature

validation:
  - type: branch_active
    expected: "master"
  - type: file_exists
    path: "feature.txt"
  - type: working_tree_clean
    expected: true
  - type: commit_count
    expected: 4
---

## Rebase vs. Merge

Wenn du Änderungen aus einem Branch in einen anderen integrieren möchtest,
hast du zwei Hauptoptionen: **Merge** und **Rebase**. Beide erreichen das
gleiche Ziel, aber auf unterschiedliche Weise.

### Merge: Die sichere Variante

```bash
git checkout master
git merge feature
```

- Erstellt einen **Merge-Commit** (wenn kein Fast-Forward möglich)
- Bewahrt die **vollständige Geschichte** aller Branches
- Die Commit-Hashes bleiben **unverändert**
- Kann zu einer **verzweigten** Geschichte führen

### Rebase: Die saubere Variante

```bash
git checkout feature
git rebase master
```

- Verschiebt die Commits auf die **Spitze** des Zielbranches
- Erzeugt eine **lineare**, saubere Geschichte
- Erstellt **neue Commit-Hashes** (die Commits werden neu geschrieben)
- Kein Merge-Commit nötig

### Der Rebase-dann-Merge-Workflow

Der eleganteste Ansatz kombiniert beides:

1. `git checkout feature` – Auf Feature-Branch wechseln
2. `git rebase master` – Feature auf aktuellem master aufbauen
3. `git checkout master` – Zurück auf master
4. `git merge feature` – Fast-Forward-Merge (linear!)

### Die goldene Regel

> **Rebase niemals Commits, die bereits gepusht und mit anderen geteilt wurden.**

Rebase schreibt die Geschichte um – das kann für Teamkollegen, die auf den
gleichen Commits aufbauen, zu Problemen führen.

| Eigenschaft | Merge | Rebase |
|-------------|-------|--------|
| Geschichte | Verzweigt | Linear |
| Commit-Hashes | Unverändert | Neu |
| Sicherheit | Hoch | Vorsicht bei geteilten Branches |
| Merge-Commit | Ja (bei non-FF) | Nein |

### Was du lernst
- Den Unterschied zwischen Merge und Rebase
- Wie du mit Rebase eine lineare Geschichte erzeugst
- Den kombinierten Rebase-dann-Merge-Workflow
- Die goldene Regel: Geteilte Commits nicht rebasen
