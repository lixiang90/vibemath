import hashlib
import json
import unittest

import PAPER_SQUARE_SUPPLEMENT_MANIFEST as manifest


class SupplementManifestTests(unittest.TestCase):
    def test_disk_manifest_matches(self):
        with manifest.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), manifest.build_manifest())

    def test_every_hash_matches_disk(self):
        data = manifest.build_manifest()
        self.assertEqual(len(data["files"]), len(manifest.ARTIFACTS))
        self.assertEqual(len({row["path"] for row in data["files"]}), len(data["files"]))
        for row in data["files"]:
            path = manifest.ROOT / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])
            self.assertEqual(path.stat().st_size, row["bytes"])

    def test_release_is_fail_closed_about_archiving(self):
        data = manifest.build_manifest()
        self.assertEqual(data["semantic_version"], "0.5.0")
        self.assertIn("NOT_PUBLICLY_ARCHIVED", data["release_status"])
        self.assertIsNone(data["archival_url"])
        self.assertIn("not decided", data["claim_boundary"]["not_proved"])

    def test_commands_cover_all_paper_generators_and_tests(self):
        commands = "\n".join(manifest.build_manifest()["reproduction_commands"])
        for needle in ("SAFE_inventory.py", "MASK77_analysis.py", "NEXT_GATE.py", "MASK108.py", "unittest"):
            self.assertIn(needle, commands)


if __name__ == "__main__":
    unittest.main()

