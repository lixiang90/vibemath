import unittest
from fractions import Fraction

from spearman_kummer import (
    alpha_x_class,
    doubled_ap_defect,
    doubled_ap_defect_formula,
    is_double_point,
    spearman_specialization,
    squarefree_model,
    torsion_alpha_classes,
)


class SpearmanKummerTests(unittest.TestCase):
    def test_t_equals_one_recovers_spearman_1254_example(self) -> None:
        data = spearman_specialization(1, 1, 7)
        self.assertEqual(data.n, 1254)
        self.assertEqual(
            data.points,
            (
                (Fraction(-198), Fraction(17424)),
                (Fraction(-363), Fraction(22869)),
                (Fraction(-528), Fraction(26136)),
            ),
        )

    def test_displayed_ap_points_are_not_doubles_or_torsion_shifts(self) -> None:
        data = spearman_specialization(1, 1, 7)
        self.assertEqual(
            [is_double_point(point, data.n) for point in data.points], [False] * 3
        )
        torsion_classes = torsion_alpha_classes(data.n)
        self.assertEqual(
            tuple(alpha_x_class(point) for point in data.points), (-22, -3, -33)
        )
        self.assertTrue(
            all(alpha_x_class(point) not in torsion_classes for point in data.points)
        )

    def test_doubling_destroys_the_spearman_progression(self) -> None:
        cases = ((1, 1, 7), (2, 1, 14), (28, 9, Fraction(818, 27)))
        for u, v, w in cases:
            with self.subTest(u=u, v=v):
                data = spearman_specialization(u, v, w)
                defect = doubled_ap_defect(data)
                self.assertEqual(
                    defect, doubled_ap_defect_formula(Fraction(u, v))
                )
                self.assertGreater(defect, 0)

    def test_square_scaled_parameters_normalize_to_the_same_curve(self) -> None:
        first = squarefree_model(spearman_specialization(1, 1, 7))
        partner = squarefree_model(spearman_specialization(2, 1, 14))
        self.assertEqual(first.d, 1254)
        self.assertEqual(partner.d, first.d)
        self.assertEqual(
            tuple((point[0], abs(point[1])) for point in partner.points),
            tuple((point[0], abs(point[1])) for point in first.points),
        )
