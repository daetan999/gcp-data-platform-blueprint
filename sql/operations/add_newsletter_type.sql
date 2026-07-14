-- =============================================================================
-- Register a new newsletter topic — the ONLY step needed besides uploading
-- the topic script. Guarded, idempotent, reusable.
-- =============================================================================

DECLARE new_type STRING DEFAULT 'example_topic';
DECLARE new_script STRING DEFAULT 'example_topic/newsletter.py';

-- Naming guard: topic ids are lowercase/numbers/underscores by contract.
ASSERT REGEXP_CONTAINS(new_type, r'^[a-z0-9_]+$')
  AS 'newsletter_type must be lowercase letters, numbers, underscores';

MERGE `<PROJECT_ID>.email_config.newsletter_type_catalog` t
USING (SELECT new_type AS newsletter_type) s
ON t.newsletter_type = s.newsletter_type
WHEN MATCHED THEN
  UPDATE SET is_active = TRUE, script_name = new_script
WHEN NOT MATCHED THEN
  INSERT (newsletter_type, is_active, supports_unsubscribe, script_name)
  VALUES (new_type, TRUE, TRUE, new_script);
