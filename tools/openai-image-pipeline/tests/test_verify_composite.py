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
import compose_cover as cc
import verify_composite as vc


class VerifyCompositeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

        self.cover_path = self.tmp / "assets" / "test-cover.png"
        self.cover_path.parent.mkdir(parents=True)
        Image.new("RGB", (100, 150), (255, 0, 0)).save(self.cover_path)

        self.registry_path = self.tmp / "covers_registry.json"
        self.registry_path.write_text(json.dumps({
            "covers": [{
                "id": "T1", "title": "Test Cover", "canva_asset_id": "MATEST0001",
                "local_path": "assets/test-cover.png", "sha256": None, "pinned_at": None,
            }]
        }))
        cr.pin_cover("Test Cover", self.registry_path)

        self.scene_path = self.tmp / "scene.png"
        Image.new("RGB", (800, 1000), (0, 255, 0)).save(self.scene_path)

        self.corners = [(100, 100), (500, 100), (500, 700), (100, 700)]
        self.output = self.tmp / "out.png"
        cc.compose(
            scene_path=self.scene_path, title="Test Cover", corners=self.corners,
            output_path=self.output, registry_path=self.registry_path,
        )
        self.manifest_path = self.output.with_suffix(self.output.suffix + ".manifest.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_untouched_composite_passes(self):
        ok, message = vc.verify(self.output, self.manifest_path, self.registry_path)
        self.assertTrue(ok, message)
        self.assertTrue(message.startswith("PASS"))

    def test_repainted_cover_region_fails(self):
        img = Image.open(self.output).convert("RGB")
        img.paste((0, 0, 255), (100, 100, 500, 700))  # overwrite the whole cover region blue
        img.save(self.output)

        ok, message = vc.verify(self.output, self.manifest_path, self.registry_path)
        self.assertFalse(ok)
        self.assertIn("PRODUCT_FIDELITY_FAIL", message)

    def test_hash_drift_detected(self):
        Image.new("RGB", (100, 150), (0, 0, 0)).save(self.cover_path)
        cr.pin_cover("Test Cover", self.registry_path)  # re-pin to the new (different) file

        ok, message = vc.verify(self.output, self.manifest_path, self.registry_path)
        self.assertFalse(ok)
        self.assertIn("HASH_DRIFT", message)

    def test_tampered_registry_file_fails_registry_check(self):
        Image.new("RGB", (100, 150), (0, 0, 0)).save(self.cover_path)  # change without re-pinning

        ok, message = vc.verify(self.output, self.manifest_path, self.registry_path)
        self.assertFalse(ok)
        self.assertIn("REGISTRY_CHECK_FAILED", message)


if __name__ == "__main__":
    unittest.main()
