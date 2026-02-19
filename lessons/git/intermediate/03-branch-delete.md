---
title: "Aufräumen"
level: intermediate
order: 3
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "git checkout -b old-feature"
  - cmd: "echo 'Altes Feature' > old.txt"
  - cmd: "git add old.txt"
  - cmd: "git commit -m 'Add old feature'"
  - cmd: "git checkout master"
  - cmd: "git merge old-feature --no-edit"
  - cmd: "git checkout -b experiment"
  - cmd: "echo 'Experiment' > experiment.txt"
  - cmd: "git add experiment.txt"
  - cmd: "git commit -m 'Add experiment'"
  - cmd: "git checkout master"

task: |
  Im Repository gibt es zwei Branches:
  - `old-feature` wurde bereits in master gemergt
  - `experiment` wurde NICHT gemergt (das Experiment ist gescheitert)

  Lösche beide Branches. Beachte: Für den gemergten Branch reicht `-d`,
  aber für den nicht-gemergten brauchst du `-D` (force delete).

  Erstelle danach einen neuen Branch namens `release`.

hints:
  - "Probiere `git branch -d experiment` – Git wird sich weigern, weil der Branch nicht gemergt ist"
  - "Mit `-D` (Grossbuchstabe) erzwingst du das Löschen: `git branch -D experiment`"
  - "git branch -d old-feature && git branch -D experiment && git branch release"

solution: |
  git branch -d old-feature
  git branch -D experiment
  git branch release

validation:
  - type: branch_exists
    expected: "release"
  - type: branch_active
    expected: "master"
---

## Aufräumen

Mit der Zeit sammeln sich viele Branches in einem Repository an. Branches,
die bereits gemergt wurden, solltest du regelmässig aufräumen, um die
Übersicht zu behalten.

### Branches löschen

| Befehl | Beschreibung |
|--------|-------------|
| `git branch -d <name>` | Branch löschen (nur wenn bereits gemergt) |
| `git branch -D <name>` | Branch erzwungen löschen (auch ungemergte) |
| `git branch --merged` | Zeigt alle gemergten Branches |
| `git branch --no-merged` | Zeigt alle nicht-gemergten Branches |

### Sicher vs. erzwungen

Der kleine Unterschied zwischen `-d` und `-D` ist wichtig:
- **`-d` (--delete)**: Git prüft, ob der Branch bereits gemergt wurde.
  Wenn nicht, verweigert Git das Löschen, um Datenverlust zu vermeiden.
- **`-D` (--delete --force)**: Git löscht den Branch ohne Prüfung.
  Nutze dies nur, wenn du dir sicher bist, dass du die Commits nicht mehr brauchst.

### Gute Gewohnheiten

Ein aufgeräumtes Repository ist ein übersichtliches Repository:
1. Lösche Branches nach dem Merge
2. Nutze `git branch --merged` um aufzuräumen
3. Verwende `-d` statt `-D` als Sicherheitsnetz

### Was du lernst
- Wie du Branches mit `git branch -d` sicher löschst
- Den Unterschied zwischen `-d` und `-D`
- Warum regelmässiges Aufräumen wichtig ist
