-- =============================================================================
-- ILLUSTRATIVE seed — fictional example rows only.
-- The production pattern: a one-time certified seed guarded by an ASSERT so
-- reruns abort instead of double-inserting.
-- =============================================================================

ASSERT (SELECT COUNT(*) FROM `<PROJECT_ID>.email_config.email_recipient_mapping`) = 0
  AS 'email_recipient_mapping is not empty — the seed already ran.';

INSERT INTO `<PROJECT_ID>.email_config.email_recipient_mapping`
  (email, display_name, email_type, send_mode, property_code, is_active)
VALUES
  -- Single-operator production test lane: one active tester, one row per product.
  ('ops.tester@example.com',   'Ops Tester',    'example_topic',       'test',       NULL,      TRUE),
  ('ops.tester@example.com',   'Ops Tester',    'weekly_performance',  'test',       'PROP-A01', TRUE),
  -- Full-audience rows seeded INACTIVE — activation is a deliberate UPDATE.
  ('gm.alpha@example.com',     'GM · Property Alpha', 'weekly_performance', 'production', 'PROP-A01', FALSE),
  ('exec.reader@example.com',  'Executive Reader',    'example_topic',      'production', NULL,      FALSE);
