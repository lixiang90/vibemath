import math
import unittest

from bst_number_field import (
    bst_parameter_has_odd_three_valuation,
    known_1254_common_halving_degree,
    known_1254_squareclass_data,
    squareclass_rank,
)


class BSTNumberFieldTests(unittest.TestCase):
    def test_known_rank_three_progression_needs_degree_eight(self) -> None:
        self.assertEqual(
            known_1254_squareclass_data(),
            (
                (-528, (-22, -33, 6)),
                (-363, (-33, -3, 11)),
                (-198, (-3, -22, 66)),
            ),
        )
        self.assertEqual(known_1254_common_halving_degree(), 8)

    def test_squareclass_linear_algebra(self) -> None:
        self.assertEqual(squareclass_rank((2, 8, 1)), 1)
        self.assertEqual(squareclass_rank((-3, 11, 6)), 3)
        self.assertEqual(squareclass_rank((-22, -33, 6)), 2)

    def test_bst_torsion_family_three_adic_obstruction(self) -> None:
        for r in range(1, 40):
            for s in range(1, 40):
                if math.gcd(r, s) == 1:
                    self.assertTrue(bst_parameter_has_odd_three_valuation(r, s))


if __name__ == "__main__":
    unittest.main()

