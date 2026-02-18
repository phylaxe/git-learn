# Git Terminal Trainer – Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an interactive terminal-based Git learning tool with TUI, modal shell switching, lesson validation, and progress tracking.

**Architecture:** Python CLI with Textual TUI. Lessons defined as Markdown+YAML files. User works in real shell (modal switch via app.suspend()). Validators check git state after exercises. Progress stored locally as JSON.

**Tech Stack:** Python 3.12+, Textual, Click, PyYAML, python-frontmatter, GitPython, pytest

---

### Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `src/git_learn/__init__.py`
- Create: `src/git_learn/__main__.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

**Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "git-learn"
version = "0.1.0"
description = "Interactive Git terminal trainer"
requires-python = ">=3.12"
dependencies = [
    "textual>=0.50.0",
    "click>=8.1.0",
    "PyYAML>=6.0",
    "python-frontmatter>=1.1.0",
    "GitPython>=3.1.0",
]

[project.scripts]
git-learn = "git_learn.__main__:cli"

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Step 2: Create package files**

`src/git_learn/__init__.py`:
```python
"""Interactive Git terminal trainer."""
```

`src/git_learn/__main__.py`:
```python
"""CLI entry point."""

import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Git Learn - Interactive Git Terminal Trainer."""
    if ctx.invoked_subcommand is None:
        click.echo("git-learn v0.1.0 - use --help for commands")


if __name__ == "__main__":
    cli()
```

`tests/__init__.py`: empty

`tests/conftest.py`:
```python
"""Shared test fixtures."""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Create a temporary git repo for testing."""
    repo = tmp_path / "test-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo, capture_output=True, check=True,
    )
    return repo
```

**Step 3: Install in dev mode and verify**

Run: `pip install -e ".[dev]"`
Expected: Installs successfully

Run: `git-learn --help`
Expected: Shows help with "Git Learn - Interactive Git Terminal Trainer"

**Step 4: Commit**

```bash
git add pyproject.toml src/ tests/
git commit -m "feat: project scaffolding with CLI entry point"
```

---

### Task 2: Lesson Loader

**Files:**
- Create: `src/git_learn/lesson_loader.py`
- Create: `tests/test_lesson_loader.py`
- Create: `lessons/beginner/01-init.md` (test fixture)

**Step 1: Create a minimal test lesson**

`lessons/beginner/01-init.md`:
```markdown
---
title: "Willkommen in der Zeitmaschine"
level: beginner
order: 1
points: 10

setup:
  - cmd: "git init"

task: |
  Schau dir den Inhalt des .git Ordners an.
  Was siehst du?

hints:
  - "Nutze `ls -la` um versteckte Dateien zu sehen"
  - "Der .git Ordner enthält die gesamte Git-Datenbank"

solution: |
  ls -la .git

validation:
  - type: working_tree_clean
    expected: true
---

## Willkommen in der Zeitmaschine

Jedes Git-Repository beginnt mit `git init`. Dieser Befehl erstellt
einen versteckten `.git` Ordner, der die gesamte Geschichte deines
Projekts speichern wird.

### Was du lernst
- Was `git init` macht
- Was im `.git` Ordner steckt
```

**Step 2: Write the failing tests**

`tests/test_lesson_loader.py`:
```python
"""Tests for lesson loader."""

from pathlib import Path

from git_learn.lesson_loader import Lesson, load_lesson, load_all_lessons


def test_load_lesson_parses_frontmatter(tmp_path: Path) -> None:
    lesson_file = tmp_path / "test.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"git init\"\n"
        'task: |\n  Do something.\n'
        "hints:\n  - \"Hint 1\"\n"
        'solution: |\n  git status\n'
        "validation:\n  - type: working_tree_clean\n    expected: true\n"
        "---\n\n## Content\n\nBody text here.\n"
    )
    lesson = load_lesson(lesson_file)
    assert lesson.title == "Test"
    assert lesson.level == "beginner"
    assert lesson.order == 1
    assert lesson.points == 10
    assert lesson.setup == [{"cmd": "git init"}]
    assert lesson.task == "Do something.\n"
    assert lesson.hints == ["Hint 1"]
    assert lesson.solution == "git status\n"
    assert len(lesson.validation) == 1
    assert lesson.validation[0]["type"] == "working_tree_clean"
    assert lesson.body == "## Content\n\nBody text here.\n"


def test_load_lesson_from_real_file() -> None:
    lesson_path = Path(__file__).parent.parent / "lessons" / "beginner" / "01-init.md"
    if not lesson_path.exists():
        return
    lesson = load_lesson(lesson_path)
    assert lesson.title == "Willkommen in der Zeitmaschine"
    assert lesson.level == "beginner"
    assert len(lesson.hints) >= 1


def test_load_all_lessons(tmp_path: Path) -> None:
    beginner = tmp_path / "beginner"
    beginner.mkdir()
    for i, title in enumerate(["First", "Second"], 1):
        (beginner / f"0{i}-test.md").write_text(
            f'---\ntitle: "{title}"\nlevel: beginner\norder: {i}\npoints: 10\n'
            f"setup:\n  - cmd: \"git init\"\n"
            f'task: |\n  Task {i}.\n'
            f"hints:\n  - \"Hint\"\n"
            f'solution: |\n  solution\n'
            f"validation:\n  - type: working_tree_clean\n    expected: true\n"
            f"---\n\nBody {i}\n"
        )
    lessons = load_all_lessons(tmp_path)
    assert len(lessons) == 2
    assert lessons[0].title == "First"
    assert lessons[1].title == "Second"


def test_load_all_lessons_sorted_by_level_and_order(tmp_path: Path) -> None:
    for level in ["beginner", "intermediate"]:
        d = tmp_path / level
        d.mkdir()
        (d / "01-test.md").write_text(
            f'---\ntitle: "{level}"\nlevel: {level}\norder: 1\npoints: 10\n'
            f"setup:\n  - cmd: \"git init\"\n"
            f'task: |\n  Task.\n'
            f"hints:\n  - \"Hint\"\n"
            f'solution: |\n  solution\n'
            f"validation:\n  - type: working_tree_clean\n    expected: true\n"
            f"---\n\nBody\n"
        )
    lessons = load_all_lessons(tmp_path)
    assert lessons[0].level == "beginner"
    assert lessons[1].level == "intermediate"
