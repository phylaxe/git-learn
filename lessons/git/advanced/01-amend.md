---
title: "Nachbessern"
level: advanced
order: 1
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Willkommen' > willkommen.txt"
  - cmd: "git add willkommen.txt"
  - cmd: "git commit -m 'Ertse Version'"

task: |
  Oh nein! In der letzten Commit-Nachricht hat sich ein Tippfehler eingeschlichen:
  "Ertse Version" statt "Erste Version".

  Korrigiere die Commit-Nachricht mit `git commit --amend`, ohne einen neuen Commit
  zu erstellen. Am Ende soll es immer noch nur einen einzigen Commit geben.

hints:
  - "Mit --amend kannst du den letzten Commit nachträglich ändern"
  - "Die Syntax lautet: `git commit --amend -m 'neue Nachricht'`"
  - "git commit --amend -m 'Erste Version'"

solution: |
  git commit --amend -m "Erste Version"

validation:
  - type: commit_message
    contains: "Erste Version"
  - type: commit_count
    expected: 1
  - type: working_tree_clean
    expected: true
---

## Nachbessern

Manchmal schleichen sich Fehler in Commit-Nachrichten ein – ein Tippfehler,
eine vergessene Datei oder eine unvollständige Beschreibung. Statt einen
neuen „Fix-Commit" zu erstellen, kannst du mit `git commit --amend` den
letzten Commit direkt korrigieren.

### Was --amend macht

Der Befehl `git commit --amend` ersetzt den letzten Commit durch einen neuen.
Dabei kannst du:
- Die **Commit-Nachricht** ändern
- Vergessene **Dateien** nachträglich hinzufügen (vorher stagen!)
- Beides gleichzeitig

### Wichtig zu wissen

- `--amend` ändert den Commit-Hash, da es technisch einen neuen Commit erstellt
- Verwende `--amend` **nur** bei Commits, die noch nicht gepusht wurden
- Bereits gepushte Commits nachträglich zu ändern kann Probleme für andere verursachen

### Beispiele

```bash
# Nur die Nachricht ändern
git commit --amend -m "Korrigierte Nachricht"

# Eine vergessene Datei hinzufügen
git add vergessene-datei.txt
git commit --amend --no-edit
```

### Was du lernst
- Wie du mit `git commit --amend` den letzten Commit korrigierst
- Wann --amend sicher verwendet werden kann
- Den Unterschied zwischen --amend und einem neuen Commit
