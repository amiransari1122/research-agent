"""
Shared helpers for the research-tracking agent — FREE STACK VERSION.

Uses:
- Tavily (free tier: 1,000 searches/month) for web search
- Groq (free tier, no credit card) for writing the report, via Llama 3.3 70B

Two API keys needed, both free to obtain:
- TAVILY_API_KEY  -> https://tavily.com     (sign up, key starts with tvly-)
- GROQ_API_KEY    -> https://console.groq.com (sign up, key starts with gsk_)
"""
import os
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText

import requests

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"


def tavily_search(query: str, max_results: int = 5) -> list:
    """Run one search query against Tavily, return a list of results."""
    resp = requests.post(
        TAVILY_URL,
        json={
            "api_key": os.environ["TAVILY_API_KEY"],
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def search_many(queries: list, max_results_per_query: int = 5, max_total_chars: int = 4500) -> str:
    """
    Run several search queries, dedupe by URL, and return the combined
    results formatted as plain text context for the LLM to work from.
    Stops adding results once max_total_chars is reached.
    """
    seen_urls = set()
    blocks = []
    total_chars = 0
    for q in queries:
        try:
            results = tavily_search(q, max_results=max_results_per_query)
        except requests.RequestException as e:
            print(f"Search failed for '{q}': {e}")
            continue
        for r in results:
            url = r.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            block = (
                f"TITLE: {r.get('title', '')}\n"
                f"URL: {url}\n"
                f"CONTENT: {r.get('content', '')[:350]}\n"
            )
            if total_chars + len(block) > max_total_chars:
                continue
            blocks.append(block)
            total_chars += len(block)
    return "\n---\n".join(blocks)


def ask_groq(system_prompt: str, user_prompt: str, max_tokens: int = 2000, max_retries: int = 3) -> str:
    """
    Call Groq's Llama 3.3 70B to write the report from given context.
    Groq's free tier limits tokens PER MINUTE, shared across all your
    requests. If a request gets rejected for being "too large" but it's
    actually just because a recent request used up this minute's quota,
    waiting ~65 seconds and retrying resolves it automatically.
    """
    payload = {
        "model": GROQ_MODEL,
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    for attempt in range(1, max_retries + 1):
        resp = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )

        if resp.status_code in (413, 429) and attempt < max_retries:
            print(
                f"Attempt {attempt}: Groq returned {resp.status_code} "
                f"(likely per-minute quota, not a real size problem). "
                f"Response: {resp.text[:500]}"
            )
            print("Waiting 65 seconds for the quota to reset, then retrying...")
            time.sleep(65)
            continue

        if resp.status_code >= 400:
            print(f"Groq error {resp.status_code} (final attempt): {resp.text}")

        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()

    raise RuntimeError("Groq request failed after all retries.")


def is_biweekly_run_week() -> bool:
    """
    Cron has no native 'every 2 weeks' - this workflow fires weekly, and this
    function decides whether THIS week is an 'on' week, based on ISO week
    number parity. Set FORCE_RUN=true (e.g. for manual/testing runs) to skip
    this check.
    """
    if os.environ.get("FORCE_RUN", "").lower() == "true":
        return True
    iso_week = datetime.now().isocalendar()[1]
    return iso_week % 2 == 0


def save_report(name: str, content: str) -> str:
    """Save the report to output/ as a timestamped markdown file. Returns the path."""
    os.makedirs("output", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"output/{date_str}_{name}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def maybe_send_email(subject: str, body: str) -> None:
    """
    Send the report by email if SMTP env vars are set.
    Required env vars: SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL
    If they're not set, this silently does nothing (report still saved to output/).
    """
    required = ["SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "TO_EMAIL"]
    if not all(os.environ.get(v) for v in required):
        print("SMTP env vars not fully set - skipping email, report saved to output/ only.")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["TO_EMAIL"]

    with smtplib.SMTP(os.environ["SMTP_SERVER"], int(os.environ["SMTP_PORT"])) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.sendmail(os.environ["SMTP_USER"], [os.environ["TO_EMAIL"]], msg.as_string())
    print("Email sent.")