```

**Step 3: Run tests to verify they fail**

Run: `pytest tests/test_lesson_loader.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'git_learn.lesson_loader'`

**Step 4: Implement lesson loader**

`src/git_learn/lesson_loader.py`:
```python
"""Load and parse lesson files (Markdown + YAML frontmatter)."""

from dataclasses import dataclass, field
from pathlib import Path

import frontmatter


LEVEL_ORDER = ["beginner", "intermediate", "advanced", "stash", "remotes", "expert"]


@dataclass
class Lesson:
    """A single lesson with metadata and content."""

    title: str
    level: str
    order: int
    points: int
    setup: list[dict[str, str]]
    task: str
    hints: list[str]
    solution: str
    validation: list[dict]
    body: str
    file_path: Path | None = None

    @property
    def slug(self) -> str:
        """Unique identifier like 'beginner/01-init'."""
        if self.file_path:
            return f"{self.level}/{self.file_path.stem}"
        return f"{self.level}/{self.order:02d}"


def load_lesson(path: Path) -> Lesson:
    """Load a single lesson from a Markdown file with YAML frontmatter."""
    post = frontmatter.load(str(path))
    meta = post.metadata
    return Lesson(
        title=meta["title"],
        level=meta["level"],
        order=meta["order"],
        points=meta["points"],
        setup=meta["setup"],
        task=meta["task"],
        hints=meta["hints"],
        solution=meta["solution"],
        validation=meta["validation"],
        body=post.content,
        file_path=path,
    )


def load_all_lessons(lessons_dir: Path) -> list[Lesson]:
    """Load all lessons from subdirectories, sorted by level and order."""
    lessons: list[Lesson] = []
    for md_file in sorted(lessons_dir.rglob("*.md")):
        lessons.append(load_lesson(md_file))
    lessons.sort(key=lambda l: (LEVEL_ORDER.index(l.level) if l.level in LEVEL_ORDER else 99, l.order))
    return lessons
```

**Step 5: Run tests to verify they pass**

Run: `pytest tests/test_lesson_loader.py -v`
Expected: All PASS

**Step 6: Commit**

```bash
git add src/git_learn/lesson_loader.py tests/test_lesson_loader.py lessons/beginner/01-init.md
git commit -m "feat: lesson loader with Markdown+YAML frontmatter parsing"
```

---

### Task 3: Validators — Base + Core Types

**Files:**
- Create: `src/git_learn/validator/__init__.py`
- Create: `src/git_learn/validator/base.py`
- Create: `src/git_learn/validator/commits.py`
- Create: `src/git_learn/validator/branches.py`
- Create: `src/git_learn/validator/files.py`
- Create: `tests/test_validators.py`

**Step 1: Write failing tests**

`tests/test_validators.py`:
```python
"""Tests for validators."""

import subprocess
from pathlib import Path

import pytest

from git_learn.validator import validate_rule
from git_learn.validator.base import ValidationResult


def _run(cmd: str, cwd: Path) -> None:
    subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, check=True)


def test_commit_count(tmp_repo: Path) -> None:
    _run("touch file.txt && git add . && git commit -m 'first'", tmp_repo)
    result = validate_rule({"type": "commit_count", "expected": 1}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "commit_count", "expected": 2}, tmp_repo)
    assert not result.passed


def test_commit_message(tmp_repo: Path) -> None:
    _run("touch file.txt && git add . && git commit -m 'initial commit'", tmp_repo)
    result = validate_rule({"type": "commit_message", "contains": "initial"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "commit_message", "contains": "nope"}, tmp_repo)
    assert not result.passed


