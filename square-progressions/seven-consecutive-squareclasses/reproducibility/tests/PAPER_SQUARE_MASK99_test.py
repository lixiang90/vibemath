import json
import unittest

import PAPER_SQUARE_MASK99 as gate


class Mask99Tests(unittest.TestCase):
    def test_complete_inventory(self):
        data = gate.occurrence_inventory()
        self.assertEqual((data["input_pattern_count"], data["total_occurrences"]), (23, 345))
        self.assertEqual(data["distinct_masks"], 55)
        self.assertEqual(data["constant_pairing_genus1_ranking"][0]["mask"], 99)
        self.assertEqual(data["constant_pairing_genus1_ranking"][0]["patterns_hit"], 8)
        histogram = {int(k): v for k, v in data["frequency_of_pattern_hit_counts"].items()}
        self.assertEqual(sum(histogram.values()), 55)
        self.assertEqual(sum(hit_count * count for hit_count, count in histogram.items()), 345)
        self.assertEqual(
            [(row["mask"], row["patterns_hit"]) for row in data["constant_pairing_genus1_ranking"]],
            [(99, 8), (54, 7), (45, 7), (90, 7), (51, 5), (85, 5), (27, 3)],
        )

    def test_complete_integral_points(self):
        data = gate.integral_point_certificate()
        self.assertEqual(data["proved_integral_points"], [
            [-6, 0], [-5, 0], [-3, -6], [-3, 6], [-1, 0], [0, 0]
        ])
        self.assertEqual(data["nondegenerate_integral_points"], [])
        self.assertFalse(data["bounded_search_used"])

    def test_squarefree_branches(self):
        data = gate.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], [1, 5])
        self.assertNotIn(13 % 8, data["d=1"]["squares_mod_8"])
        self.assertIn("A>0", data["d=5"]["consequence"])

    def test_each_source_packet_has_fifteen_distinct_characters(self):
        for row in gate.final_rows():
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_pattern_impact(self):
        impact = gate.pattern_impact()
        self.assertEqual((impact["strictly_excluded"], impact["remaining_count"]), (8, 15))
        self.assertTrue(set(impact["affected_pattern_ids"]).isdisjoint(impact["remaining_pattern_ids"]))

    def test_disk_certificate(self):
        with gate.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), gate.build_certificate())


if __name__ == "__main__":
    unittest.main()
