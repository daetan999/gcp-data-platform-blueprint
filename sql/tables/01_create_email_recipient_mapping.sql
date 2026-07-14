-- =============================================================================
-- email_recipient_mapping — who receives what, in which lane
-- Replace <PROJECT_ID> with the target environment project.
-- =============================================================================

CREATE TABLE IF NOT EXISTS `<PROJECT_ID>.email_config.email_recipient_mapping` (
  email          STRING NOT NULL,            -- recipient address
  display_name   STRING,                     -- for personalized salutations
  email_type     STRING NOT NULL,            -- newsletter topic or report cadence
  send_mode      STRING NOT NULL,            -- 'test' | 'production' lanes
  property_code  STRING,                     -- report scope; NULL = all properties
  is_active      BOOL   NOT NULL DEFAULT TRUE,
  added_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

-- Lanes are data: activating a stakeholder, or moving between test and
-- production audiences, is an UPDATE — never a deploy.
