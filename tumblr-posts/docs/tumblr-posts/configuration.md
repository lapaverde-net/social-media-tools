# Configuration and credentials

`tumblr-posts` is non-interactive and uses Tumblr **OAuth 1.0a** credentials from the Tumblr API Console.

Required credential set:

- `--consumer-key`
- `--consumer-secret`
- `--oauth-token`
- `--oauth-token-secret`

Optional transport settings:

- `--api-base-url` (default `https://api.tumblr.com`)
- `--timeout` (default `30` seconds)

## Environment variable usage

You can pass credentials with environment variables:

```bash
export TUMBLR_CONSUMER_KEY="..."
export TUMBLR_CONSUMER_SECRET="..."
export TUMBLR_OAUTH_TOKEN="..."
export TUMBLR_OAUTH_TOKEN_SECRET="..."
```

Then run:

```bash
tumblr-posts publish --blog myblog.tumblr.com --file ./post.txt
```

### Optional `.env` example

```dotenv
TUMBLR_CONSUMER_KEY=your_consumer_key
TUMBLR_CONSUMER_SECRET=your_consumer_secret
TUMBLR_OAUTH_TOKEN=your_oauth_token
TUMBLR_OAUTH_TOKEN_SECRET=your_oauth_token_secret
```

## Compatibility flags (deprecated)

- `--client-id` maps to `--consumer-key`
- `--client-secret` maps to `--consumer-secret`
- `--access-token` is deprecated and intentionally not auto-mapped because it is ambiguous with OAuth2 bearer terminology.

## Security best practices

- Avoid committing secrets to source control.
- Be cautious with shell history and process lists.
- Prefer keyring/secret managers for shared machines and CI/CD.

## Logging and redaction

Use `--verbose` for debug logging.

The CLI redacts secret values and logs only safe metadata (endpoint path, status, request id, retries).
