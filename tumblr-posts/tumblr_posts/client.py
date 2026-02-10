"""Minimal Tumblr API client wrapper for creating text posts."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests_oauthlib import OAuth1

from .errors import ApiError, AuthError
from .models import PostRequest, PostResponse

LOGGER = logging.getLogger(__name__)


class TumblrClient:
    """Simple requests-based Tumblr API wrapper using OAuth 1.0a signing."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        oauth_token: str,
        oauth_token_secret: str,
        api_base_url: str = "https://api.tumblr.com",
        timeout: int = 30,
        verbose: bool = False,
        retries: int = 3,
        backoff_base: float = 0.5,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.base_url = api_base_url.rstrip("/")
        self.timeout = timeout
        self.verbose = verbose
        self.retries = retries
        self.backoff_base = backoff_base

    def _auth(self) -> OAuth1:
        return OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret,
        )

    def create_text_post(self, request: PostRequest) -> PostResponse:
        endpoint = f"/v2/blog/{request.blog}/post"
        response_data = self._request("POST", endpoint, form_payload=request.to_payload())
        response_obj = response_data.get("response", response_data)
        post_id = response_obj.get("id") or response_obj.get("post_id")
        post_url = response_obj.get("post_url") or response_obj.get("url")
        return PostResponse(post_id=str(post_id) if post_id is not None else None, post_url=post_url, raw=response_data)

    def _request(self, method: str, endpoint: str, form_payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {"Accept": "application/json"}

        for attempt in range(1, self.retries + 2):
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=headers,
                    data=form_payload,
                    auth=self._auth(),
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                if attempt > self.retries:
                    raise ApiError(f"Request failed after retries: {exc}", status_code=0) from exc
                sleep_for = self.backoff_base * (2 ** (attempt - 1))
                LOGGER.debug("Request exception on attempt=%s; retrying in %.2fs", attempt, sleep_for)
                time.sleep(sleep_for)
                continue

            if self.verbose:
                request_id = resp.headers.get("X-Request-Id", "<none>")
                LOGGER.debug("Request completed endpoint=%s status=%s request_id=%s", endpoint, resp.status_code, request_id)

            if resp.status_code in {401, 403}:
                error_message = self._safe_error_message(resp)
                raise AuthError(f"Authentication failed with status {resp.status_code}. {error_message}".strip())

            if 200 <= resp.status_code < 300:
                try:
                    return resp.json()
                except ValueError as exc:
                    raise ApiError("API returned non-JSON response.", status_code=resp.status_code, response_text=resp.text) from exc

            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                if attempt <= self.retries:
                    sleep_for = self._compute_retry_delay(attempt, resp)
                    LOGGER.debug("Transient error status=%s attempt=%s retrying in %.2fs", resp.status_code, attempt, sleep_for)
                    time.sleep(sleep_for)
                    continue

            raise ApiError(
                message=f"Tumblr API error ({resp.status_code}) for endpoint {endpoint}.",
                status_code=resp.status_code,
                response_text=resp.text,
            )

        raise ApiError("Unexpected retry loop state.", status_code=0)

    def _compute_retry_delay(self, attempt: int, response: requests.Response) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
        return self.backoff_base * (2 ** (attempt - 1))

    def _safe_error_message(self, response: requests.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return ""
        if isinstance(payload, dict):
            meta = payload.get("meta")
            if isinstance(meta, dict):
                msg = meta.get("msg")
                if isinstance(msg, str):
                    return msg
            errors = payload.get("errors")
            if isinstance(errors, list) and errors:
                first = errors[0]
                if isinstance(first, dict):
                    detail = first.get("detail")
                    if isinstance(detail, str):
                        return detail
        return ""
