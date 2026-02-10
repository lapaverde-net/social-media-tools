"""Custom error types and exit code mapping for tumblr-posts."""

from __future__ import annotations


class TumblrPostsError(Exception):
    """Base error for this package."""


class ValidationError(TumblrPostsError):
    """Raised when CLI values fail validation."""


class AuthError(TumblrPostsError):
    """Raised when API authentication fails (401/403)."""


class ApiError(TumblrPostsError):
    """Raised when Tumblr API returns an unexpected non-2xx response."""

    def __init__(self, message: str, status_code: int, response_text: str = "") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class RetryableError(ApiError):
    """Raised internally for retryable API conditions."""
