"""Exact mask-99 gate on the final 23 squareclass patterns.

No bounded search is used.  The integral-point list follows from the constant
difference pairing t(t+6), (t+1)(t+5)=t(t+6)+5.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT.parent / "certificates" if ROOT.name == "code" else ROOT
MASK108_CERT = CERT_DIR / "PAPER_SQUARE_MASK108_CERTIFICATE.json"
ROUND4_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
OUTPUT = CERT_DIR / "PAPER_SQUARE_MASK99_CERTIFICATE.json"
MASK = 99
SUPPORT = [0, 1, 5, 6]


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


def final_rows() -> list[dict[str, object]]:
    mask108 = json.loads(MASK108_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    ids = set(mask108["pattern_impact"]["remaining_pattern_ids"])
    rows = [row for row in round4["pattern_occurrences"] if row["pattern_id"] in ids]
    assert len(rows) == len(ids) == 23
    for row in rows:
        masks = [item["character_mask_m"] for item in row["occurrences"]]
        assert len(masks) == len(set(masks)) == 15
    return rows


def occurrence_inventory() -> dict[str, object]:
    rows = final_rows()
    pattern_ids: dict[int, set[int]] = defaultdict(set)
    genus: dict[int, int] = {}
    for row in rows:
        for item in row["occurrences"]:
            mask = item["character_mask_m"]
            pattern_ids[mask].add(row["pattern_id"])
            genus[mask] = item["genus"]
    records = []
    for mask in sorted(pattern_ids):
        pairing = constant_pairing(mask)
        records.append({
            "mask": mask,
            "support": support(mask),
            "degree": len(support(mask)),
            "genus": genus[mask],
            "patterns_hit": len(pattern_ids[mask]),
            "pattern_ids": sorted(pattern_ids[mask]),
            "constant_pairing": pairing,
        })
    frequencies = Counter(record["patterns_hit"] for record in records)
    easy = [record for record in records if record["genus"] == 1 and record["constant_pairing"]]
    easy.sort(key=lambda record: (
        -record["patterns_hit"],
        abs(record["constant_pairing"]["difference_right_minus_left"]),
        record["mask"],
    ))
    assert len(rows) * 15 == 345
    assert len(records) == 55
    assert easy[0]["mask"] == MASK and easy[0]["patterns_hit"] == 8
    return {
        "input_pattern_count": len(rows),
        "characters_per_pattern": 15,
        "total_occurrences": len(rows) * 15,
        "distinct_masks": len(records),
        "frequency_of_pattern_hit_counts": {str(k): frequencies[k] for k in sorted(frequencies)},
        "all_masks": records,
        "constant_pairing_genus1_ranking": easy,
        "selection_rule": "maximize patterns hit among genus-1 masks admitting an equal-sum quadratic pairing; break ties by smaller absolute constant difference, then mask",
    }


def rhs(t: int) -> int:
    return t * (t + 1) * (t + 5) * (t + 6)


def integral_point_certificate() -> dict[str, object]:
    middle = []
    points: list[list[int]] = []
    for t in range(-6, 1):
        value = rhs(t)
        square = value >= 0 and math.isqrt(value) ** 2 == value
        ys = []
        if square:
            root = math.isqrt(value)
            ys = [0] if root == 0 else [-root, root]
            points.extend([[t, y] for y in ys])
        middle.append({"t": t, "rhs": value, "ys": ys})
    expected = [[-6, 0], [-5, 0], [-3, -6], [-3, 6], [-1, 0], [0, 0]]
    assert points == expected

    squares_mod_8 = sorted({x * x % 8 for x in range(8)})
    assert 13 % 8 not in squares_mod_8
    return {
        "curve": "y^2=t(t+1)(t+5)(t+6)",
        "mask": MASK,
        "support": SUPPORT,
        "A": "t(t+6)",
        "B": "(t+1)(t+5)",
        "B_minus_A": 5,
        "gcd_identity": "gcd(A,B)=gcd(A,5), hence gcd(A,B) divides 5",
        "positive_regions": ["t<=-7", "t>=1"],
        "common_positive_squarefree_kernels": [1, 5],
        "d=1": {
            "equation": "V^2-U^2=5",
            "positive_same_parity_factor_pairs": [[1, 5]],
            "consequence": "U=2,V=3, so A=4 and (t+3)^2=13, impossible modulo 8",
            "squares_mod_8": squares_mod_8,
        },
        "d=5": {
            "equation": "V^2-U^2=1",
            "positive_factor_pairs": [[1, 1]],
            "consequence": "U=0,V=1, contradicting A>0 in the positive regions",
        },
        "middle_interval_exact_check": middle,
        "proved_integral_points": expected,
        "nondegenerate_integral_points": [],
        "status": "PROVED_COMPLETE_BY_GCD_AND_FINITE_MIDDLE_INTERVAL",
        "bounded_search_used": False,
    }


def pattern_impact() -> dict[str, object]:
    rows = final_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == MASK for item in row["occurrences"]
    ))
    assert affected == [9, 26, 50, 188, 210, 212, 266, 271]
    survivors = sorted(set(row["pattern_id"] for row in rows) - set(affected))
    assert survivors == [12, 31, 33, 43, 59, 83, 134, 214, 230, 251, 257, 268, 276, 281, 283]
    return {
        "input_remaining_count": 23,
        "selected_mask": MASK,
        "affected_pattern_ids": affected,
        "strictly_excluded": len(affected),
        "remaining_count": len(survivors),
        "remaining_pattern_ids": survivors,
        "reason": "mask 99 has no nondegenerate integral parameter",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-square-mask99-v1",
        "semantic_version": "1.0.0",
        "input_sha256": {
            MASK108_CERT.name: sha256(MASK108_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
        },
        "occurrence_inventory": occurrence_inventory(),
        "integral_points": integral_point_certificate(),
        "pattern_impact": pattern_impact(),
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
