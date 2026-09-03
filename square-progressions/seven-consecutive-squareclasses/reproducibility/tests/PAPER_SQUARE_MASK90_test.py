import json
import unittest

import PAPER_SQUARE_MASK90 as gate


class Mask90Tests(unittest.TestCase):
    def test_authoritative_input_and_fifteen_characters(self):
        rows = gate.input_rows()
        self.assertEqual([row["pattern_id"] for row in rows], gate.INPUT_IDS)
        self.assertEqual(len(rows), 10)
        for row in rows:
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_independent_occurrence_inventory(self):
        data = gate.occurrence_inventory()
        self.assertEqual(data["total_character_occurrences"], 150)
        self.assertEqual((data["distinct_masks"], data["distinct_genus1_masks"]), (49, 25))
        self.assertEqual(
            [(row["mask"], row["patterns_hit"], row["gcd_bound"])
             for row in data["pairable_genus1_ranking"]],
            [(54, 3, 3), (45, 3, 6), (90, 3, 6), (27, 2, 3), (85, 2, 8)],
        )

    def test_mask90_geometry_and_occurrences(self):
        data = gate.occurrence_inventory()
        self.assertEqual(gate.support(90), [1, 3, 4, 6])
        self.assertEqual(
            gate.constant_pairing(90),
            {"left": [1, 6], "right": [3, 4], "difference_right_minus_left": 6},
        )
        self.assertEqual(
            [row["occurrence_id"] for row in data["selected_occurrences"]],
            ["P43:m90", "P251:m90", "P281:m90"],
        )
        self.assertTrue(all(row["same_t_map"] == "t=(1*U_m+(-1)*Z_m)/(0*U_m+(1)*Z_m)"
                            for row in data["selected_occurrences"]))

    def test_pairing_identity(self):
        for t in range(-20, 21):
            A = (t + 1) * (t + 6)
            B = (t + 3) * (t + 4)
            self.assertEqual(B - A, 6)
            self.assertEqual(gate.rhs(t), A * B)

    def test_complete_middle_interval(self):
        data = gate.integral_point_certificate()
        self.assertEqual(
            [(row["t"], row["rhs"], row["ys"])
             for row in data["middle_interval_exact_check"]],
            [(-6, 0, [0]), (-5, -8, []), (-4, 0, [0]),
             (-3, 0, [0]), (-2, -8, []), (-1, 0, [0])],
        )
        self.assertEqual(data["proved_integral_points"], [[-6, 0], [-4, 0], [-3, 0], [-1, 0]])
        self.assertEqual(data["nondegenerate_integral_points"], [])

    def test_all_four_squarefree_branches_are_terminal(self):
        data = gate.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], [1, 2, 3, 6])
        branches = {row["d"]: row for row in data["branches"]}
        self.assertEqual(set(branches), {1, 2, 3, 6})
        self.assertNotIn(branches[1]["rhs_mod_4"], branches[1]["square_differences_mod_4"])
        self.assertEqual(branches[2]["positive_same_parity_factor_pairs"], [[1, 3]])
        self.assertEqual(branches[2]["forced_U_V"], [1, 2])
        lo, value, hi = branches[2]["nonsquare_interval"]
        self.assertLess(lo, value)
        self.assertLess(value, hi)
        self.assertEqual((lo, hi), (5 * 5, 6 * 6))
        self.assertNotIn(branches[3]["rhs_mod_4"], branches[3]["square_differences_mod_4"])
        self.assertEqual(branches[6]["forced_U_V"], [0, 1])
        self.assertFalse(data["bounded_search_used"])
        self.assertFalse(data["mordell_weil_used"])

    def test_exact_pattern_impact_and_partitions(self):
        impact = gate.pattern_impact()
        self.assertEqual(impact["affected_pattern_ids"], [43, 251, 281])
        self.assertEqual(impact["affected_partitions"], ["0100021", "0102221", "0102003"])
        self.assertEqual(impact["remaining_pattern_ids"], [12, 31, 59, 134, 214, 230, 276])
        self.assertEqual(
            impact["remaining_partitions"],
            ["0012202", "0001202", "0012231", "0012131", "0122213", "0012102", "0010203"],
        )
        self.assertEqual((impact["strictly_excluded"], impact["remaining_count"]), (3, 7))

    def test_disk_certificate(self):
        with gate.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), gate.build_certificate())


if __name__ == "__main__":
    unittest.main()
