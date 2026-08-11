#!/usr/bin/env python3
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

import covers_registry as cr


class CoversRegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cover_path = self.tmp / "assets" / "test-cover.png"
        self.cover_path.parent.mkdir(parents=True)
        Image.new("RGB", (40, 60), (200, 30, 90)).save(self.cover_path)

        self.registry_path = self.tmp / "covers_registry.json"
        self.registry_path.write_text(json.dumps({
            "covers": [{
                "id": "T1",
                "title": "Test Cover",
                "canva_asset_id": "MATEST0001",
                "local_path": "assets/test-cover.png",
                "sha256": None,
                "pinned_at": None,
            }]
        }))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_unpinned_cover_fails_verification(self):
        entry = cr.get_cover("Test Cover", self.registry_path)
        ok, reason = cr.verify_cover_file(entry)
        self.assertFalse(ok)
        self.assertIn("NOT_PINNED", reason)

    def test_pin_then_verify_passes(self):
        cr.pin_cover("Test Cover", self.registry_path)
        entry = cr.get_cover("Test Cover", self.registry_path)
        ok, reason = cr.verify_cover_file(entry)
        self.assertTrue(ok, reason)

    def test_tampered_file_fails_after_pin(self):
        cr.pin_cover("Test Cover", self.registry_path)
        Image.new("RGB", (40, 60), (0, 0, 0)).save(self.cover_path)  # overwrite -- simulate tamper
        entry = cr.get_cover("Test Cover", self.registry_path)
        ok, reason = cr.verify_cover_file(entry)
        self.assertFalse(ok)
        self.assertIn("PRODUCT_FIDELITY_FAIL", reason)

    def test_missing_file_reports_asset_missing(self):
        entry = cr.get_cover("Test Cover", self.registry_path)
        entry.local_path.unlink()
        ok, reason = cr.verify_cover_file(entry)
        self.assertFalse(ok)
        self.assertIn("PRODUCT_ASSET_MISSING", reason)

    def test_unknown_title_raises(self):
        with self.assertRaises(cr.CoverNotFoundError):
            cr.get_cover("Nonexistent Title", self.registry_path)

    def test_lookup_by_id_works(self):
        entry = cr.get_cover("T1", self.registry_path)
        self.assertEqual(entry.title, "Test Cover")


if __name__ == "__main__":
    unittest.main()
