"""Regression tests for the Round-11 exact isogeny-Selmer upgrade."""

from __future__ import annotations

import json
import unittest

import NEXT_ELLIPTIC_ROUND_11 as round11


class Round11IsogenySelmerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.built = round11.build_certificate()
        cls.disk = json.loads(round11.OUTPUT.read_text(encoding="utf-8"))

    def test_frozen_certificate_rebuilds_exactly(self):
        self.assertEqual(self.disk, self.built)

    def test_isogeny_and_cover_maps_are_symbolic_identities(self):
        audit = self.built["mapping_conventions"]
        self.assertTrue(audit["composition_x_coordinate_equals_doubling"])
        self.assertTrue(audit["cover_map_identity"])
        self.assertIn("alpha((x,y))=[x]", audit["Kummer_convention"])

    def test_support_and_all_places_are_exhaustive(self):
        support = self.built["support_and_places"]
        self.assertEqual(
            support["finite_places_requiring_checks"],
            [2, 3, 5, 7, 59, 71699, 339106321],
        )
        self.assertTrue(support["real_place_required"])
        self.assertTrue(support["all_other_finite_places_automatic"])

    def test_exact_selmer_sets(self):
        local = self.built["local_to_selmer"]
        self.assertEqual(
            local["E_side"]["classes"], [1, 3, 5, 7, 15, 21, 35, 105]
        )
        self.assertEqual(
            local["E_prime_side"]["classes"],
            [1, 4230241, 339106321, 1434501462453361],
        )
        self.assertTrue(local["every_surviving_class_everywhere_locally_soluble"])
        self.assertTrue(
            local["every_other_supported_class_has_a_uniform_proved_obstruction"]
        )

    def test_selmer_dimensions_and_generators(self):
        local = self.built["local_to_selmer"]
        self.assertEqual(local["E_side"]["F2_dimension"], 3)
        self.assertEqual(local["E_side"]["generators"], [3, 5, 7])
        self.assertEqual(local["E_prime_side"]["F2_dimension"], 2)
        self.assertEqual(
            local["E_prime_side"]["generators"], [4230241, 339106321]
        )

    def test_all_survivor_bad_place_witnesses_are_revalidated(self):
        local = self.built["local_to_selmer"]
        self.assertEqual(local["surviving_rows_checked_at_infinity"], 12)
        self.assertEqual(local["finite_positive_witnesses_revalidated"], 84)

    def test_rank_formula_is_only_an_upper_bound(self):
        rank = self.built["rank_bound"]
        self.assertEqual(rank["Selmer_size_product"], 32)
        self.assertEqual(rank["kernel_orders"], [2, 2])
        self.assertEqual(rank["rank_power_upper_bound"], 8)
        self.assertEqual(rank["rank_upper_bound"], 3)
        self.assertFalse(rank["exact_rank_claimed"])

    def test_claim_boundary_stays_fail_closed(self):
        boundary = self.built["claim_boundary"]
        text = " ".join(boundary["not_proved"])
        self.assertIn("exact Mordell-Weil rank", text)
        self.assertIn("full 2-Selmer", text)
        self.assertIn("rational ninth point", text)
        self.assertIn("independent second-CAS", text)


if __name__ == "__main__":
    unittest.main()
