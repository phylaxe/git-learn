"""Integration tests for Linux lessons: load → setup → simulate solution → validate."""

import os
import subprocess
from pathlib import Path

import pytest

from terminal_learn.lesson_loader import load_lesson
from terminal_learn.setup_exercise import setup_exercise, MARKER_DIR
from terminal_learn.validator import validate_all
from terminal_learn.validator.linux import LINUX_VALIDATORS


LINUX_LESSONS = Path(__file__).parent.parent / "lessons" / "linux"


def _load_and_setup(lesson_path: Path, tmp_path: Path) -> tuple:
    """Load lesson, set up exercise, return (lesson, exercise_dir)."""
    if not lesson_path.exists():
        pytest.skip(f"Lesson file not found: {lesson_path}")
    lesson = load_lesson(lesson_path)
    exercise_dir = tmp_path / "exercise"
    # No git init needed — use no config (Linux lessons don't need git)
    setup_exercise(lesson, exercise_dir, config=None)
    return lesson, exercise_dir


def _setup_linux(lesson_path: Path, tmp_path: Path) -> tuple:
    """Load lesson and setup without git init (pure filesystem exercise)."""
    if not lesson_path.exists():
        pytest.skip(f"Lesson file not found: {lesson_path}")
    lesson = load_lesson(lesson_path)
    exercise_dir = tmp_path / "exercise"
    if exercise_dir.exists():
        import shutil
        shutil.rmtree(exercise_dir)
    exercise_dir.mkdir(parents=True)
    marker_dir = exercise_dir / MARKER_DIR
    marker_dir.mkdir()

    # Run setup commands
    for step in lesson.setup:
        subprocess.run(
            step["cmd"], shell=True, cwd=exercise_dir,
            capture_output=True, check=True,
        )
    return lesson, exercise_dir


def _simulate(cmds: str | list[str], cwd: Path) -> None:
    """Run shell commands simulating the user's solution."""
    if isinstance(cmds, str):
        cmds = [cmds]
    for cmd in cmds:
        subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, check=True)


def _assert_passes(lesson, exercise_dir: Path) -> None:
    """Assert all validations pass."""
    results = validate_all(lesson.validation, exercise_dir, LINUX_VALIDATORS)
    failed = [r.message for r in results if not r.passed]
    assert all(r.passed for r in results), f"Failed: {failed}"


# ── Chapter 1: Navigation ──────────────────────────────────────────────


def test_navigation_01_pwd_ls(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "navigation" / "01-pwd-ls.md", tmp_path)
    # Simulate: user submits check answer with exercise path
    marker = ex / MARKER_DIR / "answer"
    marker.write_text(str(ex))
    _assert_passes(lesson, ex)


def test_navigation_02_cd_paths(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "navigation" / "02-cd-paths.md", tmp_path)
    _simulate("touch docs/archiv/hier.txt", ex)
    _assert_passes(lesson, ex)


def test_navigation_03_tree_find(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "navigation" / "03-tree-find.md", tmp_path)
    _simulate("find . -name '*.ts' -o -name '*.tsx' > typescript-files.txt", ex)
    _assert_passes(lesson, ex)


# ── Chapter 2: Files ───────────────────────────────────────────────────


def test_files_01_create_copy(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "files" / "01-create-copy.md", tmp_path)
    _simulate([
        "mkdir -p projekt/backup",
        "cp projekt/src/main.py projekt/backup/",
        "touch projekt/src/utils.py",
    ], ex)
    _assert_passes(lesson, ex)


def test_files_02_remove_link(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "files" / "02-remove-link.md", tmp_path)
    _simulate([
        "rm alt/temp.txt",
        "rm alt/debug.log",
        "ln -s ../alt/daten/config.txt neu/config-link",
    ], ex)
    _assert_passes(lesson, ex)


def test_files_03_wildcards(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "files" / "03-wildcards.md", tmp_path)
    _simulate([
        "mv *.jpg *.png sortiert/bilder/",
        "mv *.md *.txt *.pdf sortiert/dokumente/",
        "mv *.py *.sh sortiert/code/",
    ], ex)
    _assert_passes(lesson, ex)


# ── Chapter 3: Permissions ─────────────────────────────────────────────


def test_permissions_01_read_permissions(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "permissions" / "01-read-permissions.md", tmp_path)
    marker = ex / MARKER_DIR / "answer"
    marker.write_text("rwx------")
    _assert_passes(lesson, ex)


