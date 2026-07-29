"""
Monthly NLP/LLM trend report — FREE STACK (Tavily search + Groq/Llama write-up).

Runs on the 1st of every month (see .github/workflows/monthly_trends.yml).
Covers papers, tools/models, industry, and events so you don't fall behind.
"""
import datetime
from common import search_many, ask_groq, save_report, maybe_send_email

SEARCH_QUERIES = [
    "NLP LLM trends this month 2026",
    "new LLM model release 2026",
    "large language model breakthrough paper 2026",
    "NLP conference deadline ACL EMNLP NeurIPS 2026",
    "open source LLM tool framework release 2026",
]

SYSTEM_PROMPT = """You are a research assistant helping a Master's student in
NLP/LLMs stay current on the field. Assume the reader knows NLP fundamentals
already - don't re-explain basics. Work ONLY from the search results given to
you - do not invent papers, models, or events not present in the context.
Be honest about what's hype vs. signal."""


def build_user_prompt(search_context: str) -> str:
    return f"""
Below are raw web search results gathered this month across NLP/LLMs.
Using ONLY this material, write a report covering:

1. Papers: the most-discussed/most-cited new papers you can find in the
   results. Short summary + why they matter.
2. Models & tools: notable new LLMs, open-source releases, libraries, or
   frameworks mentioned in the results.
3. Industry/applications: notable product launches or deployments signaling
   where the field is heading practically.
4. Events: upcoming conference deadlines/dates mentioned in the results.
5. "Signal, not noise": 2-3 sentences on what actually matters this month
   vs. what's hype, based on what you found.

If a section has no solid material in the search results, say so briefly
rather than filling it with generic filler.

Format as a single skimmable report with clear section headers.

SEARCH RESULTS:
{search_context}
"""


def main():
    search_context = search_many(SEARCH_QUERIES, max_results_per_query=3)
    if not search_context:
        print("No search results returned - aborting this run.")
        return

    report = ask_groq(SYSTEM_PROMPT, build_user_prompt(search_context))
    header = f"# NLP/LLM Trend Report - {datetime.date.today().isoformat()}\n\n"
    full_report = header + report

    path = save_report("trend_report", full_report)
    print(f"Saved to {path}")

    maybe_send_email(
        subject=f"[Trend Report] NLP/LLMs - {datetime.date.today().isoformat()}",
        body=full_report,
    )


if __name__ == "__main__":
    main()
