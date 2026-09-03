import json
import unittest

import PAPER_SQUARE_NEXT_GATE as G


class NextGateTests(unittest.TestCase):
    def test_54_rows_are_self_contained(self):
        self.assertEqual(len(G.remaining_rows()),54)

    def test_ranking_selects_102(self):
        top=G.ranking()[0]
        self.assertEqual((top["mask"],top["support"],top["patterns_hit"],top["gcd_bound"]),(102,[1,2,5,6],19,4))

    def test_mask102_integral_points(self):
        data=G.mask102_integral_point_certificate()
        self.assertEqual(data["proved_integral_points"],[[-6,0],[-5,0],[-2,0],[-1,0]])
        self.assertEqual(data["nondegenerate_integral_points"],[])
        self.assertEqual(data["d=2"]["square_differences_mod_4"],[0,1,3])

    def test_pattern_impact(self):
        data=G.pattern_impact()
        self.assertEqual((data["input_remaining_count"],data["strictly_excluded"],data["remaining_count"]),(54,19,35))
        self.assertEqual(len(set(data["affected_pattern_ids"])),19)
        self.assertEqual(len(set(data["remaining_pattern_ids"])),35)

    def test_disk_certificate(self):
        disk=json.loads(G.OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(disk,G.build_certificate())


if __name__ == "__main__":
    unittest.main(verbosity=2)
