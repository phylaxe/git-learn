---
title: "Push & Pull"
level: remotes
order: 2
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "git clone --bare . ../remote.git"
  - cmd: "git remote add origin ../remote.git"

task: |
  Dein lokales Repository ist mit einem Remote `origin` verbunden.

  Erstelle eine neue Datei `feature.txt` mit dem Inhalt "Neues Feature",
  committe sie und pushe den Commit zum Remote `origin`.

  Nutze `git push origin master` um deine Änderungen zu übertragen.

hints:
  - "Erstelle die Datei mit `echo 'Neues Feature' > feature.txt`"
  - "Füge sie zum Staging hinzu und committe: `git add feature.txt && git commit -m 'Feature hinzugefügt'`"
  - "Pushe mit: `git push origin master`"

solution: |
  echo "Neues Feature" > feature.txt
  git add feature.txt
  git commit -m "Feature hinzugefügt"
  git push origin master

validation:
  - type: working_tree_clean
    expected: true
  - type: remote_exists
    name: "origin"
  - type: file_exists
    path: "feature.txt"
  - type: file_content
    path: "feature.txt"
    contains: "Neues Feature"
  - type: commit_count
    expected: 2
---

## Push & Pull

Die beiden wichtigsten Befehle für die Zusammenarbeit mit Remote-Repositories
sind `git push` und `git pull`. Sie halten dein lokales Repository und das
Remote synchron.

### git push

Mit `git push` überträgst du deine lokalen Commits zum Remote-Repository:

```bash
# Zum Remote pushen
git push origin master

# Kurzform (wenn Upstream konfiguriert)
git push
```

Der Befehl sendet alle Commits, die lokal vorhanden sind aber noch nicht auf
dem Remote, an das Remote-Repository.

### git pull

Mit `git pull` holst du Änderungen vom Remote und integrierst sie in deinen
lokalen Branch:

```bash
# Vom Remote pullen
git pull origin master

# Kurzform (wenn Upstream konfiguriert)
git pull
```

`git pull` ist eine Kombination aus `git fetch` (Daten herunterladen) und
`git merge` (Änderungen zusammenführen).

### Typischer Workflow

```bash
# 1. Änderungen vom Remote holen
git pull origin master

# 2. Lokal arbeiten und committen
echo "Neuer Code" > feature.txt
git add feature.txt
git commit -m "Feature implementiert"

# 3. Änderungen zum Remote übertragen
git push origin master
```

### Was du lernst
- Wie du mit `git push` lokale Commits zum Remote überträgst
- Wie du mit `git pull` Remote-Änderungen lokal integrierst
- Den grundlegenden Push/Pull-Workflow
