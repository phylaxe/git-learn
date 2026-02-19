---
title: "Stash mit Kontext"
level: stash
order: 2
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'App Version 1' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Initiale Version'"
  - cmd: "echo 'App Version 2 - Work in Progress' > app.py"

task: |
  Du hast Änderungen an app.py gemacht, die du zwischenspeichern möchtest.
  Diesmal willst du dem Stash eine aussagekräftige Nachricht mitgeben,
  damit du später weisst, was darin steckt.

  1. Speichere deine Änderungen mit einer Nachricht: `git stash push -m "work in progress"`
  2. Überprüfe mit `git stash list`, dass der Stash mit deiner Nachricht existiert
  3. Hole die Änderungen mit `git stash pop` zurück

  Am Ende soll der Stash leer sein und deine Änderungen wieder in app.py vorhanden.

hints:
  - "Mit `git stash push -m` kannst du dem Stash eine beschreibende Nachricht geben"
  - "Mit `git stash list` siehst du alle Stashes mit ihren Nachrichten"
  - "git stash push -m 'work in progress' && git stash list && git stash pop"

solution: |
  git stash push -m "work in progress"
  git stash list
  git stash pop

validation:
  - type: stash_empty
    expected: true
  - type: file_content
    path: app.py
    contains: "Work in Progress"
  - type: working_tree_clean
    expected: false
---

## Stash mit Kontext

Wenn du `git stash` ohne Nachricht verwendest, bekommt der Stash-Eintrag
einen automatisch generierten Namen basierend auf dem Branch und dem letzten
Commit. Bei mehreren Stashes wird es dann schnell unübersichtlich.

Mit `git stash push -m "Nachricht"` gibst du deinem Stash eine klare
Beschreibung – so weisst du auch Tage später noch, was darin steckt.

### Stash mit Nachricht

```bash
# Stash mit beschreibender Nachricht erstellen
git stash push -m "Login-Formular halb fertig"

# Alle Stashes mit Nachrichten anzeigen
git stash list
# stash@{0}: On master: Login-Formular halb fertig
```

### Stash anwenden: pop vs. apply

| Befehl | Beschreibung |
|--------|-------------|
| `git stash pop` | Änderungen wiederherstellen **und** Stash-Eintrag entfernen |
| `git stash apply` | Änderungen wiederherstellen, Stash-Eintrag **behalten** |
| `git stash drop` | Stash-Eintrag entfernen, ohne ihn anzuwenden |

### Wann apply statt pop?

`apply` ist nützlich, wenn du dieselben Änderungen auf mehreren Branches
anwenden möchtest. Der Stash bleibt erhalten, bis du ihn manuell mit
`git stash drop` entfernst.

### Was du lernst
- Wie du mit `git stash push -m` einen beschrifteten Stash erstellst
- Wie du mit `git stash list` deine Stashes überblickst
- Den Unterschied zwischen `pop`, `apply` und `drop`