def test_branch_exists(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    _run("git branch feature", tmp_repo)
    result = validate_rule({"type": "branch_exists", "expected": "feature"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "branch_exists", "expected": "nope"}, tmp_repo)
    assert not result.passed


def test_branch_active(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    result = validate_rule({"type": "branch_active", "expected": "master"}, tmp_repo)
    assert result.passed or validate_rule({"type": "branch_active", "expected": "main"}, tmp_repo).passed


def test_file_exists(tmp_repo: Path) -> None:
    (tmp_repo / "hello.txt").write_text("hi")
    result = validate_rule({"type": "file_exists", "path": "hello.txt"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "file_exists", "path": "nope.txt"}, tmp_repo)
    assert not result.passed


def test_file_content(tmp_repo: Path) -> None:
    (tmp_repo / "data.txt").write_text("hello world")
    result = validate_rule({"type": "file_content", "path": "data.txt", "contains": "hello"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "file_content", "path": "data.txt", "contains": "nope"}, tmp_repo)
    assert not result.passed


def test_file_not_exists(tmp_repo: Path) -> None:
    result = validate_rule({"type": "file_not_exists", "path": "gone.txt"}, tmp_repo)
    assert result.passed

    (tmp_repo / "exists.txt").write_text("hi")
    result = validate_rule({"type": "file_not_exists", "path": "exists.txt"}, tmp_repo)
    assert not result.passed


def test_working_tree_clean(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    result = validate_rule({"type": "working_tree_clean", "expected": True}, tmp_repo)
    assert result.passed

    (tmp_repo / "dirty.txt").write_text("dirt")
    result = validate_rule({"type": "working_tree_clean", "expected": True}, tmp_repo)
    assert not result.passed


def test_staging_area_empty(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    result = validate_rule({"type": "staging_area_empty", "expected": True}, tmp_repo)
    assert result.passed

    (tmp_repo / "staged.txt").write_text("x")
    _run("git add staged.txt", tmp_repo)
    result = validate_rule({"type": "staging_area_empty", "expected": True}, tmp_repo)
    assert not result.passed
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_validators.py -v`
Expected: FAIL — ModuleNotFoundError

**Step 3: Implement validators**

`src/git_learn/validator/base.py`:
```python
"""Base validator interface."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of a single validation check."""

    passed: bool
    message: str
    rule_type: str
```

`src/git_learn/validator/commits.py`:
```python
"""Commit-related validators."""

import subprocess
from pathlib import Path

from .base import ValidationResult


def validate_commit_count(rule: dict, repo: Path) -> ValidationResult:
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=repo, capture_output=True, text=True,
    )
    if result.returncode != 0:
        count = 0
    else:
        count = int(result.stdout.strip())
    expected = rule["expected"]
    return ValidationResult(
        passed=count == expected,
        message=f"Expected {expected} commits, found {count}",
        rule_type="commit_count",
    )


def validate_commit_message(rule: dict, repo: Path) -> ValidationResult:
    branch = rule.get("branch")
    cmd = ["git", "log", "--format=%s"]
    if branch:
        cmd.append(branch)
    cmd.append("-1")
    result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    if result.returncode != 0:
        return ValidationResult(passed=False, message="No commits found", rule_type="commit_message")
    msg = result.stdout.strip()
    contains = rule["contains"]
    return ValidationResult(
        passed=contains in msg,
        message=f"Commit message '{msg}' {'contains' if contains in msg else 'does not contain'} '{contains}'",
        rule_type="commit_message",
    )


def validate_merge_commit(rule: dict, repo: Path) -> ValidationResult:
    result = subprocess.run(
        ["git", "cat-file", "-p", "HEAD"],
        cwd=repo, capture_output=True, text=True,
    )
    parent_count = result.stdout.count("\nparent ")
    passed = parent_count >= 2
    return ValidationResult(
        passed=passed,
        message=f"HEAD {'is' if passed else 'is not'} a merge commit",
        rule_type="merge_commit",
    )
```

`src/git_learn/validator/branches.py`:
```python
"""Branch-related validators."""

import subprocess
from pathlib import Path

from .base import ValidationResult


def validate_branch_exists(rule: dict, repo: Path) -> ValidationResult:
    expected = rule["expected"]
    result = subprocess.run(
        ["git", "branch", "--list", expected],
        cwd=repo, capture_output=True, text=True,
    )
    exists = bool(result.stdout.strip())
    return ValidationResult(
        passed=exists,
        message=f"Branch '{expected}' {'exists' if exists else 'does not exist'}",
        rule_type="branch_exists",
    )


def validate_branch_active(rule: dict, repo: Path) -> ValidationResult:
    expected = rule["expected"]
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo, capture_output=True, text=True,
    )
    current = result.stdout.strip()
    return ValidationResult(
        passed=current == expected,
        message=f"Active branch is '{current}', expected '{expected}'",
        rule_type="branch_active",
    )
```

`src/git_learn/validator/files.py`:
```python
"""File-related validators."""

import subprocess
from pathlib import Path

from .base import ValidationResult


def validate_file_exists(rule: dict, repo: Path) -> ValidationResult:
    path = repo / rule["path"]
    exists = path.exists()
    return ValidationResult(
        passed=exists,
        message=f"File '{rule['path']}' {'exists' if exists else 'does not exist'}",
        rule_type="file_exists",
    )


def validate_file_content(rule: dict, repo: Path) -> ValidationResult:
    path = repo / rule["path"]
    if not path.exists():
        return ValidationResult(
            passed=False,
            message=f"File '{rule['path']}' does not exist",
            rule_type="file_content",
        )
    content = path.read_text()
    contains = rule["contains"]
    return ValidationResult(
        passed=contains in content,
        message=f"File '{rule['path']}' {'contains' if contains in content else 'does not contain'} '{contains}'",
        rule_type="file_content",
    )


def validate_file_not_exists(rule: dict, repo: Path) -> ValidationResult:
    path = repo / rule["path"]
    not_exists = not path.exists()
    return ValidationResult(
        passed=not_exists,
        message=f"File '{rule['path']}' {'does not exist' if not_exists else 'exists'}",
        rule_type="file_not_exists",
    )


def validate_working_tree_clean(rule: dict, repo: Path) -> ValidationResult:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo, capture_output=True, text=True,
    )
    clean = result.stdout.strip() == ""
    expected = rule["expected"]
    passed = clean == expected
    return ValidationResult(
        passed=passed,
        message=f"Working tree is {'clean' if clean else 'dirty'}",
        rule_type="working_tree_clean",
    )


def validate_staging_area_empty(rule: dict, repo: Path) -> ValidationResult:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo, capture_output=True, text=True,
    )
    empty = result.stdout.strip() == ""
    expected = rule["expected"]
    passed = empty == expected
    return ValidationResult(
        passed=passed,
        message=f"Staging area is {'empty' if empty else 'not empty'}",
        rule_type="staging_area_empty",
    )
```

`src/git_learn/validator/__init__.py`:
```python
"""Validator registry — dispatches validation rules to handler functions."""

from pathlib import Path

from .base import ValidationResult
from .commits import validate_commit_count, validate_commit_message, validate_merge_commit
from .branches import validate_branch_exists, validate_branch_active
from .files import (
    validate_file_exists,
    validate_file_content,
    validate_file_not_exists,
    validate_working_tree_clean,
    validate_staging_area_empty,
)

VALIDATORS = {
    "commit_count": validate_commit_count,
    "commit_message": validate_commit_message,
    "merge_commit": validate_merge_commit,
    "branch_exists": validate_branch_exists,
    "branch_active": validate_branch_active,
    "file_exists": validate_file_exists,
    "file_content": validate_file_content,
    "file_not_exists": validate_file_not_exists,
    "working_tree_clean": validate_working_tree_clean,
    "staging_area_empty": validate_staging_area_empty,
}


def validate_rule(rule: dict, repo: Path) -> ValidationResult:
    """Validate a single rule against a repo."""
    rule_type = rule["type"]
    validator = VALIDATORS.get(rule_type)
    if validator is None:
        return ValidationResult(
            passed=False,
            message=f"Unknown validation type: {rule_type}",
            rule_type=rule_type,
        )
    return validator(rule, repo)


def validate_all(rules: list[dict], repo: Path) -> list[ValidationResult]:
    """Validate all rules, return list of results."""
    return [validate_rule(rule, repo) for rule in rules]
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_validators.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add src/git_learn/validator/ tests/test_validators.py
git commit -m "feat: validators for commits, branches, files, working tree"
```

---

### Task 4: Validators — Special Types (Stash, Bisect, Tags, Remotes, Hooks, Config)

**Files:**
- Create: `src/git_learn/validator/special.py`
- Create: `tests/test_validators_special.py`
- Modify: `src/git_learn/validator/__init__.py`

**Step 1: Write failing tests**

`tests/test_validators_special.py`:
```python
"""Tests for special validators."""

