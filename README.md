# Catapult accelerator dashboard

Static site: `index.html` (list view) and `map.html` (tree diagram) both read `data.json`.

A GitHub Action (`.github/workflows/refresh.yml`) runs every Monday, asks Claude to research the nine Catapults and rewrite `data.json`, then commits it. The site redeploys from the repo.

## Setup
1. Create a repository and push these files.
2. Add a repository secret named `ANTHROPIC_API_KEY`.
3. Install the Claude GitHub app on the repo (needed by `claude-code-action`; see its README for current inputs).
4. Turn on GitHub Pages (Settings, Pages, deploy from the main branch root).
5. Restrict access: see below.
6. Run the workflow once from the Actions tab to test.

## Access for your team
Public repos publish public pages. To limit the page to your organisation, use a private repo with GitHub Pages access control, which needs GitHub Enterprise Cloud. Without it, host the same folder behind Cloudflare Access, Netlify password protection or your internal server instead.

## Local preview
`python3 -m http.server` in this folder, then open http://localhost:8000/ (the pages fetch `data.json`, so opening the file directly won't work).
