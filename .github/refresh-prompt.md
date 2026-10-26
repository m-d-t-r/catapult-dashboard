You maintain `data.json`, which feeds a dashboard of accelerator, incubator and open-call programmes at the nine Innovate UK Catapults. Today's date is given in the instruction that pointed you to this file.

Research each Catapult (Cell and Gene Therapy, Semiconductor, Connected Places, Digital, Energy Systems, High Value Manufacturing, Medicines Discovery, Offshore Renewable Energy, Satellite Applications). Do not rely on news pages alone: also read programmes, opportunities, open-calls, our-priorities, services, funding and event pages, and follow the sitemap. Include partner-run programmes the Catapults host or deliver (for example HMGCC challenges, ESA BIC UK, KQ Labs, UKRI missions).

Then update `data.json` in place:
- `lastChecked`: today's date (YYYY-MM-DD).
- Sections: `closingSoon` (deadline within 30 days, must have a `deadline` ISO date), `openRolling`, `running` (running or recently closed), `horizon` (signalled, not open), `none` (Catapult with no cohort accelerator).
- Each item has: `org`, `name`, `desc` (one line), `deadlineLabel`, `url` (direct source page), optional `deadline`, `note`, `status` (c closing soon, o open or rolling, h horizon, r running or recently closed, n none) and `short` (two lines separated by `|`, at most about 22 characters each, used on the map). Keep `org` values exactly as already used.
- Move items between sections as their dates pass. Remove items that closed more than about six months ago.
- Flags: clear every `isNew` and `updated` flag from last week. Set `isNew: true` on programmes that were not in the file before this run, and `updated: true` on ones whose name, deadline or status changed.
- `changes`: one line per new or materially changed item (before and after for changes). Use `[]` if nothing changed.
- `gaps`: pages you could not read, and anything unconfirmed.
Say "not stated" rather than guessing. Do not change anything except `data.json`.
