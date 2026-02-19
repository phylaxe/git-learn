---
title: "Push abgelehnt!"
level: remotes
order: 3
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Version 1' > app.txt"
  - cmd: "git add app.txt"
  - cmd: "git commit -m 'Version 1'"
  - cmd: "git clone --bare . ../remote.git"
  - cmd: "git remote add origin ../remote.git"
  - cmd: "git clone ../remote.git ../temp-clone && cd ../temp-clone && git config user.email 'kollegin@team.ch' && git config user.name 'Kollegin' && echo 'Remote Änderung' > remote.txt && git add . && git commit -m 'Änderung von Kollegin' && git push origin master"
  - cmd: "echo 'Lokale Änderung' > local.txt && git add . && git commit -m 'Lokale Änderung'"

task: |
  Du und eine Kollegin arbeiten am selben Repository. Während du lokal
  einen Commit gemacht hast, hat deine Kollegin ebenfalls einen Commit
  auf den Remote gepusht.

  Wenn du jetzt `git push origin master` versuchst, wird es abgelehnt!
  Das Remote hat Commits, die du lokal noch nicht hast.

  Löse das Problem:
  1. Hole die Remote-Änderungen mit `git pull --rebase origin master`
  2. Pushe danach erfolgreich mit `git push origin master`

hints:
  - "Versuche zuerst `git push origin master` – du wirst eine Fehlermeldung sehen"
  - "Mit `git pull --rebase origin master` holst du die Remote-Änderungen und setzt deine lokalen Commits darauf"
  - "Nach dem Rebase: `git push origin master`"

solution: |
  git pull --rebase origin master
  git push origin master

validation:
  - type: working_tree_clean
    expected: true
  - type: commit_count
    expected: 3
  - type: file_exists
    path: "remote.txt"
  - type: file_exists
    path: "local.txt"
---

## Push abgelehnt!

Einer der häufigsten Situationen bei der Teamarbeit: Du versuchst zu pushen,
aber Git lehnt es ab, weil das Remote neue Commits hat, die du lokal nicht
kennst.

### Warum wird der Push abgelehnt?

Git schützt dich davor, Arbeit anderer zu überschreiben. Wenn das Remote
Commits enthält, die du lokal nicht hast, musst du diese zuerst integrieren.

```
Lokal:   A → B → D (dein Commit)
Remote:  A → B → C (Commit der Kollegin)
```

### Lösung mit Pull --rebase

```bash
# Fehlgeschlagener Push
git push origin master
# → ! [rejected] master -> master (non-fast-forward)

# Remote-Änderungen holen und eigene Commits darauf setzen
git pull --rebase origin master

# Ergebnis: A → B → C → D
# Jetzt funktioniert der Push
git push origin master
```

### Pull --rebase vs. Pull (Merge)

| Variante | Ergebnis | Wann verwenden |
|---|---|---|
| `git pull --rebase` | Lineare Historie, kein Merge-Commit | Standard für Team-Arbeit |
| `git pull` (Merge) | Erstellt einen Merge-Commit | Wenn Merge-Historie gewünscht |

### Konflikte beim Rebase

Falls deine Änderungen mit den Remote-Änderungen kollidieren, musst du die
Konflikte manuell lösen:

```bash
# Konflikte in Dateien lösen, dann:
git add <datei>
git rebase --continue
```

### Was du lernst
- Warum ein Push abgelehnt werden kann
- Wie du mit `git pull --rebase` eine saubere Historie behältst
- Den Unterschied zwischen Rebase und Merge bei Pull
