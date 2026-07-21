# GCP Data & Intelligence Platform — Architectural Blueprint

[Architecture](docs/architecture.md) · [Migration playbook](docs/migration-playbook.md) · [Portfolio](https://github.com/daetan999/technical_resume)

## Overview

This repository is a sanitized blueprint of an enterprise Google Cloud data platform and two serverless intelligence products built on top of it:

- **AI newsletter workflows:** seven topic-specific pipelines using resilient RSS ingestion, Gemini-based curation, BigQuery-managed recipient configuration, and SendGrid delivery.
- **Performance reporting:** weekly and monthly property reports with deterministic BigQuery calculations and model-generated narrative restricted to computed figures.

The public repository focuses on infrastructure, service boundaries, reliability controls, deployment procedures, SQL operation shapes, and operating documentation. It does not contain production source code, recipients, credentials, or proprietary integrations.

## Portfolio Role

This repository forms the governed-cloud foundation of the [Enterprise AI Infrastructure Portfolio](https://github.com/daetan999/technical_resume). It shows how data movement, warehouse controls, serverless execution, model boundaries, secrets, and reversible operations shape an enterprise AI platform before application and commercial decisions are made.

## Published Artifact Status

This is a **sanitized architectural blueprint**, not a deployable production environment.

| Available here | Deliberately excluded |
|---|---|
| Service contracts and failure-handling patterns | Proprietary transformations and prompts |
| Synthetic BigQuery DDL, operations, and seed shapes | Live datasets, recipients, and identifiers |
| Deterministic KPI and preference-flow structures | Complete provider integrations and credentials |
| Architecture and migration operating documentation | Infrastructure-as-code and a runnable cloud account |

The workflows below describe the represented design. Methods explicitly marked as blueprint stubs document an omitted integration boundary rather than runnable behavior.

## Public-Portfolio Boundary

- Project IDs, buckets, datasets, table names, service identities, endpoints, property codes, and recipients are placeholders.
- Internal product names and company identifiers are replaced with neutral labels.
- Proprietary transformations and integrations are represented by documented stubs.
- Measured outcomes are aggregated; illustrative examples use synthetic data.
- Current implementation and proposed extension paths are labelled separately.

## Platform Architecture

![GCP platform infrastructure](docs/assets/gcp-infrastructure.svg)

The design combines:

- Private-subnet ingestion and processing
- Cloud NAT and VPN connectivity for external and on-premises systems
- Dataflow, Dataproc, and Composer for movement and orchestration
- BigQuery silver and gold data layers
- Cloud Storage for versioned runtime assets
- Cloud Run for stateless workload services
- Secret Manager, Cloud Logging, and Cloud Monitoring for operations
- Apigee or governed service interfaces for downstream consumption

## AI Newsletter Workflow

![AI newsletter workflow](docs/assets/newsletter-pipeline.svg)

1. Cloud Scheduler invokes a Cloud Run runner using authenticated requests.
2. The runner contract loads approved scripts and shared helpers from Cloud Storage.
3. The ingestion policy defines retry, backoff, response classification, and feed-health outcomes.
4. Gemini is constrained to screening, ranking, and summarizing candidate articles.
5. A deterministic validator checks dates and year references before delivery.
6. BigQuery-backed rules resolve active recipients and exclusions.
7. The delivery contract treats SendGrid HTTP 202 as acceptance.
8. Sent-history state advances only after a ready newsletter and accepted delivery.

## Preference and Unsubscribe Flow

![Preference API workflow](docs/assets/unsubscribe-flow.svg)

- Encrypted tokens carry the recipient and newsletter context.
- GET renders a confirmation page without changing data.
- POST revalidates the token and performs an idempotent BigQuery `MERGE`.
- Preference-link generation is fail-open so a preference-service outage does not block operational delivery.
- Recipient lookup, delivery failure, and sent-history persistence remain hard-fail conditions.

## Performance Reporting Workflow

![Performance reporting workflow](docs/assets/performance-reporting.svg)

The reporting path calculates occupancy, ADR, RevPAR, pickup, and budget variance in SQL before any model call. Gemini receives computed results for narrative generation; it does not calculate the underlying KPIs.

Controls include:

- Date-filter pushdown before reservation expansion
- Deduplication before stay-night calculations
- `SAFE_DIVIDE` for rate measures
- Explicit handling of non-additive metrics
- Availability carry-forward rules across multiple source systems
- Data-quality flags for impossible outputs rather than silent correction

## Key Design Decisions

| Decision | Implementation |
|---|---|
| Pay only when workloads run | Cloud Run services scale to zero and Scheduler controls each cadence independently. |
| Treat configuration as data | Newsletter types, recipients, modes, and activation state are managed through guarded BigQuery operations. |
| Separate recoverable and blocking failures | Preference and footer issues degrade safely; missing recipients, stale data, delivery failures, and subprocess errors fail the run. |
| Restrict model responsibility | LLMs curate and narrate; deterministic code validates dates and calculates business metrics. |
| Keep migrations reversible | Sandbox, UAT, and production promotion use paused schedulers, disabled-send dry runs, validation checks, and rollback steps. |
| Keep secrets out of artifacts | Credentials remain in Secret Manager and environment configuration. |

## Representative Outcomes and Coverage

- Seven newsletter workflows and two reporting cadences
- Nine independently operated serverless services
- BigQuery-managed recipient and preference configuration
- Hardened shared RSS-fetching layer with feed-health outcomes
- Sandbox-to-UAT-to-production migration documentation
- Automated schedules that can be paused per workload

These figures describe the sanitized platform scope; the public repository contains representative code and operation shapes rather than production assets.

## Technology Stack

| Layer | Technology |
|---|---|
| Compute | Cloud Run |
| Scheduling | Cloud Scheduler |
| Warehouse | BigQuery |
| Ingestion and orchestration | Dataflow · Dataproc · Composer |
| Object storage | Cloud Storage |
| LLM | Gemini on Vertex AI |
| Delivery | SendGrid |
| Secrets | Secret Manager |
| Tokens | Fernet encryption |
| Hybrid connectivity | Cloud VPN · NAT · Apigee |

## Repository Map

```text
docs/                          Architecture and migration documentation
docs/assets/                   SVG and Mermaid diagrams
services/newsletter_engine/    Newsletter template and RSS reliability patterns
services/reporting/            Deterministic KPI engine structure
services/preference_api/       Encrypted-token preference API structure
services/runner/               Cloud Run runner and runtime-fetch pattern
services/shared/               BigQuery recipient resolution helpers
sql/tables/                    Recipient, preference, and catalog DDL
sql/operations/                Guarded day-two `MERGE` operations
sql/seeds/                     Synthetic illustrative records
```

## Extension Paths

Potential extensions are documented separately from the implemented blueprint, including reviewed self-service signup, richer monitoring, deployment automation, and expanded catalog-driven topic registration.

## Repository Verification

The published source and diagrams can be checked without a Google Cloud account:

```bash
python -m compileall services
python - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET

for diagram in Path("docs/assets").glob("*.svg"):
    ET.parse(diagram)
print("Python syntax and SVG assets verified")
PY
```

These are artifact checks only. End-to-end verification requires configured Cloud Run, BigQuery, Cloud Storage, Scheduler, Gemini, SendGrid, IAM, and Secret Manager resources that are not published here.

## Limitations

- Integration methods labelled as blueprint stubs do not execute in the public tree.
- The SQL examples use synthetic identifiers and require environment-specific review before use.
- Architecture diagrams communicate service responsibilities, not proof of a live deployment.
- Production use requires infrastructure-as-code, identity design, data-governance review, observability, and recovery testing.

## License

Released under the MIT License.

---

[Part of the Enterprise AI Infrastructure Portfolio](https://github.com/daetan999/technical_resume)
