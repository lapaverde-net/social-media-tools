# tumblr-posts

`tumblr-posts` is a production-oriented CLI package for publishing plain-text files as Tumblr text posts. It supports CLI-based credentials, post states, tag handling, and optional insertion of links/tags into the rendered post body.

## Installation

```bash
pip install .
```

Or install editable during development:

```bash
pip install -e .
```

## Quickstart

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file ./post.txt \
  --title "Hello Tumblr" \
  --state published \
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN" \
  --tags python cli \
  --insert-links https://example.com https://docs.example.com
```

## Documentation

- User HOW-TO guide: [`docs/how-to-publish.md`](docs/how-to-publish.md)
- Package documentation index: [`docs/tumblr-posts/index.md`](docs/tumblr-posts/index.md)

## Security notes

Credentials are passed by command-line flags in v1. Be careful: command history and process listings may expose secrets.

Recommended mitigations:

- Use environment variables and shell expansion instead of hardcoding secrets.
- Use a secure shell history configuration (or disable history for sensitive commands).
- Use CI/CD secret stores for automation.
