-- =============================================================================
-- newsletter_unsubscribe — topic-level or 'all' opt-outs
-- Written ONLY by the preference API's MERGE upserts.
-- =============================================================================

CREATE TABLE IF NOT EXISTS `<PROJECT_ID>.email_config.newsletter_unsubscribe` (
  email            STRING NOT NULL,
  newsletter_type  STRING NOT NULL,          -- specific topic, or 'all'
  is_unsubscribed  BOOL   NOT NULL DEFAULT TRUE,
  unsubscribed_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

-- The send path matches (newsletter_type = @type OR newsletter_type = 'all')
-- directly against this table — the authoritative filter is deliberately
-- simple and independent of the fail-open catalog check.
