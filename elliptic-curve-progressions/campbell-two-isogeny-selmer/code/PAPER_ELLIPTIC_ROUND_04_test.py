import json
import unittest

import PAPER_ELLIPTIC_ROUND_04_analysis as audit


class CampbellRound04Tests(unittest.TestCase):
    def test_quadratic_field_structure(self):
        data = audit.quadratic_field_and_z_certificate()
        self.assertEqual(data["field"]["D_factorization"], {"59": 1, "71699": 1, "339106321": 1})
        self.assertEqual(data["quadratic_resolvent_factor"]["phi_plus_coefficients_in_basis_1_w"], [-134689011712, 6144])

    def test_both_z_components_and_norms(self):
        data = audit.quadratic_field_and_z_certificate()
        self.assertEqual(data["z_components"]["Q"]["square_equivalent_representative"], 35)
        self.assertEqual(data["z_components"]["K"]["square_equivalent_reduced_coefficients"], [114071137835762, -1700158])
        self.assertEqual(data["z_components"]["K"]["norm_squareclass"], 35)
        self.assertTrue(data["full_etale_norm"]["is_square"])

    def test_weierstrass_scaling_and_translation(self):
        data = audit.scaling_certificate()
        self.assertEqual(data["weierstrass_scaling"]["u"], 64)
        self.assertEqual(data["translated_E"]["a"], -591895071)
        self.assertEqual(data["translated_E"]["b"], 58536289153843200)

    def test_exact_selmer_groups(self):
        data = audit.isogeny_selmer_certificate()["exact_selmer_groups"]
        self.assertEqual(data["E_side_F2_dimension"], 3)
        self.assertEqual(data["E_prime_side_F2_dimension"], 2)
        self.assertEqual(data["rank_upper_bound"], 3)
        self.assertTrue(audit.is_subgroup(data["E_side_classes"]))
        self.assertTrue(audit.is_subgroup(data["E_prime_side_classes"]))

    def test_good_prime_bridge_covers_all_unchecked_places(self):
        data = audit.isogeny_selmer_certificate()
        self.assertEqual(data["good_prime_lemma"]["S"], ["infinity", 2, 3, 5, 7, 59, 71699, 339106321])
        self.assertTrue(data["good_prime_lemma"]["all_S_places_checked"])
        self.assertEqual(data["support_lemma"]["number_of_signed_candidate_classes_on_each_side"], 32)
        self.assertEqual(data["good_prime_lemma"]["quartic_polynomial_discriminant"], "16*b*(a^2-4*b)^2")

    def test_known_kummer_images_only(self):
        data = audit.known_mordell_weil_images()
        self.assertEqual(data["proved_MW_image_subgroups"]["E"], [1, 7])
        self.assertEqual(data["proved_MW_image_subgroups"]["E_prime"], [1, audit.D_FIELD])
        self.assertIn("not proved Sha", data["unexplained_selmer_cosets_not_yet_Sha"]["warning"])

    def test_clean_certificate_excludes_superseded_pairing_fields(self):
        data = audit.build_certificate()
        self.assertEqual(data["schema"], "paper-elliptic-campbell-round-04-clean-v2")
        self.assertNotIn("d35_cassels_tate_setup", data)
        serialized = json.dumps(data)
        self.assertNotIn("<35,4230241>", serialized)
        self.assertNotIn("<35,339106321>", serialized)
        self.assertEqual(
            data["supersession"]["negative_audit"],
            "ct_formula_rejection.json",
        )

    def test_disk_certificate_matches(self):
        expected = audit.build_certificate()
        with audit.CERTIFICATE_PATH.open(encoding="utf-8") as handle:
            actual = json.load(handle)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
