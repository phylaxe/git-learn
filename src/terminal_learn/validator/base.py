"""Base validator interface."""

from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a single validation check."""

    passed: bool
    message: str
    rule_type: str
