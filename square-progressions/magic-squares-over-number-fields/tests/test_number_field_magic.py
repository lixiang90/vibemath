import unittest

from cubic_field_magic import circle_data as cubic_circle_data
from cubic_field_magic import search as search_pure_cubic
from number_field_magic import (
    circle_data,
    find_offset_configuration,
    search_general_quadratic,
    search_two_square_classes,
)
from fractions import Fraction
from verify_number_field_examples import bremner_real_example, pythagorean_example


class NumberFieldMagicTests(unittest.TestCase):
    def test_circle_parametrization(self) -> None:
        result = circle_data((1, 1), 2)
        self.assertIsNotNone(result)

    def test_small_two_class_search_is_negative(self) -> None:
        self.assertIsNone(search_two_square_classes(-1, 30))

    def test_small_general_search_is_negative(self) -> None:
        self.assertIsNone(search_general_quadratic(2, 2, 1))

    def test_modular_offset_sieve_finds_exact_configuration(self) -> None:
        q = lambda value: (Fraction(value), Fraction(0))
        offsets = {q(value) for value in (-4, -3, -2, -1, 1, 2, 3, 4)}
        configuration = find_offset_configuration(offsets, modulus=5)
        self.assertIsNotNone(configuration)
        b, c = configuration
        self.assertIn((b[0] + c[0], b[1] + c[1]), offsets)
        self.assertIn((b[0] - c[0], b[1] - c[1]), offsets)

    def test_modular_offset_sieve_keeps_bad_denominators(self) -> None:
        q = lambda value: (Fraction(value), Fraction(0))
        values = (Fraction(1), Fraction(1, 5), Fraction(6, 5), Fraction(4, 5))
        offsets = {
            (signed_value, Fraction(0))
            for value in values
            for signed_value in (value, -value)
        }
        # Construct a relation involving a denominator divisible by the sieve
        # modulus and verify that it is not pruned.
        self.assertIsNotNone(find_offset_configuration(offsets, modulus=5))

    def test_pure_cubic_circle_parametrization(self) -> None:
        self.assertIsNotNone(cubic_circle_data((1, 1, 0), 2))

    def test_small_pure_cubic_search_is_negative(self) -> None:
        self.assertIsNone(search_pure_cubic(2, 1, 1))

    def test_pythagorean_quartic_certificate(self) -> None:
        example = pythagorean_example()
        self.assertEqual(example["field_degree"], 4)
        self.assertTrue(example["distinct"])
        self.assertEqual(set(example["line_sums"]), {0})

    def test_bremner_real_quartic_certificate(self) -> None:
        example = bremner_real_example()
        self.assertEqual(example["field_degree"], 4)
        self.assertTrue(example["distinct"])
        self.assertEqual(len(set(example["line_sums"])), 1)


if __name__ == "__main__":
    unittest.main()
