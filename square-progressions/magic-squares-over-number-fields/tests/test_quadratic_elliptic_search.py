import unittest
from fractions import Fraction

from quadratic_elliptic_search import (
    enumerate_centers,
    lift_rational_point,
    point_is_on_curve,
    quadratic_square_root,
    transport_twist_point,
)
from number_field_magic import qmul


class QuadraticEllipticSearchTests(unittest.TestCase):
    def test_transport_twist_point(self) -> None:
        point = transport_twist_point((Fraction(45), Fraction(225)), 6)
        self.assertTrue(point_is_on_curve(point, 5, 6))

    def test_quadratic_square_root(self) -> None:
        root = (Fraction(2, 3), Fraction(5, 7))
        value = qmul(root, root, 6)
        self.assertEqual(qmul(quadratic_square_root(value, 6), quadratic_square_root(value, 6), 6), value)

    def test_rank_two_box_enumeration(self) -> None:
        generators = (
            lift_rational_point((Fraction(25, 4), Fraction(75, 8))),
            transport_twist_point((Fraction(45), Fraction(225)), 6),
        )
        centers = enumerate_centers(5, 6, generators, 2)
        self.assertGreaterEqual(len(centers), 10)


if __name__ == "__main__":
    unittest.main()
