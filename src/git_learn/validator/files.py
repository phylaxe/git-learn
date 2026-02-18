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
