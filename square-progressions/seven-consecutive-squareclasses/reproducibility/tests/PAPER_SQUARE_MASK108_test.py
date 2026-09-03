import json
import unittest

import PAPER_SQUARE_MASK108 as audit


class Mask108Tests(unittest.TestCase):
    def test_complete_integral_points(self):
        data = audit.integral_point_certificate()
        self.assertEqual(data["proved_integral_points"], [
            [-6, 0], [-5, 0], [-4, -2], [-4, 2], [-3, 0], [-2, 0]
        ])
        self.assertEqual(data["nondegenerate_integral_points"], [])

    def test_kernel_branches_are_complete(self):
        data = audit.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], [1, 3])
        self.assertNotIn(5, data["d=1"]["squares_mod_8"])

    def test_rows_are_self_contained(self):
        rows = audit.remaining_rows()
        self.assertEqual(len(rows), 35)
        for row in rows:
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_pattern_impact(self):
        impact = audit.pattern_impact()
        self.assertEqual((impact["strictly_excluded"], impact["remaining_count"]), (12, 23))
        self.assertTrue(set(impact["affected_pattern_ids"]).isdisjoint(impact["remaining_pattern_ids"]))

    def test_disk_certificate(self):
        with audit.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), audit.build_certificate())


if __name__ == "__main__":
    unittest.main()

