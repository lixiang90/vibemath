import unittest
from fractions import Fraction

from spearman_parameters import (
    canonical_parameter,
    fourth_intersection,
    generate_quartic_points,
    on_spearman_quartic,
    parameter_orbits,
)


class SpearmanParameterTests(unittest.TestCase):
    def test_fourth_intersection_recovers_first_new_parameter(self) -> None:
        result = fourth_intersection(
            (
                (Fraction(0), Fraction(6)),
                (Fraction(1), Fraction(-7)),
                (Fraction(2), Fraction(14)),
            )
        )
        self.assertEqual(result, (Fraction(9, 14), Fraction(-1227, 196)))
        self.assertTrue(on_spearman_quartic(result))

    def test_involution_has_one_canonical_representative(self) -> None:
        point = (Fraction(9, 14), Fraction(1227, 196))
        partner = (Fraction(28, 9), Fraction(818, 27))
        self.assertEqual(canonical_parameter(point), canonical_parameter(partner))

    def test_two_rounds_produce_four_essential_orbits(self) -> None:
        orbits = parameter_orbits(generate_quartic_points(rounds=2))
        self.assertEqual(
            [point[0] for point in orbits],
            [
                Fraction(230, 703),
                Fraction(9, 14),
                Fraction(1),
                Fraction(206136, 147103),
            ],
        )

    def test_higher_height_closure_adds_two_orbits(self) -> None:
        orbits = parameter_orbits(
            generate_quartic_points(rounds=3, max_component=10**30)
        )
        self.assertEqual(len(orbits), 6)
        self.assertIn(Fraction(29662529, 95793739), [point[0] for point in orbits])
        self.assertIn(
            Fraction(482976761260, 730628799543), [point[0] for point in orbits]
        )
