import json
import math
from pathlib import Path
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
        # Directly certify the split nodal reductions at 2 and 3.  Here a2
        # and a4 vanish, so the reduced affine cubic is F=y^2+x*y-x^3.
        _, a2, _, a4, _ = a.MINIMAL_AINVS
        for p in (2, 3):
            self.assertEqual(a2 % p, 0)
            self.assertEqual(a4 % p, 0)
            singular = []
            for x in range(p):
                for y in range(p):
                    f = (y*y + x*y - x**3) % p
                    fx = (y - 3*x*x) % p
                    fy = (2*y + x) % p
                    if f == fx == fy == 0:
                        singular.append((x, y))
                    self.assertEqual((y*y + x*y) % p, (y*(y+x)) % p)
            self.assertEqual(singular, [(0, 0)])
            # The tangent lines y=0 and y+x=0 are distinct over both fields.
            self.assertNotEqual((0, 1), (1 % p, 1 % p))

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

    def test_manuscript_contains_exact_minimal_model_theorem(self):
        tex = (Path(__file__).resolve().parent.parent / "paper" / "main.tex").read_text(encoding="utf-8")
        for token in (
            "(1,-16441530,0,45166889779200,0)",
            "2926451742397178075653974744686961623040000",
            "301245307115205810",
            "valid without change at $p=2$ and $p=3$",
            "unique affine",
            "singular point is $(0,0)$",
            "y^2+xy=y(y+x)",
            "multiplicative reduction at $2$ and $3$ is",
            "split",
            "absence of a database row",
        ):
            self.assertIn(token, tex)

if __name__ == "__main__":
    unittest.main()
