"""Independent checks for the Round-11 0102 existence closure."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "round11_existence", HERE / "PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11.py"
)
round11 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(round11)


class Round11ExistenceTests(unittest.TestCase):
    def test_independent_symbolic_curve_identity(self):
        X, Y, W = sp.symbols("X Y W")
        expanded = sp.expand((X**3 + Y**3) * (2 * Y**3 - X**3) - 2 * W**3)
        expected = -X**6 + X**3 * Y**3 + 2 * Y**6 - 2 * W**3
        self.assertEqual(sp.expand(expanded - expected), 0)
        self.assertEqual(expanded.subs({X: 2, Y: 1, W: -3}), 0)

    def test_independent_ap_and_field_witnesses(self):
        X, Y = 2, 1
        rational_ap = tuple(
            sp.Rational((2-k)*X**3 + k*Y**3, 2) for k in range(5)
        )
        integer_ap = tuple(8 * value for value in rational_ap)
        self.assertEqual(integer_ap, (64, 36, 8, -20, -48))
        self.assertEqual(len(set(integer_ap)), 5)
        self.assertTrue(all(integer_ap))

        self.assertEqual(4**3, integer_ap[0])
        self.assertEqual(6**2, integer_ap[1])          # (alpha^2)^3
        self.assertEqual(2**3, integer_ap[2])
        self.assertEqual((-2)**3 * 6, integer_ap[4])  # (-2 alpha)^3

        # Independent valuation-vector exclusion for -20 from <6> modulo cubes.
        self.assertEqual(sp.factorint(20)[5] % 3, 1)
        self.assertTrue(
            all(sp.factorint(d).get(5, 0) % 3 == 0 for d in (1, 6, 36))
        )
        t = sp.Symbol("t")
        self.assertTrue(sp.Poly(t**3 - 6).is_irreducible)

    def test_independent_color_word(self):
        raw = (0, 2, 0, 1)
        self.assertEqual(tuple(2*c % 3 for c in raw), (0, 1, 0, 2))

    def test_independent_quotient_identity_and_point(self):
        X, Y, W = sp.symbols("X Y W")
        u = -2 * W / Y**2
        v = 2 * X**3 / Y**3 - 1
        source = (X**3 + Y**3) * (2 * Y**3 - X**3) - 2 * W**3
        numerator = sp.together(v**2 - u**3 - 9).as_numer_denom()[0]
        quotient, remainder = sp.div(
            sp.expand(numerator), sp.expand(source), X, Y, W
        )
        self.assertEqual(sp.expand(remainder), 0)
        self.assertNotEqual(quotient, 0)
        point = {X: 2, Y: 1, W: -3}
        self.assertEqual((u.subs(point), v.subs(point)), (6, 15))

    def test_independent_nagell_lutz(self):
        x, y = 6, 15
        discriminant = -16 * 27 * 9**2
        self.assertEqual(y*y, x**3 + 9)
        self.assertNotEqual(discriminant % (y*y), 0)

    def test_stored_certificate(self):
        stored = json.loads(round11.CERTIFICATE.read_text(encoding="utf-8"))
        self.assertEqual(stored, round11.certificate_data())


if __name__ == "__main__":
    unittest.main()