import subprocess
from pathlib import Path

from git_learn.validator import validate_rule


def _run(cmd: str, cwd: Path) -> None:
    subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, check=True)


def test_stash_empty_when_empty(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    result = validate_rule({"type": "stash_empty", "expected": True}, tmp_repo)
    assert result.passed


def test_stash_empty_when_not_empty(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    (tmp_repo / "f").write_text("changed")
    _run("git stash", tmp_repo)
    result = validate_rule({"type": "stash_empty", "expected": True}, tmp_repo)
    assert not result.passed


def test_tag_exists(tmp_repo: Path) -> None:
    _run("touch f && git add . && git commit -m 'init'", tmp_repo)
    _run("git tag v1.0", tmp_repo)
    result = validate_rule({"type": "tag_exists", "name": "v1.0"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "tag_exists", "name": "v2.0"}, tmp_repo)
    assert not result.passed


def test_hook_exists(tmp_repo: Path) -> None:
    hook_path = tmp_repo / ".git" / "hooks" / "pre-commit"
    hook_path.write_text("#!/bin/sh\nexit 0\n")
    hook_path.chmod(0o755)
    result = validate_rule({"type": "hook_exists", "name": "pre-commit"}, tmp_repo)
    assert result.passed

    result = validate_rule({"type": "hook_exists", "name": "post-commit"}, tmp_repo)
    assert not result.passed


def test_config_value(tmp_repo: Path) -> None:
    _run("git config user.name 'TestUser'", tmp_repo)
    result = validate_rule(
        {"type": "config_value", "key": "user.name", "expected": "TestUser"},
        tmp_repo,
    )
    assert result.passed

    result = validate_rule(
        {"type": "config_value", "key": "user.name", "expected": "Other"},
        tmp_repo,
    )
    assert not result.passed
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_validators_special.py -v`
Expected: FAIL

**Step 3: Implement special validators**

`src/git_learn/validator/special.py`:
```python
"""Special validators: stash, bisect, tags, remotes, hooks, config."""

import subprocess
from pathlib import Path

from .base import ValidationResult


def validate_stash_empty(rule: dict, repo: Path) -> ValidationResult:
    result = subprocess.run(
        ["git", "stash", "list"], cwd=repo, capture_output=True, text=True,
    )
    empty = result.stdout.strip() == ""
    expected = rule["expected"]
    return ValidationResult(
        passed=empty == expected,
        message=f"Stash is {'empty' if empty else 'not empty'}",
        rule_type="stash_empty",
    )


def validate_tag_exists(rule: dict, repo: Path) -> ValidationResult:
    name = rule["name"]
    result = subprocess.run(
        ["git", "tag", "--list", name], cwd=repo, capture_output=True, text=True,
    )
    exists = bool(result.stdout.strip())
    return ValidationResult(
        passed=exists,
        message=f"Tag '{name}' {'exists' if exists else 'does not exist'}",
        rule_type="tag_exists",
    )


def validate_remote_exists(rule: dict, repo: Path) -> ValidationResult:
    name = rule["name"]
    result = subprocess.run(
        ["git", "remote"], cwd=repo, capture_output=True, text=True,
    )
    remotes = result.stdout.strip().splitlines()
    exists = name in remotes
    return ValidationResult(
        passed=exists,
        message=f"Remote '{name}' {'exists' if exists else 'does not exist'}",
        rule_type="remote_exists",
    )


def validate_hook_exists(rule: dict, repo: Path) -> ValidationResult:
    name = rule["name"]
    hook_path = repo / ".git" / "hooks" / name
    exists = hook_path.exists() and hook_path.stat().st_mode & 0o111
    return ValidationResult(
        passed=bool(exists),
        message=f"Hook '{name}' {'exists' if exists else 'does not exist'}",
        rule_type="hook_exists",
    )


def validate_config_value(rule: dict, repo: Path) -> ValidationResult:
    key = rule["key"]
    expected = rule["expected"]
    result = subprocess.run(
        ["git", "config", "--get", key], cwd=repo, capture_output=True, text=True,
    )
    actual = result.stdout.strip()
    passed = actual == expected
    return ValidationResult(
        passed=passed,
        message=f"Config '{key}' is '{actual}', expected '{expected}'",
        rule_type="config_value",
    )
```

**Step 4: Register special validators in `__init__.py`**

Add to `src/git_learn/validator/__init__.py` imports:
```python
from .special import (
    validate_stash_empty,
    validate_tag_exists,
    validate_remote_exists,
    validate_hook_exists,
    validate_config_value,
)
```

Add to `VALIDATORS` dict:
```python
    "stash_empty": validate_stash_empty,
    "tag_exists": validate_tag_exists,
    "remote_exists": validate_remote_exists,
    "hook_exists": validate_hook_exists,
    "config_value": validate_config_value,
```

**Step 5: Run tests**

Run: `pytest tests/test_validators_special.py tests/test_validators.py -v`
Expected: All PASS

**Step 6: Commit**

```bash
git add src/git_learn/validator/ tests/test_validators_special.py
git commit -m "feat: special validators for stash, tags, remotes, hooks, config"
```

---

### Task 5: Exercise Setup (Repo Creation + Command Logging)

**Files:**
- Create: `src/git_learn/setup_exercise.py`
- Create: `tests/test_setup_exercise.py`

**Step 1: Write failing tests**

`tests/test_setup_exercise.py`:
```python
"""Tests for exercise setup."""

from pathlib import Path

from git_learn.lesson_loader import load_lesson
from git_learn.setup_exercise import setup_exercise, get_exercise_path, teardown_exercise


def test_get_exercise_path() -> None:
    path = get_exercise_path("beginner/01-init")
    assert "git-learn" in str(path)
    assert "beginner-01-init" in str(path)


def test_setup_exercise_creates_repo(tmp_path: Path) -> None:
    lesson_file = tmp_path / "lesson.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"touch hello.txt\"\n"
        'task: |\n  Do it.\n'
        "hints:\n  - \"Hint\"\n"
        'solution: |\n  solution\n'
        "validation:\n  - type: file_exists\n    path: hello.txt\n"
        "---\n\nBody\n"
    )
    lesson = load_lesson(lesson_file)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    assert (exercise_dir / ".git").is_dir()
    assert (exercise_dir / "hello.txt").exists()


def test_setup_exercise_installs_command_log_hook(tmp_path: Path) -> None:
    lesson_file = tmp_path / "lesson.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"git init\"\n"
        'task: |\n  Do it.\n'
        "hints:\n  - \"Hint\"\n"
        'solution: |\n  solution\n'
        "validation:\n  - type: working_tree_clean\n    expected: true\n"
        "---\n\nBody\n"
    )
    lesson = load_lesson(lesson_file)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    # Check that the bashrc file with logging functions exists
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    assert bashrc.exists()
    content = bashrc.read_text()
    assert "check" in content
    assert "hint" in content


