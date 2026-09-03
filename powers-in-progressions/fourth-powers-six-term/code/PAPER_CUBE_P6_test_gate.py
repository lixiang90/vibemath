import unittest

import PAPER_CUBE_P6_gate as gate


class P6GateTests(unittest.TestCase):
    def test_ap_equivalence(self):
        out = gate.check_ap_equivalence()
        self.assertEqual(out["C1"]["positions"], [0, 1, 5])
        self.assertEqual(out["C2"]["positions"], [0, 2, 5])

    def test_geometry(self):
        out = gate.check_geometry_and_obvious_points()
        self.assertTrue(all(v["smooth_plane_genus"] == 3 for v in out.values()))

    def test_local_classes(self):
        out = gate.check_local_classes()
        self.assertIn("odd", out["C1"]["at_2"])
        self.assertIn("3-adic units", out["C2"]["at_3"])

    def test_quotient_trace_audit(self):
        out = gate.check_jacobian_split_traces()
        self.assertEqual(len(out["C1"]), 5)
        self.assertEqual(len(out["C2"]), 5)

    def test_fail_closed(self):
        self.assertEqual(gate.build_certificate()["rational_points_status"], "UNKNOWN_FAIL_CLOSED")


if __name__ == "__main__":
    unittest.main()
