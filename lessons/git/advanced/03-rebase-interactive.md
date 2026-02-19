---
title: "Interaktives Rebase"
level: advanced
order: 3
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Basis' > projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'Feature A' >> projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'Feature A hinzugefügt'"
  - cmd: "echo 'Feature B' >> projekt.txt"
  - cmd: "git add projekt.txt"
  - cmd: "git commit -m 'WIP noch nicht fertig'"

task: |
  Das Repository hat 3 Commits. Die letzten beiden Commits (Feature A und
  ein WIP-Commit) sollen zu einem einzigen Commit zusammengefasst werden.

  Nutze `git reset --soft HEAD~2`, um die letzten zwei Commits aufzulösen
  (die Änderungen bleiben in der Staging Area). Erstelle dann einen neuen
  Commit mit der Nachricht "Features A und B hinzugefügt".

  Am Ende soll das Repository genau 2 Commits haben.

hints:
  - "`git reset --soft` setzt den Branch-Zeiger zurück, behält aber alle Änderungen in der Staging Area"
  - "Mit `HEAD~2` gehst du zwei Commits zurück – danach kannst du alles in einem neuen Commit zusammenfassen"
  - "git reset --soft HEAD~2 && git commit -m 'Features A und B hinzugefügt'"

solution: |
  git reset --soft HEAD~2
  git commit -m "Features A und B hinzugefügt"

validation:
  - type: commit_count
    expected: 2
  - type: working_tree_clean
    expected: true
---

## Interaktives Rebase

In der Praxis entstehen oft viele kleine Commits: „WIP", „Fixup", „Oops".
Bevor du deine Arbeit teilst, möchtest du die Geschichte aufräumen und
zusammengehörige Commits zusammenfassen (squash).

### Commits zusammenfassen mit reset --soft

Die einfachste Methode, Commits zusammenzufassen, ist `git reset --soft`:

```bash
# Die letzten 2 Commits auflösen, Änderungen bleiben gestaged
git reset --soft HEAD~2

# Alles in einem neuen Commit zusammenfassen
git commit -m "Zusammengefasste Beschreibung"
```

### Das vollständige Interactive Rebase

Für komplexere Fälle gibt es `git rebase -i` (interaktiv):

```bash
# Die letzten 3 Commits interaktiv bearbeiten
git rebase -i HEAD~3
```

Im Editor kannst du dann für jeden Commit wählen:
- **pick** – Commit behalten
- **reword** – Nachricht ändern
- **squash** – Mit vorherigem Commit verschmelzen
- **drop** – Commit entfernen
- **edit** – Commit anhalten und bearbeiten

### Die drei Reset-Modi

| Modus | Arbeitsverzeichnis | Staging Area |
|-------|-------------------|--------------|
| `--soft` | Unverändert | Behält alles |
| `--mixed` (Standard) | Unverändert | Wird geleert |
| `--hard` | Wird zurückgesetzt | Wird geleert |

### Was du lernst
- Wie du mit `git reset --soft` Commits zusammenfasst
- Die Grundidee von interaktivem Rebase
- Den Unterschied zwischen den drei Reset-Modi
