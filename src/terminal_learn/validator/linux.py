"""Linux module validators: file permissions, symlinks, directory structure, etc."""

import os
import subprocess
from pathlib import Path

from .base import ValidationResult


def validate_command_output(rule: dict, repo: Path) -> ValidationResult:
    """Run a command and check stdout matches expected output."""
    cmd = rule["cmd"]
    expected = rule["expected"].strip()
    result = subprocess.run(
        cmd, shell=True, cwd=repo, capture_output=True, text=True,
    )
    actual = result.stdout.strip()
    mode = rule.get("mode", "exact")
    if mode == "contains":
        passed = expected in actual
    elif mode == "regex":
        import re
        passed = bool(re.search(expected, actual))
    else:
        passed = actual == expected
    return ValidationResult(
        passed=passed,
        message=f"Command output {'matches' if passed else 'does not match'} expected",
        rule_type="command_output",
    )


def validate_file_permissions(rule: dict, repo: Path) -> ValidationResult:
    """Check file permissions match expected octal string."""
    file_path = repo / rule["path"]
    expected = rule["expected"]
    if not file_path.exists():
        return ValidationResult(
            passed=False,
            message=f"File '{rule['path']}' does not exist",
            rule_type="file_permissions",
        )
    mode = oct(file_path.stat().st_mode)[-3:]
    passed = mode == expected
    return ValidationResult(
        passed=passed,
        message=f"Permissions on '{rule['path']}': {mode} ({'match' if passed else f'expected {expected}'})",
        rule_type="file_permissions",
    )


def validate_symlink_target(rule: dict, repo: Path) -> ValidationResult:
    """Verify a symlink points to the expected target."""
    link_path = repo / rule["path"]
    expected = rule["expected"]
    if not link_path.is_symlink():
        return ValidationResult(
            passed=False,
            message=f"'{rule['path']}' is not a symlink",
            rule_type="symlink_target",
        )
    actual = os.readlink(link_path)
    passed = actual == expected
    return ValidationResult(
        passed=passed,
        message=f"Symlink '{rule['path']}' -> '{actual}' ({'correct' if passed else f'expected {expected}'})",
        rule_type="symlink_target",
    )


def validate_directory_structure(rule: dict, repo: Path) -> ValidationResult:
    """Verify that expected directories/files exist in a tree."""
    expected_paths = rule["expected"]
    missing = []
    for p in expected_paths:
        if not (repo / p).exists():
            missing.append(p)
    passed = len(missing) == 0
    if passed:
        message = "All expected paths exist"
    else:
        message = f"Missing: {', '.join(missing)}"
    return ValidationResult(
        passed=passed,
        message=message,
        rule_type="directory_structure",
    )


def validate_process_running(rule: dict, repo: Path) -> ValidationResult:
    """Check if a process is running (by name)."""
    name = rule["name"]
    result = subprocess.run(
        ["pgrep", "-x", name], capture_output=True, text=True,
    )
    running = result.returncode == 0
    return ValidationResult(
        passed=running,
        message=f"Process '{name}' is {'running' if running else 'not running'}",
        rule_type="process_running",
    )


LINUX_VALIDATORS = {
    "command_output": validate_command_output,
    "file_permissions": validate_file_permissions,
    "symlink_target": validate_symlink_target,
    "directory_structure": validate_directory_structure,
    "process_running": validate_process_running,
}
