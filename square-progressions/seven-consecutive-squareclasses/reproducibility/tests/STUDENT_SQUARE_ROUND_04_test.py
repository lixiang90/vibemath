import hashlib
import json
import unittest
from fractions import Fraction

import STUDENT_SQUARE_ROUND_02_patterns as round2
import STUDENT_SQUARE_ROUND_03_isomorphisms as round3
import STUDENT_SQUARE_ROUND_04_pipeline as round4


class RoundFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = round4.build_certificate()
        cls.rank_text, cls.point_text = round4.simulated_csv(cls.certificate)
        cls.ranks = round4.parse_rank_csv(cls.rank_text, cls.certificate)
        cls.points = round4.parse_point_csv(cls.point_text, cls.certificate)

    def test_twelve_distinct_j_invariants_and_discriminants(self):
        records = self.certificate["quartic_j_invariants"]
        self.assertEqual(len(records), 12)
        self.assertEqual(len({tuple(row["j_invariant"]) for row in records}), 12)
        for row in records:
            mask = row["representative_mask"]
            indices = tuple(i for i in range(7) if mask >> i & 1)
            polynomial_disc = round2.discriminant_for_roots(indices)
            self.assertEqual(row["27_times_binary_quartic_discriminant"], 27 * polynomial_disc)
            I, J = row["binary_quartic_I"], row["binary_quartic_J"]
            j = Fraction(*row["j_invariant"])
            self.assertEqual(j, Fraction(6912 * I**3, 4 * I**3 - J**2))

    def test_affine_and_pgl_partitions_equal_and_eleven_nonaffine(self):
        r3 = round3.build_certificate()
        affine = [sorted(row["members"]) for row in r3["affine_classes"]]
        pgl = [sorted(row["members"]) for row in r3["pgl2_Q_classes"]]
        self.assertEqual(affine, pgl)
        self.assertTrue(self.certificate["affine_and_pgl_member_partitions_equal"])
        transforms = self.certificate["nonaffine_transforms"]
        self.assertEqual(len(transforms), 11)
        self.assertEqual(self.certificate["nonaffine_transform_count"], 11)
        for transform in transforms:
            self.assertNotEqual(transform["matrix"][2], 0)
            self.assertFalse(transform["affine"])
            source_roots = set(round3.roots(transform["source_mask"]))
            target_roots = round3.roots(transform["target_mask"])
            images = {round3.apply_mobius(tuple(transform["matrix"]), root) for root in target_roots}
            self.assertEqual(images, source_roots)
            square = Fraction(*transform["sqrt_K"])
            self.assertEqual(square * square, Fraction(*transform["multiplier_K"]))

    def test_every_occurrence_has_its_own_u_m_and_exact_constraints(self):
        patterns = self.certificate["pattern_occurrences"]
        self.assertEqual(len(patterns), 284)
        self.assertEqual(sum(len(row["occurrences"]) for row in patterns), 284 * 15)
        for pattern in patterns:
            variables = [row["machine_variable"] for row in pattern["occurrences"]]
            self.assertEqual(len(variables), len(set(variables)))
            for occurrence in pattern["occurrences"]:
                self.assertEqual(occurrence["local_notation"], "u_m")
                self.assertIn("nonbranch", occurrence["nonbranch_constraint"])
                self.assertEqual(len(occurrence["t_numerator_homogeneous"]), 2)
                self.assertEqual(len(occurrence["t_denominator_homogeneous"]), 2)
                if occurrence["genus"] > 0:
                    a, b, c, d = occurrence["mobius_matrix_rep_to_occurrence"]
                    self.assertEqual(occurrence["t_numerator_homogeneous"], [a, b])
                    self.assertEqual(occurrence["t_denominator_homogeneous"], [c, d])
                    self.assertIn("!= 0", occurrence["finite_constraint"])

    def test_mapped_t_is_always_finite_and_nonbranch(self):
        for pattern in self.certificate["pattern_occurrences"]:
            for occurrence in pattern["occurrences"]:
                if occurrence["genus"] == 0:
                    continue
                for point in self.points[occurrence["class_id"]].points:
                    t = round4.mapped_t(point, occurrence)
                    if t is not None:
                        self.assertNotIn(t, {Fraction(-i) for i in range(7)})

    def test_strict_parsers_accept_complete_simulated_schema(self):
        self.assertEqual(set(self.ranks), set(range(16)))
        self.assertEqual(set(self.points), set(range(16)))
        self.assertTrue(all(record.rank_lo == record.rank_hi == 0 for record in self.ranks.values()))
        self.assertTrue(all(record.complete for record in self.points.values()))
        for class_id, record in self.points.items():
            mask = self.certificate["pgl2_Q_classes"][class_id]["representative_mask"]
            self.assertTrue(all(round4.projective_point_is_on_curve(mask, point) for point in record.points))

    def test_strict_rank_parser_rejects_bad_header_and_missing_class(self):
        with self.assertRaises(ValueError):
            round4.parse_rank_csv(self.rank_text.replace("rank_hi", "rank_upper", 1), self.certificate)
        lines = self.rank_text.splitlines()
        with self.assertRaises(ValueError):
            round4.parse_rank_csv("\n".join(lines[:-1]) + "\n", self.certificate)

    def test_strict_point_parser_rejects_bad_boolean_and_off_curve_point(self):
        with self.assertRaises(ValueError):
            round4.parse_point_csv(self.point_text.replace(",true,", ",yes,", 1), self.certificate)
        lines = self.point_text.splitlines()
        fields = lines[1].split(",")
        fields[4] = "1"  # A branch point with V=1 is off the curve.
        lines[1] = ",".join(fields)
        with self.assertRaises(ValueError):
            round4.parse_point_csv("\n".join(lines) + "\n", self.certificate)

    def test_simulated_rank0_torsion_pipeline_reaches_all_284_patterns(self):
        outcomes = round4.evaluate_same_t(self.certificate, self.ranks, self.points)
        self.assertEqual(len(outcomes), 284)
        self.assertEqual(
            {row["status"] for row in outcomes},
            {"excluded_by_complete_same_t_intersection"},
        )
        self.assertIn("fixtures, not Magma results", self.certificate["simulation_warning"])

    def test_stored_json_body_and_hash(self):
        with round4.CERTIFICATE_PATH.open(encoding="utf-8") as stream:
            stored = json.load(stream)
        self.assertEqual(stored, json.loads(json.dumps(self.certificate)))
        claimed = stored.pop("sha256_without_this_field")
        canonical = json.dumps(stored, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), claimed)


if __name__ == "__main__":
    unittest.main()
