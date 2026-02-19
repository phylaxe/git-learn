---
title: "Fetch vs. Pull"
level: remotes
order: 5
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Projektstart' > projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Projektstart'"
  - cmd: "git clone --bare . ../remote.git"
  - cmd: "git remote add origin ../remote.git"
  - cmd: "git clone ../remote.git ../temp-clone && cd ../temp-clone && git config user.email 'dev@team.ch' && git config user.name 'Entwickler' && echo 'Neue Funktion' > funktion.txt && git add . && git commit -m 'Neue Funktion implementiert' && git push origin master"

task: |
  Das Remote-Repository hat einen neuen Commit, den du lokal noch nicht hast.

  Statt direkt `git pull` zu nutzen, sollst du den sicheren Weg gehen:
  1. Hole die Änderungen mit `git fetch origin` (ohne zu mergen!)
  2. Schau dir an, was sich geändert hat: `git log origin/master`
  3. Wenn alles gut aussieht, merge mit `git merge origin/master`

hints:
  - "`git fetch` lädt die Änderungen herunter, ändert aber deine lokalen Dateien nicht"
  - "Nach dem Fetch kannst du mit `git log origin/master` oder `git diff master origin/master` die Unterschiede sehen"
  - "Zum Integrieren: `git merge origin/master`"

solution: |
  git fetch origin
  git log origin/master
  git merge origin/master

validation:
  - type: working_tree_clean
    expected: true
  - type: commit_count
    expected: 2
  - type: file_exists
    path: "funktion.txt"
---

## Fetch vs. Pull

Viele Einsteiger nutzen immer `git pull`, aber `git fetch` gibt dir mehr
Kontrolle. Der Unterschied ist entscheidend:

### git fetch

`git fetch` lädt alle neuen Daten vom Remote herunter, **ändert aber nichts**
an deinem Arbeitsverzeichnis oder deinen lokalen Branches:

```bash
git fetch origin
```

Nach dem Fetch kannst du die Remote-Änderungen inspizieren:

```bash
# Was hat sich geändert?
git log master..origin/master

# Unterschiede anzeigen
git diff master origin/master
```

### git pull = fetch + merge

`git pull` ist einfach eine Kombination aus zwei Schritten:

```bash
# Das hier...
git pull origin master

# ...ist dasselbe wie:
git fetch origin
git merge origin/master
```

### Warum Fetch bevorzugen?

| Situation | Empfehlung |
|---|---|
| Du willst wissen, was sich geändert hat | `git fetch` + inspizieren |
| Du vertraust den Änderungen | `git pull` |
| Du willst Konflikte vermeiden | `git fetch` + manueller Merge |
| Schnell synchronisieren | `git pull --rebase` |

### Remote-Tracking-Branches

Nach einem Fetch werden **Remote-Tracking-Branches** aktualisiert. Diese
Branches wie `origin/master` zeigen den letzten bekannten Stand des Remotes:

```bash
# Alle Branches anzeigen (lokal + remote)
git branch -a

# Nur Remote-Branches
git branch -r
```

### Was du lernst
- Den Unterschied zwischen `git fetch` und `git pull`
- Wie du Remote-Änderungen vor dem Merge inspizierst
- Was Remote-Tracking-Branches sind