def test_permissions_02_chmod(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "permissions" / "02-chmod.md", tmp_path)
    _simulate([
        "chmod 755 deploy.sh",
        "chmod 600 config.txt",
        "chmod 664 public.txt",
    ], ex)
    _assert_passes(lesson, ex)


def test_permissions_03_chown_groups(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "permissions" / "03-chown-groups.md", tmp_path)
    # Lesson is designed for Docker (user=root). Simulate Docker answer.
    marker = ex / MARKER_DIR / "answer"
    marker.write_text("root")
    _simulate("echo 'teamwork' > shared/team.txt", ex)
    _assert_passes(lesson, ex)


# ── Chapter 4: Text ───────────────────────────────────────────────────


def test_text_01_cat_head_tail(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "text" / "01-cat-head-tail.md", tmp_path)
    _simulate([
        "head -n 5 logfile.txt > erste.txt",
        "tail -n 3 logfile.txt > letzte.txt",
    ], ex)
    # Count lines and submit answer
    result = subprocess.run(
        "wc -l < logfile.txt", shell=True, cwd=ex, capture_output=True, text=True,
    )
    count = result.stdout.strip()
    marker = ex / MARKER_DIR / "answer"
    marker.write_text(count)
    _assert_passes(lesson, ex)


def test_text_02_grep(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "text" / "02-grep.md", tmp_path)
    _simulate([
        "grep 'ERROR' server.log > errors.txt",
        "grep -rl 'export' src/ > exports.txt",
    ], ex)
    _assert_passes(lesson, ex)


def test_text_03_sed_awk(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "text" / "03-sed-awk.md", tmp_path)
    import platform
    # macOS sed -i requires backup extension; GNU sed does not
    if platform.system() == "Darwin":
        sed_cmd = "sed -i '' 's/Old Name/Neuer Autor/g' metadata.txt"
    else:
        sed_cmd = "sed -i 's/Old Name/Neuer Autor/g' metadata.txt"
    _simulate([
        sed_cmd,
        "awk -F, '{print $1\",\"$3}' mitarbeiter.csv > namen-staedte.txt",
    ], ex)
    _assert_passes(lesson, ex)


# ── Chapter 5: Pipes ──────────────────────────────────────────────────


def test_pipes_01_pipe_redirect(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "pipes" / "01-pipe-redirect.md", tmp_path)
    _simulate([
        "grep '200' access.log | wc -l > ok-count.txt",
        "grep -v '200' access.log > errors.log",
    ], ex)
    _assert_passes(lesson, ex)


def test_pipes_02_tee_xargs(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "pipes" / "02-tee-xargs.md", tmp_path)
    _simulate([
        "sort fruits.txt | uniq > unique-fruits.txt",
        "find cleanup/ -name '*.tmp' -exec rm {} +",
    ], ex)
    _assert_passes(lesson, ex)


# ── Chapter 6: Search ─────────────────────────────────────────────────


def test_search_01_find_advanced(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "search" / "01-find-advanced.md", tmp_path)
    _simulate([
        "find projekt/ -name '*.py' > python-files.txt",
        "find projekt/tests/ -type f -exec chmod 755 {} +",
    ], ex)
    _assert_passes(lesson, ex)


def test_search_02_locate_which(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "search" / "02-locate-which.md", tmp_path)
    marker = ex / MARKER_DIR / "answer"
    # Find actual bash path
    result = subprocess.run("which bash", shell=True, capture_output=True, text=True)
    marker.write_text(result.stdout.strip())
    _simulate("type cd > cd-type.txt", ex)
    _assert_passes(lesson, ex)


# ── Chapter 7: Processes ──────────────────────────────────────────────


def test_processes_01_ps_top(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "processes" / "01-ps-top.md", tmp_path)
    _simulate("ps aux > prozesse.txt", ex)
    _assert_passes(lesson, ex)


def test_processes_02_signals_bg(tmp_path: Path) -> None:
    lesson, ex = _setup_linux(LINUX_LESSONS / "processes" / "02-signals-bg.md", tmp_path)
    # The worker script writes to /exercise/bg-output.txt (Docker path).
    # For local testing, rewrite to use the actual exercise dir.
    worker = ex / "worker.sh"
    worker.write_text(
        f"#!/bin/bash\nwhile true; do echo running >> {ex}/bg-output.txt; sleep 1; done\n"
    )
    worker.chmod(0o755)
    # Start worker in background, capture PID, let it write, then kill
    _simulate([
        f"bash -c './worker.sh & echo $! > worker-pid.txt && sleep 2 && kill $(cat worker-pid.txt) 2>/dev/null; true'",
    ], ex)
    _assert_passes(lesson, ex)