def test_teardown_exercise(tmp_path: Path) -> None:
    exercise_dir = tmp_path / "exercise"
    exercise_dir.mkdir()
    (exercise_dir / "file.txt").write_text("x")
    teardown_exercise(exercise_dir)
    assert not exercise_dir.exists()
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_setup_exercise.py -v`
Expected: FAIL

**Step 3: Implement exercise setup**

`src/git_learn/setup_exercise.py`:
```python
"""Set up exercise repos for lessons."""

import shutil
import subprocess
import tempfile
from pathlib import Path

from .lesson_loader import Lesson


def get_exercise_path(slug: str) -> Path:
    """Get the path for an exercise repo."""
    safe_name = slug.replace("/", "-")
    return Path(tempfile.gettempdir()) / "git-learn" / safe_name


def setup_exercise(lesson: Lesson, exercise_dir: Path) -> Path:
    """Create exercise repo, run setup commands, install logging."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
    exercise_dir.mkdir(parents=True)

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=exercise_dir, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "learner@git-learn"],
        cwd=exercise_dir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Git Learner"],
        cwd=exercise_dir, capture_output=True, check=True,
    )

    # Run setup commands
    for step in lesson.setup:
        cmd = step["cmd"]
        subprocess.run(
            cmd, shell=True, cwd=exercise_dir,
            capture_output=True, check=True,
        )

    # Install command logging bashrc
    _install_logging(exercise_dir)

    return exercise_dir


def _install_logging(exercise_dir: Path) -> None:
    """Install bash functions for check/hint/solution and git command logging."""
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    log_file = exercise_dir / ".git" / "git-learn-log"

    bashrc.write_text(f"""\
# git-learn shell environment
export GIT_LEARN_EXERCISE="{exercise_dir}"
export GIT_LEARN_LOG="{log_file}"

# Log git commands
_git_learn_log() {{
    echo "$(date +%s) $@" >> "$GIT_LEARN_LOG"
    command git "$@"
}}
alias git='_git_learn_log'

# Shell commands
check() {{
    echo "__GIT_LEARN_CHECK__"
    exit 0
}}

hint() {{
    echo "__GIT_LEARN_HINT__"
}}

solution() {{
    echo "__GIT_LEARN_SOLUTION__"
}}

echo ""
echo "  Git Learn Exercise: {exercise_dir.name}"
echo "  Type 'check' when done, 'hint' for help, 'solution' to see the answer."
echo "  Press Ctrl+D to return to Git Learn."
echo ""
""")


def teardown_exercise(exercise_dir: Path) -> None:
    """Remove exercise directory."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
```

**Step 4: Run tests**

Run: `pytest tests/test_setup_exercise.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add src/git_learn/setup_exercise.py tests/test_setup_exercise.py
git commit -m "feat: exercise setup with repo creation and command logging"
```

---

### Task 6: Progress Tracking

**Files:**
- Create: `src/git_learn/progress.py`
- Create: `tests/test_progress.py`

**Step 1: Write failing tests**

`tests/test_progress.py`:
```python
"""Tests for progress tracking."""

from pathlib import Path

from git_learn.progress import Progress


