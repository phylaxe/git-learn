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
