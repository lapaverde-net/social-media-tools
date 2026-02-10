"""Utility helpers for normalization, redaction, and file handling."""

from __future__ import annotations

from pathlib import Path

from .errors import ValidationError


def ensure_text_file_contents(file_path: Path) -> str:
    """Read plain-text content from a file path."""
    if not file_path.exists():
        raise ValidationError(f"Input file does not exist: {file_path}")
    if not file_path.is_file():
        raise ValidationError(f"Input path is not a file: {file_path}")
    return file_path.read_text(encoding="utf-8")


def normalize_tags(tags: list[str] | None) -> list[str]:
    """Trim whitespace, drop leading #, and drop empty values."""
    normalized: list[str] = []
    for tag in tags or []:
        candidate = tag.strip()
        if candidate.startswith("#"):
            candidate = candidate[1:].strip()
        if candidate:
            normalized.append(candidate)
    return normalized


def ensure_nonempty(value: str | None, field_name: str) -> str:
    """Validate required credentials and other text fields."""
    if value is None or not value.strip():
        raise ValidationError(f"Missing required value for --{field_name}.")
    return value.strip()


def redact_secret(secret: str, unmasked: int = 4) -> str:
    """Return a masked representation of a secret."""
    if not secret:
        return "<empty>"
    if len(secret) <= unmasked:
        return "*" * len(secret)
    return "*" * (len(secret) - unmasked) + secret[-unmasked:]
