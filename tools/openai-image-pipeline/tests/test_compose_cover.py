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


class ComposeCoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

        self.cover_path = self.tmp / "assets" / "test-cover.png"
        self.cover_path.parent.mkdir(parents=True)
        Image.new("RGB", (100, 150), (255, 0, 0)).save(self.cover_path)  # solid red cover

        self.registry_path = self.tmp / "covers_registry.json"
        self.registry_path.write_text(json.dumps({
            "covers": [{
                "id": "T1", "title": "Test Cover", "canva_asset_id": "MATEST0001",
                "local_path": "assets/test-cover.png", "sha256": None, "pinned_at": None,
            }]
        }))
        cr.pin_cover("Test Cover", self.registry_path)

        self.scene_path = self.tmp / "scene.png"
        Image.new("RGB", (800, 1000), (0, 255, 0)).save(self.scene_path)  # solid green scene

        # axis-aligned quad well inside the scene -- easy to reason about
        self.corners = [(100, 100), (500, 100), (500, 700), (100, 700)]
        self.output = self.tmp / "out.png"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run_compose(self, occlusion_mask_path=None, output=None):
        output = output or self.output
        cc.compose(
            scene_path=self.scene_path,
            title="Test Cover",
            corners=self.corners,
            output_path=output,
            occlusion_mask_path=occlusion_mask_path,
            registry_path=self.registry_path,
        )
        return output

    def test_composite_places_cover_inside_quad_only(self):
        output = self._run_compose()
        img = Image.open(output).convert("RGB")
        self.assertEqual(img.getpixel((300, 400)), (255, 0, 0))  # inside quad -> cover
        self.assertEqual(img.getpixel((700, 900)), (0, 255, 0))  # outside quad -> untouched scene

    def test_manifest_written_and_correct(self):
        output = self._run_compose()
        manifest = json.loads((output.with_suffix(output.suffix + ".manifest.json")).read_text())
        self.assertEqual(manifest["title"], "Test Cover")
        self.assertEqual(manifest["canva_asset_id"], "MATEST0001")
        self.assertFalse(manifest["generative_model_touched_cover_pixels"])
        self.assertEqual(manifest["compositing_method"], "deterministic_perspective_transform")
        self.assertFalse(manifest["occlusion_mask_used"])
        self.assertIsNotNone(manifest["cover_sha256"])

    def test_refuses_unpinned_cover(self):
        registry2 = self.tmp / "registry2.json"
        registry2.write_text(json.dumps({
            "covers": [{
                "id": "T2", "title": "Unpinned Cover", "canva_asset_id": "MAUNPINNED",
                "local_path": "assets/test-cover.png", "sha256": None, "pinned_at": None,
            }]
        }))
        output = self.tmp / "should_not_exist_1.png"
        with self.assertRaises(cc.CompositingError):
            cc.compose(
                scene_path=self.scene_path, title="Unpinned Cover", corners=self.corners,
                output_path=output, registry_path=registry2,
            )
        self.assertFalse(output.exists())

    def test_refuses_tampered_cover(self):
        Image.new("RGB", (100, 150), (0, 0, 0)).save(self.cover_path)  # tamper after pin
        output = self.tmp / "should_not_exist_2.png"
        with self.assertRaises(cc.CompositingError):
            self._run_compose(output=output)
        self.assertFalse(output.exists())

    def test_degenerate_quad_rejected(self):
        output = self.tmp / "should_not_exist_3.png"
        with self.assertRaises(cc.CompositingError):
            cc.compose(
                scene_path=self.scene_path, title="Test Cover",
                corners=[(10, 10), (11, 10), (11, 11), (10, 11)],  # tiny quad
                output_path=output, registry_path=self.registry_path,
            )
        self.assertFalse(output.exists())

    def test_missing_scene_rejected(self):
        output = self.tmp / "should_not_exist_4.png"
        with self.assertRaises(cc.CompositingError):
            cc.compose(
                scene_path=self.tmp / "does_not_exist.png", title="Test Cover",
                corners=self.corners, output_path=output, registry_path=self.registry_path,
            )
        self.assertFalse(output.exists())

    def test_occlusion_mask_preserves_foreground(self):
        mask_path = self.tmp / "mask.png"
        mask = Image.new("L", (800, 1000), 0)
        for x in range(250, 350):
            for y in range(350, 450):
                mask.putpixel((x, y), 255)
        mask.save(mask_path)

        output = self._run_compose(occlusion_mask_path=mask_path)
        img = Image.open(output).convert("RGB")
        self.assertEqual(img.getpixel((300, 400)), (0, 255, 0))  # occluded -> original scene
        self.assertEqual(img.getpixel((150, 150)), (255, 0, 0))  # inside quad, not occluded -> cover

        manifest = json.loads((output.with_suffix(output.suffix + ".manifest.json")).read_text())
        self.assertTrue(manifest["occlusion_mask_used"])


if __name__ == "__main__":
    unittest.main()
