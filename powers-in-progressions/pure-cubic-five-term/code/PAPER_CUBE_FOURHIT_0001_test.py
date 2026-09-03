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


fh = load("fourhit", "PAPER_CUBE_FOURHIT_0001.py")
km = load("kummer5", "PAPER_CUBE_KUMMER5.py")


class FourHit0001Tests(unittest.TestCase):
    def test_selected_model_is_one_of_the_31(self):
        item = ((0, 1, 3, 4), (0, 0, 0, 1))
        self.assertIn(item, km.four_hit_orbit_representatives())
        self.assertEqual(km.four_hit_classification_gate()["arithmetic_point_classification_remaining"], 31)

    def test_curve_points_and_tangent(self):
        self.assertEqual(fh.curve_value(fh.ORIGIN), 0)
        self.assertEqual(fh.curve_value(fh.GENERATOR), 0)
        self.assertTrue(fh.projectively_equal(
            fh.third_intersection(fh.ORIGIN, fh.ORIGIN), fh.GENERATOR
        ))

    def test_symbolic_mordell_map(self):
        self.assertNotEqual(fh.symbolic_map_identity(), 0)
        self.assertEqual(fh.map_to_mordell(fh.ORIGIN), (fh.Q[0], -fh.Q[1]))
        self.assertEqual(fh.map_to_mordell(fh.GENERATOR), fh.ec_add(fh.Q, fh.Q))

    def test_nagell_lutz_certificate(self):
        data = fh.certificate_data()["nagell_lutz"]
        self.assertEqual(data["discriminant"], -2**4*3**13)
        self.assertFalse(data["Q_y_squared_divides_discriminant"])

    def test_exact_chord_multiples(self):
        points = fh.multiples(7)
        self.assertEqual(len(set(points)), 7)
        for point in points:
            self.assertEqual(fh.curve_value(point), 0)

    def test_progression_and_boundary(self):
        ap = fh.progression(fh.GENERATOR)
        self.assertEqual(ap, (64, 1, -62, -125, -188))
        self.assertEqual(len({ap[i+1]-ap[i] for i in range(4)}), 1)
        self.assertTrue(all(ap[i] != 0 for i in range(5)))
        # Counted entries: 4^3, 1^3, (-5)^3, and (-cuberoot(188))^3.
        self.assertEqual((ap[0], ap[1], ap[3], ap[4]), (4**3, 1, (-5)**3, -188))

    def test_stored_certificate(self):
        stored = json.loads(fh.CERTIFICATE.read_text(encoding="utf-8"))
        self.assertEqual(stored, fh.certificate_data())


if __name__ == "__main__":
    unittest.main()
