"""Exact mask-54 gate on the seven patterns surviving mask 90.

The integral-point proof is both a bijective integer translation of the
already certified mask-108 curve and an independent squarefree-kernel split.
No bounded search or Mordell--Weil computation is used.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT.parent / "certificates" if ROOT.name == "code" else ROOT
MASK90_CERT = CERT_DIR / "PAPER_SQUARE_MASK90_CERTIFICATE.json"
MASK108_CERT = CERT_DIR / "PAPER_SQUARE_MASK108_CERTIFICATE.json"
ROUND4_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
ROUND2_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_02_certificate.json"
OUTPUT = CERT_DIR / "PAPER_SQUARE_MASK54_CERTIFICATE.json"
MASK = 54
SUPPORT = [1, 2, 4, 5]
INPUT_IDS = [12, 31, 59, 134, 214, 230, 276]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support(mask: int) -> list[int]:
    return [i for i in range(7) if (mask >> i) & 1]


def constant_pairing(mask: int) -> dict[str, object] | None:
    roots = support(mask)
    if len(roots) != 4:
        return None
    first = roots[0]
    for mate in roots[1:]:
        left = (first, mate)
        right = tuple(x for x in roots if x not in left)
        if sum(left) == sum(right):
            return {
                "left": list(left),
                "right": list(right),
                "difference_right_minus_left": right[0] * right[1] - left[0] * left[1],
            }
    return None


def input_rows() -> list[dict[str, object]]:
    mask90 = json.loads(MASK90_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    ids = mask90["pattern_impact"]["remaining_pattern_ids"]
    assert ids == INPUT_IDS
    wanted = set(ids)
    rows = [row for row in round4["pattern_occurrences"] if row["pattern_id"] in wanted]
    assert [row["pattern_id"] for row in rows] == INPUT_IDS
    for row in rows:
        masks = [item["character_mask_m"] for item in row["occurrences"]]
        assert len(masks) == len(set(masks)) == 15
    return rows


def partition_string(pattern_id: int) -> str:
    round2 = json.loads(ROUND2_CERT.read_text(encoding="utf-8"))
    row = round2["unresolved_patterns_ranked"][pattern_id]
    return "".join(str(x) for x in row["partition"])


def occurrence_inventory() -> dict[str, object]:
    rows = input_rows()
    hit_ids: dict[int, set[int]] = defaultdict(set)
    genus: dict[int, int] = {}
    counter: Counter[int] = Counter()
    selected_occurrences = []
    for row in rows:
        for item in row["occurrences"]:
            mask = item["character_mask_m"]
            counter[mask] += 1
            hit_ids[mask].add(row["pattern_id"])
            genus[mask] = item["genus"]
            if mask == MASK:
                selected_occurrences.append({
                    key: item[key]
                    for key in (
                        "occurrence_id",
                        "character_mask_m",
                        "genus",
                        "representative_mask",
                        "class_id",
                        "mobius_matrix_rep_to_occurrence",
                        "same_t_map",
                        "finite_constraint",
                        "nonbranch_constraint",
                    )
                })

    pairable = []
    for mask in sorted(hit_ids):
        pairing = constant_pairing(mask)
        if genus[mask] == 1 and pairing is not None:
            pairable.append({
                "mask": mask,
                "support": support(mask),
                "patterns_hit": len(hit_ids[mask]),
                "pattern_ids": sorted(hit_ids[mask]),
                "constant_pairing": pairing,
                "gcd_bound": abs(pairing["difference_right_minus_left"]),
            })
    pairable.sort(key=lambda row: (-row["patterns_hit"], row["gcd_bound"], row["mask"]))
    assert [(row["mask"], row["patterns_hit"], row["gcd_bound"]) for row in pairable] == [
        (54, 3, 3), (27, 2, 3), (45, 2, 6), (85, 2, 8)
    ]
    assert [row["occurrence_id"] for row in selected_occurrences] == [
        "P59:m54", "P214:m54", "P230:m54"
    ]
    assert all(row["representative_mask"] == 27 and row["class_id"] == 2
               for row in selected_occurrences)
    return {
        "authoritative_input_pattern_ids": INPUT_IDS,
        "input_pattern_count": len(rows),
        "characters_per_pattern": 15,
        "total_character_occurrences": len(rows) * 15,
        "distinct_masks": len(counter),
        "distinct_genus1_masks": sum(1 for mask in counter if genus[mask] == 1),
        "pairable_genus1_ranking": pairable,
        "selected_mask": MASK,
        "selected_support": SUPPORT,
        "selected_curve": "y^2=(t+1)(t+2)(t+4)(t+5)",
        "selected_occurrences": selected_occurrences,
        "selection_note": "mask 54 uniquely maximizes affected patterns among the remaining pairable genus-one masks",
    }


def rhs(t: int) -> int:
    return (t + 1) * (t + 2) * (t + 4) * (t + 5)


def mask108_rhs(s: int) -> int:
    return (s + 2) * (s + 3) * (s + 5) * (s + 6)


def translation_certificate() -> dict[str, object]:
    source = json.loads(MASK108_CERT.read_text(encoding="utf-8"))["integral_points"]
    source_points = source["proved_integral_points"]
    assert source_points == [[-6, 0], [-5, 0], [-4, -2], [-4, 2], [-3, 0], [-2, 0]]
    target_points = [[s + 1, y] for s, y in source_points]
    assert target_points == [[-5, 0], [-4, 0], [-3, -2], [-3, 2], [-2, 0], [-1, 0]]
    return {
        "source_mask": 108,
        "source_curve": "Y^2=(s+2)(s+3)(s+5)(s+6)",
        "target_mask": MASK,
        "target_curve": "y^2=(t+1)(t+2)(t+4)(t+5)",
        "forward_map_source_to_target": "(s,Y) -> (t,y)=(s+1,Y)",
        "inverse_map_target_to_source": "(t,y) -> (s,Y)=(t-1,y)",
        "factorwise_identity": "(s+2,s+3,s+5,s+6)=(t+1,t+2,t+4,t+5) when s=t-1",
        "parameter_domains": "Z bijectively maps to Z; y is unchanged",
        "source_points": source_points,
        "mapped_target_points": target_points,
        "source_certificate_sha256": sha256(MASK108_CERT),
    }


def integral_point_certificate() -> dict[str, object]:
    middle = []
    points: list[list[int]] = []
    for t in range(-5, 0):
        value = rhs(t)
        ys = []
        if value >= 0:
            root = math.isqrt(value)
            if root * root == value:
                ys = [0] if root == 0 else [-root, root]
                points.extend([[t, y] for y in ys])
        middle.append({"t": t, "rhs": value, "ys": ys})
    expected = [[-5, 0], [-4, 0], [-3, -2], [-3, 2], [-2, 0], [-1, 0]]
    assert points == expected

    squares_mod_8 = sorted({x * x % 8 for x in range(8)})
    assert squares_mod_8 == [0, 1, 4]
    assert 5 not in squares_mod_8
    branches = [
        {
            "d": 1,
            "equation": "V^2-U^2=3",
            "positive_same_parity_factor_pairs": [[1, 3]],
            "forced_U_V": [1, 2],
            "forced_A": 1,
            "transformed_equation": "(t+3)^2=A+4=5",
            "method": "impossible modulo 8",
            "squares_mod_8": squares_mod_8,
            "conclusion": "impossible",
        },
        {
            "d": 3,
            "equation": "V^2-U^2=1",
            "nonnegative_factor_pairs": [[1, 1]],
            "forced_U_V": [0, 1],
            "conclusion": "U=0 contradicts A>0",
        },
    ]
    degeneracy = [
        {"point": point, "zero_position_in_original_block": -point[0]}
        for point in expected
    ]
    assert all(0 <= row["zero_position_in_original_block"] <= 6 for row in degeneracy)
    return {
        "curve": "y^2=(t+1)(t+2)(t+4)(t+5)",
        "mask": MASK,
        "support": SUPPORT,
        "translation_to_mask108": translation_certificate(),
        "A": "(t+1)(t+5)",
        "B": "(t+2)(t+4)",
        "B_minus_A": 3,
        "gcd_identity": "gcd(A,B)=gcd(A,3), hence gcd(A,B) divides 3",
        "positive_regions": ["t<=-6", "t>=0"],
        "common_positive_squarefree_kernels": [1, 3],
        "kernel_equation": "d(V^2-U^2)=3",
        "branches": branches,
        "middle_interval_exact_check": middle,
        "proved_integral_points": expected,
        "degeneracy_in_original_seven_term_block": degeneracy,
        "nondegenerate_integral_points": [],
        "rational_y_is_integral_note": "an integer which is a rational square is an integer square",
        "bounded_search_used": False,
        "mordell_weil_used": False,
        "status": "PROVED_COMPLETE_BY_INTEGER_TRANSLATION_AND_INDEPENDENT_SQUAREFREE_KERNELS",
    }


def pattern_impact() -> dict[str, object]:
    rows = input_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == MASK for item in row["occurrences"]
    ))
    assert affected == [59, 214, 230]
    survivors = sorted(set(INPUT_IDS) - set(affected))
    assert survivors == [12, 31, 134, 276]
    return {
        "input_remaining_count": 7,
        "selected_mask": MASK,
        "affected_pattern_ids": affected,
        "affected_partitions": [partition_string(i) for i in affected],
        "strictly_excluded": len(affected),
        "remaining_count": len(survivors),
        "remaining_pattern_ids": survivors,
        "remaining_partitions": [partition_string(i) for i in survivors],
        "same_parameter_reason": "each listed row contains mask 54 at its original normalized parameter t; the curve has no nondegenerate integral t",
        "reason": "mask 54 has no nondegenerate integral parameter",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-square-mask54-v1",
        "semantic_version": "1.0.0",
        "input_sha256": {
            MASK90_CERT.name: sha256(MASK90_CERT),
            MASK108_CERT.name: sha256(MASK108_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
            ROUND2_CERT.name: sha256(ROUND2_CERT),
        },
        "occurrence_inventory": occurrence_inventory(),
        "integral_points": integral_point_certificate(),
        "pattern_impact": pattern_impact(),
        "claim_boundary": {
            "proved": "the complete integer-point set for mask 54 and the resulting 7-to-4 necessary-pattern exclusion",
            "not_proved": "realizability or impossibility of any of the four survivors; R_2(7) is not decided",
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
