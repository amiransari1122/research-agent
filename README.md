# NLP/LLM Research Tracking Agent

Two scripts, run automatically for free via GitHub Actions:
- `paper_digest.py` — every 2 weeks, 10 papers on your chosen topic
- `trend_report.py` — every month, a broader trend/landscape report

No server needed. Reports are saved to `output/` (committed to the repo)
and optionally emailed to you.

## Setup (10-15 minutes, one time)

### 1. Get an API key
Go to https://platform.claude.com, create an account, add credit, and
generate an API key under API Keys.

### 2. Create a GitHub repo
- Create a new **private** repo (your reports will be committed to it).
- Upload all files in this folder, keeping the `.github/workflows/` structure.

### 3. Add secrets
In the repo: Settings → Secrets and variables → Actions → New repository secret.

Required:
- `ANTHROPIC_API_KEY` — your API key from step 1

Optional (only if you want reports emailed, not just committed to the repo):
- `SMTP_SERVER` (e.g. `smtp.gmail.com`)
- `SMTP_PORT` (e.g. `587`)
- `SMTP_USER` (your email address)
- `SMTP_PASS` (an **app password**, not your normal password — for Gmail,
  generate one at https://myaccount.google.com/apppasswords)
- `TO_EMAIL` (where to send the reports — can be the same as SMTP_USER)

If you skip the SMTP secrets, the agent still works — reports just show up
as new files in `output/` in your repo instead of your inbox.

### 4. Enable Actions
Go to the "Actions" tab in your repo and enable workflows if prompted.
That's it — the schedules in `.github/workflows/*.yml` take over from here.

### 5. Test it immediately (don't wait 2 weeks)
Actions tab → select "Biweekly Paper Digest" or "Monthly Trend Report" →
"Run workflow" button → for the digest, set `force_run: true` so it doesn't
skip due to the week-parity check.

## Customizing

- **Change your topic**: edit the `TOPIC` variable at the top of
  `paper_digest.py`, commit the change. Do this every cycle as your thesis
  focus narrows.
- **Change the schedule**: edit the `cron:` line in the workflow files.
  Cron format: `minute hour day month weekday`. https://crontab.guru helps.
- **Change the prompt**: edit `USER_PROMPT` / `SYSTEM_PROMPT` in either
  script to adjust sources, depth, or format.

## Cost

Each run does up to ~15 web searches plus one Claude Sonnet 5 call.
Roughly a few cents to low tens of cents per report — cheap enough that
cost isn't a real constraint here. Check current pricing at
https://platform.claude.com (Docs → Pricing) before relying on this number.

## Notes on the "every 2 weeks" cron trick

GitHub Actions cron doesn't support "every N weeks" natively, only fixed
weekly/monthly patterns. `paper_digest.py` fires weekly but checks the ISO
week number (even/odd) and skips half the time — so effectively it runs
every 2 weeks. If you'd rather have it always run and just track it
yourself, remove the `is_biweekly_run_week()` check in `paper_digest.py`.
