"""
Bi-weekly paper digest.

Runs every 2 weeks (see .github/workflows/biweekly_digest.yml).
Searches for 10 recent papers on your topic and emails/saves a summary.
"""
import datetime
from common import call_claude, save_report, maybe_send_email, is_biweekly_run_week

# --- EDIT THIS: your current research focus -------------------------------
TOPIC = "hallucination detection and mitigation in retrieval-augmented generation (RAG) systems"
# ----------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a research assistant helping a Master's student in
NLP/LLMs track literature for their thesis. Be precise, cite real papers with
real links, and don't pad the report with filler."""

USER_PROMPT = f"""
Topic: {TOPIC}

1. Search arXiv (cs.CL, cs.LG), Google Scholar, and top-venue proceedings
   (ACL, EMNLP, NAACL, NeurIPS, ICLR, ICML) for the most recent papers on
   this topic. Prioritize papers from the last 2-3 weeks; if there aren't
   enough, include the most-cited recent ones from the last 3 months.
2. Return exactly 10 papers. For each one give:
   - Title, authors, venue/date, link
   - 2-3 sentence summary of the core contribution
   - 1 sentence on why it's relevant to the topic
   - A novelty/gap note: what open question does it leave, or what would
     extending it look like?
3. Group papers by sub-theme if patterns emerge.
4. End with a short "if I were picking a thesis angle from this batch"
   paragraph, flagging the paper(s) with the most promising unexplored gap.

Keep it scannable in under 10 minutes. No filler.
"""

def main():
    if not is_biweekly_run_week():
        print("Off week — skipping (this runs every 2 weeks).")
        return

    report = call_claude(SYSTEM_PROMPT, USER_PROMPT)
    header = f"# Paper Digest — {TOPIC}\n{datetime.date.today().isoformat()}\n\n"
    full_report = header + report

    path = save_report("paper_digest", full_report)
    print(f"Saved to {path}")

    maybe_send_email(
        subject=f"[Paper Digest] {TOPIC} — {datetime.date.today().isoformat()}",
        body=full_report,
    )

if __name__ == "__main__":
    main()
