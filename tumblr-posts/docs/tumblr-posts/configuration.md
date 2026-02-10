# Configuration and credentials

`tumblr-posts` v1 is CLI-only and non-interactive. Credentials must be provided as command-line parameters:

- `--client-id`
- `--client-secret`
- `--access-token`

Optional transport settings:

- `--api-base-url` (default `https://api.tumblr.com/v2`)
- `--timeout` (default `30` seconds)

## Security best practices

- Prefer environment variables:
  - `--client-id "$TUMBLR_CLIENT_ID"`
  - `--client-secret "$TUMBLR_CLIENT_SECRET"`
  - `--access-token "$TUMBLR_ACCESS_TOKEN"`
- Avoid checking credentials into scripts or shell history.
- Use dedicated secrets management for CI/CD.

## Logging and redaction

Use `--verbose` for debug logging.

The CLI logs endpoint/status/request-id where available, and redacts sensitive values (`client_secret`, `access_token`).
