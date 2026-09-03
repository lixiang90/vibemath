import json
import math
from pathlib import Path
import unittest

import NEXT_ELLIPTIC_ROUND_09 as r9


class Round09TwoPlaceGateTests(unittest.TestCase):
    def test_environment_audit_is_fail_closed(self):
        audit = r9.environment_audit()
        self.assertFalse(audit["independent_elliptic_cas_available"])
        self.assertTrue(all(value is None for value in audit["applications"].values()))
        self.assertTrue(all(not value for value in audit["python_modules"].values()))
        self.assertIn("not counted as an independent reproduction", audit["claim_boundary"])

    def test_discriminant_and_double_root_identity(self):
        self.assertEqual(r9.DELTA, 3**4 * 59 * 71699 * 339106321)
        for p in r9.MULTIPLICATIVE_PRIMES:
            self.assertTrue(r9.is_prime_trial(p))
            self.assertEqual(r9.valuation(r9.DELTA, p), 1)
        # Compare coefficients of U^4, U^2*V^2 and V^4.
        for d in r9.signed_candidates():
            self.assertEqual(
                (4*d*d, 4*d*r9.A, 4*r9.B),
                (4*d*d, 4*d*r9.A, r9.A*r9.A-r9.DELTA),
            )

    def test_exact_local_classification_at_both_primes(self):
        expected_yes = [
            -210, -70, -42, -30, -14, -10, -6, -2,
            1, 3, 5, 7, 15, 21, 35, 105,
        ]
        cert = r9.local_gate_certificate()
        for p in ("59", "71699"):
            row = cert["local_classification"][p]
            self.assertEqual(row["soluble_classes"], expected_yes)
            self.assertEqual(len(row["obstructed_classes"]), 16)
            self.assertEqual(
                row["legendre_generators"],
                {"-1": -1, "2": -1, "3": 1, "5": 1, "7": 1},
            )

    def test_real_gate_and_eight_combined_survivors(self):
        cert = r9.local_gate_certificate()
        self.assertEqual(cert["real_soluble_classes"], [
            1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 30, 35, 42, 70, 105, 210,
        ])
        self.assertEqual(cert["real_and_Q59_survivors"], list(r9.EXPECTED_COMBINED))
        self.assertEqual(cert["real_and_Q71699_survivors"], list(r9.EXPECTED_COMBINED))

    def test_disk_certificate(self):
        self.assertEqual(
            json.loads(r9.OUTPUT.read_text(encoding="utf-8")),
            r9.build_certificate(),
        )

    def test_manuscript_contains_closed_two_place_gate(self):
        tex = (Path(__file__).resolve().parent.parent / "paper" / "main.tex").read_text(encoding="utf-8")
        for token in (
            "two-place $E$-side gate",
            r"C_d(\mathbf Q_{59})",
            r"C_d(\mathbf Q_{71699})",
            "y(y+x)",
            r"\{1,3,5,7,15,21,35,105\}",
            r"4dF_d=(2dU^2+aV^2)^2-\delta V^4",
            r"\left(\frac{2}{p}\right)=-1,\qquad",
        ):
            self.assertIn(token, tex)
        self.assertNotIn(r"\left(\frac{2}{p}\right)=-1,qquad", tex)


if __name__ == "__main__":
    unittest.main()
