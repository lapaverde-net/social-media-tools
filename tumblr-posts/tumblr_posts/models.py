"""Data models for post requests and responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PostRequest:
    """Represents a create-post payload for Tumblr's API."""

    blog: str
    body: str
    title: str | None = None
    state: str = "published"
    tags: list[str] = field(default_factory=list)
    post_type: str = "text"

    def to_payload(self) -> dict[str, Any]:
        """Serialize to an API payload.

        TODO(v2): support additional post types (photo/video/link) when schema is finalized.
        """
        payload: dict[str, Any] = {
            "type": self.post_type,
            "state": self.state,
            "body": self.body,
        }
        if self.title:
            payload["title"] = self.title
        if self.tags:
            payload["tags"] = ",".join(self.tags)
        return payload


@dataclass(slots=True)
class PostResponse:
    """Normalized response from the post creation endpoint."""

    post_id: str | None
    post_url: str | None
    raw: dict[str, Any]
