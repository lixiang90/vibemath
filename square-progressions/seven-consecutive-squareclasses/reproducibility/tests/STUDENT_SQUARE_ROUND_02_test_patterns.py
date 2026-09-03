import unittest

from STUDENT_SQUARE_ROUND_02_patterns import (
    affine_rank_with_zero,
    build_certificate,
    canonical_partition,
    discriminant_for_roots,
    quotient_data,
    relation_basis,
    relation_space,
    restricted_growth_strings,
)


class RoundTwoPatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = build_certificate((11, 13))

    def test_stirling_count_651(self):
        count = sum(1 for k in (3, 4) for _ in restricted_growth_strings(7, k))
        self.assertEqual(count, 651)

    def test_certified_reduction_counts(self):
        self.assertEqual(
            self.certificate["counts"],
            {
                "raw_AGL_orbits_with_3_or_4_blocks": 651,
                "all_orbits_after_reflection": 343,
                "strictly_excluded_before_reflection": 109,
                "strictly_excluded_after_reflection": 59,
                "survive_before_reflection": 542,
                "unresolved_after_reflection": 284,
            },
        )

    def test_every_survivor_has_dimension_four_and_fifteen_characters(self):
        for row in self.certificate["unresolved_patterns_ranked"]:
            self.assertEqual(row["relation_dimension"], 4)
            self.assertEqual(len(row["quotients"]), 15)
            self.assertEqual(sum(row["genus_counts"].values()), 15)

    def test_relation_weights_and_genera(self):
        word = (0, 1, 2, 0, 1, 2, 0)
        relations = relation_space(word)
        self.assertEqual(len(relation_basis(relations)), 4)
        self.assertEqual(len(relations), 16)
        for mask in relations[1:]:
            self.assertIn(mask.bit_count(), (2, 4, 6))
            self.assertEqual(quotient_data(mask).genus, (mask.bit_count() - 2) // 2)

    def test_quartic_discriminant(self):
        self.assertEqual(discriminant_for_roots((0, 1, 2, 3)), 144)

    def test_all_zero_branches_have_rank_over_two(self):
        ranks = [affine_rank_with_zero([i - j for i in range(7)]) for j in range(7)]
        self.assertEqual(ranks, [3, 4, 3, 3, 3, 4, 3])

    def test_partition_canonicalization_forgets_names(self):
        self.assertEqual(canonical_partition((3, 3, 1, 2, 1)), (0, 0, 1, 2, 1))


if __name__ == "__main__":
    unittest.main()
