import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fh = load("fourhit0010", "PAPER_CUBE_FOURHIT_0010.py")
km = load("kummer5_for_0010", "PAPER_CUBE_KUMMER5.py")


class FourHit0010Tests(unittest.TestCase):
    def test_selected_model_is_a_remaining_representative(self):
        item = (fh.INDICES, fh.COLORS)
        self.assertIn(item, km.four_hit_orbit_representatives())
        self.assertEqual(km.four_hit_classification_gate()["arithmetic_point_classification_remaining"], 31)

    def test_orbit_is_distinct_from_0001(self):
        new = fh.affine_color_orbit(fh.INDICES, fh.COLORS)
        old = fh.affine_color_orbit(fh.OLD_INDICES, fh.OLD_COLORS)
        self.assertTrue(new.isdisjoint(old))
        self.assertEqual(len(new), 12)
        self.assertEqual(len(old), 12)

    def test_exact_curve_derivation_and_progression(self):
        x, y, z = fh.GENERATOR
        self.assertEqual(2*x**3-3*y**3+z**3, 0)
        ap = fh.progression(fh.GENERATOR)
        self.assertEqual(ap[3], 3*ap[1]-2*ap[0])
        self.assertEqual(len({ap[i+1]-ap[i] for i in range(4)}), 1)

    def test_positive_rank_certificate_is_exact(self):
        self.assertEqual(fh.base.map_to_mordell(fh.ORIGIN), (fh.base.Q[0], -fh.base.Q[1]))
        self.assertEqual(
            fh.base.map_to_mordell(fh.GENERATOR),
            fh.base.ec_add(fh.base.Q, fh.base.Q),
        )
        disc = -2**4*3**13
        self.assertNotEqual(disc % (fh.base.Q[1]**2), 0)
        twice_q = fh.base.ec_add(fh.base.Q, fh.base.Q)
        three_q = fh.base.ec_add(twice_q, fh.base.Q)
        translated = fh.certificate_data()["translated_point_image"]
        self.assertEqual(translated["coordinates"], [str(v) for v in three_q])
        self.assertEqual(
            three_q,
            (fh.base.Fraction(2838722167, 174477681),
             fh.base.Fraction(146917312265870, 2304675688329)),
        )
        dep = fh.certificate_data()["inherited_mordell_identity_dependency"]
        self.assertEqual(dep["source"]["sha256"], fh.sha256(fh.BASE_SOURCE))
        self.assertEqual(dep["test"]["sha256"], fh.sha256(fh.BASE_TEST))
        self.assertEqual(dep["base_certificate"]["sha256"], fh.sha256(fh.BASE_CERTIFICATE))
        self.assertTrue(dep["cleared_identity_recomputed"])
        self.assertNotEqual(fh.base.symbolic_map_identity(), 0)

    def test_sample_pure_cubic_lift(self):
        ap = fh.progression(fh.GENERATOR)
        self.assertEqual(ap, (64, 1, -62, -125, -188))
        D, w = fh.cube_free_representative(ap[2])
        self.assertEqual((D, w), (62, -1))
        self.assertEqual(ap[2], D*w**3)
        self.assertTrue(all(ap[i] != 0 for i in range(5)))
        data = fh.boundary_data()
        entries = tuple(tuple(row) for row in data["entry_coefficient_vectors"])
        curve = tuple(data["curve_relation_vector"])
        self.assertEqual(
            tuple(entries[3][i]-3*entries[1][i]+2*entries[0][i]
                  for i in range(3)),
            curve,
        )
        self.assertEqual(tuple(data["A2_zero"]["coefficient_vector"]), (-1, 2, 0))
        self.assertEqual(data["A2_zero"]["cleared_equation"], {"X^3": 1, "Y^3": -2})
        self.assertEqual(data["A2_zero"]["implied_rational_ratio_cube"]["value"], "2")
        self.assertEqual(tuple(data["A4_zero"]["coefficient_vector"]), (-3, 4, 0))
        self.assertEqual(data["A4_zero"]["cleared_equation"], {"X^3": 3, "Y^3": -4})
        self.assertEqual(data["A4_zero"]["implied_rational_ratio_cube"]["value"], "4/3")
        fifth = data["fifth_hit"]
        self.assertEqual(fifth["extended_color_words"], ["00100", "00101", "00102"])
        self.assertEqual(
            set(fifth["known_indices"] + [fifth["remaining_index"]]), set(range(5))
        )
        self.assertEqual(fifth["hit_count_if_condition_holds"], 5)
        self.assertGreater(fifth["hit_count_if_condition_holds"], fifth["proved_upper_bound"])
        self.assertTrue(fifth["contradiction"])

    def test_cube_free_normalization_exact(self):
        from fractions import Fraction
        samples = (
            (Fraction(-62), 62, Fraction(-1)),
            (Fraction(16, 27), 2, Fraction(2, 3)),
            (Fraction(-125), 1, Fraction(-5)),
        )
        for value, D, w in samples:
            got_D, got_w = fh.cube_free_representative(value)
            self.assertEqual(got_D, D)
            self.assertEqual(got_w, w)

    def test_stored_certificate(self):
        stored = json.loads(fh.CERTIFICATE.read_text(encoding="utf-8"))
        self.assertEqual(stored, fh.certificate_data())


if __name__ == "__main__":
    unittest.main()
