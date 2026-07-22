"""BigQuery recipient resolution — illustrative blueprint skeleton.

The audience is data, not code: who receives what lives in
`email_config.email_recipient_mapping`, opt-outs in
`email_config.newsletter_unsubscribe`, and valid topics in
`email_config.newsletter_type_catalog`.
"""
from __future__ import annotations

import os

# Fully-qualified table ids arrive via env — the same code serves UAT and
# production with no branches.
EMAIL_RECIPIENT_BQ_TABLE = os.getenv("EMAIL_RECIPIENT_BQ_TABLE", "<PROJECT_ID>.email_config.email_recipient_mapping")
UNSUBSCRIBE_BQ_TABLE = os.getenv("UNSUBSCRIBE_BQ_TABLE", "<PROJECT_ID>.email_config.newsletter_unsubscribe")
NEWSLETTER_TYPE_CATALOG_BQ_TABLE = os.getenv("NEWSLETTER_TYPE_CATALOG_BQ_TABLE", "")


class UnsubscribeLookupError(RuntimeError):
    """Raised when recipient preferences cannot be resolved safely."""


def _normalize_email(value: str) -> str:
    """Return the canonical form used by the illustrative SQL contract."""
    return value.strip().lower()


def _lookup_unsubscribed_emails(newsletter_type: str) -> set[str]:
    """Load topic-level and global opt-outs from BigQuery.

    The public blueprint omits the BigQuery client and parameterized query.
    Deployments must implement this boundary and let failures propagate.
    """
    raise NotImplementedError("Blueprint stub: BigQuery unsubscribe query omitted")


def validate_unsubscribe_type_from_catalog(newsletter_type: str) -> None:
    """Best-effort catalog check — WARNING-ONLY AND FAIL-OPEN by design.

    Missing env var, missing table, failed query, or an uncatalogued type each
    print a warning and the send continues exactly as before. The catalog
    exists so new topics need no code change; it must never become a new way
    for sends to fail."""
    raise NotImplementedError("Blueprint stub — catalog query omitted")


def get_newsletter_recipients(newsletter_type: str, send_mode: str = "production") -> list[str]:
    """Resolve the send list: active recipients for this type/mode, minus
    unsubscribes matching this type or 'all', deduplicated.

    HARD-FAIL contract: query failure or an empty final list raises — a run
    that reached delivery with nobody to deliver to is an incident, not a
    silent no-op."""
    raise NotImplementedError("Blueprint stub — parameterized query omitted")


def filter_unsubscribed(recipients: list[str], newsletter_type: str) -> list[str]:
    """Return a normalized, deduplicated audience with opt-outs removed.

    Fail closed: an unsubscribe lookup or result-shape failure raises
    ``UnsubscribeLookupError``. The caller must stop delivery rather than
    return the unfiltered audience.
    """
    normalized_type = newsletter_type.strip()
    if not normalized_type:
        raise ValueError("newsletter_type must not be blank")

    try:
        unsubscribed: set[str] = set()
        for email in _lookup_unsubscribed_emails(normalized_type):
            normalized_email = _normalize_email(email)
            if normalized_email:
                unsubscribed.add(normalized_email)
    except Exception as exc:
        raise UnsubscribeLookupError(
            f"Unable to enforce unsubscribe preferences for {normalized_type!r}"
        ) from exc

    filtered: list[str] = []
    seen: set[str] = set()
    for email in recipients:
        normalized_email = _normalize_email(email)
        if not normalized_email or normalized_email in seen:
            continue
        seen.add(normalized_email)
        if normalized_email not in unsubscribed:
            filtered.append(normalized_email)

    return filtered
