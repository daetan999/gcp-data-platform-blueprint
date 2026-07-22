"""Behavioral tests for recipient preference enforcement."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from services.shared import recipients


class FilterUnsubscribedTests(unittest.TestCase):
    def test_removes_topic_and_global_opt_outs_and_deduplicates(self) -> None:
        with patch.object(
            recipients,
            "_lookup_unsubscribed_emails",
            return_value={"blocked@example.com", "global@example.com"},
        ):
            result = recipients.filter_unsubscribed(
                [
                    "Allowed@Example.com",
                    "blocked@example.com",
                    "allowed@example.com",
                    "global@example.com",
                ],
                "weekly-performance",
            )

        self.assertEqual(result, ["allowed@example.com"])

    def test_lookup_failure_raises_instead_of_returning_unfiltered_list(self) -> None:
        with patch.object(
            recipients,
            "_lookup_unsubscribed_emails",
            side_effect=ConnectionError("BigQuery unavailable"),
        ):
            with self.assertRaises(recipients.UnsubscribeLookupError) as raised:
                recipients.filter_unsubscribed(
                    ["person@example.com"],
                    "weekly-performance",
                )

        self.assertIn("weekly-performance", str(raised.exception))

    def test_rejects_blank_newsletter_type_before_lookup(self) -> None:
        with self.assertRaises(ValueError):
            recipients.filter_unsubscribed(["person@example.com"], "  ")


if __name__ == "__main__":
    unittest.main()
