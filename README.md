# Git Learn

An interactive Git terminal trainer — learn Git hands-on in your real terminal.

Inspired by [Oh My Git!](https://ohmygit.org/), but entirely in the terminal.

## Features

- **Real terminal, real git** — work in your actual shell, not a simulation
- **Progressive lessons** — from `git init` to interactive rebase and beyond
- **Automatic validation** — the tool checks your git state after each exercise
- **Hint system** — progressive hints when you're stuck
- **Star ratings** — earn up to 3 stars per lesson based on how much help you needed

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
git-learn          # Launch interactive TUI
git-learn status   # View your progress
git-learn reset    # Reset all progress
```

### How it works

1. The TUI shows you a lesson with a task description
2. Press **Enter** to open your shell in the exercise repo
3. Solve the task using real git commands
4. Press **Ctrl+D** to return — the tool validates your work
5. Earn stars and move to the next lesson

## Lesson Overview

| Chapter | Topic | Lessons |
|---------|-------|---------|
| 1 | Grundlagen (Beginner) | git init, status, add, commit, log, diff |
| 2 | Branches (Intermediate) | branch, switch, merge, conflicts |
| 3 | History umschreiben (Advanced) | amend, cherry-pick, rebase -i, reflog |
| 4 | Stash & Bisect | stash, bisect, blame, clean |
| 5 | Remotes & Collaboration | clone, push/pull, tags, fetch |
| 6 | Profi-Workflows (Expert) | feature branches, worktrees, hooks |

## Development

```bash
pip install -e ".[dev]"
pytest -v
```

## License

MIT
