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
    """Direct match against the unsubscribe table (type or 'all').
    Fail-open: on lookup failure, warn and return the input list — a
    preference-subsystem problem must never block operational sends."""
    raise NotImplementedError("Blueprint stub")
