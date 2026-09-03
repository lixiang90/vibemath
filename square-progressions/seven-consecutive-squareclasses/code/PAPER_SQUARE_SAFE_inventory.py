"""Strict inventory for the integral R_2(7) safety project.

Consumes the audited Round-03/04 structural certificates.  It makes no CAS
rank or rational-point completeness claim.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import STUDENT_SQUARE_ROUND_02_patterns as R2

R3 = Path("STUDENT_SQUARE_ROUND_03_CERTIFICATE.json")
R4 = Path("STUDENT_SQUARE_ROUND_04_CERTIFICATE.json")
OUT = Path("PAPER_SQUARE_SAFE_CERTIFICATE.json")
t = sp.symbols("t")

AUDIT_INPUTS = [
    Path("STUDENT_SQUARE_ROUND_02_patterns.py"),
    Path("STUDENT_SQUARE_ROUND_02_certificate.json"),
    Path("STUDENT_SQUARE_ROUND_03_isomorphisms.py"),
    R3,
    Path("STUDENT_SQUARE_ROUND_04_pipeline.py"),
    R4,
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support(mask):
    return [i for i in range(7) if (mask >> i) & 1]


def affine_rank(labels):
    base = labels[0]
    vectors = [x ^ base for x in labels[1:]]
    basis = []
    for v in vectors:
        w = v
        for b in basis:
            w = min(w, w ^ b)
        if w:
            basis.append(w)
            basis.sort(reverse=True)
    return len(basis)


def relation_masks(labels):
    """Recompute ker(e -> (sum e_i, sum e_i*label_i)) from a partition."""
    out = []
    for mask in range(1 << 7):
        if mask.bit_count() % 2:
            continue
        label_sum = 0
        for i, label in enumerate(labels):
            if (mask >> i) & 1:
                label_sum ^= label
        if label_sum == 0:
            out.append(mask)
    return out


def build_certificate():
    r3 = json.loads(R3.read_text(encoding="utf-8"))
    r4 = json.loads(R4.read_text(encoding="utf-8"))

    # End-to-end enumeration, independent of the final 284-row certificate.
    raw = [
        word
        for blocks in (3, 4)
        for word in R2.restricted_growth_strings(7, blocks)
    ]
    all_reflection_reps = {R2.reflection_canonical(word) for word in raw}
    reflection_fixed = [
        word for word in raw
        if R2.canonical_partition(tuple(reversed(word))) == word
    ]
    strict_raw = [word for word in raw if R2.strict_pattern_reasons(word)]
    survivors_raw = [word for word in raw if not R2.strict_pattern_reasons(word)]
    strict_reps = {R2.reflection_canonical(word) for word in strict_raw}
    survivor_reps = {R2.reflection_canonical(word) for word in survivors_raw}
    survivor_fixed = [
        word for word in survivors_raw
        if R2.canonical_partition(tuple(reversed(word))) == word
    ]
    assert (len(raw), len(reflection_fixed), len(all_reflection_reps)) == (651, 35, 343)
    assert (len(strict_raw), len(strict_reps), len(survivors_raw), len(survivor_fixed), len(survivor_reps)) == (109, 59, 542, 26, 284)
    jmap = {z["representative_mask"]: z["j_invariant"] for z in r4["quartic_j_invariants"]}
    classes = []
    for cid, cl in enumerate(r3["pgl2_Q_classes"]):
        m = cl["representative_mask"]
        S = support(m)
        f = sp.Poly(sp.prod(t+i for i in S), t)
        degree = len(S)
        disc = abs(int(sp.discriminant(f.as_expr(), t)))
        primes = sorted(set([2]) | set(sp.factorint(disc)))
        occ = cl["affected_pattern_occurrences"]
        classes.append({
            "class_id": cid,
            "representative_mask": m,
            "members": cl["members"],
            "support": S,
            "normalized_primitive_integral_model": f"y^2={sp.sstr(f.as_expr())}",
            "coefficients_descending": [int(x) for x in f.all_coeffs()],
            "degree": degree,
            "genus": (degree-2)//2,
            "polynomial_discriminant": disc,
            "discriminant_factorization": {str(k): v for k,v in sp.factorint(disc).items()},
            "candidate_bad_primes": primes,
            "j_invariant": jmap.get(m),
            "occurrence_count": len(occ),
            "affected_pattern_count": len({z["pattern_id"] for z in occ}),
            "integral_point_entry": (
                "quartic genus-1: compute a proven Mordell-Weil group, then integral points/Thue equations"
                if degree == 4 else
                "sextic genus-2: 2-Selmer rank, Chabauty/Mordell-Weil sieve, then integral pullback"
            ),
        })

    window_rows = []
    all_proper = []
    for row in r3["pattern_compatibility"]:
        labels = row["partition"]
        ranks = [affine_rank(labels[:6]), affine_rank(labels[1:]), affine_rank(labels)]
        window_rows.append({"pattern_id": row["pattern_id"], "partition": labels,
                            "first_six_affine_rank": ranks[0],
                            "last_six_affine_rank": ranks[1], "all_seven_affine_rank": ranks[2]})
        if ranks == [2,2,2]:
            all_proper.append(row["pattern_id"])
    assert len(all_proper) == 284

    # Recompute every 15-character kernel and compare it with every occurrence.
    r4_by_partition = {tuple(row["partition"]): row for row in r4["pattern_occurrences"]}
    kernel_verified = 0
    for row in r3["pattern_compatibility"]:
        labels = row["partition"]
        kernel = relation_masks(labels)
        assert len(kernel) == 16
        occurrence_masks = {
            item["character_mask_m"]
            for item in r4_by_partition[tuple(labels)]["occurrences"]
        }
        assert occurrence_masks == set(kernel) - {0}
        kernel_verified += 1
    assert kernel_verified == 284

    consecutive_masks = {15,30,60,120}
    excluded, witnesses = [], {}
    for row in r4["pattern_occurrences"]:
        masks = {z["character_mask_m"] for z in row["occurrences"]}
        hit = sorted(masks & consecutive_masks)
        if hit:
            excluded.append(row["pattern_id"])
            witnesses[str(row["pattern_id"])] = hit
    remaining = sorted(set(range(284))-set(excluded))
    assert len(excluded) == 186 and len(remaining) == 98


    remaining_set = set(remaining)
    ids_77 = {
        row["pattern_id"] for row in r4["pattern_occurrences"]
        if row["pattern_id"] in remaining_set
        and any(item["character_mask_m"] == 77 for item in row["occurrences"])
    }
    ids_89 = {
        row["pattern_id"] for row in r4["pattern_occurrences"]
        if row["pattern_id"] in remaining_set
        and any(item["character_mask_m"] == 89 for item in row["occurrences"])
    }
    assert (len(ids_77), len(ids_89), len(ids_77 & ids_89), len(ids_77 | ids_89)) == (26, 25, 7, 44)

    return {
        "schema": "PAPER_SQUARE_SAFE-integral-pattern-inventory-v1",
        "source_sha256": {path.name: sha(path) for path in AUDIT_INPUTS},
        "scope_warning": "Structural and elementary integral exclusions only; no unverified 2026 hypothesis is treated as an exclusion.",
        "self_contained_enumeration": {
            "raw_unlabelled_partitions_3_or_4_blocks": len(raw),
            "reflection_fixed_before_screen": len(reflection_fixed),
            "reflection_orbits_before_screen": len(all_reflection_reps),
            "strictly_excluded_raw": len(strict_raw),
            "strictly_excluded_reflection_orbits": len(strict_reps),
            "surviving_raw": len(survivors_raw),
            "reflection_fixed_after_screen": len(survivor_fixed),
            "surviving_reflection_orbits": len(survivor_reps),
            "kernel_rows_recomputed_exactly": kernel_verified,
            "nonzero_characters_per_row": 15,
            "total_nonzero_character_occurrences": kernel_verified * 15,
        },
        "representative_classes": classes,
        "window_rank_audit": {
            "total_patterns": 284,
            "both_six_windows_affinely_span_F2_squared": len(all_proper),
            "rows": window_rows,
        },
        "theorem_2026_scope": {
            "conditionally_in_scope_patterns": 284,
            "hypotheses_verified_from_labels_alone": 0,
            "unconditionally_excluded_by_2026_citations": 0,
            "reason": "The three quadratic subfields (squareclasses D) depend on the unknown integer t, so rank/class-number hypotheses are not pattern invariants."
        },
        "consecutive_four_character_theorem": {
            "masks": sorted(consecutive_masks),
            "identity": "x(x+1)(x+2)(x+3)=(x(x+3)+1)^2-1",
            "integral_x_solutions": [-3,-2,-1,0],
            "strictly_excluded_pattern_count": len(excluded),
            "strictly_excluded_pattern_ids": excluded,
            "witness_masks_by_pattern": witnesses,
            "remaining_pattern_count": len(remaining),
            "remaining_pattern_ids": remaining,
        },
        "mask_77_89_affine_reflection": {
            "support_77": [0, 2, 3, 6],
            "support_89": [0, 3, 4, 6],
            "integer_preserving_map": "t=-u-6",
            "polynomial_identity": "t(t+3)(t+4)(t+6)=u(u+2)(u+3)(u+6)",
            "remaining_patterns_with_77": len(ids_77),
            "remaining_patterns_with_89": len(ids_89),
            "overlap": len(ids_77 & ids_89),
            "union": len(ids_77 | ids_89),
            "pattern_ids_77": sorted(ids_77),
            "pattern_ids_89": sorted(ids_89),
            "pattern_ids_union": sorted(ids_77 | ids_89),
        },
    }


def main():
    OUT.write_text(json.dumps(build_certificate(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
