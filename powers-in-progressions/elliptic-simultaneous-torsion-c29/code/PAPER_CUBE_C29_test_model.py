import hashlib
import json
from pathlib import Path
import unittest

import PAPER_CUBE_C29_model as model


class C29ModelTests(unittest.TestCase):
    def test_freeze_manifest_hash(self):
        root = Path(__file__).resolve().parent
        manifest = json.loads((root / "PAPER_CUBE_C29_FREEZE.json").read_text())
        source = (root / manifest["source_file"]).read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest().upper(),
                         manifest["source_sha256"])
        self.assertEqual(manifest["status"], "EXACT_POLYNOMIAL_CERTIFICATE")

    def test_original_rs_rk_freeze(self):
        out = model.check_original_rs_rk_freeze()
        self.assertEqual(out["status"], "EXACT_POLYNOMIAL_CERTIFICATE")
        self.assertEqual(len(out["exceptional_fibres"]), 4)
        root = Path(__file__).resolve().parent
        manifest = json.loads((root / "PAPER_CUBE_C29_FREEZE.json").read_text())
        self.assertEqual(manifest["live_certificate"], out)

    def test_kubert_full_change(self):
        self.assertEqual(model.check_kubert_coordinates()["A1"], "-r**3 + 3*r**2 - 1")

    def test_hyperelliptic_descent(self):
        out = model.check_normalization_and_descent()
        self.assertEqual(out["discriminant_factorization"], "-2^45*3^4")
        self.assertIn("modulo 5", out["rational_2_torsion"])

    def test_fail_closed(self):
        self.assertEqual(model.build_certificate()["rank_status"], "UNKNOWN_FAIL_CLOSED")

    def test_six_cusp_branches(self):
        rows = model.check_cusp_branches()
        self.assertEqual(len(rows), 6)
        self.assertEqual(len(set(rows)), 6)

    def test_absolute_invariants(self):
        inv = model.check_absolute_invariants()
        self.assertEqual(inv["absolute_tuple"][:2], ["24", "24"])

    def test_main_open_denominators(self):
        den = model.main_open_denominators()
        self.assertEqual(len(den["source_C29_to_rk_to_H29"]), 4)
        self.assertEqual(len(den["target_H29_to_rk_to_C29"]), 3)
        self.assertEqual(
            model.sp.factor(model.sp.prod(den["source_C29_to_rk_to_H29"])),
            model.k*(model.s+2)*(model.r+2*model.k)*model.D(model.r),
        )


if __name__ == "__main__":
    unittest.main()
