---
title: "Feature Branch Workflow"
level: expert
order: 1
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'App v1' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'App erstellt'"

task: |
  Du arbeitest an einem Projekt mit 2 Commits auf `master`. Jetzt soll ein
  Login-Feature entwickelt werden – aber nicht direkt auf `master`, sondern
  auf einem eigenen Feature Branch.

  1. Erstelle einen neuen Branch `feature/login`
  2. Wechsle auf diesen Branch
  3. Erstelle eine Datei `login.py` mit dem Inhalt "Login Modul"
  4. Stage und committe die Datei mit der Nachricht "Login Feature implementiert"
  5. Wechsle zurück auf `master`
  6. Merge den Feature Branch in `master`

hints:
  - "Erstelle und wechsle auf einen neuen Branch mit `git checkout -b feature/login`"
  - "Nach dem Commit auf dem Feature Branch musst du mit `git checkout master` zurückwechseln"
  - |
    git checkout -b feature/login
    echo 'Login Modul' > login.py
    git add login.py
    git commit -m 'Login Feature implementiert'
    git checkout master
    git merge feature/login

solution: |
  git checkout -b feature/login
  echo "Login Modul" > login.py
  git add login.py
  git commit -m "Login Feature implementiert"
  git checkout master
  git merge feature/login

validation:
  - type: branch_active
    expected: "master"
  - type: file_exists
    path: "login.py"
  - type: file_content
    path: "login.py"
    contains: "Login Modul"
  - type: commit_ancestry
    ancestor: "feature/login"
  - type: working_tree_clean
    expected: true
---

## Feature Branch Workflow

Der Feature Branch Workflow ist einer der wichtigsten Arbeitsabläufe in der
professionellen Softwareentwicklung. Die Grundidee: Jedes neue Feature wird
auf einem eigenen Branch entwickelt, getestet und erst dann in den
Hauptzweig integriert.

### Das Prinzip: Branch → Commit → Merge

```
master:  A → B ────────→ M (Merge)
              ↘         ↗
feature:       C → D ──
```

1. **Branch erstellen** – Vom Hauptzweig abzweigen
2. **Entwickeln & committen** – Auf dem Feature Branch arbeiten
3. **Zurück mergen** – Fertiges Feature in den Hauptzweig integrieren

### Branch-Namenskonventionen

In der Praxis haben sich Präfixe etabliert:

| Präfix | Bedeutung |
|--------|-----------|
| `feature/` | Neues Feature |
| `bugfix/` | Fehlerbehebung |
| `hotfix/` | Dringender Fix für Produktion |
| `release/` | Release-Vorbereitung |

### Vorteile

- **Isolation**: Features beeinflussen den Hauptzweig nicht
- **Parallelarbeit**: Mehrere Features gleichzeitig entwickeln
- **Code Review**: Änderungen vor dem Merge prüfen
- **Sauberkeit**: `master` bleibt immer in einem stabilen Zustand

### Was du lernst
- Wie der Feature Branch Workflow funktioniert
- Wie du einen Feature Branch erstellst, entwickelst und zurückmergst
- Warum Branches für professionelle Entwicklung unverzichtbar sind
