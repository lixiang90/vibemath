import unittest

from sympy import expand

from campbell_j1728 import (
    c6_condition,
    full_2_torsion_polynomial,
    primitive_j1728_polynomial,
)


class CampbellJ1728Tests(unittest.TestCase):
    def test_j1728_intersection_is_irreducible_degree_twelve(self) -> None:
        polynomial = primitive_j1728_polynomial()
        self.assertEqual(polynomial.degree(), 12)
        self.assertTrue(polynomial.is_irreducible)
        self.assertEqual(
            expand(c6_condition() - 16384 * polynomial.as_expr()), 0
        )

    def test_full_two_torsion_requires_degree_twenty_four(self) -> None:
        polynomial = full_2_torsion_polynomial()
        self.assertEqual(polynomial.degree(), 24)
        self.assertTrue(polynomial.is_irreducible)


if __name__ == "__main__":
    unittest.main()
