---
title: "Zeitreisen"
level: intermediate
order: 4
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Version 1' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Version 1'"
  - cmd: "git tag v1.0"
  - cmd: "echo 'Version 2' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Version 2'"
  - cmd: "echo 'Version 3' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Version 3'"

task: |
  Das Repository hat drei Commits. Der erste Commit wurde mit dem Tag `v1.0` markiert.

  Reise zurück in der Zeit: Checke den Tag `v1.0` aus, um den alten Stand
  zu sehen (Detached HEAD). Schau dich um (z.B. `cat app.py`).

  Kehre danach zurück auf den Branch `master`.

hints:
  - "Mit `git checkout <tag>` kannst du einen bestimmten Tag auschecken"
  - "Im Detached HEAD-Zustand bist du auf keinem Branch – Änderungen gehen verloren, wenn du sie nicht sicherst"
  - "git checkout v1.0 && cat app.py && git checkout master"

solution: |
  git checkout v1.0
  cat app.py
  git checkout master

validation:
  - type: branch_active
    expected: "master"
  - type: tag_exists
    name: "v1.0"
  - type: working_tree_clean
    expected: true
---

## Zeitreisen

Einer der grössten Vorteile von Git ist die Möglichkeit, in der Geschichte
deines Projekts zurückzureisen. Du kannst jeden beliebigen Commit oder Tag
auschecken und dir den damaligen Stand ansehen.

### Was ist ein Detached HEAD?

Normalerweise zeigt HEAD auf einen Branch, der wiederum auf einen Commit zeigt:

```
HEAD → master → Commit C
```

Wenn du einen Tag oder einen Commit direkt auscheckst, zeigt HEAD direkt
auf den Commit, ohne einen Branch dazwischen:

```
HEAD → Commit A  (kein Branch!)
```

Das nennt man **Detached HEAD**. Du kannst dich umschauen und sogar Commits
machen, aber sobald du auf einen Branch zurückkehrst, sind diese Commits
schwer wiederzufinden (sie hängen an keinem Branch).

### Wann ist Detached HEAD nützlich?

- **Code-Review**: Einen alten Stand anschauen
- **Debugging**: Herausfinden, wann ein Bug eingeführt wurde
- **Releases prüfen**: Den Stand eines bestimmten Tags untersuchen

### Zurückkehren

Um den Detached HEAD-Zustand zu verlassen, wechsle einfach zurück auf
einen Branch:

```bash
git checkout master
# oder
git switch master
```

### Was du lernst
- Was der Detached HEAD-Zustand bedeutet
- Wie du alte Commits und Tags auscheckst
- Wie du sicher zurück auf einen Branch wechselst
