---
title: "Abbrechen und Reset"
level: intermediate
order: 7
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'Ursprünglicher Inhalt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Zweite Version' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Zweiter Commit'"
  - cmd: "echo 'Dritter Inhalt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Schlechte Nachricht'"

task: |
  Das Repository hat drei Commits. Der letzte Commit hat eine schlechte Nachricht
  ("Schlechte Nachricht").

  Nutze `git reset --soft HEAD~1`, um den letzten Commit rückgängig zu machen.
  Die Änderungen bleiben dabei in der Staging Area erhalten.
  Erstelle dann einen neuen Commit mit der besseren Nachricht "Dritter Commit überarbeitet".

hints:
  - "Mit `git reset --soft HEAD~1` machst du den letzten Commit rückgängig, behältst aber die Änderungen in der Staging Area"
  - "Nach dem Reset kannst du einfach einen neuen Commit mit `git commit -m '...'` erstellen"
  - "git reset --soft HEAD~1 && git commit -m 'Dritter Commit überarbeitet'"

solution: |
  git reset --soft HEAD~1
  git commit -m "Dritter Commit überarbeitet"

validation:
  - type: commit_count
    expected: 3
  - type: commit_message
    contains: "Dritter Commit überarbeitet"
  - type: working_tree_clean
    expected: true
---

## Abbrechen und Reset

Nicht immer läuft alles nach Plan. Manchmal möchtest du einen Merge abbrechen
oder einen Commit rückgängig machen. Git bietet dafür mächtige Werkzeuge.

### git merge --abort

Wenn du mitten in einem Merge-Konflikt steckst und entscheidest, dass du
den Merge doch nicht durchführen willst:

```bash
git merge --abort
```

Dieser Befehl bricht den laufenden Merge ab und stellt den Zustand vor
dem Merge wieder her. Alle Konflikte verschwinden, als wäre nichts passiert.

### git reset

Der Befehl `git reset` ist vielseitiger und hat drei wichtige Modi:

| Modus | Befehl | Wirkung |
|-------|--------|---------|
| **soft** | `git reset --soft HEAD~1` | Commit rückgängig, Änderungen bleiben in Staging Area |
| **mixed** | `git reset HEAD~1` | Commit rückgängig, Änderungen im Working Directory |
| **hard** | `git reset --hard HEAD~1` | Commit rückgängig, Änderungen werden **gelöscht** |

### Soft Reset im Detail

`git reset --soft HEAD~1` ist besonders nützlich, wenn du:
- Eine **Commit-Nachricht** korrigieren willst
- Mehrere Commits zu einem **zusammenfassen** willst
- Den letzten Commit **aufteilen** willst

Die Änderungen bleiben in der Staging Area – du kannst direkt einen neuen
Commit erstellen.

### Vorsicht mit --hard

`git reset --hard` löscht Änderungen unwiderruflich. Nutze diesen Modus nur,
wenn du dir absolut sicher bist, dass du die Änderungen nicht mehr brauchst.

### Was du lernst
- Wie du einen laufenden Merge mit `git merge --abort` abbrichst
- Wie du mit `git reset` Commits rückgängig machst
- Den Unterschied zwischen `--soft`, `--mixed` und `--hard`
