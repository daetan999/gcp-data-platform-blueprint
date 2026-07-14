-- =============================================================================
-- newsletter_type_catalog — valid topics as data (no code edits for new topics)
-- =============================================================================

CREATE TABLE IF NOT EXISTS `<PROJECT_ID>.email_config.newsletter_type_catalog` (
  newsletter_type      STRING NOT NULL,      -- lowercase / numbers / underscores
  is_active            BOOL   NOT NULL DEFAULT TRUE,
  supports_unsubscribe BOOL   NOT NULL DEFAULT TRUE,
  script_name          STRING                -- runtime script for this topic
);

-- Four columns on purpose: an earlier 11-column version (display names,
-- categories, service/job references, audit timestamps) was cut — every
-- extra column was a second place for the same fact to go stale.
