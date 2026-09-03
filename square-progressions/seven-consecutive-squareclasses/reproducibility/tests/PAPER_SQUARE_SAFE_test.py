import json
import unittest
from pathlib import Path

import sympy as sp

import PAPER_SQUARE_SAFE_inventory as S
import STUDENT_SQUARE_ROUND_02_patterns as R2


class SafeInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=S.build_certificate()

    def test_sixteen_representatives(self):
        reps=self.c["representative_classes"]
        self.assertEqual(len(reps),16)
        self.assertEqual([z["representative_mask"] for z in reps],
                         [15,23,27,39,43,45,51,71,75,77,83,99,63,95,111,119])

    def test_integral_models(self):
        t=sp.symbols("t")
        for z in self.c["representative_classes"]:
            f=sp.Poly.from_list(z["coefficients_descending"],gens=t)
            self.assertEqual(sp.expand(f.as_expr()),sp.expand(sp.prod(t+i for i in z["support"])))
            self.assertEqual(z["genus"],1 if z["degree"]==4 else 2)

    def test_discriminants_and_bad_support(self):
        for z in self.c["representative_classes"]:
            self.assertEqual(set(z["candidate_bad_primes"])-{2,3,5},set())
            fac={int(k):v for k,v in z["discriminant_factorization"].items()}
            self.assertEqual(sp.prod(k**v for k,v in fac.items()),z["polynomial_discriminant"])

    def test_quartic_j_coverage(self):
        q=[z for z in self.c["representative_classes"] if z["degree"]==4]
        self.assertEqual(len(q),12)
        self.assertTrue(all(z["j_invariant"] is not None for z in q))
        self.assertEqual(len({tuple(z["j_invariant"]) for z in q}),12)

    def test_all_windows_span(self):
        a=self.c["window_rank_audit"]
        self.assertEqual(a["both_six_windows_affinely_span_F2_squared"],284)
        self.assertTrue(all((z["first_six_affine_rank"],z["last_six_affine_rank"],z["all_seven_affine_rank"])==(2,2,2) for z in a["rows"]))

    def test_2026_is_conditional_only(self):
        a=self.c["theorem_2026_scope"]
        self.assertEqual((a["conditionally_in_scope_patterns"],a["hypotheses_verified_from_labels_alone"],a["unconditionally_excluded_by_2026_citations"]),(284,0,0))

    def test_consecutive_four_identity(self):
        x=sp.symbols("x")
        self.assertEqual(sp.expand(x*(x+1)*(x+2)*(x+3)-((x*(x+3)+1)**2-1)),0)
        # (n+1-y)(n+1+y)=1 over Z has only factor pairs (1,1),(-1,-1).
        self.assertEqual(self.c["consecutive_four_character_theorem"]["integral_x_solutions"],[-3,-2,-1,0])

    def test_strict_subfamily_counts(self):
        a=self.c["consecutive_four_character_theorem"]
        self.assertEqual((a["strictly_excluded_pattern_count"],a["remaining_pattern_count"]),(186,98))
        self.assertEqual(set(a["strictly_excluded_pattern_ids"]) & set(a["remaining_pattern_ids"]),set())
        self.assertEqual(set(a["strictly_excluded_pattern_ids"]) | set(a["remaining_pattern_ids"]),set(range(284)))

    def test_end_to_end_rgs_kernels_and_77_89(self):
        audit=self.c["self_contained_enumeration"]
        self.assertEqual(
            (audit["raw_unlabelled_partitions_3_or_4_blocks"],
             audit["reflection_fixed_before_screen"],
             audit["reflection_orbits_before_screen"]),
            (651,35,343),
        )
        self.assertEqual(
            (audit["strictly_excluded_raw"],
             audit["strictly_excluded_reflection_orbits"],
             audit["surviving_raw"],
             audit["reflection_fixed_after_screen"],
             audit["surviving_reflection_orbits"]),
            (109,59,542,26,284),
        )
        self.assertEqual((audit["kernel_rows_recomputed_exactly"],audit["nonzero_characters_per_row"],audit["total_nonzero_character_occurrences"]),(284,15,4260))
        r4=json.loads(Path("STUDENT_SQUARE_ROUND_04_CERTIFICATE.json").read_text(encoding="utf-8"))
        for row in r4["pattern_occurrences"]:
            expected=set(R2.relation_space(tuple(row["partition"]))) - {0}
            actual={item["character_mask_m"] for item in row["occurrences"]}
            self.assertEqual(actual,expected)
        m=self.c["mask_77_89_affine_reflection"]
        self.assertEqual((m["remaining_patterns_with_77"],m["remaining_patterns_with_89"],m["overlap"],m["union"]),(26,25,7,44))
        u=sp.symbols("u")
        tt=-u-6
        self.assertEqual(sp.expand(tt*(tt+3)*(tt+4)*(tt+6)-u*(u+2)*(u+3)*(u+6)),0)

    def test_disk(self):
        self.assertEqual(json.loads(Path("PAPER_SQUARE_SAFE_CERTIFICATE.json").read_text(encoding="utf-8")),self.c)


if __name__=="__main__":
    unittest.main(verbosity=2)
