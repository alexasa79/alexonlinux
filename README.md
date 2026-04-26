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
hugo server --bind 0.0.0.0 --baseURL http://localhost:1313/alexonlinux.com/
```

## Codeberg Pages

The configured project URL is:

- `https://alexasa79.codeberg.page/alexonlinux.com/`

Important limitation from current Codeberg documentation: custom domains on the
newer Pages stack do not support repository names containing dots. Since this
repository is named `alexonlinux.com`, using it directly with a custom domain
may require a different repository layout later, for example a dedicated
`pages` repository or a renamed repository.

Sources:

- https://docs.codeberg.org/codeberg-pages/
- https://docs.codeberg.org/codeberg-pages/forgejo-actions/
- https://docs.codeberg.org/codeberg-pages/using-custom-domain/
