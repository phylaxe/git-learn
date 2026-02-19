# Terminal Learn

Ein interaktiver Terminal-Trainer — lerne Git, Linux und mehr direkt in deinem echten Terminal.

Inspiriert von [Oh My Git!](https://ohmygit.org/), aber komplett im Terminal.

## Features

- **Echtes Terminal, echte Befehle** — arbeite in deiner echten Shell, keine Simulation
- **Mehrere Module** — Git, Linux (Docker) und erweiterbar
- **Progressive Lektionen** — von `git init` bis Interactive Rebase und darüber hinaus
- **Automatische Validierung** — das Tool prüft deinen Zustand nach jeder Übung
- **Hint-System** — schrittweise Hilfe wenn du nicht weiterkommst
- **Sterne-Bewertung** — bis zu 3 Sterne pro Lektion, je nachdem wie viel Hilfe du brauchst

## Installation

Voraussetzungen: Python 3.12+, [uv](https://docs.astral.sh/uv/)

```bash
uv tool install git+https://github.com/phylaxe/git-learn.git
```

Das installiert `terminal-learn` als globalen Befehl — fertig.

> **Linux-Modul:** Zusätzlich wird [Docker](https://www.docker.com/) benötigt. Das Docker-Image wird beim ersten Start automatisch gebaut.

### Alternative Installation

```bash
# Mit pipx
pipx install git+https://github.com/phylaxe/git-learn.git

# Für Entwickler (aus geklontem Repo)
pip install -e ".[dev]"
```

## Usage

```bash
terminal-learn              # Git-Modul starten (Standard)
terminal-learn -m linux     # Linux-Modul starten (braucht Docker)
terminal-learn status       # Fortschritt anzeigen
terminal-learn reset        # Fortschritt zurücksetzen
terminal-learn modules      # Verfügbare Module auflisten
git-learn                   # Alias für terminal-learn
```

### So funktioniert's

1. Die TUI zeigt dir eine Lektion mit Aufgabenbeschreibung
2. Drücke **Enter** um deine Shell im Übungsverzeichnis zu öffnen
3. Löse die Aufgabe mit echten Befehlen
4. Tippe **check** um zu validieren — das Tool prüft deine Arbeit
5. Sammle Sterne und gehe zur nächsten Lektion

### Tastenkürzel

| Taste | Aktion |
|-------|--------|
| Enter | Shell öffnen / Nächste Lektion |
| h | Hint anzeigen |
| s | Lösung anzeigen |
| q | Beenden |
| Esc | Zurück |

## Module

### Git (46 Lektionen)

| Kapitel | Thema | Lektionen |
|---------|-------|-----------|
| 1 | Grundlagen | git init, status, add, commit, log, diff |
| 2 | Branches | branch, switch, merge, conflicts |
| 3 | History umschreiben | amend, cherry-pick, rebase -i, reflog |
| 4 | Stash & Bisect | stash, bisect, blame, clean |
| 5 | Remotes & Collaboration | clone, push/pull, tags, fetch |
| 6 | Profi-Workflows | feature branches, worktrees, hooks |

### Linux (18 Lektionen, braucht Docker)

| Kapitel | Thema | Lektionen |
|---------|-------|-----------|
| 1 | Navigation | pwd, ls, cd, tree, find |
| 2 | Dateien & Verzeichnisse | touch, mkdir, cp, mv, rm, ln |
| 3 | Berechtigungen | chmod, chown, chgrp |
| 4 | Textverarbeitung | cat, head, tail, grep, sed, awk |
| 5 | Pipes & Redirects | \|, >, >>, tee, xargs |
| 6 | Suchen & Finden | find, locate, which |
| 7 | Prozesse | ps, top, kill, bg, fg |

## Development

```bash
git clone https://github.com/phylaxe/git-learn.git
cd git-learn
pip install -e ".[dev]"
pytest -v
```

## License

MIT
