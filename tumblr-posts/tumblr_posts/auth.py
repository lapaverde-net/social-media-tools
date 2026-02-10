"""Authentication helpers for Tumblr OAuth 1.0a API calls."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ValidationError
from .utils import ensure_nonempty

OAUTH1_REQUIRED_MESSAGE = (
    "Tumblr posting requires OAuth 1.0a: consumer_key, consumer_secret, "
    "oauth_token, oauth_token_secret (from the Tumblr API Console)."
)


@dataclass(slots=True)
class Credentials:
    """CLI-provided Tumblr OAuth 1.0a credentials."""

    consumer_key: str
    consumer_secret: str
    oauth_token: str
    oauth_token_secret: str

    @classmethod
    def from_cli(
        cls,
        consumer_key: str | None,
        consumer_secret: str | None,
        oauth_token: str | None,
        oauth_token_secret: str | None,
    ) -> "Credentials":
        """Validate and construct credentials from CLI flags."""
        try:
            return cls(
                consumer_key=ensure_nonempty(consumer_key, "consumer-key"),
                consumer_secret=ensure_nonempty(consumer_secret, "consumer-secret"),
                oauth_token=ensure_nonempty(oauth_token, "oauth-token"),
                oauth_token_secret=ensure_nonempty(oauth_token_secret, "oauth-token-secret"),
            )
        except ValidationError as exc:
            raise ValidationError(OAUTH1_REQUIRED_MESSAGE) from exc
