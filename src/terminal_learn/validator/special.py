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


def validate_check_answer(rule: dict, repo: Path) -> ValidationResult:
    answer_file = repo / ".terminal-learn" / "answer"
    if not answer_file.exists():
        return ValidationResult(
            passed=False,
            message="Keine Antwort übermittelt. Nutze: check \"deine antwort\"",
            rule_type="check_answer",
        )
    answer = answer_file.read_text().strip().lower()
    contains = rule["contains"].lower()
    passed = contains in answer
    return ValidationResult(
        passed=passed,
        message=f"Antwort '{answer}' {'enthält' if passed else 'enthält nicht'} '{rule['contains']}'",
        rule_type="check_answer",
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
