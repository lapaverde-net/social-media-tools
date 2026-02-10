"""Minimal Tumblr API client wrapper for creating text posts."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from .auth import Credentials
from .errors import ApiError, AuthError
from .models import PostRequest, PostResponse

LOGGER = logging.getLogger(__name__)


class TumblrClient:
    """Simple requests-based Tumblr API wrapper."""

    def __init__(
        self,
        credentials: Credentials,
        base_url: str = "https://api.tumblr.com/v2",
        timeout: int = 30,
        retries: int = 3,
        backoff_base: float = 0.5,
    ) -> None:
        self.credentials = credentials
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff_base = backoff_base

    def create_text_post(self, request: PostRequest) -> PostResponse:
        """Create a text post.

        TODO(v2): support photo/video/link post creation in dedicated methods.
        """
        endpoint = f"/blog/{request.blog}/posts"
        response_data = self._request("POST", endpoint, json_payload=request.to_payload())
        # Tumblr wrappers often place useful fields under response object.
        response_obj = response_data.get("response", response_data)
        post_id = response_obj.get("id") or response_obj.get("post_id")
        post_url = response_obj.get("post_url") or response_obj.get("url")
        return PostResponse(post_id=str(post_id) if post_id is not None else None, post_url=post_url, raw=response_data)

    def _request(self, method: str, endpoint: str, json_payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.credentials.auth_header(),
            "X-Client-Id": self.credentials.client_id,
        }

        for attempt in range(1, self.retries + 2):
            try:
                resp = requests.request(method, url, headers=headers, json=json_payload, timeout=self.timeout)
            except requests.RequestException as exc:
                if attempt > self.retries:
                    raise ApiError(f"Request failed after retries: {exc}", status_code=0) from exc
                sleep_for = self.backoff_base * (2 ** (attempt - 1))
                LOGGER.debug("Request exception on attempt %s; retrying in %.2fs", attempt, sleep_for)
                time.sleep(sleep_for)
                continue

            request_id = resp.headers.get("X-Request-Id", "<none>")
            LOGGER.debug("Request completed endpoint=%s status=%s request_id=%s", endpoint, resp.status_code, request_id)

            if resp.status_code in {401, 403}:
                raise AuthError(f"Authentication failed with status {resp.status_code}.")

            if 200 <= resp.status_code < 300:
                try:
                    return resp.json()
                except ValueError as exc:
                    raise ApiError("API returned non-JSON response.", status_code=resp.status_code, response_text=resp.text) from exc

            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                if attempt <= self.retries:
                    sleep_for = self._compute_retry_delay(attempt, resp)
                    LOGGER.debug(
                        "Transient error status=%s on attempt=%s, retrying in %.2fs",
                        resp.status_code,
                        attempt,
                        sleep_for,
                    )
                    time.sleep(sleep_for)
                    continue

            raise ApiError(
                message=f"Tumblr API error ({resp.status_code}) for endpoint {endpoint}.",
                status_code=resp.status_code,
                response_text=resp.text,
            )

        raise ApiError("Unexpected retry loop state.", status_code=0)

    def _compute_retry_delay(self, attempt: int, response: requests.Response) -> float:
        """Use Retry-After for 429 if present, otherwise exponential backoff."""
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            return float(retry_after)
        return self.backoff_base * (2 ** (attempt - 1))
