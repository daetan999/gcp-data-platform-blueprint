"""Topic-newsletter template — illustrative blueprint skeleton.

Every newsletter topic is a copy of this shape with its own FEEDS list and
topic brief. The three-stage Gemini pipeline, the deterministic year gate,
and the delivery contract are identical across topics by construction.
"""
from __future__ import annotations

import os
import re

# --- Topic configuration (per-newsletter) ------------------------------------

NEWSLETTER_TYPE = "example_topic"          # must exist in newsletter_type_catalog
TOPIC_BRIEF = "One paragraph telling the model exactly what this audience cares about."

# Curated feed list: direct publisher RSS, or source-constrained Google News
# queries against reputable domains only. Production topics carry ~40-60 feeds.
FEEDS: list[dict] = [
    {"name": "Example Publisher", "url": "https://example.com/feed.xml"},
]

# Env-driven model config — never hardcoded, changeable without redeploy.
NARRATIVE_MODEL = os.getenv("NARRATIVE_MODEL", "gemini-flash-class")
GEMINI_LOCATION = os.getenv("GEMINI_LOCATION", "<region>")

ALLOW_SEND = os.getenv("ALLOW_SEND", "false").lower() == "true"

# --- Stage 1 + 2: screen, dedup, rank ----------------------------------------

def screen_articles(articles: list[dict]) -> list[dict]:
    """Gemini call 1 — relevance + quality gate against TOPIC_BRIEF."""
    raise NotImplementedError("Blueprint stub — proprietary prompt omitted")


def _headline_score(title: str) -> tuple[int, int]:
    """Best-survivor dedup scoring: prefer titles carrying a concrete figure
    (currency, percentage, count), then longer titles. Deterministic Python —
    the model does not pick survivors."""
    has_figure = int(bool(re.search(r"[$€£¥]|\d+(\.\d+)?\s*(%|bn|m\b|billion|million)", title, re.I)))
    return (has_figure, len(title))


def deduplicate_by_title(articles: list[dict]) -> list[dict]:
    """Cluster near-duplicate headlines; keep the highest _headline_score."""
    raise NotImplementedError("Blueprint stub — similarity clustering omitted")


def rank_and_select(articles: list[dict], top_n: int = 8) -> list[dict]:
    """Gemini call 2 — rank + source/region diversity selection."""
    raise NotImplementedError("Blueprint stub — proprietary prompt omitted")


# --- Stage 3: grounded narrative with the anti-hallucination stack ------------

FACTUAL_FIDELITY_RULES = """
FACTUAL FIDELITY RULES:
- Reproduce dates, years, quarters/halves, currencies and figures EXACTLY as
  they appear in the source Context.
- Never infer, adjust, or "correct" a year. If the source states no date,
  state none. If a figure is ambiguous, omit it rather than guess.
SELF-CHECK: before emitting, re-read each summary and takeaway against that
article's Context and confirm every date, number and currency matches.
"""

_YEAR_FORMS = re.compile(r"(?:FY|1H|2H|Q[1-4]\s*)?'?(\d{2,4})(?:/\d{2})?")


def validate_briefing(analyses: list[dict], source_articles: list[dict]) -> list[str]:
    """Deterministic year gate. Any 4-digit year (or shorthand: FY26, 1H26,
    2025/26, '26) present in generated text but absent from that article's
    title/context/URL becomes an issue string fed back into the retry loop.

    This layer needs no model cooperation — it is the backstop that turned a
    silent date-mutation incident into a structurally prevented error class.
    """
    raise NotImplementedError("Blueprint stub — full extraction table omitted")


def build_briefing(selected: list[dict]) -> list[dict]:
    """Gemini call 3 — summary + takeaway per article, retried with structured
    year-gate feedback until validate_briefing returns no issues."""
    raise NotImplementedError("Blueprint stub — proprietary prompt omitted")


# --- Delivery -----------------------------------------------------------------

def main() -> dict:
    """Run contract: returns a structured delivery report to the runner.
    Fail-open: unsubscribe filtering, footer minting. Hard-fail: recipient
    lookup, non-202 delivery, sent-history persistence."""
    raise NotImplementedError("Blueprint stub — see docs/architecture.md")


if __name__ == "__main__":
    main()
