import unittest
from fractions import Fraction

from magic_square_search import (
    add_points,
    CertifiedCenter,
    certified_center_progressions,
    is_rational_square,
    magic_grid_from_centers,
    point_is_on_curve,
    search_curve,
    verify_magic_grid,
)


class ExactArithmeticTests(unittest.TestCase):
    def test_certified_center_progressions(self) -> None:
        centers = [
            CertifiedCenter(Fraction(1), (1,)),
            CertifiedCenter(Fraction(4), (2,)),
            CertifiedCenter(Fraction(7), (3,)),
            CertifiedCenter(Fraction(11), (4,)),
        ]
        progressions = certified_center_progressions(centers)
        self.assertEqual(
            [[center.x for center in progression] for progression in progressions],
            [[Fraction(1), Fraction(4), Fraction(7)]],
        )

    def test_rational_square(self) -> None:
        self.assertTrue(is_rational_square(Fraction(49, 900)))
        self.assertFalse(is_rational_square(Fraction(2, 3)))
        self.assertFalse(is_rational_square(Fraction(-1, 4)))

    def test_e154_generators_and_doubling(self) -> None:
        n = 154
        generators = [(Fraction(-98), Fraction(1176)), (Fraction(350), Fraction(5880))]
        for generator in generators:
            self.assertTrue(point_is_on_curve(generator, n))
            doubled = add_points(generator, generator, n)
            self.assertTrue(point_is_on_curve(doubled, n))

    def test_magic_form(self) -> None:
        grid = magic_grid_from_centers(154, [Fraction(139129, 900), Fraction(7225, 36), Fraction(222121, 900)])
        self.assertTrue(verify_magic_grid(grid))
        self.assertEqual(sum(is_rational_square(value) for row in grid for value in row), 7)

    def test_recovers_bremner(self) -> None:
        n = 154
        generators = [(Fraction(-98), Fraction(1176)), (Fraction(350), Fraction(5880))]
        _, candidates = search_curve(n, generators, box=10, minimum_squares=7)
        bremner_entries = {
            373**2,
            289**2,
            565**2,
            360721,
            425**2,
            23**2,
            205**2,
            527**2,
            222121,
        }
        self.assertTrue(
            any(
                {value for row in candidate.integer_grid for value in row} == bremner_entries
                for candidate in candidates
            )
        )


if __name__ == "__main__":
    unittest.main()
