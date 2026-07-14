"""Cadence KPI engine — illustrative blueprint skeleton.

Deterministic SQL computes every number; the model only narrates them.
"""
from __future__ import annotations

import os

BQ_PROJECT = os.getenv("BQ_PROJECT", "<DATA_PLATFORM_PROJECT_ID>")

RESERVATIONS_VIEW = f"{BQ_PROJECT}.operations_gold.vw_reservations"
INVENTORY_TABLES = (
    f"{BQ_PROJECT}.operations_silver.fact_pms_a_room_inventory",
    f"{BQ_PROJECT}.operations_silver.fact_pms_b_room_inventory",
    f"{BQ_PROJECT}.operations_silver.fact_pms_c_room_inventory",
)

AAN_CARRY_FORWARD_DAYS = 30

# The reservations base pattern that survived production:
#
#   WITH exploded AS (
#     SELECT night, roomrevenue / NULLIF(oan, 0) AS revenue_per_night
#     FROM (
#       SELECT DISTINCT *              -- duplicate reservation rows exist;
#       FROM `<reservations view>`     -- without DISTINCT they inflate OAN
#       WHERE propertycode = @property
#     ),
#     UNNEST(GENERATE_DATE_ARRAY(arrivaldate,
#            DATE_SUB(departuredate, INTERVAL 1 DAY))) AS night
#     WHERE arrivaldate <= @end AND departuredate > @start   -- pushdown BEFORE
#   )                                                        -- unnesting: prune
#   ...                                                      -- rows, not TB
#
# Two hard-won rules encoded above:
#   1. DISTINCT before UNNEST — exact-duplicate reservation rows otherwise
#      count twice and produce impossible occupancy.
#   2. Date-filter pushdown — filtering after UNNEST scans the property's
#      entire history and blows the byte-billing cap.


def compute_property_kpis(property_code: str, start: str, end: str) -> dict:
    """Occupancy, ADR, RevPAR, pickup, budget variance — dual currency.

    Invariants enforced here, not in prompts:
    - rates use SAFE_DIVIDE on raw components (revenue / occupied nights);
    - rate measures are never summed across properties or periods;
    - raw components (revenue, OAN, AAN) are always returned alongside
      ratios so an impossible result is diagnosable;
    - occupancy > 100% or negative ⇒ the result is returned as a flagged
      data-quality finding, never presented as a confirmed KPI."""
    raise NotImplementedError("Blueprint stub — full query set omitted")


def build_availability_cte() -> str:
    """Union the per-PMS inventory tables onto (night, property, aan), then
    carry the last known AAN forward up to AAN_CARRY_FORWARD_DAYS for nights
    with no inventory row. Missing-after-window nights drop out of the
    denominator AND flag the result."""
    raise NotImplementedError("Blueprint stub — per-source column maps omitted")
