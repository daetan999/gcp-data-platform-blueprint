"""Shared RSS reliability layer — illustrative blueprint skeleton.

One helper used by every newsletter topic. Replaced per-script silent fetch
loops with a single hardened client that makes source health observable.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FetchStatus(Enum):
    """Every fetch resolves to exactly one of eight outcome classes —
    per-source health becomes a queryable time series instead of a mystery."""
    OK = "ok"
    OK_EMPTY = "ok_empty"                  # 200, parsed, zero entries
    HTML_RESPONSE = "html_response"        # 200 but an HTML page, not a feed
    RATE_LIMITED = "rate_limited"          # 429 after retries exhausted
    SERVER_ERROR = "server_error"          # 5xx after retries exhausted
    CLIENT_ERROR = "client_error"          # other 4xx
    PARSE_ERROR = "parse_error"            # transport ok, feed unparseable
    NETWORK_ERROR = "network_error"        # DNS / TLS / timeout

RETRYABLE = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 2.0

# Browser-profile headers: several reputable publishers serve bot requests an
# HTML challenge page with HTTP 200 — which a naive parser reads as "empty
# feed" forever. Detecting HTML-200 responses was the single biggest
# reliability win in this layer.
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; newsletter-fetcher)",
    "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8",
}


@dataclass
class FetchResult:
    source_name: str
    status: FetchStatus
    entries: list
    detail: str = ""


def fetch_feed(name: str, url: str) -> FetchResult:
    """Fetch one feed with retry/backoff on RETRYABLE statuses, HTML-200
    detection, and outcome classification. Never raises — a dead source is a
    classified data point, not a crashed run."""
    raise NotImplementedError("Blueprint stub — retry/classification loop omitted")


def fetch_all(feeds: list[dict]) -> tuple[list, list[FetchResult]]:
    """Fetch every configured source; return (all_entries, per_source_health).
    The health list is written to the run log for trend analysis."""
    raise NotImplementedError("Blueprint stub")