def test_new_progress_is_empty(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    assert progress.get_lesson("beginner/01-init") is None
    assert progress.total_stars == 0
    assert progress.lessons_completed == 0


def test_complete_lesson(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    lesson = progress.get_lesson("beginner/01-init")
    assert lesson is not None
    assert lesson["stars"] == 3
    assert lesson["completed"] is True
    assert progress.total_stars == 3
    assert progress.lessons_completed == 1


def test_progress_persists(tmp_path: Path) -> None:
    path = tmp_path / "progress.json"
    progress = Progress(path)
    progress.complete_lesson("beginner/01-init", stars=2, hints_used=1)

    progress2 = Progress(path)
    lesson = progress2.get_lesson("beginner/01-init")
    assert lesson is not None
    assert lesson["stars"] == 2


def test_best_score_kept(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=1, hints_used=2)
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    assert progress.get_lesson("beginner/01-init")["stars"] == 3


def test_worse_score_not_overwritten(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    progress.complete_lesson("beginner/01-init", stars=1, hints_used=2)
    assert progress.get_lesson("beginner/01-init")["stars"] == 3


def test_reset(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    progress.reset()
    assert progress.lessons_completed == 0
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_progress.py -v`
Expected: FAIL

**Step 3: Implement progress**

`src/git_learn/progress.py`:
```python
"""Progress tracking — stores lesson completion and stars."""

import json
from datetime import datetime, timezone
from pathlib import Path


class Progress:
    """Manages lesson progress stored in a JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".git-learn" / "progress.json"
        self._data: dict = {"lessons": {}}
        if self.path.exists():
            self._data = json.loads(self.path.read_text())

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))

    def get_lesson(self, slug: str) -> dict | None:
        return self._data["lessons"].get(slug)

    def complete_lesson(self, slug: str, stars: int, hints_used: int) -> None:
        existing = self._data["lessons"].get(slug)
        if existing and existing["stars"] >= stars:
            # Keep best score, just increment attempts
            existing["attempts"] = existing.get("attempts", 1) + 1
            self._save()
            return
        self._data["lessons"][slug] = {
            "completed": True,
            "stars": stars,
            "hints_used": hints_used,
            "attempts": (existing["attempts"] + 1) if existing else 1,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()

    @property
    def total_stars(self) -> int:
        return sum(l["stars"] for l in self._data["lessons"].values())

    @property
    def lessons_completed(self) -> int:
        return len(self._data["lessons"])

    def reset(self) -> None:
        self._data = {"lessons": {}}
        self._save()
```

**Step 4: Run tests**

Run: `pytest tests/test_progress.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add src/git_learn/progress.py tests/test_progress.py
git commit -m "feat: progress tracking with stars and persistence"
```

---

### Task 7: Shell Spawning (Modal Switch)

**Files:**
- Create: `src/git_learn/shell.py`
- Create: `tests/test_shell.py`

**Step 1: Write failing test**

`tests/test_shell.py`:
```python
"""Tests for shell spawning."""

from pathlib import Path

from git_learn.shell import build_shell_env, ShellResult


def test_build_shell_env(tmp_path: Path) -> None:
    env = build_shell_env(tmp_path)
    assert env["GIT_LEARN_EXERCISE"] == str(tmp_path)
    assert "GIT_LEARN_LOG" in env


def test_shell_result_from_check() -> None:
    result = ShellResult.CHECK
    assert result == ShellResult.CHECK


def test_shell_result_from_exit() -> None:
    result = ShellResult.EXIT
    assert result == ShellResult.EXIT
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_shell.py -v`
Expected: FAIL

**Step 3: Implement shell spawning**

`src/git_learn/shell.py`:
```python
"""Shell spawning for modal TUI-Shell switch."""

import os
import subprocess
from enum import Enum, auto
from pathlib import Path


class ShellResult(Enum):
    """Result of the shell session."""

    CHECK = auto()  # User typed 'check' or Ctrl+D
    EXIT = auto()   # User wants to quit


def build_shell_env(exercise_dir: Path) -> dict[str, str]:
    """Build environment variables for the exercise shell."""
    env = os.environ.copy()
    env["GIT_LEARN_EXERCISE"] = str(exercise_dir)
    env["GIT_LEARN_LOG"] = str(exercise_dir / ".git" / "git-learn-log")
    return env


def spawn_shell(exercise_dir: Path) -> ShellResult:
    """Spawn an interactive shell in the exercise directory.

    The shell loads git-learn-bashrc which provides check/hint/solution commands.
    Returns ShellResult.CHECK when the user exits (check or Ctrl+D).
    """
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    env = build_shell_env(exercise_dir)

    shell = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell:
        env["ZDOTDIR"] = str(exercise_dir / ".git")
        zshrc = exercise_dir / ".git" / ".zshrc"
        zshrc.write_text(f"source {bashrc}\n")
        cmd = [shell]
    else:
        cmd = [shell, "--rcfile", str(bashrc)]

    subprocess.run(cmd, cwd=exercise_dir, env=env)
    return ShellResult.CHECK
```

**Step 4: Run tests**

Run: `pytest tests/test_shell.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add src/git_learn/shell.py tests/test_shell.py
git commit -m "feat: shell spawning with exercise environment"
```

---

### Task 8: TUI — Textual App with Screens

**Files:**
- Create: `src/git_learn/app.py`
- Create: `src/git_learn/screens/__init__.py`
- Create: `src/git_learn/screens/lesson_list.py`
- Create: `src/git_learn/screens/lesson.py`
- Create: `src/git_learn/screens/result.py`

**Note:** TUI tests are harder to unit-test. We test the app via Textual's `app.run_test()` for basic smoke tests, but focus on manual testing for UX.

**Step 1: Write a basic smoke test**

Create `tests/test_app.py`:
```python
"""Smoke test for the TUI app."""

from git_learn.app import GitLearnApp


async def test_app_starts() -> None:
    app = GitLearnApp()
    async with app.run_test() as pilot:
        assert app.title == "Git Learn"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_app.py -v`
Expected: FAIL

**Step 3: Implement TUI screens**

`src/git_learn/screens/__init__.py`: empty

`src/git_learn/screens/lesson_list.py`:
```python
"""Lesson list screen — shows all lessons grouped by level."""

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label

from ..lesson_loader import Lesson
from ..progress import Progress


LEVEL_LABELS = {
    "beginner": "Kapitel 1: Grundlagen",
    "intermediate": "Kapitel 2: Branches",
    "advanced": "Kapitel 3: History umschreiben",
    "stash": "Kapitel 4: Stash & Bisect",
    "remotes": "Kapitel 5: Remotes & Collaboration",
    "expert": "Kapitel 6: Profi-Workflows",
}


class LessonListItem(ListItem):
    """A single lesson entry in the list."""

    def __init__(self, lesson: Lesson, progress: Progress) -> None:
        super().__init__()
        self.lesson = lesson
        self._progress = progress

    def compose(self) -> ComposeResult:
        entry = self._progress.get_lesson(self.lesson.slug)
        if entry:
            stars = "\u2b50" * entry["stars"] + "\u2606" * (3 - entry["stars"])
        else:
            stars = "\u2606\u2606\u2606"
        yield Label(
            f"  {self.lesson.order:2d}. {self.lesson.title}  {stars}  [{self.lesson.points}pt]"
        )


class LessonListScreen(Screen):
    """Main screen showing all available lessons."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("enter", "select", "Start Lesson"),
    ]

    def __init__(self, lessons: list[Lesson], progress: Progress) -> None:
        super().__init__()
        self.lessons = lessons
        self._progress = progress

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            current_level = ""
            for lesson in self.lessons:
                if lesson.level != current_level:
                    current_level = lesson.level
                    label = LEVEL_LABELS.get(current_level, current_level)
                    yield Static(f"\n  [bold]{label}[/bold]\n")
                yield LessonListItem(lesson, self._progress)
        yield Footer()

    def action_select(self) -> None:
        list_view = self.query(LessonListItem)
        focused = self.focused
        if isinstance(focused, LessonListItem):
            self.app.selected_lesson = focused.lesson
            self.app.push_screen("lesson")

    def action_quit(self) -> None:
        self.app.exit()
```

`src/git_learn/screens/lesson.py`:
```python
"""Lesson screen — shows task description, handles shell switch."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Markdown

from ..lesson_loader import Lesson


class LessonScreen(Screen):
    """Shows the current lesson task and instructions."""

    BINDINGS = [
        ("enter", "start_exercise", "Start Exercise"),
        ("h", "show_hint", "Hint"),
        ("s", "show_solution", "Solution"),
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, lesson: Lesson) -> None:
        super().__init__()
        self.lesson = lesson
        self.hints_shown = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"\n  [bold]{self.lesson.title}[/bold]"
            f"  |  Level: {self.lesson.level}  |  {self.lesson.points} Punkte\n"
        )
        yield Markdown(self.lesson.body)
        yield Static(f"\n  [bold]Aufgabe:[/bold]\n  {self.lesson.task}")
        yield Static(
            "\n  [dim]Enter: Shell öffnen  |  h: Hint  |  s: Lösung  |  Esc: Zurück[/dim]\n"
        )
        yield Footer()

    def action_start_exercise(self) -> None:
        self.app.start_exercise(self.lesson, self.hints_shown)

    def action_show_hint(self) -> None:
        if self.hints_shown < len(self.lesson.hints):
            hint = self.lesson.hints[self.hints_shown]
            self.hints_shown += 1
            self.mount(Static(f"\n  [yellow]Hint {self.hints_shown}:[/yellow] {hint}"))

    def action_show_solution(self) -> None:
        self.app.solution_viewed = True
        self.mount(Static(f"\n  [red]Lösung:[/red]\n  {self.lesson.solution}"))

    def action_go_back(self) -> None:
        self.app.pop_screen()
```

`src/git_learn/screens/result.py`:
```python
"""Result screen — shows validation results after exercise."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from ..validator.base import ValidationResult


class ResultScreen(Screen):
    """Shows the result of the exercise validation."""

    BINDINGS = [
        ("enter", "next_lesson", "Next"),
        ("r", "retry", "Retry"),
        ("escape", "go_back", "Back to List"),
    ]

    def __init__(
        self,
        results: list[ValidationResult],
        stars: int,
        lesson_title: str,
    ) -> None:
        super().__init__()
        self.results = results
        self.stars = stars
        self.lesson_title = lesson_title

    def compose(self) -> ComposeResult:
        yield Header()
        all_passed = all(r.passed for r in self.results)

        if all_passed:
            star_display = "\u2b50" * self.stars + "\u2606" * (3 - self.stars)
            yield Static(
                f"\n  [bold green]Bestanden![/bold green]  {star_display}\n"
                f"  {self.lesson_title}\n"
            )
        else:
            yield Static(f"\n  [bold red]Noch nicht geschafft.[/bold red]\n")

        for r in self.results:
            icon = "[green]\u2713[/green]" if r.passed else "[red]\u2717[/red]"
            yield Static(f"  {icon} {r.message}")

        if all_passed:
            yield Static("\n  [dim]Enter: Nächste Lektion  |  Esc: Zurück zur Liste[/dim]\n")
        else:
            yield Static("\n  [dim]r: Nochmal versuchen  |  Esc: Zurück zur Liste[/dim]\n")
        yield Footer()

    def action_next_lesson(self) -> None:
        self.app.next_lesson()

    def action_retry(self) -> None:
        self.app.retry_lesson()

    def action_go_back(self) -> None:
        self.app.pop_screen()
        self.app.pop_screen()  # Back to lesson list
```

`src/git_learn/app.py`:
```python
"""Main Textual application for Git Learn."""

from pathlib import Path

from textual.app import App

from .lesson_loader import Lesson, load_all_lessons
from .progress import Progress
from .screens.lesson import LessonScreen
from .screens.lesson_list import LessonListScreen
from .screens.result import ResultScreen
from .setup_exercise import setup_exercise, get_exercise_path, teardown_exercise
from .shell import spawn_shell
from .validator import validate_all


LESSONS_DIR = Path(__file__).parent.parent.parent / "lessons"


class GitLearnApp(App):
    """The Git Learn TUI application."""

    TITLE = "Git Learn"
    CSS = """
    Screen {
        background: $surface;
    }
    """

    def __init__(self, lessons_dir: Path | None = None) -> None:
        super().__init__()
        self._lessons_dir = lessons_dir or LESSONS_DIR
        self.progress = Progress()
        self.lessons: list[Lesson] = []
        self.selected_lesson: Lesson | None = None
        self.solution_viewed = False
        self._current_hints_shown = 0
        self._current_exercise_dir: Path | None = None

    def on_mount(self) -> None:
        self.lessons = load_all_lessons(self._lessons_dir)
        self.push_screen(LessonListScreen(self.lessons, self.progress))

    def start_exercise(self, lesson: Lesson, hints_shown: int) -> None:
        """Set up exercise and drop to shell."""
        self._current_hints_shown = hints_shown
        exercise_dir = get_exercise_path(lesson.slug)
        setup_exercise(lesson, exercise_dir)
        self._current_exercise_dir = exercise_dir

        # Suspend TUI and spawn shell
        with self.suspend():
            spawn_shell(exercise_dir)

        # Back from shell — validate
        self._validate_exercise(lesson)

    def _validate_exercise(self, lesson: Lesson) -> None:
        """Validate the exercise and show results."""
        exercise_dir = self._current_exercise_dir
        if exercise_dir is None:
            return
        results = validate_all(lesson.validation, exercise_dir)
        all_passed = all(r.passed for r in results)

        if all_passed:
            if self.solution_viewed:
                stars = 1
            elif self._current_hints_shown > 0:
                stars = 2
            else:
                stars = 3
            self.progress.complete_lesson(lesson.slug, stars, self._current_hints_shown)
        else:
            stars = 0

        self.push_screen(ResultScreen(results, stars, lesson.title))
        self.solution_viewed = False

    def next_lesson(self) -> None:
        """Move to the next lesson."""
        if self.selected_lesson:
            idx = self.lessons.index(self.selected_lesson)
            if idx + 1 < len(self.lessons):
                self.selected_lesson = self.lessons[idx + 1]
                self.pop_screen()  # Remove result
                self.pop_screen()  # Remove current lesson
                self.push_screen(LessonScreen(self.selected_lesson))

    def retry_lesson(self) -> None:
        """Retry the current lesson."""
        if self.selected_lesson:
            self.pop_screen()  # Remove result screen

    def action_push_lesson(self) -> None:
        """Push lesson screen for the selected lesson."""
        if self.selected_lesson:
            self.push_screen(LessonScreen(self.selected_lesson))
```

**Step 4: Run smoke test**

Run: `pytest tests/test_app.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/git_learn/app.py src/git_learn/screens/ tests/test_app.py
git commit -m "feat: TUI app with lesson list, lesson, and result screens"
```

---

### Task 9: CLI Integration (Wire Everything Together)

**Files:**
- Modify: `src/git_learn/__main__.py`

**Step 1: Write CLI integration test**

Add to `tests/test_app.py`:
```python
from click.testing import CliRunner
from git_learn.__main__ import cli


def test_cli_status() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "Lessons completed" in result.output or "lessons" in result.output.lower()


def test_cli_reset_confirm() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["reset"], input="n\n")
    assert result.exit_code == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_app.py::test_cli_status -v`
Expected: FAIL

**Step 3: Update CLI**

`src/git_learn/__main__.py`:
```python
"""CLI entry point for git-learn."""

from pathlib import Path

import click

from .app import GitLearnApp
from .progress import Progress


LESSONS_DIR = Path(__file__).parent.parent.parent / "lessons"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Git Learn - Interactive Git Terminal Trainer."""
    if ctx.invoked_subcommand is None:
        app = GitLearnApp()
        app.run()


@cli.command()
def status() -> None:
    """Show learning progress."""
    progress = Progress()
    click.echo(f"Lessons completed: {progress.lessons_completed}")
    click.echo(f"Total stars: {progress.total_stars}")

    if progress._data["lessons"]:
        click.echo("\nCompleted lessons:")
        for slug, data in progress._data["lessons"].items():
            stars = "\u2b50" * data["stars"] + "\u2606" * (3 - data["stars"])
            click.echo(f"  {slug}: {stars}")


@cli.command()
def reset() -> None:
    """Reset all progress."""
    if click.confirm("Are you sure you want to reset all progress?"):
        progress = Progress()
        progress.reset()
        click.echo("Progress reset.")
    else:
        click.echo("Cancelled.")


if __name__ == "__main__":
    cli()
```

**Step 4: Run tests**

Run: `pytest tests/test_app.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add src/git_learn/__main__.py tests/test_app.py
git commit -m "feat: CLI commands for status and reset, TUI as default"
```

---

### Task 10: First Lesson Set — Beginner Chapter (Lessons 1.1–1.5)

**Files:**
- Create: `lessons/beginner/01-init.md` (already exists, refine)
- Create: `lessons/beginner/02-editing.md`
- Create: `lessons/beginner/03-staging.md`
- Create: `lessons/beginner/04-selective-add.md`
- Create: `lessons/beginner/05-commit.md`

**Step 1: Create the lessons**

Each lesson follows the established Markdown+Frontmatter format. Write each lesson file with:
- Meaningful setup commands that create a realistic scenario
- Clear task description in German
- 2–3 progressive hints
- Solution
- Validation rules that check the expected git state

Refer to `docs/plans/2026-02-18-git-terminal-trainer-design.md` and Issue #1 for lesson content details.

**Step 2: Test each lesson loads correctly**

Run: `python -c "from git_learn.lesson_loader import load_all_lessons; from pathlib import Path; lessons = load_all_lessons(Path('lessons')); print(f'{len(lessons)} lessons loaded'); [print(f'  {l.slug}: {l.title}') for l in lessons]"`
Expected: All 5 lessons load without errors

**Step 3: Manual test — run a lesson end-to-end**

Run: `git-learn`
Expected: TUI shows lesson list with 5 beginner lessons. Select one, press Enter, solve in shell, check validates correctly.

**Step 4: Commit**

```bash
git add lessons/beginner/
git commit -m "feat: beginner lessons 1.1-1.5 (init, editing, staging, selective add, commit)"
```

---

### Task 11: Remaining Beginner Lessons (1.6–1.8) + Integration Test

**Files:**
- Create: `lessons/beginner/06-log.md`
- Create: `lessons/beginner/07-diff.md`
- Create: `lessons/beginner/08-graph-alias.md`
- Create: `tests/test_integration.py`

**Step 1: Create lessons 1.6–1.8**

Follow same pattern. Lesson 1.8 is special: it validates that the user set up a git alias (`git tree`), using `config_value` validator.

**Step 2: Write integration test**

`tests/test_integration.py`:
```python
"""Integration test: load lesson, setup exercise, validate."""

import subprocess
from pathlib import Path

from git_learn.lesson_loader import load_lesson
from git_learn.setup_exercise import setup_exercise
from git_learn.validator import validate_all


def test_beginner_01_init_full_flow(tmp_path: Path) -> None:
    lesson_path = Path(__file__).parent.parent / "lessons" / "beginner" / "01-init.md"
    if not lesson_path.exists():
        return
    lesson = load_lesson(lesson_path)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    # Simulate user solving the lesson
    # (lesson 01-init just needs a clean working tree after git init)
    results = validate_all(lesson.validation, exercise_dir)
    assert all(r.passed for r in results), [r.message for r in results if not r.passed]
```

**Step 3: Run tests**

Run: `pytest tests/test_integration.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add lessons/beginner/ tests/test_integration.py
git commit -m "feat: beginner lessons 1.6-1.8 (log, diff, graph alias) + integration test"
```

---

### Task 12: CLAUDE.md + README.md Update

**Files:**
- Modify: `CLAUDE.md`
- Create: `README.md`

**Step 1: Update CLAUDE.md with project info**

Update `CLAUDE.md` with build commands, test commands, architecture overview, and stack info.

**Step 2: Create README.md**

Create a README with project description, installation, usage, and contribution guide.

**Step 3: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: update CLAUDE.md and add README"
```

---

### Future Tasks (not in v1 scope, for reference)

- **Task 13–18:** Intermediate, Advanced, Stash, Remotes, Expert lesson chapters
- **Task 19:** Package and publish to PyPI
- **Task 20:** AI Trainer integration (optional v2)
