import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST as manifest


class SupplementManifestTests(unittest.TestCase):
    def test_disk_and_hashes(self):
        disk = json.loads(manifest.OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(disk, manifest.build_manifest())
        for row in disk["files"]:
            path = manifest.ROOT / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])
            self.assertEqual(path.stat().st_size, row["bytes"])
        paths = {row["path"] for row in disk["files"]}
        self.assertIn("PAPER_ELLIPTIC_NEXT_test.py", paths)
        self.assertIn("PAPER_ELLIPTIC_MOODY_JUYAL.py", paths)
        self.assertIn("PAPER_ELLIPTIC_ROUND_05_test.py", paths)
        self.assertEqual(disk["test_accounting"]["full_release_total"], 45)
        command = disk["reproduction_commands"][-1]
        self.assertIn("PAPER_ELLIPTIC_NEXT_test.py", command)
        self.assertIn("PAPER_ELLIPTIC_ROUND_05_test.py", command)

    def test_unexecuted_magma_is_fail_closed(self):
        disk = manifest.build_manifest()
        row = next(x for x in disk["files"] if x["path"].endswith("full_two_selmer.m"))
        self.assertFalse(row["mathematical_evidence_eligible"])
        self.assertIn("No transcript", disk["ineligible_input_policy"][row["path"]])
        self.assertIn("Cassels-Tate", disk["claim_boundary"]["not_proved"])
        clean = json.loads(
            (manifest.ROOT / disk["supersession_policy"]["clean_certificate"])
            .read_text(encoding="utf-8")
        )
        serialized = json.dumps(
            {key: value for key, value in clean.items() if key != "supersession"}
        )
        for forbidden in disk["supersession_policy"]["forbidden_clean_certificate_fields"]:
            self.assertNotIn(forbidden, serialized)
        negative = json.loads(
            (manifest.ROOT / disk["supersession_policy"]["negative_audit"])
            .read_text(encoding="utf-8")
        )
        self.assertIn("withdrawn", negative["claim_boundary"])
        self.assertIn("FAIL_BRANCH_INDEPENDENCE", json.dumps(negative))

    def test_isolated_python_rebuild(self):
        original = manifest.build_manifest()
        names = [row["path"] for row in original["files"]]
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td)
            for name in names:
                shutil.copy2(manifest.ROOT / name, dst / name)
            commands = [
                [sys.executable, "PAPER_ELLIPTIC_CAMPBELL_analysis.py"],
                [sys.executable, "PAPER_ELLIPTIC_ROUND_04_analysis.py"],
                [sys.executable, "PAPER_ELLIPTIC_ROUND_05_analysis.py"],
                [sys.executable, "PAPER_ELLIPTIC_ROUND_06_analysis.py"],
                [sys.executable, "PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.py"],
            ]
            for command in commands:
                subprocess.run(command, cwd=dst, check=True, capture_output=True, text=True)
            rebuilt = json.loads((dst / manifest.OUTPUT.name).read_text(encoding="utf-8"))
            self.assertEqual(rebuilt, original)
            if os.environ.get("PAPER_ELLIPTIC_ISOLATED_CHILD") == "1":
                return
            suite = [
                sys.executable,
                "-m",
                "unittest",
                "-v",
                "PAPER_ELLIPTIC_NEXT_test.py",
                "PAPER_ELLIPTIC_CAMPBELL_test.py",
                "PAPER_ELLIPTIC_ROUND_04_test.py",
                "PAPER_ELLIPTIC_ROUND_05_test.py",
                "PAPER_ELLIPTIC_ROUND_06_test.py",
            ]
            completed = subprocess.run(
                suite, cwd=dst, check=True, capture_output=True, text=True
            )
            transcript = completed.stdout + completed.stderr
            self.assertIn("Ran 39 tests", transcript)
            self.assertIn("OK", transcript)


if __name__ == "__main__":
    unittest.main()
