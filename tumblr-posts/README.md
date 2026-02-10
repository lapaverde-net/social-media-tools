# tumblr-posts

`tumblr-posts` is a production-oriented CLI package for publishing plain-text files as Tumblr text posts using OAuth 1.0a credentials from the Tumblr API Console.

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
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET" \
  --tags python cli \
  --insert-links https://example.com https://docs.example.com
```

## Getting credentials from Tumblr API Console

Tumblr posting in this package uses **OAuth 1.0a**, not OAuth2 bearer-token auth. In the Tumblr API Console, use **Show keys** to copy the four required values:

- `consumer_key`
- `consumer_secret`
- `oauth_token` (sometimes labeled token/access token)
- `oauth_token_secret` (sometimes labeled token_secret)

**Important:** token_secret alone is not enough; you need both token + token_secret.

## Documentation

- User HOW-TO guide: [`docs/how-to-publish.md`](docs/how-to-publish.md)
- Package documentation index: [`docs/tumblr-posts/index.md`](docs/tumblr-posts/index.md)

## Security

Credentials may be visible in shell history and process listings if passed directly on the CLI.

Recommended mitigations:

- Prefer environment variables and shell expansion.
- Use a `.env` file with restricted permissions if desired.
- Use OS keyring/secret managers for local automation.
- Use CI/CD secret stores for pipelines.
