---
title: "Worktrees"
level: expert
order: 3
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Hauptprojekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'App Code' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'App erstellt'"
  - cmd: "git branch feature/dashboard"

task: |
  Du arbeitest auf `master` an einem dringenden Bugfix, möchtest aber gleichzeitig
  am `feature/dashboard`-Branch arbeiten – ohne ständig hin- und herzuwechseln.

  Mit `git worktree` kannst du einen zweiten Arbeitsordner erstellen, der einen
  anderen Branch ausgecheckt hat. So kannst du parallel an mehreren Branches arbeiten.

  Beantworte folgende Frage mit dem `check`-Befehl:
  Wie lautet der Git-Befehl, um einen Worktree für den Branch `feature/dashboard`
  im Ordner `../dashboard-wt` zu erstellen?

  Übermittle deine Antwort mit: check "dein befehl"

hints:
  - "Der Befehl heisst `git worktree` – schau dir die Unterkommandos an"
  - "Mit `git worktree add <pfad> <branch>` erstellst du einen neuen Worktree"
  - 'check "git worktree add ../dashboard-wt feature/dashboard"'

solution: |
  check "git worktree add ../dashboard-wt feature/dashboard"

validation:
  - type: check_answer
    contains: "worktree add"
---

## Worktrees

Hast du schon einmal mitten in der Arbeit an einem Feature einen dringenden
Bugfix machen müssen? Normalerweise müsstest du deine Änderungen stashen,
den Branch wechseln, den Fix machen und dann zurückwechseln. Mit **Worktrees**
geht das eleganter.

### Was ist ein Worktree?

Ein Worktree ist ein zusätzliches Arbeitsverzeichnis, das mit demselben
Repository verbunden ist, aber einen anderen Branch ausgecheckt hat.

```bash
# Worktree erstellen
git worktree add ../bugfix-ordner bugfix/critical

# Alle Worktrees anzeigen
git worktree list

# Worktree entfernen
git worktree remove ../bugfix-ordner
```

### Wie es funktioniert

```
/mein-projekt/           ← Hauptverzeichnis (master)
/mein-projekt-bugfix/    ← Worktree (bugfix/critical)
/mein-projekt-feature/   ← Worktree (feature/dashboard)
```

Alle Worktrees teilen sich das gleiche `.git`-Repository. Commits in einem
Worktree sind sofort in allen anderen sichtbar.

### Regeln für Worktrees

- Jeder Branch kann nur in **einem** Worktree gleichzeitig ausgecheckt sein
- Worktrees teilen sich Stash, Reflog und alle Referenzen
- Temporäre Worktrees sollten nach Gebrauch mit `git worktree remove` aufgeräumt werden

### Wann sind Worktrees nützlich?

- **Paralleles Arbeiten**: An Feature und Bugfix gleichzeitig arbeiten
- **Code Review**: Einen PR-Branch auschecken, ohne den eigenen Branch zu verlassen
- **Vergleichen**: Zwei Versionen nebeneinander im Dateisystem haben
- **Lange Builds**: Auf einem Branch bauen, während du auf einem anderen entwickelst

### Was du lernst
- Wie du mit `git worktree` mehrere Arbeitsverzeichnisse erstellst
- Wann Worktrees gegenüber Branch-Wechseln Vorteile bieten
- Wie du Worktrees erstellst, auflistest und entfernst
