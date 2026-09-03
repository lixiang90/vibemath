import json
from itertools import product
from pathlib import Path
import unittest

import sympy as sp

import PAPER_CUBE_KUMMER5 as km


class PureCubicKummerFiveTests(unittest.TestCase):
    def test_kernel_symbolic_elimination(self):
        out = km.check_kernel_symbolics()
        self.assertEqual(out["kernel"], "{1,[D],[D]^2}")
        self.assertIn("B**3*D - 1", out["a_nonzero_resultant_C"])

    def test_radicand_normalization(self):
        self.assertEqual(km.canonical_pure_cubic_radicand(8), 1)
        self.assertEqual(km.canonical_pure_cubic_radicand(-12), 12)
        self.assertEqual(km.canonical_pure_cubic_radicand(18), 12)
        self.assertEqual(km.canonical_pure_cubic_radicand(km.Fraction(2, 9)), 6)

    def test_all_color_orbits_and_partition(self):
        reps = km.five_color_orbit_representatives()
        self.assertEqual(len(reps), 25)
        union = set().union(*(km.color_orbit(rep) for rep in reps))
        self.assertEqual(len(union), 3**5)
        mono, four_same, local = km.candidate_partition()
        self.assertEqual((len(mono), len(four_same), len(local)), (9, 1, 15))

    def test_burnside_fixed_point_counts(self):
        words = list(product(range(3), repeat=5))
        counts = []
        for reverse in (False, True):
            for slope in (1, 2):
                for shift in range(3):
                    fixed = 0
                    for word in words:
                        transformed = tuple((slope*c + shift) % 3 for c in word)
                        if reverse:
                            transformed = transformed[::-1]
                        fixed += transformed == word
                    counts.append(fixed)
        self.assertEqual(sorted(counts, reverse=True), [243, 27, 9, 9, 9, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(sum(counts) // len(counts), 25)

    def test_good_prime_jacobian_minors(self):
        u0, u1, u2, u3, u4 = sp.symbols("u0 u1 u2 u3 u4")
        jac = sp.Matrix([
            [u0, -2*u1, u2, 0, 0],
            [0, u1, -2*u2, u3, 0],
            [0, 0, u2, -2*u3, u4],
        ])
        cases = {
            None: ((0, 1, 2), u0*u1*u2),
            0: ((1, 2, 4), 3*u1*u2*u4),
            1: ((0, 2, 4), -2*u0*u2*u4),
            2: ((0, 1, 4), u0*u1*u4),
            3: ((0, 1, 4), u0*u1*u4),
            4: ((0, 1, 3), -2*u0*u1*u3),
        }
        for zero_index, (columns, expected) in cases.items():
            matrix = jac if zero_index is None else jac.subs([u0, u1, u2, u3, u4][zero_index], 0)
            self.assertEqual(sp.expand(matrix[:, columns].det() - expected), 0)

    def test_four_hit_classification_gate_is_fail_closed(self):
        out = km.four_hit_classification_gate()
        self.assertEqual(out["all_four_hit_color_position_orbits"], 38)
        self.assertEqual(out["arithmetic_point_classification_remaining"], 31)
        self.assertIn("NOT_CLASSIFIED", out["status"])

    def test_all_sixty_good_prime_obstructions(self):
        rows = km.local_obstruction_table()
        self.assertEqual(len(rows), 60)
        for row in rows:
            word = tuple(map(int, row["word"]))
            self.assertEqual(km.math.gcd(row["prime"], 3*row["D"]), 1)
            summary = row["finite_field_count"]
            self.assertEqual(summary["parameter_pairs_scanned"], row["prime"]**2-1)
            self.assertEqual(summary["compatible_parameter_pairs"], 0)
            self.assertEqual(
                sum(summary["first_failure_counts_by_position"]),
                summary["parameter_pairs_scanned"],
            )
            self.assertTrue(summary["count_identity_verified"])
            self.assertTrue(all(summary["good_prime_conditions"].values()))
            self.assertFalse(km.has_nonzero_projective_point_mod_p(
                word, row["D"], row["prime"]
            ))

    def test_stored_certificate_matches_live_data(self):
        stored = json.loads(
            (Path(__file__).resolve().parent / "PAPER_CUBE_KUMMER5_CERTIFICATE.json").read_text()
        )
        live = km.build_certificate()
        # Normalize tuples to their canonical JSON array representation before
        # requiring byte-content equivalence at the data-model level.
        self.assertEqual(stored, json.loads(json.dumps(live, sort_keys=True)))

    def test_nonzero_lower_witness(self):
        witness = km.verify_lower_witness()
        self.assertNotIn(0, witness["AP"])
        self.assertEqual(witness["counted_positions"], [0, 1, 2, 3])


if __name__ == "__main__":
    unittest.main()
