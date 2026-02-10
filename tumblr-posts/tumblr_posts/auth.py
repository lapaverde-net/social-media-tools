"""Authentication helpers for Tumblr API calls."""

from __future__ import annotations

from dataclasses import dataclass

from .utils import ensure_nonempty


@dataclass(slots=True)
class Credentials:
    """CLI-provided Tumblr credentials for this non-interactive v1 client."""

    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_cli(cls, client_id: str, client_secret: str, access_token: str) -> "Credentials":
        """Validate and construct credentials from CLI flags."""
        return cls(
            client_id=ensure_nonempty(client_id, "client-id"),
            client_secret=ensure_nonempty(client_secret, "client-secret"),
            access_token=ensure_nonempty(access_token, "access-token"),
        )

    def auth_header(self) -> dict[str, str]:
        """Build Authorization header from access token."""
        return {"Authorization": f"Bearer {self.access_token}"}
