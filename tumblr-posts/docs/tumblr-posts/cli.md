# CLI reference

## Entrypoints

- Console script: `tumblr-posts`
- Module mode: `python -m tumblr_posts`

## Command

### `tumblr-posts publish`

Required options:

- `--blog TEXT`
- `--file PATH`
- `--client-id TEXT`
- `--client-secret TEXT`
- `--access-token TEXT`

Optional options:

- `--title TEXT`
- `--state [published|draft|queue|private]` (default: `published`)
- `--tags TEXT...`
- `--insert-tags`
- `--tags-header TEXT` (default: `Tags:`)
- `--insert-links TEXT...`
- `--links-header TEXT` (default: `Links:`)
- `--links-position [top|bottom]` (default: `bottom`)
- `--api-base-url TEXT`
- `--timeout INTEGER` (default: `30`)
- `--verbose`

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
