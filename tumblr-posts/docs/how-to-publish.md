# How to publish a Tumblr post from a plain-text file

This guide walks you through publishing Tumblr text posts with the `tumblr-posts` CLI.

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
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN"
```

## 3) Add links at the bottom (default)

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN" \
  --insert-links https://example.com https://status.example.com
```

This inserts:

- `Links:`
- one link per line

...after your file content, separated by a blank line.

## 4) Add links at the top

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN" \
  --insert-links https://example.com https://docs.example.com \
  --links-position top \
  --links-header "References:"
```

## 5) Add tags to API only

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN" \
  --tags "#Python" " cli " devlog
```

Tags are normalized before sending to Tumblr:

- trimmed
- leading `#` removed
- empty values dropped

## 6) Add tags to API and body

```bash
tumblr-posts publish \
  --blog myblog.tumblr.com \
  --file post.txt \
  --client-id "$TUMBLR_CLIENT_ID" \
  --client-secret "$TUMBLR_CLIENT_SECRET" \
  --access-token "$TUMBLR_ACCESS_TOKEN" \
  --tags Python CLI DevLog \
  --insert-tags \
  --tags-header "Topics:"
```

When `--insert-tags` is present, a readable line is appended to body content, e.g.:

`Topics: Python, CLI, DevLog`

## 7) Publish state control: published vs draft vs queue

Published:

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state published --client-id "$TUMBLR_CLIENT_ID" --client-secret "$TUMBLR_CLIENT_SECRET" --access-token "$TUMBLR_ACCESS_TOKEN"
```

Draft:

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state draft --client-id "$TUMBLR_CLIENT_ID" --client-secret "$TUMBLR_CLIENT_SECRET" --access-token "$TUMBLR_ACCESS_TOKEN"
```

Queue:

```bash
tumblr-posts publish --blog myblog.tumblr.com --file post.txt --state queue --client-id "$TUMBLR_CLIENT_ID" --client-secret "$TUMBLR_CLIENT_SECRET" --access-token "$TUMBLR_ACCESS_TOKEN"
```

(You can also use `--state private`.)

## Common errors and fixes

### 401 Unauthorized
- Cause: invalid or expired `--access-token`.
- Fix: regenerate token and retry.

### 403 Forbidden
- Cause: token lacks permission for the target blog.
- Fix: verify app authorization and blog ownership/permissions.

### 429 Too Many Requests
- Cause: rate limit reached.
- Fix: retry later. The CLI automatically retries transient failures and respects `Retry-After` for HTTP 429.
