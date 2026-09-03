import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "round09", HERE / "PAPER_CUBE_FOURHIT_CLUSTER_ROUND09.py"
)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class Round09ClusterTests(unittest.TestCase):
    def test_complete_29_partition(self):
        models = r.current_models()
        self.assertEqual(len(models), 29)
        self.assertTrue(r.SOLVED_BEFORE_ROUND09.isdisjoint(models))
        counts = {}
        for _, word in models:
            kind = r.multiplicity_type(word)
            counts[kind] = counts.get(kind, 0) + 1
        self.assertEqual(counts, {"3+1": 4, "2+2": 9, "2+1+1": 16})

    def test_every_model_has_exact_curve_and_genus(self):
        for model in r.all_model_data():
            curve = model["curve"]
            self.assertIn(curve["genus"], (1, 4))
            if model["multiplicity_type"] == "3+1":
                c = curve["coefficient_vector"]
                self.assertEqual(sum(c), 0)
                self.assertEqual(curve["genus"], 1)
            elif model["multiplicity_type"] == "2+2":
                matrix = curve["coefficient_matrix_rows_XY_columns_UV"]
                self.assertTrue(all(value != 0 for row in matrix for value in row))
                self.assertNotEqual(matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0], 0)
                self.assertTrue(curve["six_simple_branch_points"])
            else:
                a, b, c, w = curve["coefficient_vector_X6_X3Y3_Y6_W3"]
                self.assertNotEqual(a*c, 0)
                self.assertNotEqual(b*b-4*a*c, 0)
                self.assertLess(w, 0)
                self.assertTrue(curve["six_simple_branch_points"])

    def test_canonical_keys_are_realized_by_recorded_permutations(self):
        for model in r.all_model_data():
            curve = model["curve"]
            key = tuple(curve["canonical_permutation_key"])
            if model["multiplicity_type"] == "3+1":
                coeff = tuple(curve["coefficient_vector"])
                perm = tuple(curve["map_to_canonical_coordinate_permutation"])
                self.assertEqual(r.normalize_tuple(coeff[i] for i in perm), key)
            elif model["multiplicity_type"] == "2+2":
                matrix = tuple(tuple(row) for row in curve["coefficient_matrix_rows_XY_columns_UV"])
                action = curve["map_to_canonical_factor_action"]
                got = r.matrix_action(
                    matrix, action["transpose_factors"],
                    action["swap_first_factor"], action["swap_second_factor"]
                )
                self.assertEqual(r.normalize_tuple(got[0]+got[1]), key)
            else:
                coeff = tuple(curve["coefficient_vector_X6_X3Y3_Y6_W3"])
                if curve["map_to_canonical_coordinate_action"]["swap_X_Y"]:
                    coeff = (coeff[2], coeff[1], coeff[0], coeff[3])
                self.assertEqual(r.normalize_tuple(coeff), key)

    def test_two_new_models_reuse_the_positive_rank_cubic(self):
        families = r.new_family_data()
        self.assertTrue(families["base_symbolic_mordell_identity_recomputed"])
        self.assertEqual(
            families["translated_generator_image_3Q"],
            ["2838722167/174477681", "146917312265870/2304675688329"],
        )
        got = {(tuple(m["indices"]), tuple(map(int, m["word"]))) for m in families["models"]}
        self.assertEqual(got, r.NEWLY_SOLVED)
        all_orbits = [r.km.partial_color_orbit(i, w) for i, w in r.SOLVED_BEFORE_ROUND09 | r.NEWLY_SOLVED]
        for j, orbit in enumerate(all_orbits):
            for other in all_orbits[j+1:]:
                self.assertTrue(orbit.isdisjoint(other))

    def test_new_samples_and_boundaries(self):
        first, second = r.new_family_data()["models"]
        self.assertEqual(first["sample_AP"], ["-125", "-62", "1", "64", "127"])
        self.assertEqual((first["D"], first["singleton_scale"]), (62, "-1"))
        zero = first["zero_checks"]
        self.assertEqual(zero["A1=0"]["forced_linear_relation_over_Q"], "Z=-Y")
        self.assertEqual(zero["A1=0"]["forced_cube_relation"], "X^3=2Y^3")
        self.assertEqual(zero["A1=0"]["other_factor_dehomogenized_discriminant"], -3)
        self.assertEqual(zero["A4=0"]["equivalent_cube_relation"], "Z^3=2Y^3")
        X, Y, Z = r.sp.symbols("X Y Z")
        curve = 2*X**3 - 3*Y**3 + Z**3
        A1 = (Z**3 + Y**3) / 2
        A4 = 2*Y**3 - Z**3
        self.assertEqual(r.sp.factor(2*A1), (Z + Y)*(Z**2 - Z*Y + Y**2))
        self.assertEqual(r.sp.expand(curve.subs(Z, -Y)), 2*(X**3 - 2*Y**3))
        self.assertEqual(r.sp.expand(-A4), Z**3 - 2*Y**3)
        self.assertEqual(second["sample_AP"], ["127", "64", "1", "-62", "-125"])
        self.assertEqual((second["D"], second["singleton_scale"]), (127, "1"))
        for model in (first, second):
            values = list(map(int, model["sample_AP"]))
            self.assertTrue(all(values))
            self.assertEqual(len({values[i+1]-values[i] for i in range(4)}), 1)

    def test_stored_certificate(self):
        stored = json.loads(r.OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(stored, r.certificate_data())


if __name__ == "__main__":
    unittest.main()
