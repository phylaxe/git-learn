---
title: "Zwischenspeicher"
level: stash
order: 1
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Hauptprogramm v1' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Initiale Version'"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Hauptprogramm v2 mit Feature' > app.py"

task: |
  Du arbeitest auf dem Branch `feature` und hast Änderungen an app.py gemacht,
  die noch nicht committet sind. Plötzlich musst du kurz auf den master-Branch
  wechseln – aber deine Arbeit ist noch nicht fertig.

  1. Speichere deine Änderungen mit `git stash` zwischen
  2. Wechsle auf den `master`-Branch
  3. Wechsle zurück auf den `feature`-Branch
  4. Hole deine Änderungen mit `git stash pop` zurück

  Am Ende sollst du wieder auf `feature` sein, der Stash leer, und deine
  Änderungen wieder in app.py vorhanden (aber nicht gestaged).

hints:
  - "Mit `git stash` kannst du unfertige Änderungen zwischenspeichern, ohne sie zu committen"
  - "Nach dem Stash ist dein Arbeitsverzeichnis sauber und du kannst den Branch wechseln"
  - "git stash && git checkout master && git checkout feature && git stash pop"

solution: |
  git stash
  git checkout master
  git checkout feature
  git stash pop

validation:
  - type: branch_active
    expected: "feature"
  - type: stash_empty
    expected: true
  - type: file_content
    path: app.py
    contains: "Feature"
  - type: working_tree_clean
    expected: false
---

## Zwischenspeicher

Stell dir vor, du bist mitten in der Arbeit an einem Feature und musst
plötzlich den Branch wechseln – etwa für einen dringenden Bugfix. Deine
Änderungen sind aber noch nicht bereit für einen Commit. Was tun?

Genau hier kommt `git stash` ins Spiel. Der Stash ist wie ein
Zwischenspeicher, in den du deine unfertigen Änderungen temporär ablegen
kannst.

### Wie git stash funktioniert

| Befehl | Beschreibung |
|--------|-------------|
| `git stash` | Änderungen zwischenspeichern |
| `git stash pop` | Letzte Änderungen wiederherstellen und aus dem Stash entfernen |
| `git stash list` | Alle gespeicherten Stashes anzeigen |

### Der typische Workflow

```bash
# Du arbeitest an einem Feature...
echo "neue Funktion" >> feature.py

# Plötzlich: Unterbrechung!
git stash

# Jetzt ist das Arbeitsverzeichnis sauber
git checkout master
# ... dringende Arbeit erledigen ...
git checkout feature

# Arbeit fortsetzen
git stash pop
```

### Wichtig zu wissen

- `git stash` speichert sowohl gestagte als auch ungestagte Änderungen
- Nach `git stash pop` werden die Änderungen als **ungestaged** wiederhergestellt
- Der Stash funktioniert wie ein Stapel (Stack): zuletzt rein, zuerst raus

### Was du lernst
- Wie du mit `git stash` Änderungen zwischenspeicherst
- Wie du mit `git stash pop` Änderungen wiederherstellst
- Warum der Stash beim Branch-Wechsel unverzichtbar ist
