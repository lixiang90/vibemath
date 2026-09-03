import json
import math
import unittest

import NEXT_ELLIPTIC_ISOMORPHISM_AUDIT as a


class MinimalModelIdentityTests(unittest.TestCase):
    def test_explicit_q_isomorphism(self):
        self.assertEqual(
            a.transform_ainvs(a.ORIGINAL_AINVS, **a.TRANSFORMATION),
            a.MINIMAL_AINVS,
        )

    def test_invariant_scaling(self):
        old = a.invariants(a.ORIGINAL_AINVS)
        new = a.invariants(a.MINIMAL_AINVS)
        self.assertEqual(old["c4"], 6**4*new["c4"])
        self.assertEqual(old["c6"], 6**6*new["c6"])
        self.assertEqual(old["discriminant"], 6**12*new["discriminant"])

    def test_minimality_certificate(self):
        d = a.certificate()
        inv = d["invariants"]
        self.assertEqual(math.gcd(inv["c4"], inv["discriminant"]), 1)
        self.assertTrue(d["semistable"])
        self.assertTrue(all(row["v_c4"] == 0 for row in d["local_reduction"].values()))

    def test_discriminant_conductor_and_j(self):
        d = a.certificate()
        self.assertEqual(d["conductor"], 301245307115205810)
        self.assertEqual(
            d["factorizations"]["minimal_discriminant"],
            {"2": 28, "3": 16, "5": 4, "7": 10, "59": 1,
             "71699": 1, "339106321": 1},
        )
        self.assertEqual(d["j_invariant"]["numerator"], d["invariants"]["c4"]**3)
        self.assertEqual(d["j_invariant"]["denominator"], d["invariants"]["discriminant"])

    def test_disk_certificate(self):
        self.assertEqual(json.loads(a.OUTPUT.read_text(encoding="utf-8")), a.certificate())


if __name__ == "__main__":
    unittest.main()
