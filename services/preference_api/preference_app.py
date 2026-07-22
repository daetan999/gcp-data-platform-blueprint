"""Preference (unsubscribe) API — illustrative blueprint skeleton.

Contract: GET is idempotent and writes nothing; only an explicit POST mutates.
Preference-link and footer minting may degrade when this service is unavailable.
Already stored opt-outs remain authoritative and their lookup is fail-closed.
"""
from __future__ import annotations

# Framework elided: any minimal WSGI/ASGI app fits this shape.


def decode_token(token: str) -> dict:
    """Fernet-decrypt the footer token → {email, newsletter_type}.
    The key lives in Secret Manager; tokens are self-contained, so there is
    no token table to store, index, or leak."""
    raise NotImplementedError("Blueprint stub — key handling omitted")


def get_preferences(token: str):
    """GET /preferences/:token — render a confirmation page.
    Invalid/expired token → error page, no data written. Mail-client link
    previewers hit this constantly; that is why GET must never mutate."""
    raise NotImplementedError("Blueprint stub")


def post_preferences(token: str):
    """POST /preferences/:token — re-decode the token (never trust the GET),
    then MERGE-upsert the unsubscribe row:

        MERGE `<PROJECT_ID>.email_config.newsletter_unsubscribe` ...
        WHEN MATCHED THEN UPDATE SET is_unsubscribed = TRUE, ...
        WHEN NOT MATCHED THEN INSERT ...

    Idempotent by construction — double-submits are harmless."""
    raise NotImplementedError("Blueprint stub — MERGE statement omitted")


def ready():
    """GET /ready — verifies secret access and BigQuery reachability.
    Used as the hard gate in migration runbook 3."""
    raise NotImplementedError("Blueprint stub")
