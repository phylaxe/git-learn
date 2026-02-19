---
title: "Der Notfall-Koffer"
level: expert
order: 7
points: 25

setup:
  - cmd: "git init"
  - cmd: "echo 'Grundgerüst' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'Datenbankanbindung' >> app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Datenbank angebunden'"
  - cmd: "echo 'API Schicht' >> app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'API Schicht implementiert'"
  - cmd: "echo 'Login System' >> app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Wichtiges Feature'"
  - cmd: "git reset --hard HEAD~2"

task: |
  Katastrophe! Jemand hat `git reset --hard HEAD~2` ausgeführt und damit
  die letzten zwei Commits „verloren". Das Repository zeigt nur noch 2 Commits,
  aber eigentlich waren es 4.

  Die gute Nachricht: Git vergisst (fast) nichts. Im **Reflog** sind alle
  Bewegungen des HEAD-Zeigers gespeichert – auch nach einem Hard Reset.

  Deine Aufgabe:
  1. Finde die verlorenen Commits mit `git reflog`
  2. Stelle alle 4 Commits wieder her

  Am Ende soll das Repository wieder genau 4 Commits haben, inklusive dem
  Commit mit der Nachricht "Wichtiges Feature".

hints:
  - "Mit `git reflog` siehst du alle bisherigen HEAD-Positionen, auch nach einem Reset"
  - "Suche im Reflog nach dem Commit 'Wichtiges Feature' und notiere den Hash oder die Referenz (z.B. HEAD@{1})"
  - "Nutze `git reset --hard HEAD@{1}` oder den Commit-Hash, um zum Zustand vor dem Reset zurückzukehren"

solution: |
  git reflog
  git reset --hard HEAD@{1}

validation:
  - type: commit_count
    expected: 4
  - type: working_tree_clean
    expected: true
  - type: commit_message
    contains: "Wichtiges Feature"
---

## Der Notfall-Koffer

Fehler passieren: Ein versehentliches `git reset --hard`, ein gelöschter Branch,
ein kaputter Rebase. In solchen Momenten ist das **Reflog** dein Rettungsanker.

### Das Reflog: Gits Gedächtnis

Das Reflog (Reference Log) speichert jede Bewegung des HEAD-Zeigers:

```bash
git reflog
```

Ausgabe:
```
a1b2c3d HEAD@{0}: reset: moving to HEAD~2
f4e5d6c HEAD@{1}: commit: Wichtiges Feature
8g9h0i1 HEAD@{2}: commit: API Schicht implementiert
...
```

Selbst nach einem `git reset --hard` sind die Commits noch im Reflog sichtbar.

### Verlorene Commits wiederherstellen

```bash
# 1. Reflog anschauen
git reflog

# 2. Zum gewünschten Zustand zurückkehren
git reset --hard HEAD@{1}

# Oder mit dem Commit-Hash:
git reset --hard f4e5d6c
```

### Cherry-Pick als Alternative

Wenn du nur bestimmte verlorene Commits wiederherstellen möchtest:

```bash
# Einzelne Commits aus dem Reflog pflücken
git cherry-pick <hash>
```

### Weitere Notfall-Werkzeuge

#### git fsck – Verwaiste Objekte finden
```bash
git fsck --unreachable
```
Findet Commits, die von keinem Branch oder Tag referenziert werden.

#### git stash – Änderungen sichern
```bash
# Vor riskanten Operationen
git stash
# Nach der Operation
git stash pop
```

### Wie lange bleiben Reflog-Einträge?

- Standard: **90 Tage** für erreichbare Commits
- **30 Tage** für nicht erreichbare Commits
- Konfigurierbar mit `gc.reflogExpire` und `gc.reflogExpireUnreachable`

### Präventive Massnahmen

- **Vor riskantem Rebase/Reset**: Einen Tag oder Branch als Sicherung erstellen
- **Regelmässig pushen**: Remote-Repositories als Backup
- **`git stash`** vor experimentellen Änderungen

### Was du lernst
- Wie du mit `git reflog` verlorene Commits findest
- Wie du nach einem `git reset --hard` Commits wiederherstellst
- Welche Notfall-Werkzeuge Git bietet
- Wie du solche Situationen in Zukunft vermeidest
