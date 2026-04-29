# Alex on Linux

This repository now contains the Hugo site for Alex on Linux.

The site uses the `hugo-PaperMod` theme as a Git submodule under
`themes/hugo-PaperMod`. It is pinned to PaperMod `v8.0` because the installed
Hugo version is `0.123.7`; newer PaperMod releases require Hugo `0.146.0` or
newer.

## Content layout

- `content/essays/`: curated published writing
- `static/assets/`: local assets referenced by essays
- `original/`: preserved archive of the broader recovered material

To run locally:

```bash
hugo server --bind 0.0.0.0 --baseURL http://localhost:1313/
```

## Codeberg Pages

The canonical URL is:

- `https://alexonlinux.com/`

The source branch is `main`. Generated output is published to the `pages`
branch in the same Codeberg repository.

The custom domains are listed in `static/.domains` so Hugo copies them to
`public/.domains` during the build:

- `alexonlinux.com`
- `www.alexonlinux.com`

To publish:

```bash
./publish.sh
```

The script removes stale local output, builds the Hugo site, creates or reuses a
local `../pages` worktree for the generated `pages` branch, commits generated
changes if there are any, and pushes `HEAD:pages` to `origin`.

The DNS setup should follow the same pattern used by the `alchemy-lang` site,
with the domain records pointing Codeberg Pages at this repository's Pages
target.

Sources:

- https://docs.codeberg.org/codeberg-pages/
- https://docs.codeberg.org/codeberg-pages/forgejo-actions/
- https://docs.codeberg.org/codeberg-pages/using-custom-domain/
