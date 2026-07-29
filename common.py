"""
Shared helpers for the research-tracking agent.
"""
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import anthropic

MODEL = "claude-sonnet-5"


def call_claude(system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
    """Call Claude with the web search tool enabled and return the final text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        tools=[{"type": "web_search_20250305", "max_uses": 15}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()


def save_report(name: str, content: str) -> str:
    """Save the report to output/ as a timestamped markdown file. Returns the path."""
    os.makedirs("output", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"output/{date_str}_{name}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def is_biweekly_run_week() -> bool:
    """
    Cron has no native 'every 2 weeks' — this workflow fires weekly, and this
    function decides whether THIS week is an 'on' week, based on ISO week
    number parity. Set FORCE_RUN=true (e.g. for manual/testing runs) to skip
    this check.
    """
    if os.environ.get("FORCE_RUN", "").lower() == "true":
        return True
    iso_week = datetime.now().isocalendar()[1]
    return iso_week % 2 == 0


def maybe_send_email(subject: str, body: str) -> None:
    """
    Send the report by email if SMTP env vars are set.
    Required env vars: SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL
    If they're not set, this silently does nothing (report still saved to output/).
    """
    required = ["SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "TO_EMAIL"]
    if not all(os.environ.get(v) for v in required):
        print("SMTP env vars not fully set — skipping email, report saved to output/ only.")
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
