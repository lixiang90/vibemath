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


r10 = load("fourhit_second_3plus1", "PAPER_CUBE_FOURHIT_3PLUS1_ROUND10.py")
cluster = load("fourhit_cluster_round09", "PAPER_CUBE_FOURHIT_CLUSTER_ROUND09.py")


class FourHitSecondThreePlusOneTests(unittest.TestCase):
    def test_exactly_the_two_frozen_models(self):
        models = cluster.all_model_data()
        selected = [
            model for model in models
            if tuple(model["cluster_key"]) == ("3+1", 1, -4, 3)
        ]
        got = {(tuple(m["indices"]), m["word"]) for m in selected}
        expected = {(indices, word) for indices, word, _ in r10.SELECTED_MODELS}
        self.assertEqual(got, expected)
        self.assertEqual(len(selected), 2)

    def test_curve_points_smoothness_and_tangent(self):
        self.assertEqual(r10.curve_value(r10.ORIGIN), 0)
        self.assertEqual(r10.curve_value(r10.GENERATOR), 0)
        self.assertTrue(r10.projectively_equal(
            r10.third_intersection(r10.ORIGIN, r10.ORIGIN), r10.GENERATOR
        ))
        # Partial derivatives 9X^2,-12Y^2,3Z^2 vanish together only at (0,0,0).
        self.assertTrue(all(coefficient != 0 for coefficient in (9, -12, 3)))

    def test_symbolic_mordell_map(self):
        self.assertNotEqual(r10.symbolic_map_identity(), 0)
        self.assertEqual(r10.map_to_mordell(r10.ORIGIN), (r10.Q[0], -r10.Q[1]))
        self.assertEqual(r10.map_to_mordell(r10.GENERATOR), r10.ec_add(r10.Q, r10.Q))

    def test_nagell_lutz_certificate(self):
        data = r10.certificate_data()["nagell_lutz"]
        self.assertEqual(data["discriminant"], -2**8*3**13)
        self.assertEqual(data["Q_y_squared"], 35**2)
        self.assertFalse(data["Q_y_squared_divides_discriminant"])

    def test_exact_chord_multiples(self):
        points = r10.multiples(7)
        self.assertEqual(len(set(points)), 7)
        for point in points:
            self.assertEqual(r10.curve_value(point), 0)

    def test_example_and_two_field_classes(self):
        ap = r10.progression(r10.GENERATOR)
        self.assertEqual(ap, (125, 8, -109, -226, -343))
        self.assertEqual({ap[i+1]-ap[i] for i in range(4)}, {-117})
        self.assertEqual(
            [r10.pure_cubic_class(v, 109) for v in ap],
            [0, 0, 1, None, 0],
        )
        self.assertEqual(
            [r10.pure_cubic_class(v, 226) for v in ap],
            [0, 0, None, 1, 0],
        )

    def test_stored_certificate(self):
        stored = json.loads(r10.CERTIFICATE.read_text(encoding="utf-8"))
        self.assertEqual(stored, r10.certificate_data())


if __name__ == "__main__":
    unittest.main()
