# CLI reference

## Entrypoints

- Console script: `tumblr-posts`
- Module mode: `python -m tumblr_posts`

## Command

### `tumblr-posts publish`

Required options:

- `--blog TEXT`
- `--file PATH`
- `--consumer-key TEXT`
- `--consumer-secret TEXT`
- `--oauth-token TEXT`
- `--oauth-token-secret TEXT`

Optional options:

- `--title TEXT`
- `--state [published|draft|queue|private]` (default: `published`)
- `--tags TEXT...`
- `--insert-tags`
- `--tags-header TEXT` (default: `Tags:`)
- `--insert-links TEXT...`
- `--links-header TEXT` (default: `Links:`)
- `--links-position [top|bottom]` (default: `bottom`)
- `--api-base-url TEXT` (default: `https://api.tumblr.com`)
- `--timeout INTEGER` (default: `30`)
- `--verbose`

Environment variable fallback:

- `TUMBLR_CONSUMER_KEY`
- `TUMBLR_CONSUMER_SECRET`
- `TUMBLR_OAUTH_TOKEN`
- `TUMBLR_OAUTH_TOKEN_SECRET`

Deprecated compatibility flags:

- `--client-id` → `--consumer-key`
- `--client-secret` → `--consumer-secret`
- `--access-token` (deprecated; do not use)

Validation behavior:

Missing OAuth values return exit code `2` with:

`Tumblr posting requires OAuth 1.0a: consumer_key, consumer_secret, oauth_token, oauth_token_secret (from the Tumblr API Console).`

### Deprecated auth command

If older automation calls `tumblr-posts auth-login`, the command exits with a message explaining no callback/request-token authorize flow is needed.

## Rendering behavior

- File content is preserved as-is.
- Final body always ends with newline.
- Inserted links/tags blocks are separated by one blank line.
- Tags passed with `--tags` go to API payload; `--insert-tags` controls optional body insertion.

## Exit codes

- `0`: success
- `2`: validation/CLI usage
- `3`: auth errors (`401`/`403`)
- `4`: API errors (other non-2xx)
