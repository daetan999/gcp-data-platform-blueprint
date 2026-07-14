"""Cloud Run runner shell — illustrative blueprint skeleton.

The same runner serves every product service; TARGET_SCRIPT is the only
per-service difference. See docs/architecture.md — "Runtime model".
"""
from __future__ import annotations

import os
import subprocess
import sys

# --- Environment contract (hard-fail on anything missing) ---------------------

REQUIRED_ENV = (
    "RUNTIME_BUCKET",        # gs://<newsletter-runtime-bucket> or reports bucket
    "TARGET_SCRIPT",         # e.g. example_topic/newsletter.py
    "HELPER_GCS_PREFIX",     # shared/
    "MAIL_SECRET_ID",        # Secret Manager resource id — never the key itself
)

WORKDIR = "/tmp"  # Cloud Run writable scratch; PYTHONPATH for helper imports


def load_environment() -> dict:
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        # No silent degrade: a misconfigured service must fail its health check.
        raise RuntimeError(f"missing required env: {missing}")
    return {k: os.environ[k] for k in REQUIRED_ENV}


def fetch_runtime_assets(env: dict) -> str:
    """Download TARGET_SCRIPT + the three shared helpers from the runtime
    bucket into /tmp. Assets are individual files from one reviewed commit —
    promotion is a file upload, not an image rebuild."""
    raise NotImplementedError("Blueprint stub — GCS download loop omitted")


def execute(script_path: str) -> dict:
    """Run the target via subprocess with PYTHONPATH=/tmp; parse and return
    its structured delivery report. A non-zero exit, missing report, or
    hard-failure flag in the report fails the whole run."""
    proc = subprocess.run(
        [sys.executable, script_path],
        cwd=WORKDIR,
        env={**os.environ, "PYTHONPATH": WORKDIR},
        capture_output=True,
        text=True,
        timeout=15 * 60,
    )
    raise NotImplementedError("Blueprint stub — report parsing omitted")


# HTTP surface: POST /run (invoked by Cloud Scheduler with an OIDC identity)
# and GET /ready (used as the migration verification gate).
