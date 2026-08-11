#!/usr/bin/env python3
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import openai_client as oc


class OpenAIClientTest(unittest.TestCase):
    def setUp(self):
        self._saved = os.environ.pop("OPENAI_API_KEY", None)

    def tearDown(self):
        if self._saved is not None:
            os.environ["OPENAI_API_KEY"] = self._saved
        else:
            os.environ.pop("OPENAI_API_KEY", None)

    def test_missing_key_raises_clear_error(self):
        with self.assertRaises(oc.MissingAPIKeyError) as ctx:
            oc.get_api_key()
        message = str(ctx.exception)
        self.assertIn("OPENAI_API_KEY", message)
        self.assertNotIn("sk-", message)  # never echoes a key-shaped value

    def test_blank_key_treated_as_missing(self):
        os.environ["OPENAI_API_KEY"] = "   "
        with self.assertRaises(oc.MissingAPIKeyError):
            oc.get_api_key()

    def test_present_key_is_returned_verbatim(self):
        os.environ["OPENAI_API_KEY"] = "sk-test-dummy-not-a-real-key"
        self.assertEqual(oc.get_api_key(), "sk-test-dummy-not-a-real-key")

    def test_build_client_succeeds_with_key_present(self):
        os.environ["OPENAI_API_KEY"] = "sk-test-dummy-not-a-real-key"
        client = oc.build_client()
        self.assertEqual(client.api_key, "sk-test-dummy-not-a-real-key")

    def test_build_client_raises_without_key(self):
        with self.assertRaises(oc.MissingAPIKeyError):
            oc.build_client()


if __name__ == "__main__":
    unittest.main()
