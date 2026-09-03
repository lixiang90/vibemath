"""Exact mask-90 gate on the ten patterns surviving mask 51.

The proof is a complete squarefree-kernel split.  No bounded search or
Mordell--Weil computation is used.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT.parent / "certificates" if ROOT.name == "code" else ROOT
MASK51_CERT = CERT_DIR / "PAPER_SQUARE_MASK51_CERTIFICATE.json"
ROUND4_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
ROUND2_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_02_certificate.json"
OUTPUT = CERT_DIR / "PAPER_SQUARE_MASK90_CERTIFICATE.json"
MASK = 90
SUPPORT = [1, 3, 4, 6]
INPUT_IDS = [12, 31, 43, 59, 134, 214, 230, 251, 276, 281]


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
    mask51 = json.loads(MASK51_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    ids = mask51["pattern_impact"]["remaining_pattern_ids"]
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
        (54, 3, 3), (45, 3, 6), (90, 3, 6), (27, 2, 3), (85, 2, 8)
    ]
    assert [row["occurrence_id"] for row in selected_occurrences] == [
        "P43:m90", "P251:m90", "P281:m90"
    ]
    assert all(row["representative_mask"] == 45 and row["class_id"] == 5 for row in selected_occurrences)
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
        "selected_curve": "y^2=(t+1)(t+3)(t+4)(t+6)",
        "selected_occurrences": selected_occurrences,
        "selection_note": "mask 90 was the specified Round-09 priority among the three masks tied at three affected patterns",
    }


def rhs(t: int) -> int:
    return (t + 1) * (t + 3) * (t + 4) * (t + 6)


def integral_point_certificate() -> dict[str, object]:
    middle = []
    points: list[list[int]] = []
    for t in range(-6, 0):
        value = rhs(t)
        ys = []
        if value >= 0:
            root = math.isqrt(value)
            if root * root == value:
                ys = [0] if root == 0 else [-root, root]
                points.extend([[t, y] for y in ys])
        middle.append({"t": t, "rhs": value, "ys": ys})
    expected = [[-6, 0], [-4, 0], [-3, 0], [-1, 0]]
    assert points == expected

    squares_mod_4 = sorted({x * x % 4 for x in range(4)})
    differences_mod_4 = sorted({(v - u) % 4 for u in squares_mod_4 for v in squares_mod_4})
    assert squares_mod_4 == [0, 1]
    assert 2 not in differences_mod_4
    assert 6 % 4 not in differences_mod_4

    branches = [
        {
            "d": 1,
            "equation": "V^2-U^2=6",
            "method": "modulo 4",
            "rhs_mod_4": 2,
            "square_differences_mod_4": differences_mod_4,
            "conclusion": "impossible",
        },
        {
            "d": 2,
            "equation": "V^2-U^2=3",
            "positive_same_parity_factor_pairs": [[1, 3]],
            "forced_U_V": [1, 2],
            "forced_A": 2,
            "transformed_equation": "(2t+7)^2=4A+25=33",
            "nonsquare_interval": [25, 33, 36],
            "conclusion": "impossible",
        },
        {
            "d": 3,
            "equation": "V^2-U^2=2",
            "method": "modulo 4",
            "rhs_mod_4": 2,
            "square_differences_mod_4": differences_mod_4,
            "conclusion": "impossible",
        },
        {
            "d": 6,
            "equation": "V^2-U^2=1",
            "positive_factor_pairs": [[1, 1]],
            "forced_U_V": [0, 1],
            "conclusion": "U=0 contradicts A>0",
        },
    ]
    return {
        "curve": "y^2=(t+1)(t+3)(t+4)(t+6)",
        "mask": MASK,
        "support": SUPPORT,
        "A": "(t+1)(t+6)",
        "B": "(t+3)(t+4)",
        "B_minus_A": 6,
        "gcd_identity": "gcd(A,B)=gcd(A,6), hence gcd(A,B) divides 6",
        "positive_regions": ["t<=-7", "t>=0"],
        "common_positive_squarefree_kernels": [1, 2, 3, 6],
        "kernel_equation": "d(V^2-U^2)=6",
        "branches": branches,
        "middle_interval_exact_check": middle,
        "proved_integral_points": expected,
        "nondegenerate_integral_points": [],
        "rational_y_is_integral_note": "an integer which is a rational square is an integer square",
        "bounded_search_used": False,
        "mordell_weil_used": False,
        "status": "PROVED_COMPLETE_BY_SQUAREFREE_KERNELS_AND_FINITE_SIGN_INTERVAL",
    }


def pattern_impact() -> dict[str, object]:
    rows = input_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == MASK for item in row["occurrences"]
    ))
    assert affected == [43, 251, 281]
    survivors = sorted(set(INPUT_IDS) - set(affected))
    assert survivors == [12, 31, 59, 134, 214, 230, 276]
    return {
        "input_remaining_count": 10,
        "selected_mask": MASK,
        "affected_pattern_ids": affected,
        "affected_partitions": [partition_string(i) for i in affected],
        "strictly_excluded": len(affected),
        "remaining_count": len(survivors),
        "remaining_pattern_ids": survivors,
        "remaining_partitions": [partition_string(i) for i in survivors],
        "reason": "mask 90 has no nondegenerate integral parameter",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-square-mask90-v1",
        "semantic_version": "1.0.0",
        "input_sha256": {
            MASK51_CERT.name: sha256(MASK51_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
            ROUND2_CERT.name: sha256(ROUND2_CERT),
        },
        "occurrence_inventory": occurrence_inventory(),
        "integral_points": integral_point_certificate(),
        "pattern_impact": pattern_impact(),
        "claim_boundary": {
            "proved": "the complete integer-point set for mask 90 and the resulting 10-to-7 necessary-pattern exclusion",
            "not_proved": "realizability or impossibility of any of the seven survivors; R_2(7) is not decided",
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
