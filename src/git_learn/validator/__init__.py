"""Validator registry -- dispatches validation rules to handler functions."""

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
