import json
from math import isqrt
import unittest

import PAPER_SQUARE_MASK54 as gate
import sympy as sp


class Mask54Tests(unittest.TestCase):
    def test_authoritative_input_and_fifteen_characters(self):
        rows = gate.input_rows()
        self.assertEqual([row["pattern_id"] for row in rows], gate.INPUT_IDS)
        self.assertEqual(len(rows), 7)
        for row in rows:
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_independent_occurrence_inventory(self):
        data = gate.occurrence_inventory()
        self.assertEqual(data["total_character_occurrences"], 105)
        self.assertEqual((data["distinct_masks"], data["distinct_genus1_masks"]), (41, 22))
        self.assertEqual(
            [(row["mask"], row["patterns_hit"], row["gcd_bound"])
             for row in data["pairable_genus1_ranking"]],
            [(54, 3, 3), (27, 2, 3), (45, 2, 6), (85, 2, 8)],
        )

    def test_mask54_geometry_and_occurrences(self):
        data = gate.occurrence_inventory()
        self.assertEqual(gate.support(54), [1, 2, 4, 5])
        self.assertEqual(
            gate.constant_pairing(54),
            {"left": [1, 5], "right": [2, 4], "difference_right_minus_left": 3},
        )
        self.assertEqual(
            [row["occurrence_id"] for row in data["selected_occurrences"]],
            ["P59:m54", "P214:m54", "P230:m54"],
        )
        self.assertTrue(all(row["same_t_map"] == "t=(1*U_m+(-1)*Z_m)/(0*U_m+(1)*Z_m)"
                            for row in data["selected_occurrences"]))

    def test_integer_translation_is_a_point_bijection(self):
        t, s = sp.symbols("t s")
        target = (t + 1) * (t + 2) * (t + 4) * (t + 5)
        source = (s + 2) * (s + 3) * (s + 5) * (s + 6)
        self.assertTrue(sp.Poly(sp.expand(target - source.subs(s, t - 1)), t).is_zero)
        self.assertEqual(sp.expand((t - 1) + 1 - t), 0)

        data = gate.translation_certificate()
        self.assertEqual(
            data["mapped_target_points"],
            [[-5, 0], [-4, 0], [-3, -2], [-3, 2], [-2, 0], [-1, 0]],
        )

    def test_independent_pairing_identity(self):
        t = sp.symbols("t")
        A = (t + 1) * (t + 5)
        B = (t + 2) * (t + 4)
        target = (t + 1) * (t + 2) * (t + 4) * (t + 5)
        self.assertTrue(sp.Poly(sp.expand(B - A - 3), t).is_zero)
        self.assertTrue(sp.Poly(sp.expand(target - A * B), t).is_zero)
        self.assertTrue(sp.Poly(sp.expand(A + 4 - (t + 3) ** 2), t).is_zero)

    def test_complete_middle_interval_and_degeneracy(self):
        data = gate.integral_point_certificate()
        self.assertEqual(
            [(row["t"], row["rhs"], row["ys"])
             for row in data["middle_interval_exact_check"]],
            [(-5, 0, [0]), (-4, 0, [0]), (-3, 4, [-2, 2]),
             (-2, 0, [0]), (-1, 0, [0])],
        )
        self.assertEqual(
            data["proved_integral_points"],
            [[-5, 0], [-4, 0], [-3, -2], [-3, 2], [-2, 0], [-1, 0]],
        )
        self.assertEqual(data["nondegenerate_integral_points"], [])
        self.assertTrue(all(
            0 <= row["zero_position_in_original_block"] <= 6
            for row in data["degeneracy_in_original_seven_term_block"]
        ))

    def test_both_squarefree_branches_are_terminal(self):
        def is_squarefree(value):
            return all(value % (prime * prime) for prime in range(2, isqrt(value) + 1))

        kernels = [
            divisor for divisor in range(1, 4)
            if 3 % divisor == 0 and is_squarefree(divisor)
        ]
        derived = {}
        for divisor in kernels:
            quotient = 3 // divisor
            rows = []
            for left in range(1, quotient + 1):
                if quotient % left:
                    continue
                right = quotient // left
                if left > right or (left + right) % 2:
                    continue
                U = (right - left) // 2
                V = (right + left) // 2
                rows.append({"factor_pair": [left, right], "U_V": [U, V]})
            derived[divisor] = rows
        self.assertEqual(
            derived,
            {
                1: [{"factor_pair": [1, 3], "U_V": [1, 2]}],
                3: [{"factor_pair": [1, 1], "U_V": [0, 1]}],
            },
        )

        data = gate.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], kernels)
        branches = {row["d"]: row for row in data["branches"]}
        self.assertEqual(set(branches), set(kernels))
        self.assertEqual(
            branches[1]["positive_same_parity_factor_pairs"],
            [row["factor_pair"] for row in derived[1]],
        )
        self.assertEqual(branches[1]["forced_U_V"], derived[1][0]["U_V"])
        self.assertNotIn(5, branches[1]["squares_mod_8"])
        self.assertEqual(
            branches[3]["nonnegative_factor_pairs"],
            [row["factor_pair"] for row in derived[3]],
        )
        self.assertEqual(branches[3]["forced_U_V"], derived[3][0]["U_V"])
        self.assertFalse(data["bounded_search_used"])
        self.assertFalse(data["mordell_weil_used"])

    def test_exact_pattern_impact_and_partitions(self):
        impact = gate.pattern_impact()
        self.assertEqual(impact["affected_pattern_ids"], [59, 214, 230])
        self.assertEqual(impact["affected_partitions"], ["0012231", "0122213", "0012102"])
        self.assertEqual(impact["remaining_pattern_ids"], [12, 31, 134, 276])
        self.assertEqual(
            impact["remaining_partitions"],
            ["0012202", "0001202", "0012131", "0010203"],
        )
        self.assertEqual((impact["strictly_excluded"], impact["remaining_count"]), (3, 4))

    def test_disk_certificate(self):
        with gate.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), gate.build_certificate())


if __name__ == "__main__":
    unittest.main()
