"""Tests for special validators."""

import subprocess
from pathlib import Path

from terminal_learn.validator import validate_rule


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


def test_check_answer_correct(tmp_repo: Path) -> None:
    marker_dir = tmp_repo / ".terminal-learn"
    marker_dir.mkdir(exist_ok=True)
    answer_file = marker_dir / "answer"
    answer_file.write_text("Zweite Datei hinzugefügt\n")
    result = validate_rule({"type": "check_answer", "contains": "Zweite Datei"}, tmp_repo)
    assert result.passed


def test_check_answer_wrong(tmp_repo: Path) -> None:
    marker_dir = tmp_repo / ".terminal-learn"
    marker_dir.mkdir(exist_ok=True)
    answer_file = marker_dir / "answer"
    answer_file.write_text("falsche antwort\n")
    result = validate_rule({"type": "check_answer", "contains": "Zweite Datei"}, tmp_repo)
    assert not result.passed


def test_check_answer_missing(tmp_repo: Path) -> None:
    result = validate_rule({"type": "check_answer", "contains": "Zweite Datei"}, tmp_repo)
    assert not result.passed


def test_check_answer_case_insensitive(tmp_repo: Path) -> None:
    marker_dir = tmp_repo / ".terminal-learn"
    marker_dir.mkdir(exist_ok=True)
    answer_file = marker_dir / "answer"
    answer_file.write_text("zweite datei hinzugefügt\n")
    result = validate_rule({"type": "check_answer", "contains": "Zweite Datei"}, tmp_repo)
    assert result.passed


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
