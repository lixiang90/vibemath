import unittest

import sympy as sp

import PAPER_ELLIPTIC_NEXT_analysis as nxt
import PAPER_ELLIPTIC_MOODY_JUYAL as old


class NextStageTests(unittest.TestCase):
    def test_general_r_elimination_and_tangent(self):
        data = nxt.general_r_identities()
        self.assertEqual(data["quartic_elimination"], 0)
        self.assertEqual(data["tangent_vanish_c0_order3"], [0, 0, 0])
        self.assertEqual(data["tangent_section_on_quartic"], 0)
        self.assertEqual(data["published_r3_match"], 0)

    def test_r2_is_different_section(self):
        data = nxt.general_r_identities()
        self.assertEqual(data["endpoint_r2_match"], 0)
        self.assertNotEqual(data["two_r2_sections_difference"], 0)
        self.assertEqual(
            sp.factor(
                nxt.C_CHORD.subs({nxt.r: 2, nxt.m: old.q}) - old.U_SECTION
            ),
            0,
        )

    def test_y_slice(self):
        self.assertTrue(all(value == 0 for value in nxt.y_slice_identities().values()))
        self.assertEqual(
            nxt.y_slice_boundary_map(),
            {
                "rho=0,eta=+1": "O",
                "rho=0,eta=-1": (0, 0),
                "infinity_+": (-4, 0),
                "infinity_-": (-8, 0),
            },
        )

    def test_y_slice_inverse_formula(self):
        X, Y = sp.symbols("X Y")
        rr, ee = nxt.y_slice_from_jacobian(X, Y)
        denominator = (X + 4) * (X + 8)
        self.assertEqual(rr, 2 * Y / denominator)
        self.assertEqual(ee, (X**2 - 32) / denominator)

    def test_endpoint_j_nonconstant(self):
        tt = old.T_SECTION
        jj = sp.factor((tt**4 - 16 * tt**2 + 16) ** 3 / (tt**2 * (tt**2 - 16)))
        self.assertNotEqual(sp.factor(jj.subs(old.q, 3)), sp.factor(jj.subs(old.q, sp.Rational(5, 2))))

    def test_rational_singular_q(self):
        tt = old.T_SECTION
        numerator_t = sp.together(tt).as_numer_denom()[0]
        numerator_t4 = sp.together(tt**2 - 16).as_numer_denom()[0]
        self.assertEqual(sp.Poly(numerator_t, old.q).ground_roots(), {})
        self.assertEqual(sp.Poly(numerator_t4, old.q).ground_roots(), {})
        denominator = sp.factor(sp.together(tt).as_numer_denom()[1])
        self.assertEqual(set(sp.Poly(denominator, old.q).ground_roots()), {sp.Integer(-2), sp.Integer(0), sp.Integer(2)})

    def test_campbell_matrix_shape_and_real_obstruction(self):
        rows = nxt.campbell_local_matrix()
        self.assertEqual(len(rows), 64)
        self.assertEqual(len({(row["side"], row["d"]) for row in rows}), 64)
        self.assertEqual(nxt.matrix_summary(rows)["real_obstructed"], 16)
        self.assertTrue(all(row["d"] < 0 and row["side"] == "E" for row in rows if row["infinity"] == "REAL_NO_SIGN"))

    def test_matrix_never_calls_missing_witness_obstruction(self):
        rows = nxt.campbell_local_matrix()
        allowed = {
            "Q2_YES_EXACT_SQUARE",
            "Q2_UNRESOLVED",
            "QP_YES_EXACT_SQUARECLASS",
            "QP_NO_MODULUS",
            "QP_UNRESOLVED_NO_SMALL_UNIT_WITNESS",
        }
        self.assertTrue(all(cell["status"] in allowed for row in rows for cell in row["places"].values()))

    def test_exact_first_stage_survivors(self):
        summary = nxt.matrix_summary()
        self.assertEqual(
            summary["survivors_after_proven_obstructions"]["E"],
            [1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 30, 35, 42, 70, 105, 210],
        )
        self.assertEqual(
            summary["survivors_after_proven_obstructions"]["E_dual"],
            [1, 4230241, 339106321, 1434501462453361],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
