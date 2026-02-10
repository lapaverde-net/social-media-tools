# Troubleshooting

## Error matrix

| Symptom | Exit code | Likely cause | Action |
|---|---:|---|---|
| `ERROR(validation)` | 2 | Missing/invalid option value (`--state`, file path, credentials) | Correct CLI input and retry |
| `ERROR(auth)` with 401 | 3 | Invalid or expired token | Refresh token |
| `ERROR(auth)` with 403 | 3 | Missing permission for blog | Verify app scope/blog permissions |
| `ERROR(api)` with 429 | 4 | Rate limiting | Retry later; client retries automatically and honors `Retry-After` |
| `ERROR(api)` with 5xx | 4 | Tumblr transient/server issue | Retry; client uses exponential backoff |

## Diagnostics tips

- Add `--verbose` to print endpoint, status, and request id.
- Verify API base URL if testing against a non-default environment.
- Validate that the blog hostname is correct (`myblog.tumblr.com`).

## Tumblr API notes

- Different response wrappers may return either `id` or `post_id`; the client normalizes both.
- v1 only implements text posts. Photo/video/link post flows are TODO for future versions.
