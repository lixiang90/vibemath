import unittest

import PAPER_CUBE_P6_maps as maps


class P6MapsTests(unittest.TestCase):
    def test_all_six_explicit_maps(self):
        rows = maps.check_six_quotient_maps()
        self.assertEqual(len(rows), 6)
        self.assertEqual({r["curve"] for r in rows}, {"C1", "C2"})

    def test_total_quotient(self):
        out = maps.check_total_quotient_conics()
        self.assertEqual(out["genus"], 0)

    def test_exceptional_charts_and_inverse_landing(self):
        out = maps.check_exceptional_charts()
        self.assertIn("finite quartic", out["T2_equals_a_minus_sign"])

    def test_fixed_fields_have_degree_two(self):
        rows = maps.check_fixed_fields_and_degrees()
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["generic_degree"] == 2 for row in rows))

    def test_c1_finite_covering_collection(self):
        out = maps.check_c1_finite_covering_collection()
        self.assertEqual(len(out["covers"]), 2)
        self.assertTrue(all(
            c["local_status"] == "EVERYWHERE_LOCALLY_SOLUBLE_BY_POINT"
            for c in out["covers"]
        ))

    def test_classifier_returns_verified_fourth_roots(self):
        self.assertEqual(
            maps.classify_c1_primitive_cover(1, 1, 1),
            {"label": "A=R^4,B=5S^4", "R": 1, "S": 1},
        )

    def test_dplus_exact_reduction_and_closed_symmetry_loci(self):
        out = maps.check_dplus_reduction()
        self.assertEqual(out["branch_count"], 8)
        self.assertEqual(out["cover_genus"], 5)
        sym = maps.check_dplus_symmetry_loci()
        self.assertEqual(sym["proof_status"], "ELEMENTARY_COMPLETE_ON_THESE_LOCI")

    def test_dplus_three_elliptic_projections_and_lifts(self):
        rows = maps.check_dplus_three_elliptic_projections()
        self.assertEqual([row["factor"] for row in rows], ["E_20", "E_80", "E_-400"])
        self.assertTrue(all(len(row["Dplus_lift_tower"]) == 2 for row in rows))

    def test_fail_closed(self):
        cert = maps.build_certificate()
        self.assertEqual(cert["rank_status"], "UNKNOWN_FAIL_CLOSED")
        self.assertEqual(cert["rational_points_status"], "UNKNOWN_FAIL_CLOSED")


if __name__ == "__main__":
    unittest.main()
