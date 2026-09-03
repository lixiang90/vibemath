import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import PAPER_SQUARE_MASK77_analysis as M


class Mask77Tests(unittest.TestCase):
    def test_symbolic_birational_map(self):
        data=M.symbolic_map_certificate()
        for key in ("forward_curve_identity","inverse_curve_identity","t_roundtrip","y_roundtrip","X_roundtrip","Y_roundtrip"):
            self.assertEqual(data[key],"0")

    def test_affine_maps_both_directions(self):
        for tt,yy in [(6,72),(-2,0),(-3,0),(-6,0)]:
            xx,YY=M.forward_affine(tt,yy)
            self.assertEqual(YY*YY,xx**3-36*xx)
            self.assertEqual(M.inverse_affine(xx,YY),(Fraction(tt),Fraction(yy)))

    def test_boundary_table(self):
        data=M.symbolic_map_certificate()["boundary"]
        self.assertEqual(len(data),6)
        self.assertEqual({row["E"] for row in data},{"O","(-6,0)","(0,0)","(6,0)","(12,36)","(12,-36)"})

    def test_gcd_divides_72_and_branch_recovery(self):
        point=M.exact_branch_data(6,72)
        self.assertEqual((point["d"],point["u"],point["v"]),(2,6,6))
        self.assertEqual(72 % point["gcd_A_B"],0)

    def test_d1_is_closed(self):
        data=M.d1_closed_proof_data()
        self.assertEqual(data["candidate_x"],[-5,-3,3,5])
        self.assertTrue(all(math.isqrt(v)**2 != v for v in data["x_times_x_minus_1"].values()))
        self.assertEqual(data["status"],"PROVED_EMPTY")

    def test_finite_branch_disjunction(self):
        rows=M.pell_thue_branches()
        self.assertEqual(len(rows),18)
        self.assertEqual({row["d"] for row in rows},{1,2,3,6})
        for row in rows:
            modulus=row["strict_congruence_obstruction_modulus"]
            if modulus:
                self.assertFalse(M.branch_has_solution_mod(row["d"],row["a"],row["b"],row["sign"],modulus))
        self.assertEqual(sum(row["status"]=="STRICTLY_EXCLUDED_BY_CONGRUENCE" for row in rows),15)
        self.assertEqual(sum(row["status"]=="PROVED_CLOSED_BY_FACTOR_SIZE" for row in rows),3)
        self.assertFalse(any(row["status"].startswith("UNRESOLVED") for row in rows))

    def test_factor_size_certificate_is_structured(self):
        rows=M.factor_size_structured_certificate()
        self.assertEqual(len(rows),3)
        self.assertEqual({row["factor_identity_after_equations"] for row in rows},{"0"})
        self.assertEqual([row["threshold"] for row in rows],[5,3,3])
        self.assertEqual(
            [item["status"] for row in rows for item in row["small_results"]].count("solution"),
            3,
        )

    def test_bounded_search_is_labelled_conjectural(self):
        cert=M.build_certificate(1000)
        self.assertTrue(cert["bounded_search"]["conjectural_only"])
        self.assertEqual(cert["global_completeness_status"],"PROVED_BY_GCD_BRANCHES")
        self.assertEqual(cert["bounded_search"]["points_with_nonnegative_y"],[[-6,0],[-3,0],[-2,0],[0,0],[6,72]])
        self.assertEqual(cert["proved_integral_points"],[[-6,0],[-3,0],[-2,0],[0,0],[6,-72],[6,72]])

    def test_same_t_audit_excludes_all_44(self):
        audit=M.mask_77_89_pattern_audit()
        self.assertEqual((audit["affected_remaining_patterns"],audit["strictly_excluded"],audit["survivors"],audit["remaining_patterns_after_this_theorem"]),(44,44,0,54))
        self.assertEqual(len({row["pattern_id"] for row in audit["rows"]}),44)
        self.assertEqual(len(audit["remaining_pattern_ids"]),54)
        self.assertEqual(len(set(audit["remaining_pattern_ids"])),54)
        self.assertTrue(audit["all_safe_survivors_have_15_distinct_character_masks"])
        for row in audit["rows"]:
            self.assertEqual(row["status"],"STRICTLY_EXCLUDED_BY_COMPLETE_MASK77_89_LIST")
            self.assertTrue(not row["candidate_intersection"] or all(not check["all_15_pass"] for check in row["same_t_checks"]))

    def test_disk_certificate(self):
        disk=json.loads(Path("PAPER_SQUARE_MASK77_CERTIFICATE.json").read_text(encoding="utf-8"))
        self.assertEqual(disk,M.build_certificate(disk["bounded_search"]["bound_abs_t"]))
        self.assertEqual(disk["input_sha256"],{
            M.SAFE_CERT.name:M.sha256(M.SAFE_CERT),
            M.ROUND4_CERT.name:M.sha256(M.ROUND4_CERT),
        })


if __name__=="__main__":
    unittest.main(verbosity=2)
