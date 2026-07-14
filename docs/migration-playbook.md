# Migration Playbook — Sandbox → UAT → Production

The platform was migrated from a development sandbox project into dedicated UAT and production projects — nine services, three BigQuery tables, two buckets, and a certified recipient base — with **no automated deployment pipeline available in the target environment**. This document records the discipline that made a manual migration safe.

## Operating model

- **Two-project model:** UAT first, then production. UAT permanently retains paused schedulers after verification; it exists to prove the runbooks, not to run.
- **Hard boundary:** repository tooling and cloud consoles never operate each other. Repo checks are static; Cloud Shell never clones the repo. Operators upload individual files from one reviewed commit through the console, verified by SHA-256 comparison.
- **Everything deploys paused and send-disabled.** Services are configured, tested, and verified while their Scheduler jobs are paused and `ALLOW_SEND` is false.

## Runbook sequence

| # | Runbook | Verifies |
|---|---|---|
| 1 | Project, IAM, buckets, upload | Folder structure matches spec; file hashes match the reviewed commit |
| 2 | BigQuery | Dataset + three tables created; one-shot seed guarded by a non-empty `ASSERT`; catalog seeded via idempotent MERGE |
| 3 | Secrets + preference API | Secret creation; `/ready` endpoint; a real GET-confirm → POST-mutate → BigQuery-write → cleanup cycle |
| 4 | Newsletter services | All topic services deployed paused with env contracts applied |
| 5 | Report services | Weekly + monthly deployed paused; production-scale send-disabled dry run |
| 6 | Scheduler | All jobs created **paused** with exact cadences |
| 7 | Verification | Row counts, catalog integrity, per-service direct tests |
| 8 | Activation | Single-operator test lane first; old sandbox jobs paused and visually verified; then and only then, resume all production jobs |

## Principles that earned their place

- **Single-operator test lane.** The production recipient seed includes exactly one active tester with one test row per product (nine rows). Full-audience rows exist but are seeded inactive — activation is a deliberate `UPDATE`, never a side effect of deployment.
- **Reconcile before you seed.** The live sandbox recipient table was reconciled row-by-row into a certified production seed immediately before execution; the seed documents every correction applied against the raw export.
- **No rollback theater.** With paused schedulers and send-disabled services, the safe rollback is "don't activate." The playbook deliberately removed automated rollback, backup ceremony, and state-restoration steps that added surface area without adding safety.
- **History is preserved, not rewritten.** Sent-article history files are copied per an exact source→target map so the new environment doesn't re-send old articles on day one.
