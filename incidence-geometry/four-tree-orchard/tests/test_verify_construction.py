"""Regression tests for the four-tree orchard construction."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


CODE = Path(__file__).resolve().parents[1] / "code"
sys.path.insert(0, str(CODE))

from verify_construction import (  # noqa: E402
    admissible_pairs,
    guaranteed_line_count,
    integer_dilation,
    intervals,
    line_value,
    mistyped_line_count,
    parameters,
    rational_points,
    target_count,
)


class OrchardConstructionTests(unittest.TestCase):
    def test_count_matches_closed_formula(self) -> None:
        for n in range(28, 28 + 28 * 20):
            with self.subTest(n=n):
                self.assertEqual(guaranteed_line_count(n), target_count(n))

    def test_point_count_is_n(self) -> None:
        for n in range(28, 200):
            with self.subTest(n=n):
                _, a, b, c, d, _, _ = parameters(n)
                self.assertEqual(a + b + c + d, n)

    def test_special_improvements(self) -> None:
        self.assertEqual(guaranteed_line_count(59), 124)
        self.assertEqual(guaranteed_line_count(60), 129)

    def test_typo_is_detected_at_29(self) -> None:
        self.assertEqual(mistyped_line_count(29), 29)
        self.assertEqual(target_count(29), 30)

    def test_four_points_satisfy_the_same_line_equation(self) -> None:
        for n in (28, 29, 59, 60):
            p_family, q_family, r_family, s_family = rational_points(n)
            a_set, b_set, c_set, d_set = intervals(n)
            r_by_index = dict(zip(c_set, r_family, strict=True))
            s_by_index = dict(zip(d_set, s_family, strict=True))
            for x, y in admissible_pairs(n):
                points = (
                    p_family[x],
                    q_family[y],
                    r_by_index[x + y],
                    s_by_index[x - y],
                )
                self.assertEqual(
                    [line_value(n, x, y, point) for point in points],
                    [Fraction(1)] * 4,
                )

    def test_integer_dilation_preserves_distinct_points(self) -> None:
        for n in (28, 59, 60):
            scale, points = integer_dilation(n)
            self.assertGreater(scale, 0)
            self.assertEqual(len(points), n)
            self.assertEqual(len(set(points)), n)
            self.assertTrue(all(isinstance(value, int) for point in points for value in point))


if __name__ == "__main__":
    unittest.main()
