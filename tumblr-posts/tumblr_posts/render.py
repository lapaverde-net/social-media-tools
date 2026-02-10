"""Rendering helpers for final post body composition."""

from __future__ import annotations


def _normalize_newline_ending(text: str) -> str:
    return text if text.endswith("\n") else f"{text}\n"


def _build_links_block(links: list[str] | None, links_header: str) -> str:
    if not links:
        return ""
    lines = [links_header.strip() or "Links:"] + [link.strip() for link in links if link.strip()]
    return "\n".join(lines)


def _build_tags_block(tags: list[str], tags_header: str) -> str:
    if not tags:
        return ""
    label = tags_header.strip() or "Tags:"
    return f"{label} {', '.join(tags)}"


def render_post_body(
    file_content: str,
    *,
    links: list[str] | None = None,
    links_header: str = "Links:",
    links_position: str = "bottom",
    tags: list[str] | None = None,
    insert_tags: bool = False,
    tags_header: str = "Tags:",
) -> str:
    """Create final post text while preserving original file text and newline behavior."""
    file_body = file_content
    links_block = _build_links_block(links, links_header)

    blocks: list[str] = []
    if links_position == "top" and links_block:
        blocks.append(links_block)

    blocks.append(file_body.rstrip("\n"))

    if links_position == "bottom" and links_block:
        blocks.append(links_block)

    if insert_tags and tags:
        blocks.append(_build_tags_block(tags, tags_header))

    return _normalize_newline_ending("\n\n".join(blocks))
