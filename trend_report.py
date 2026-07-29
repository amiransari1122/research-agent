"""
Monthly NLP/LLM trend report.

Runs on the 1st of every month (see .github/workflows/monthly_trends.yml).
Covers papers, tools/models, industry, and events so you don't fall behind.
"""
import datetime
from common import call_claude, save_report, maybe_send_email

SYSTEM_PROMPT = """You are a research assistant helping a Master's student in
NLP/LLMs stay current on the field. Assume the reader knows NLP fundamentals
already — don't re-explain basics. Be honest about what's hype vs. signal."""

USER_PROMPT = """
Cover the past month across NLP/LLMs broadly:

1. Papers: 5-8 of the most-discussed/most-cited new papers (arXiv, ACL
   anthology, top labs' publications). Short summary + why people are
   talking about it.
2. Models & tools: notable new LLMs, open-source releases, libraries, or
   frameworks launched this month.
3. Industry/applications: notable product launches or deployments using
   LLMs/NLP that signal where the field is heading practically.
4. Events: upcoming conference deadlines/dates (ACL, EMNLP, NeurIPS, ICLR,
   workshops) relevant in the next 1-3 months, especially paper deadlines.
5. "Signal, not noise": 2-3 sentences on what actually matters this month
   vs. what's hype.

Format as a single skimmable report with clear section headers.
"""

def main():
    report = call_claude(SYSTEM_PROMPT, USER_PROMPT)
    header = f"# NLP/LLM Trend Report — {datetime.date.today().isoformat()}\n\n"
    full_report = header + report

    path = save_report("trend_report", full_report)
    print(f"Saved to {path}")

    maybe_send_email(
        subject=f"[Trend Report] NLP/LLMs — {datetime.date.today().isoformat()}",
        body=full_report,
    )

if __name__ == "__main__":
    main()
