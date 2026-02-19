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
