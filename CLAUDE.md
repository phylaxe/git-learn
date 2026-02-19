# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
uv tool install git+https://github.com/phylaxe/git-learn.git  # User install
pip install -e ".[dev]"          # Dev install with test dependencies
terminal-learn                   # Launch the TUI (git module by default)
terminal-learn -m linux          # Launch with Linux module (needs Docker)
terminal-learn status            # Show progress
terminal-learn reset             # Reset progress
terminal-learn modules           # List available modules
git-learn                        # Alias — same as terminal-learn
```

## Testing

```bash
pytest                                  # Run all tests
pytest tests/test_validators.py         # Run specific test file
pytest tests/test_linux_integration.py  # Run Linux integration tests (needs Docker)
pytest -k "test_commit"                 # Run tests matching pattern
pytest -v                               # Verbose output
```

## Architecture

**terminal-learn** is a multi-module interactive terminal trainer with a Textual TUI.

- **Modules:** Each module (git, linux, ...) is a `ModuleConfig` in `modules/`. Modules define lessons dir, validators, shell target (local/docker), and setup function
- **Modal flow:** TUI shows lesson → user presses Enter → TUI suspends → user works in real shell (or Docker) → Ctrl+D returns → TUI validates state
- **Lessons:** Markdown files with YAML frontmatter in `lessons/<module>/<level>/`. Parsed by `lesson_loader.py`
- **Validators:** Registry pattern in `validator/__init__.py`. Modules can add extra validators via `ModuleConfig.extra_validators`
- **Progress:** JSON file at `~/.terminal-learn/progress.json`, keyed by module. Stars: 3=no help, 2=hints, 1=solution viewed
- **Exercise dirs:** Created in `/tmp/terminal-learn/<module>/` with `.terminal-learn/` marker dir for bashrc/logging
- **Docker:** Linux module uses Docker containers (`docker/linux/Dockerfile`) for consistent environments

## Key Files

- `src/terminal_learn/app.py` — Textual App, orchestrates the flow
- `src/terminal_learn/module_config.py` — ModuleConfig dataclass
- `src/terminal_learn/modules/` — Module configs (git.py, linux.py) and registry
- `src/terminal_learn/lesson_loader.py` — Parses lesson Markdown+YAML
- `src/terminal_learn/validator/` — Validation rules (commits, branches, files, special, linux)
- `src/terminal_learn/setup_exercise.py` — Creates exercise dirs with module-specific setup
- `src/terminal_learn/shell.py` — Shell spawning (local + Docker)
- `src/terminal_learn/progress.py` — Star/progress persistence (multi-module)

## Adding Lessons

Create `lessons/<module>/<level>/NN-name.md` with frontmatter: title, level, order, points, setup, task, hints, solution, validation. See existing lessons for format.

**Every lesson must have an integration test** in `tests/test_integration.py` (git) or `tests/test_linux_integration.py` (linux) that plays through the full flow: load lesson → setup exercise repo → simulate the solution → assert all validations pass.

## Adding Modules

1. Create `src/terminal_learn/modules/mymodule.py` with a `ModuleConfig`
2. Register it in `modules/__init__.py`
3. Create lessons in `lessons/mymodule/<level>/`
4. Optionally add custom validators in `validator/mymodule.py`
