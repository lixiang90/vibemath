import unittest

from sympy import Poly

from bremner_j1728 import (
    EIGHTH_POINT_1,
    EIGHTH_POINT_2,
    PRIMARY_J1728,
    SECOND_J1728,
    eighth_point_polynomial,
    primary_specialization_remainders,
    z,
)


class BremnerJ1728Tests(unittest.TestCase):
    def test_primary_intersection_is_quadratic(self) -> None:
        self.assertEqual(PRIMARY_J1728.degree(), 2)
        self.assertTrue(PRIMARY_J1728.is_irreducible)
        self.assertEqual(
            primary_specialization_remainders(),
            {
                "d": 12 - 12 * PRIMARY_J1728.gens[0],
                "A": 1008,
                "B": 0,
                "eighth_1": 48 - 48 * PRIMARY_J1728.gens[0],
                "eighth_2": 48 * PRIMARY_J1728.gens[0] - 48,
            },
        )

    def test_eighth_point_needs_a_quartic_field(self) -> None:
        expected = Poly(z**4 + 2304, z, domain="QQ")
        for expression in (EIGHTH_POINT_1, EIGHTH_POINT_2):
            polynomial = eighth_point_polynomial(expression)
            self.assertEqual(polynomial, expected)
            self.assertTrue(polynomial.is_irreducible)

    def test_second_family_intersection_has_degree_twenty_four(self) -> None:
        self.assertEqual(SECOND_J1728.degree(), 24)
        self.assertTrue(SECOND_J1728.is_irreducible)


if __name__ == "__main__":
    unittest.main()
