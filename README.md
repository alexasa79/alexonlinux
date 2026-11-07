# Alex on Linux

Source for <https://alexonlinux.com/>, built with Hugo and the PaperMod theme.

The site uses Hugo Extended `0.123.7` and PaperMod `v8.0`, pinned by the Git
submodule under `themes/hugo-PaperMod`.

## Content layout

- `content/essays/`: curated published writing
- `static/assets/`: local assets referenced by essays
- `original/`: preserved archive of the broader recovered material

## Local preview

Install Hugo Extended `0.123.7`, then run:

```bash
git submodule update --init --recursive
hugo server --buildDrafts --baseURL http://localhost:1313/
```

## Publishing

Pushing to `main` builds and deploys the website through GitHub Actions to GitHub
Pages. The build includes drafts, matching the previous publishing script.

To rebuild the latest GitHub `main` without a new commit, run `./publish.sh` with
the GitHub CLI installed and authenticated. Local, unpushed changes are not
included in that rebuild.

The workflow pins Hugo `0.123.7` and verifies the downloaded archive's checksum.
It keeps the production `baseURL` from `hugo.yaml` so existing article and asset
URLs remain unchanged.

The custom domain is configured in the repository's Pages settings. DNS must
point `alexonlinux.com` and `www.alexonlinux.com` to GitHub Pages.
