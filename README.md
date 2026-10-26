# Catapult accelerator dashboard

Static site on GitHub Pages: `index.html` (list view) and `map.html` (tree diagram, Innovate UK > Catapults > programmes) both read `data.json`.

## Weekly refresh

The data is refreshed by hand once a week in a live Claude chat. Open a chat with this repository attached and ask:

> Refresh the Catapult dashboard: follow `refresh-instructions.md`, run `validate.py`, and push `data.json`.

- `refresh-instructions.md`: the research and update rules (sources to check, sections, flags, changes and gaps).
- `validate.py`: checks `data.json` against the shape the pages expect. Run `python3 validate.py data.json` before pushing; it exits with an error if the file is malformed.

GitHub Pages redeploys automatically after each push to `main`.

## Access

Public repos publish public pages, so nothing sensitive belongs in this repository. Limiting the page to a team needs either GitHub Enterprise Cloud (private Pages) or hosting the same files behind an access-controlled service such as Cloudflare Pages with Cloudflare Access.

## Local preview

Run `python3 -m http.server` in this folder, then open http://localhost:8000/. Opening the HTML files directly will not work, because the pages fetch `data.json`.
