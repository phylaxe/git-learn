"""Validator registry -- dispatches validation rules to handler functions."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

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
from .special import (
    validate_stash_empty,
    validate_tag_exists,
    validate_remote_exists,
    validate_hook_exists,
    validate_config_value,
    validate_check_answer,
)

VALIDATORS: dict[str, Callable] = {
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
    "stash_empty": validate_stash_empty,
    "tag_exists": validate_tag_exists,
    "remote_exists": validate_remote_exists,
    "hook_exists": validate_hook_exists,
    "config_value": validate_config_value,
    "check_answer": validate_check_answer,
}


def validate_rule(
    rule: dict, repo: Path, extra_validators: dict[str, Callable] | None = None
) -> ValidationResult:
    """Validate a single rule against a repo."""
    rule_type = rule["type"]
    all_validators = VALIDATORS
    if extra_validators:
        all_validators = {**VALIDATORS, **extra_validators}
    validator = all_validators.get(rule_type)
    if validator is None:
        return ValidationResult(
            passed=False,
            message=f"Unknown validation type: {rule_type}",
            rule_type=rule_type,
        )
    return validator(rule, repo)


def validate_all(
    rules: list[dict], repo: Path, extra_validators: dict[str, Callable] | None = None
) -> list[ValidationResult]:
    """Validate all rules, return list of results."""
    return [validate_rule(rule, repo, extra_validators) for rule in rules]
