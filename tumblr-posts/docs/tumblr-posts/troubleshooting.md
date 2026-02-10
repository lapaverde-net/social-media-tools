# Troubleshooting

## Error matrix

| Symptom | Exit code | Likely cause | Action |
|---|---:|---|---|
| `ERROR(validation)` | 2 | Missing required OAuth 1.0a values | Provide consumer_key, consumer_secret, oauth_token, oauth_token_secret |
| `ERROR(auth)` with 401 | 3 | Wrong token/token secret pair, revoked token, token issued for different app | Re-copy OAuth 1.0a keys from API Console and ensure app/token match |
| `ERROR(auth)` with 403 | 3 | Authenticated but missing blog permission or wrong blog identifier | Verify blog hostname and that token has publish rights |
| `ERROR(api)` with 429 | 4 | Rate limiting | Use queue/draft, reduce publish bursts; retries honor `Retry-After` |
| `ERROR(api)` with 5xx | 4 | Tumblr transient/server issue | Retry; client uses exponential backoff |

## 401 Unauthorized

Common causes:

- `oauth_token` and `oauth_token_secret` are from different token generations.
- Token was revoked in Tumblr settings.
- Consumer keys belong to app A while token belongs to app B.

Fix checklist:

1. Open Tumblr API Console and click **Show keys**.
2. Copy all four OAuth 1.0a values again.
3. Confirm blog/account matches the token owner.

## 403 Forbidden

Common causes:

- Token lacks permission to post to the target blog.
- Blog identifier is incorrect (`myblog.tumblr.com`).

Fix checklist:

1. Confirm target blog hostname.
2. Verify app authorization and roles for the account/blog.

## 429 Too Many Requests

- The client retries transient responses and uses `Retry-After` when present.
- If you publish high volume, prefer queue posts and spread requests over time.

## Diagnostics tips

- Add `--verbose` to print endpoint paths, status, and request IDs.
- Confirm credentials are loaded from intended env vars/flags.
- Ensure no OAuth2 bearer token assumptions in your automation.
