"""
Bi-weekly paper digest — FREE STACK (Tavily search + Groq/Llama write-up).

Runs every 2 weeks (see .github/workflows/biweekly_digest.yml).
Searches for recent papers on your topic and emails/saves a summary.
"""
import datetime
from common import search_many, ask_groq, save_report, maybe_send_email, is_biweekly_run_week

# --- EDIT THIS: your current research focus -------------------------------
TOPIC = "hallucination detection and mitigation in retrieval-augmented generation (RAG) systems"
# ----------------------------------------------------------------------------

# Multiple angled queries tend to surface more/better results than one query.
SEARCH_QUERIES = [
    f"{TOPIC} arxiv 2026",
    f"{TOPIC} paper",
    f"{TOPIC} ACL EMNLP NeurIPS",
    f"recent research {TOPIC}",
]

SYSTEM_PROMPT = """You are a research assistant helping a Master's student in
NLP/LLMs track literature for their thesis. Work ONLY from the search results
given to you below — do not invent papers, authors, or links that aren't in
the provided context. Be precise and don't pad the report with filler."""


def build_user_prompt(search_context: str) -> str:
    return f"""
Topic: {TOPIC}

Below are raw web search results (title, URL, content snippet) gathered on
this topic. Using ONLY this material:

1. Select up to 10 of the most relevant, distinct papers/articles from the
   results (fewer is fine if the results don't contain 10 genuine papers -
   never invent ones that aren't there).
2. For each one give:
   - Title, link (use the exact URL given)
   - 2-3 sentence summary of the core contribution, based on the snippet
   - 1 sentence on why it's relevant to the topic
   - A novelty/gap note: what open question does it leave, or what would
     extending it look like?
3. Group by sub-theme if patterns emerge.
4. End with a short "if I were picking a thesis angle from this batch"
   paragraph, flagging the most promising unexplored gap.

Keep it scannable in under 10 minutes. If the search results are too thin
or off-topic to support 10 solid entries, say so honestly instead of padding.

SEARCH RESULTS:
{search_context}
"""


def main():
    if not is_biweekly_run_week():
        print("Off week - skipping (this runs every 2 weeks).")
        return

    search_context = search_many(SEARCH_QUERIES, max_results_per_query=5)
    if not search_context:
        print("No search results returned - aborting this run.")
        return

    report = ask_groq(SYSTEM_PROMPT, build_user_prompt(search_context))
    header = f"# Paper Digest - {TOPIC}\n{datetime.date.today().isoformat()}\n\n"
    full_report = header + report

    path = save_report("paper_digest", full_report)
    print(f"Saved to {path}")

    maybe_send_email(
        subject=f"[Paper Digest] {TOPIC} - {datetime.date.today().isoformat()}",
        body=full_report,
    )


if __name__ == "__main__":
    main()
