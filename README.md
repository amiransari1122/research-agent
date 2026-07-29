# NLP/LLM Research Tracking Agent — Free Stack

Two scripts, run automatically for free via GitHub Actions, using a
**fully free** API stack:
- **Tavily** (free tier: 1,000 searches/month, no credit card) — web search
- **Groq** (free tier, no credit card) — writes the report using Llama 3.3 70B

- `paper_digest.py` — every 2 weeks, searches your topic, writes a digest
- `trend_report.py` — every month, a broader trend/landscape report

Reports save to `output/` (committed to the repo) and optionally get emailed.

## Setup (15-20 minutes, one time)

### 1. Get a free Tavily API key
- Go to https://tavily.com → sign up (no credit card)
- Your API key is on the dashboard, starts with `tvly-`

### 2. Get a free Groq API key
- Go to https://console.groq.com → sign up (no credit card)
- Create an API key, starts with `gsk_`

### 3. Create a GitHub repo
- Create a new **private** repo.
- Upload all files in this folder, keeping the `.github/workflows/` structure.

### 4. Add secrets
Repo → Settings → Secrets and variables → Actions → New repository secret.

Required:
- `TAVILY_API_KEY`
- `GROQ_API_KEY`

Optional (only if you want reports emailed, not just saved to the repo):
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `TO_EMAIL`
  (see earlier setup notes — Gmail needs an app password, not your normal one)

### 5. Enable Actions
Actions tab → enable workflows if prompted.

### 6. Test it immediately
Actions tab → pick a workflow → "Run workflow" → for the digest, set
`force_run: true` so it doesn't skip due to the week-parity check.

## Customizing

- **Topic**: edit `TOPIC` at the top of `paper_digest.py`.
- **Schedule**: edit the `cron:` line in the workflow files.
- **Search queries**: edit `SEARCH_QUERIES` in either script — more/better
  angled queries = better source material for the report.
- **Prompt**: edit `SYSTEM_PROMPT` / `build_user_prompt()` in either script.

## Cost

$0. Both free tiers comfortably cover this volume:
- Tavily: ~9-20 searches per run x 3 runs/month = well under the 1,000/month cap
- Groq: 3 calls/month is nowhere near free-tier rate limits (30 req/min, ~1,000 req/day)

## Honest trade-off vs. the Claude API version

This free stack trades some quality for $0 cost:
- **Search quality**: Tavily is a solid general web search API, but it isn't
  purpose-built for academic paper search the way Claude's tool-use +
  reasoning about arXiv/Scholar is. You may get more blog posts/news
  alongside papers — the prompts try to filter for real papers/results but
  can't invent sources that aren't in the search results.
- **Synthesis quality**: Llama 3.3 70B (via Groq) is a strong open model,
  but the "which paper has the most interesting thesis gap" kind of nuanced
  judgment tends to be a bit shallower than what Opus/Sonnet produce.
  Read the reports with that in mind — treat them as a strong starting
  point for your own reading, not a substitute for actually reading the
  papers that catch your eye.
- Both scripts are written to only work from actual search results (not
  invent papers) — if a run's search results are thin, the report will
  say so rather than padding with made-up content.

If quality ever feels too thin, the previous Claude-API version of these
scripts is a straightforward drop-in swap — happy to hand that version back
anytime.

## Notes on the "every 2 weeks" cron trick

GitHub Actions cron doesn't support "every N weeks" natively. `paper_digest.py`
fires weekly but checks the ISO week number (even/odd) and skips half the
time - so effectively it runs every 2 weeks.
