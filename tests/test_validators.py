"""Tests for validators."""

import subprocess
from pathlib import Path

from terminal_learn.validator import validate_rule
from terminal_learn.validator.base import ValidationResult


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
    # Default branch could be master or main
    result_master = validate_rule({"type": "branch_active", "expected": "master"}, tmp_repo)
    result_main = validate_rule({"type": "branch_active", "expected": "main"}, tmp_repo)
    assert result_master.passed or result_main.passed


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
