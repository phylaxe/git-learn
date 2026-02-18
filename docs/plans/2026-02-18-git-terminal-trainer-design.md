# Git Terminal Trainer – Design Document

> Interaktives CLI-Lerntool für Git, inspiriert von [Oh My Git!](https://ohmygit.org/)

## Überblick

Ein Python-basiertes Terminal-Tool das Git interaktiv beibringt. Der User installiert es via `pip`, arbeitet in seiner normalen Shell, und interagiert mit dem Tool über eine Textual-TUI mit modalem Wechsel zur Shell.

## Kernkonzept

### Modaler Wechsel (inspiriert von githug)

```
TUI (Textual)          Shell (User)           TUI (Textual)
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ Aufgabe      │       │ $ git add .  │       │ ✓ Bestanden! │
│ Fortschritt  │──→    │ $ git commit │  ──→  │ ⭐⭐⭐        │
│ [Enter]      │       │ [Ctrl+D]     │       │ Weiter? [y]  │
└──────────────┘       └──────────────┘       └──────────────┘
```

1. TUI zeigt Aufgabe, Lernziel, Fortschritt
2. User drückt Enter → TUI suspendiert sich, User ist in normaler Shell
3. User arbeitet mit Git, tippt `check` oder `Ctrl+D`
4. TUI kommt zurück, validiert Git-State + Command-Log, zeigt Ergebnis

**Technisch:** Textual `app.suspend()`, dann Subshell spawnen. Bei Rückkehr Validierung ausführen.

## CLI-Interface

```bash
git-learn                  # TUI starten (Lektionsübersicht)
git-learn start <lektion>  # Direkt eine Lektion starten
git-learn status           # Fortschritt anzeigen (CLI)
git-learn reset            # Fortschritt zurücksetzen
```

Innerhalb der Shell (während einer Lektion):
```bash
check      # Alias/Script: Validiert und kehrt zur TUI zurück
hint       # Nächsten Hint anzeigen (ohne TUI zu verlassen)
solution   # Lösung anzeigen
```

## Lektionsformat

Markdown-Dateien mit YAML-Frontmatter unter `lessons/<level>/`.

```yaml
---
title: "Dein erster Commit"
level: beginner
order: 2
points: 10

setup:
  - cmd: "mkdir project && cd project && git init"
  - cmd: "echo 'Hello World' > README.md"

task: |
  Stage die Datei README.md und erstelle einen Commit
  mit der Message "initial commit".

hints:
  - "Schau dir `git status` an — welche Datei ist untracked?"
  - "Mit `git add <datei>` kannst du Dateien stagen"
  - "Mit `git commit -m \"message\"` erstellst du einen Commit"

solution: |
  git add README.md
  git commit -m "initial commit"

validation:
  - type: commit_count
    expected: 1
  - type: commit_message
    contains: "initial commit"
  - type: working_tree_clean
    expected: true
---

## Dein erster Commit

Du hast ein frisches Git-Repository vor dir. Eine Datei wartet darauf,
in die Git-Geschichte aufgenommen zu werden.

### Was du lernst
- Dateien zur Staging Area hinzufügen
- Einen Commit erstellen
```

## Lektionsplan

### Kapitel 1: Grundlagen (Beginner) — 8 Lektionen
git init, status, add, commit, log, diff, graph-alias

### Kapitel 2: Branches (Intermediate) — 7 Lektionen
branch, switch, merge, conflicts, reset

### Kapitel 3: History umschreiben (Advanced) — 6 Lektionen
amend, cherry-pick, rebase -i, restore, reflog

### Kapitel 4: Stash & Bisect — 5 Lektionen
stash, bisect, blame, clean

### Kapitel 5: Remotes & Collaboration — 6 Lektionen
clone, push/pull, tags, fetch, upstream

### Kapitel 6: Profi-Workflows (Expert) — 7 Lektionen
Feature-Branch, Rebase-Workflow, Worktrees, Submodules, Hooks, Notfall-Koffer

**Total: 39 Lektionen**

Vollständiger Lektionsplan mit Details: [Issue #1](https://github.com/phylaxe/git-learn/issues/1)

## Validierung

Jeder Validierungstyp ist eine Python-Klasse mit einer `check(repo_path) -> bool` Methode.

**Typen:**

| Kategorie | Typen |
|-----------|-------|
| Commits | `commit_count`, `commit_message`, `merge_commit`, `commit_ancestry` |
| Branches | `branch_exists`, `branch_active` |
| Dateien | `file_exists`, `file_content`, `file_not_exists` |
| Working Tree | `working_tree_clean`, `staging_area_empty` |
| Spezial | `stash_empty`, `bisect_complete`, `last_bisect_result` |
| Infra | `tag_exists`, `remote_exists`, `hook_exists`, `config_value` |

## Command-Logging

Bei `git-learn start` wird ein Git-Hook (`post-command` via `.bashrc`-Wrapper) ins Übungs-Repo installiert. Jeder Git-Befehl wird in `.git/git-learn-log` protokolliert.

Das ermöglicht:
- Feedback wie "Gelöst, aber `git switch` wäre moderner als `git checkout`"
- Erkennung ob Hints nötig waren
- Keine Auswirkung auf die User-Experience (transparent)

## Sterne-System

| Sterne | Bedingung |
|--------|-----------|
| ⭐⭐⭐ | Ohne Hint, ohne Solution gelöst |
| ⭐⭐ | Mit Hint(s) gelöst |
| ⭐ | Solution angeschaut |

## Fortschritt

Gespeichert in `~/.git-learn/progress.json`:

```json
{
  "lessons": {
    "beginner/01-init": {
      "completed": true,
      "stars": 3,
      "attempts": 1,
      "hints_used": 0,
      "completed_at": "2026-02-18T14:30:00"
    }
  },
  "stats": {
    "total_stars": 42,
    "lessons_completed": 14,
    "current_streak": 3
  }
}
```

## Technische Architektur

```
git-learn/
├── src/git_learn/
│   ├── __init__.py
│   ├── __main__.py        # CLI entry point
│   ├── app.py             # Textual App (TUI)
│   ├── screens/           # TUI Screens
│   │   ├── lesson_list.py # Lektionsübersicht
│   │   ├── lesson.py      # Aufgabenanzeige
│   │   └── result.py      # Ergebnis nach Validierung
│   ├── shell.py           # Shell-Spawning, suspend/resume
│   ├── validator/
│   │   ├── __init__.py
│   │   ├── base.py        # BaseValidator ABC
│   │   ├── commits.py     # Commit-bezogene Validatoren
│   │   ├── branches.py    # Branch-bezogene Validatoren
│   │   ├── files.py       # Datei-bezogene Validatoren
│   │   └── special.py     # Stash, Bisect, etc.
│   ├── lesson_loader.py   # Markdown + YAML Parser
│   ├── progress.py        # Fortschrittsspeicherung
│   └── setup_exercise.py  # Übungs-Repo aufsetzen + Hooks
├── lessons/
│   ├── beginner/
│   ├── intermediate/
│   ├── advanced/
│   ├── stash/
│   ├── remotes/
│   └── expert/
├── tests/
├── pyproject.toml
└── README.md
```

## Stack

| Dependency | Zweck |
|-----------|-------|
| Python 3.12+ | Runtime |
| Textual | TUI Framework |
| PyYAML | Lesson-Frontmatter parsen |
| python-frontmatter | Markdown + YAML trennen |
| GitPython | Git-State abfragen für Validierung |
| Click | CLI-Argument-Parsing |

## Übungs-Repos

- Erstellt unter `/tmp/git-learn/<lektion-name>/`
- Jede Lektion bekommt ein frisches Repo via Setup-Commands
- Command-Logging via Bash-Wrapper (`check`, `hint`, `solution` als Shell-Funktionen)
- Temporär — wird bei `git-learn start` neu aufgesetzt

## Abgrenzung

- **Kein AI-Trainer** in v1 — kann später ergänzt werden
- **Keine Remote-Server** — alles lokal, Remotes werden via lokale bare-Repos simuliert
- **Kein Multiplayer/Leaderboard** — rein lokales Lerntool
