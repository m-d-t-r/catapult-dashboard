# Catapult accelerator map

Private working repository for the weekly map of accelerator, incubator and open-call programmes across the nine Innovate UK Catapults. The shared output is a one-page A3 landscape PDF.

## Weekly refresh

Once a week, open a chat with Claude, attach this repository, and ask:

> Refresh the Catapult map: follow `refresh-instructions.md`, run `validate.py`, push `data.json`, and produce this week's PDF with `render_pdf.py`.

## Files

- `data.json`: all programme data.
- `refresh-instructions.md`: research and update rules (sources to check, sections, flags, changes and gaps).
- `validate.py`: checks `data.json` before it is committed. Run `python3 validate.py data.json`.
- `render_pdf.py`: builds the A3 landscape PDF from `map.html` and `data.json`, using the IBM Plex fonts in `fonts/`. Needs Python Playwright with Chromium.
- `map.html` and `index.html`: the map and list views. They fetch `data.json`, so serve the folder with `python3 -m http.server` rather than opening the files directly.
