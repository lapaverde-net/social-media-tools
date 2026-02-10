"""CLI application for publishing plain-text files to Tumblr."""

from __future__ import annotations

import json
import logging
from enum import Enum
from pathlib import Path

import typer

from .auth import Credentials
from .client import TumblrClient
from .errors import ApiError, AuthError, ValidationError
from .models import PostRequest
from .render import render_post_body
from .utils import ensure_text_file_contents, normalize_tags, redact_secret

app = typer.Typer(help="Publish plain-text files to Tumblr.", no_args_is_help=True)
LOGGER = logging.getLogger("tumblr_posts")


class PostState(str, Enum):
    published = "published"
    draft = "draft"
    queue = "queue"
    private = "private"


class LinksPosition(str, Enum):
    top = "top"
    bottom = "bottom"


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


@app.callback()
def _root() -> None:
    """tumblr-posts command group."""


def _log_redacted_credentials(credentials: Credentials) -> None:
    LOGGER.debug(
        "Using credentials client_id=%s client_secret=%s access_token=%s",
        credentials.client_id,
        redact_secret(credentials.client_secret),
        redact_secret(credentials.access_token),
    )


@app.command("publish")
def publish(
    blog: str = typer.Option(..., "--blog", help="Target Tumblr blog, e.g. myblog.tumblr.com"),
    file: Path = typer.Option(..., "--file", exists=False, dir_okay=False, readable=True, help="Plain-text file to publish."),
    client_id: str = typer.Option(..., "--client-id", help="Tumblr app client ID."),
    client_secret: str = typer.Option(..., "--client-secret", help="Tumblr app client secret."),
    access_token: str = typer.Option(..., "--access-token", help="Tumblr OAuth access token used as bearer token."),
    title: str | None = typer.Option(None, "--title", help="Optional post title."),
    state: PostState = typer.Option(PostState.published, "--state", case_sensitive=False, help="Post state.", show_default=True),
    tags: list[str] | None = typer.Option(None, "--tags", help="One or more tags for the API tags field."),
    insert_tags: bool = typer.Option(False, "--insert-tags", help="Insert tags into body as readable text."),
    tags_header: str = typer.Option("Tags:", "--tags-header", help="Prefix label when inserting tags in body."),
    insert_links: list[str] | None = typer.Option(None, "--insert-links", help="One or more links to add to content."),
    links_header: str = typer.Option("Links:", "--links-header", help="Header label for inserted links block."),
    links_position: LinksPosition = typer.Option(LinksPosition.bottom, "--links-position", case_sensitive=False, help="Insert links at top or bottom."),
    api_base_url: str = typer.Option("https://api.tumblr.com/v2", "--api-base-url", help="Tumblr API base URL."),
    timeout: int = typer.Option(30, "--timeout", min=1, help="HTTP timeout in seconds."),
    verbose: bool = typer.Option(False, "--verbose", help="Enable debug logs."),
) -> None:
    """Publish a text post from a plain-text file."""
    _configure_logging(verbose)
    try:
        valid_state = state.value
        valid_links_position = links_position.value

        credentials = Credentials.from_cli(client_id=client_id, client_secret=client_secret, access_token=access_token)
        _log_redacted_credentials(credentials)

        file_content = ensure_text_file_contents(file)
        normalized_tags = normalize_tags(tags)

        body = render_post_body(
            file_content,
            links=insert_links,
            links_header=links_header,
            links_position=valid_links_position,
            tags=normalized_tags,
            insert_tags=insert_tags,
            tags_header=tags_header,
        )

        client = TumblrClient(credentials=credentials, base_url=api_base_url, timeout=timeout)
        response = client.create_text_post(
            PostRequest(
                blog=blog,
                title=title,
                state=valid_state,
                body=body,
                tags=normalized_tags,
            )
        )

        details: dict[str, str] = {}
        if response.post_id:
            details["post_id"] = response.post_id
        if response.post_url:
            details["post_url"] = response.post_url

        message = "Successfully published Tumblr post"
        if details:
            message = f"{message}: {json.dumps(details)}"
        typer.echo(message)

    except ValidationError as exc:
        typer.echo(f"ERROR(validation): {exc}", err=True)
        raise typer.Exit(code=2)
    except AuthError as exc:
        typer.echo(f"ERROR(auth): {exc}", err=True)
        raise typer.Exit(code=3)
    except ApiError as exc:
        body_preview = f" Response: {exc.response_text[:300]}" if exc.response_text else ""
        typer.echo(f"ERROR(api): {exc}.{body_preview}", err=True)
        raise typer.Exit(code=4)


def main() -> None:
    """Console script entrypoint."""
    app()
