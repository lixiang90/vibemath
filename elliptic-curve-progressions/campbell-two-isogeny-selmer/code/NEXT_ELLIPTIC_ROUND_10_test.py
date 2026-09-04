import json
from pathlib import Path
import unittest

import NEXT_ELLIPTIC_ROUND_10 as r10


class Round10EPrimeLocalGateTests(unittest.TestCase):
    def test_normalized_constants(self):
        self.assertEqual(r10.A, 2 * r10.C)
        self.assertEqual(r10.B, 3**4 * 59 * 71_699 * 339_106_321)
        self.assertEqual(r10.DELTA, 2**22 * r10.K2)
        self.assertEqual(r10.K2 % 2, 1)
        self.assertEqual((r10.C % 8, r10.B % 8), (7, 1))
        self.assertEqual(r10.valuation(r10.A, 3), 2)
        self.assertEqual(((r10.A // 9) % 3, r10.D % 3), (1, 1))

    def test_double_root_identity_by_coefficients(self):
        # 4*d*F_d and (2*d*U^2+A*V^2)^2-DELTA*V^4.
        for d in r10.signed_squarefree_candidates():
            self.assertEqual(
                (4 * d * d, 4 * d * r10.A, 4 * r10.B),
                (4 * d * d, 4 * d * r10.A, r10.A * r10.A - r10.DELTA),
            )

    def test_exact_two_adic_classification(self):
        candidates = r10.signed_squarefree_candidates()
        survivors = tuple(d for d in candidates if r10.q2_soluble(d))
        self.assertEqual(survivors, r10.EXPECTED_Q2)
        self.assertTrue(all(d % 8 == 1 for d in survivors))
        self.assertTrue(all(d % 8 != 1 for d in set(candidates) - set(survivors)))

    def test_two_adic_both_odd_valuation_cases(self):
        # For odd U,V, squares are 1 mod 8 and C=7 mod 8.
        # Hence T=d*U^2+C*V^2 has the following forced valuations.
        for residue, expected_valuation in ((3, 1), (5, 2), (7, 1)):
            t_mod_8 = (residue + r10.C) % 8
            self.assertEqual(r10.valuation(t_mod_8, 2), expected_valuation)
            self.assertGreaterEqual(20 - 2 * expected_valuation, 16)

    def test_exact_three_adic_classification(self):
        candidates = r10.signed_squarefree_candidates()
        survivors = tuple(d for d in candidates if r10.q3_soluble(d))
        self.assertEqual(survivors, r10.EXPECTED_Q3)
        self.assertTrue(all(r10.valuation(d, 3) == 0 and d % 3 == 1 for d in survivors))

    def test_exact_two_three_intersection(self):
        candidates = r10.signed_squarefree_candidates()
        intersection = tuple(d for d in candidates if r10.q2_soluble(d) and r10.q3_soluble(d))
        self.assertEqual(intersection, r10.EXPECTED_INTERSECTION)
        self.assertEqual(
            intersection,
            (1, 59 * 71_699, 339_106_321, 59 * 71_699 * 339_106_321),
        )

    def test_compatibility_and_minimality_audit(self):
        audit = r10.local_matrix_audit()
        self.assertEqual(audit["disagreements"], [])
        self.assertEqual(audit["checked_cells"], 64)
        self.assertEqual(audit["minimum_number_of_finite_places_for_four_stored_survivors"], 2)
        self.assertEqual(
            audit["all_minimal_pairs_with_the_same_four_stored_survivors"],
            [[2, 3], [2, 5]],
        )
        self.assertEqual(audit["chosen_uniform_pair"], [2, 3])

    def test_disk_certificate(self):
        disk = json.loads(r10.OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(disk, r10.build_certificate())
        self.assertEqual(disk["matrix_compatibility_audit"]["source_sha256"],
                         "fff2f35f398c2d14227d9b032d205e24d5332a39346487c76180cdf805ba32c9")

    def test_manuscript_contains_uniform_theorem_and_boundaries(self):
        tex = (Path(__file__).resolve().parent.parent / "paper" / "main.tex").read_text(
            encoding="utf-8"
        )
        for token in (
            "two-place $E'$-side gate",
            r"C'_d(\mathbf Q_2)\ne\varnothing",
            r"C'_d(\mathbf Q_3)\ne\varnothing",
            r"dN^2=T^2-2^{20}kV^4",
            r"\{1,4230241,339106321,D\}",
            "ninth-point problem.",
            "elliptic-curve CAS was available",
        ):
            self.assertIn(token, tex)


if __name__ == "__main__":
    unittest.main()
