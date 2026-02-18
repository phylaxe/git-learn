# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
pip install -e ".[dev]"    # Install in dev mode with test dependencies
git-learn                  # Launch the TUI
git-learn status           # Show progress
git-learn reset            # Reset progress
```

## Testing

```bash
pytest                          # Run all tests
pytest tests/test_validators.py # Run specific test file
pytest -k "test_commit"         # Run tests matching pattern
pytest -v                       # Verbose output
```

## Architecture

**git-learn** is an interactive Git terminal trainer with a Textual TUI.

- **Modal flow:** TUI shows lesson → user presses Enter → TUI suspends → user works in real shell → Ctrl+D returns → TUI validates git state
- **Lessons:** Markdown files with YAML frontmatter in `lessons/<level>/`. Parsed by `lesson_loader.py`
- **Validators:** Registry pattern in `validator/__init__.py`. Each type (commit_count, branch_exists, etc.) is a function in its own module
- **Progress:** JSON file at `~/.git-learn/progress.json`. Stars: 3=no help, 2=hints, 1=solution viewed
- **Exercise repos:** Created in `/tmp/git-learn/` with git-learn-bashrc for command logging

## Key Files

- `src/git_learn/app.py` — Textual App, orchestrates the flow
- `src/git_learn/lesson_loader.py` — Parses lesson Markdown+YAML
- `src/git_learn/validator/` — Validation rules (commits, branches, files, special)
- `src/git_learn/setup_exercise.py` — Creates temp repos with logging
- `src/git_learn/shell.py` — Shell spawning with modal switch
- `src/git_learn/progress.py` — Star/progress persistence

## Adding Lessons

Create `lessons/<level>/NN-name.md` with frontmatter: title, level, order, points, setup, task, hints, solution, validation. See existing lessons for format.
