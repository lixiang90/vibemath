import hashlib
import json
import unittest
from fractions import Fraction

import STUDENT_SQUARE_ROUND_02_patterns as round2
import STUDENT_SQUARE_ROUND_03_isomorphisms as round3


def multiply_polynomials(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def transformed_numerator(mask, matrix):
    a, b, c, d = matrix
    polynomial = [Fraction(1)]
    for root in round3.roots(mask):
        polynomial = multiply_polynomials(
            polynomial,
            [Fraction(b) - root * d, Fraction(a) - root * c],
        )
    return polynomial


def monic_root_polynomial(mask):
    polynomial = [Fraction(1)]
    for root in round3.roots(mask):
        polynomial = multiply_polynomials(polynomial, [-root, Fraction(1)])
    return polynomial


class RoundThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generated = round3.build_certificate()

    def test_round_two_has_all_63_character_supports_and_bad_primes(self):
        certificate = round2.build_certificate((11, 13))
        quotients = certificate["unique_character_quotients"]
        self.assertEqual(len(quotients), 63)
        distribution = {}
        for row in quotients:
            distribution[row["genus"]] = distribution.get(row["genus"], 0) + 1
        self.assertEqual(distribution, {0: 21, 1: 35, 2: 7})
        bad = {p for row in quotients for p in row["candidate_bad_primes"]}
        self.assertEqual(bad, {2, 3, 5})

    def test_positive_genus_cover_class_counts(self):
        self.assertEqual(
            self.generated["counts"],
            {
                "quartic_masks": 35,
                "sextic_masks": 7,
                "positive_genus_masks": 42,
                "affine_cover_classes": 16,
                "pgl2_Q_cover_classes": 16,
            },
        )
        pgl = self.generated["pgl2_Q_classes"]
        self.assertEqual(sum(row["representative_mask"].bit_count() == 4 for row in pgl), 12)
        self.assertEqual(sum(row["representative_mask"].bit_count() == 6 for row in pgl), 4)
        self.assertEqual(
            {mask for row in pgl for mask in row["members"]},
            set(self.generated["quartic_masks"] + self.generated["sextic_masks"]),
        )

    def test_every_recorded_mobius_map_is_exact_over_Q(self):
        for class_row in self.generated["pgl2_Q_classes"]:
            representative = class_row["representative_mask"]
            target_polynomial = monic_root_polynomial(representative)
            for member, transform in zip(
                class_row["members"], class_row["maps_from_representative_to_member"]
            ):
                self.assertEqual(transform["source_mask"], member)
                self.assertEqual(transform["target_mask"], representative)
                numerator = transformed_numerator(member, tuple(transform["matrix"]))
                K = Fraction(*transform["multiplier_K"])
                self.assertEqual(numerator, [K * coefficient for coefficient in target_polynomial])
                square = Fraction(*transform["sqrt_K"])
                self.assertEqual(square * square, K)

    def test_padic_witness_formula(self):
        for witness in self.generated["padic_witnesses"]:
            prime = witness["prime"]
            m = witness["m"]
            t = Fraction(*witness["t"])
            self.assertEqual(t, Fraction(1, prime ** (2 * m)))
            self.assertTrue(witness["all_certified_squares_in_Qp"])
            for row in witness["checks"]:
                i = row["i"]
                self.assertEqual(Fraction(*row["t_plus_i"]), t + i)
                self.assertEqual(t + i, Fraction(row["unit"], prime ** (2 * m)))
                modulus = 8 if prime == 2 else prime
                self.assertEqual(row["unit"] % modulus, 1)

    def test_compatibility_records_have_four_basis_conditions(self):
        records = self.generated["pattern_compatibility"]
        self.assertEqual(len(records), 284)
        for row in records:
            self.assertEqual(len(row["basis_masks"]), 4)
            self.assertEqual(len(row["conditions"]), 4)

    def test_corrected_affine_formula_and_exact_blocks(self):
        # An injective phi preserves the three label blocks exactly.
        labels = (0, 1, 2, 0, 1, 2, 0)
        c, phi1, phi2 = 8, 1, 2
        classes = [c ^ (phi1 if label & 1 else 0) ^ (phi2 if label & 2 else 0) for label in labels]
        self.assertEqual(
            [[i for i, value in enumerate(classes) if value == classes[j]] for j in range(7)],
            [[i for i, label in enumerate(labels) if label == labels[j]] for j in range(7)],
        )
        # A rank-one phi merges labels 0 and 2, showing why injectivity is needed.
        merged = [c ^ (phi1 if label & 1 else 0) for label in labels]
        self.assertEqual(merged[0], merged[2])

    def test_stored_json_and_hash_are_recomputed(self):
        with round3.CERTIFICATE_PATH.open(encoding="utf-8") as stream:
            stored = json.load(stream)
        normalized_generated = json.loads(json.dumps(self.generated))
        self.assertEqual(stored, normalized_generated)
        claimed = stored.pop("sha256_without_this_field")
        canonical = json.dumps(stored, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), claimed)


if __name__ == "__main__":
    unittest.main()
