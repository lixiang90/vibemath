import json
import unittest

import PAPER_SQUARE_MASK51 as gate


class Mask51Tests(unittest.TestCase):
    def test_complete_genus1_inventory(self):
        data = gate.genus1_inventory()
        self.assertEqual((data["input_pattern_count"], data["total_character_occurrences"]), (15, 225))
        self.assertEqual(data["all_distinct_masks"], 53)
        self.assertEqual(data["distinct_genus1_four_factor_masks"], 26)
        self.assertEqual(sum(row["patterns_hit"] for row in data["all_genus1_masks"]), data["genus1_occurrences"])
        self.assertEqual(data["already_proved_translate_ranking"][0]["mask"], 51)
        self.assertEqual(data["already_proved_translate_ranking"][0]["patterns_hit"], 5)

    def test_pairable_ranking(self):
        rows = gate.genus1_inventory()["pairable_ranking"]
        self.assertEqual(
            [(row["mask"], row["patterns_hit"], row["gcd_bound_from_pairing"]) for row in rows],
            [(51, 5, 4), (90, 5, 6), (54, 4, 3), (27, 3, 3), (45, 3, 6), (85, 2, 8)],
        )

    def test_complete_integral_points_and_translation(self):
        data = gate.integral_point_certificate()
        self.assertEqual(data["proved_integral_points"], [[-5, 0], [-4, 0], [-1, 0], [0, 0]])
        self.assertEqual(data["nondegenerate_integral_points"], [])
        self.assertTrue(data["integral_translation_to_mask102"]["bijection_on_integer_parameters"])
        self.assertFalse(data["bounded_search_used"])

    def test_independent_squarefree_branches(self):
        data = gate.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], [1, 2])
        self.assertNotIn(2, data["d=2"]["square_differences_mod_4"])

    def test_every_input_packet_has_fifteen_distinct_characters(self):
        for row in gate.input_rows():
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_pattern_impact(self):
        impact = gate.pattern_impact()
        self.assertEqual((impact["strictly_excluded"], impact["remaining_count"]), (5, 10))
        self.assertTrue(set(impact["affected_pattern_ids"]).isdisjoint(impact["remaining_pattern_ids"]))

    def test_disk_certificate(self):
        with gate.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), gate.build_certificate())


if __name__ == "__main__":
    unittest.main()
