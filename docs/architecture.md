# Architecture Deep-Dive

## Runtime model — one runner, many services

Every product service (seven newsletter topics, two report cadences) runs the **same runner shell** on Cloud Run. The runner is deliberately dumb:

1. Load secrets from Secret Manager and configuration from environment variables — hard-fail on anything missing.
2. Download the target script plus three shared helpers (`rss_fetcher`, `recipients`, `preference_tokens`) from the environment's runtime bucket into `/tmp`.
3. Execute the target via subprocess with `PYTHONPATH=/tmp`, capture the structured delivery report, and return it as the HTTP response to the Scheduler invocation.

Why this shape instead of an image per service:

- **Review-what-you-run:** the bucket holds individual files from one reviewed commit; promoting a change is a file upload, not an image rebuild across nine services.
- **Blast-radius control:** each topic is its own Cloud Run service and its own Scheduler job — pausable and testable in isolation.
- **One escape hatch:** `TARGET_SCRIPT` is the only thing that differs between services of the same family.

## Storage model

Two fixed buckets per environment (newsletters, reports). No release folders, no checksum manifests — versioning comes from the reviewed commit and hash verification during migration.

```
gs://<newsletter-runtime-bucket>/
  <topic_folder>/            one folder per newsletter topic
    <topic_script>.py
    sent_articles.json       cross-run dedup history
    newsletter_log.json      per-run health log
  shared/                    the three runtime helpers
  design_files/              inline logo assets
  cloud_run_runner/          runner source
  preference/                preference API source
  sql/                       operational SQL kept next to the data

gs://<reports-runtime-bucket>/
  weekly/  monthly/  shared/  design_files/
```

## BigQuery data model

The operational configuration dataset is `email_config`:

| Table | Role | Write path |
|---|---|---|
| `email_recipient_mapping` | Who receives what, in which send mode, for which property | One-time certified seed + guarded MERGE operations |
| `newsletter_unsubscribe` | Topic-level or `'all'` opt-outs | Preference API MERGE upserts only |
| `newsletter_type_catalog` | Valid newsletter types as data (`newsletter_type`, `is_active`, `supports_unsubscribe`, `script_name`) | Guarded MERGE with a naming `ASSERT` |

Design decisions worth stealing:

- **Catalog validation is advisory; opt-out enforcement is authoritative.** A catalog check may warn and continue, but an unsubscribe-table lookup failure stops delivery. The send path never substitutes the unfiltered audience.
- **Recipient identity is data, not code.** Test lanes vs production lanes are `send_mode` values; property assignments are `property_code` values. Activating a stakeholder is an `UPDATE`, not a deploy.
- **Seeds are one-shot by construction.** The production seed opens with a BigQuery scripting `ASSERT` that aborts if the table is non-empty — reruns cannot double-insert.

The lakehouse side follows a silver → gold discipline: source-conformed silver tables (per-PMS room inventory, reservations) and consumer-facing gold views (P&L view, property master view, reservations output). Reporting reads **only** gold views plus the three silver inventory tables it needs for availability.

## The availability (AAN) model

Available-room-nights come from three PMS-specific inventory tables with different schemas, unioned onto a common `(date, property, available_rooms)` shape. For any night with no inventory row, the engine carries the most recent available count forward up to 30 days. Properties with constant availability carry forward exactly; variable-availability properties carry forward with a small, accepted error. A night that is still missing after the window drops out of the denominator **and flags the result** rather than silently pretending completeness.

## Reliability contracts

| Concern | Contract |
|---|---|
| RSS source failure | Retry with backoff on 429/5xx; classify one of 8 outcome statuses; per-source health in the run log; a failed source never kills the run |
| Preference API down | Link and footer minting may be omitted; stored preferences still apply |
| Unsubscribe filter failure | Hard failure; never fall back to the unfiltered audience |
| Recipient lookup failure | Hard failure — surfaced in the runner response |
| SendGrid non-202 | Hard failure per recipient, aggregated in the delivery report |
| Sent-history load/save failure | Hard failure — duplicate-prevention is not optional |
| Stale finance data / required property skip | Hard failure for report runs |

## Security posture

- No public IPs in the ingestion subnet; SaaS access via NAT static egress IPs; on-prem EPM via IPsec VPN.
- Secrets exist only in Secret Manager; scripts receive secret *IDs* via env and resolve them at start-up.
- Unsubscribe tokens are Fernet-encrypted payloads — no PII in URLs, no token table to protect.
- Scheduler invokes services with OIDC service identities; each service family has a dedicated service account.
