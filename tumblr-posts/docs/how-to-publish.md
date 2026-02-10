# How to publish a Tumblr post from a plain-text file

This guide walks you through publishing Tumblr text posts with the `tumblr-posts` CLI using OAuth 1.0a API Console credentials.

## 1) Create a plain-text file

```bash
cat > post.txt <<'TEXT'
Today I shipped a small CLI tool.
It reads plain-text files and publishes directly to Tumblr.
TEXT
```

The file content is preserved as-is. The renderer guarantees the final published body ends with a newline.

## 2) Publish your first post

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --title "Ship log" \
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET"
```

## 3) Where do I get `oauth_token` and `oauth_token_secret`?

Open the Tumblr API Console for your app and click **Show keys**. Copy all OAuth 1.0a values:

- `consumer_key`
- `consumer_secret`
- `oauth_token`
- `oauth_token_secret`

`oauth_token_secret` alone is not sufficient; you must provide both token and token secret.

## 4) Add links at the bottom (default)

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET" \
  --insert-links https://example.com https://status.example.com
```

## 5) Add links at the top

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET" \
  --insert-links https://example.com https://docs.example.com \
  --links-position top \
  --links-header "References:"
```

## 6) Add tags to API only

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET" \
  --tags "#Python" " cli " devlog
```

## 7) Add tags to API and body

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --consumer-key "$TUMBLR_CONSUMER_KEY" \
  --consumer-secret "$TUMBLR_CONSUMER_SECRET" \
  --oauth-token "$TUMBLR_OAUTH_TOKEN" \
  --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET" \
  --tags Python CLI DevLog \
  --insert-tags \
  --tags-header "Topics:"
```

## 8) Publish state control: published vs draft vs queue

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state published --consumer-key "$TUMBLR_CONSUMER_KEY" --consumer-secret "$TUMBLR_CONSUMER_SECRET" --oauth-token "$TUMBLR_OAUTH_TOKEN" --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET"
```

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state draft --consumer-key "$TUMBLR_CONSUMER_KEY" --consumer-secret "$TUMBLR_CONSUMER_SECRET" --oauth-token "$TUMBLR_OAUTH_TOKEN" --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET"
```

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state queue --consumer-key "$TUMBLR_CONSUMER_KEY" --consumer-secret "$TUMBLR_CONSUMER_SECRET" --oauth-token "$TUMBLR_OAUTH_TOKEN" --oauth-token-secret "$TUMBLR_OAUTH_TOKEN_SECRET"
```

(You can also use `--state private`.)
