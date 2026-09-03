import json
import unittest

import sympy as sp

import PAPER_ELLIPTIC_ROUND_06_analysis as a
import PAPER_ELLIPTIC_ROUND_05_analysis as correction


class Round06Tests(unittest.TestCase):
    def test_campbell_nine_indices(self):
        data = a.campbell_source_certificate()
        self.assertEqual(data["square_identity_residuals"], ["0"] * 7)
        self.assertEqual(data["g_at_7_minus_D"], "0")
        self.assertEqual(data["g_at_8_minus_H"], "0")
        self.assertEqual(data["indices"]["eighth_index"], 7)
        self.assertEqual(data["indices"]["ninth_candidate_index"], 8)

    def test_all_rational_degeneracy_boundaries(self):
        d = a.campbell_source_certificate()["degeneracy_boundaries"]
        self.assertTrue(d["leading_coefficient_has_no_rational_zero"])
        self.assertTrue(d["primitive_irreducible_mod_53"])
        self.assertTrue(d["hence_no_rational_singular_specialization"])
        self.assertEqual(d["primitive_factor_degrees_over_Q"], [[16, 1]])
        self.assertTrue(d["nine_x_coordinates_are_distinct"])

    def test_same_m_summary_is_exact_copy(self):
        d = a.same_m_certificate_summary()
        self.assertEqual(d["odd_witness_count"], 30)
        self.assertIn(59, d["odd_primes"])
        self.assertIn(339106321, d["odd_primes"])
        self.assertEqual(d["two_adic_witness"]["D_mod_8"], 1)
        self.assertEqual(d["two_adic_witness"]["H_mod_8"], 1)

    def test_magma_is_fail_closed(self):
        d = a.provenance()["magma_full_descent"]
        self.assertFalse(d["mathematical_evidence_eligible"])
        self.assertEqual(d["status"], "BUNDLED_UNEXECUTED_NOT_EVIDENCE")
        self.assertEqual(len(d["candidate_inputs"]), 3)
        for item in d["candidate_inputs"]:
            path = a.ROOT.parent / item["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(a.sha256(path), item["sha256"])
        self.assertIsNone(d["transcript"])
        self.assertIsNone(d["magma_binary_sha256"])
        self.assertIn("C_H(Q) empty or nonempty", d["forbidden_promotions"])

    def test_rejected_pairing_formula_remains_only_negative_evidence(self):
        d = correction.certificate_payload()
        audit = d["rejected_opposite_side_formula_audit"]
        self.assertEqual(audit["well_definedness_test"], "FAIL_BRANCH_INDEPENDENCE")
        self.assertEqual(audit["possible_products_from_independent_local_branches"], [-1, 1])
        self.assertIn("not promoted", audit["warning"])

    def test_disk_certificate(self):
        with a.OUTPUT.open(encoding="utf-8") as f:
            self.assertEqual(json.load(f), a.build_certificate())


if __name__ == "__main__":
    unittest.main()
