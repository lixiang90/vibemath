"""Exact mask-51 gate on the 15 patterns surviving mask 99.

The curve is an integral translate of the proved mask-102 curve and also has
an independent constant-difference squarefree-kernel proof. No bounded search
is used.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT.parent / "certificates" if ROOT.name == "code" else ROOT
MASK99_CERT = CERT_DIR / "PAPER_SQUARE_MASK99_CERTIFICATE.json"
ROUND4_CERT = CERT_DIR / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
OUTPUT = CERT_DIR / "PAPER_SQUARE_MASK51_CERTIFICATE.json"
MASK = 51
SUPPORT = [0, 1, 4, 5]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support(mask: int) -> list[int]:
    return [i for i in range(7) if (mask >> i) & 1]


def gap_signature(mask: int) -> list[int] | None:
    roots = support(mask)
    if len(roots) != 4:
        return None
    gaps = [roots[i + 1] - roots[i] for i in range(3)]
    return min(gaps, list(reversed(gaps)))


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


def known_translate(mask: int) -> dict[str, object] | None:
    signature = gap_signature(mask)
    if signature == [1, 3, 1]:
        return {"proved_mask_family": 102, "gap_signature": signature}
    if signature == [1, 2, 1]:
        return {"proved_mask_family": 108, "gap_signature": signature}
    return None


def input_rows() -> list[dict[str, object]]:
    mask99 = json.loads(MASK99_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    ids = set(mask99["pattern_impact"]["remaining_pattern_ids"])
    rows = [row for row in round4["pattern_occurrences"] if row["pattern_id"] in ids]
    assert len(rows) == len(ids) == 15
    for row in rows:
        masks = [item["character_mask_m"] for item in row["occurrences"]]
        assert len(masks) == len(set(masks)) == 15
    return rows


def genus1_inventory() -> dict[str, object]:
    rows = input_rows()
    pattern_ids: dict[int, set[int]] = defaultdict(set)
    for row in rows:
        for item in row["occurrences"]:
            if item["genus"] == 1:
                pattern_ids[item["character_mask_m"]].add(row["pattern_id"])
    records = []
    for mask in sorted(pattern_ids):
        pairing = constant_pairing(mask)
        records.append({
            "mask": mask,
            "support": support(mask),
            "gap_signature_up_to_reflection": gap_signature(mask),
            "patterns_hit": len(pattern_ids[mask]),
            "pattern_ids": sorted(pattern_ids[mask]),
            "constant_pairing": pairing,
            "gcd_bound_from_pairing": abs(pairing["difference_right_minus_left"]) if pairing else None,
            "known_complete_integral_translate": known_translate(mask),
        })
    all_mask_counter = Counter(
        item["character_mask_m"] for row in rows for item in row["occurrences"]
    )
    pairable = [row for row in records if row["constant_pairing"]]
    pairable.sort(key=lambda row: (
        -row["patterns_hit"],
        0 if row["known_complete_integral_translate"] else 1,
        row["gcd_bound_from_pairing"],
        row["mask"],
    ))
    proved_translates = [row for row in pairable if row["known_complete_integral_translate"]]
    proved_translates.sort(key=lambda row: (-row["patterns_hit"], row["gcd_bound_from_pairing"], row["mask"]))
    assert len(rows) * 15 == 225
    assert len(all_mask_counter) == 53
    assert len(records) == 26
    assert proved_translates[0]["mask"] == MASK
    return {
        "input_pattern_count": 15,
        "characters_per_pattern": 15,
        "total_character_occurrences": 225,
        "all_distinct_masks": len(all_mask_counter),
        "distinct_genus1_four_factor_masks": len(records),
        "genus1_occurrences": sum(row["patterns_hit"] for row in records),
        "all_genus1_masks": records,
        "pairable_ranking": pairable,
        "already_proved_translate_ranking": proved_translates,
        "selection_rule": "among genus-1 masks with a complete integral translate already proved, maximize patterns hit; break ties by smaller pairing gcd bound, then mask",
    }


def rhs(t: int) -> int:
    return t * (t + 1) * (t + 4) * (t + 5)


def integral_point_certificate() -> dict[str, object]:
    middle = []
    points: list[list[int]] = []
    for t in range(-5, 1):
        value = rhs(t)
        root = math.isqrt(value) if value >= 0 else -1
        ys = []
        if root >= 0 and root * root == value:
            ys = [0] if root == 0 else [-root, root]
            points.extend([[t, y] for y in ys])
        middle.append({"t": t, "rhs": value, "ys": ys})
    expected = [[-5, 0], [-4, 0], [-1, 0], [0, 0]]
    assert points == expected

    squares_mod_4 = sorted({x * x % 4 for x in range(4)})
    square_differences_mod_4 = sorted({(v - u) % 4 for u in squares_mod_4 for v in squares_mod_4})
    assert 2 not in square_differences_mod_4
    return {
        "curve": "y^2=t(t+1)(t+4)(t+5)",
        "mask": MASK,
        "support": SUPPORT,
        "integral_translation_to_mask102": {
            "substitution": "s=t-1",
            "identity": "(s+1)(s+2)(s+5)(s+6)=t(t+1)(t+4)(t+5)",
            "bijection_on_integer_parameters": True,
        },
        "A": "t(t+5)",
        "B": "(t+1)(t+4)",
        "B_minus_A": 4,
        "gcd_identity": "gcd(A,B)=gcd(A,4), hence gcd(A,B) divides 4",
        "positive_regions": ["t<=-6", "t>=1"],
        "common_positive_squarefree_kernels": [1, 2],
        "d=1": {
            "equation": "V^2-U^2=4",
            "positive_same_parity_factor_pairs": [[2, 2]],
            "consequence": "U=0,V=2, contradicting A>0",
        },
        "d=2": {
            "equation": "V^2-U^2=2",
            "squares_mod_4": squares_mod_4,
            "square_differences_mod_4": square_differences_mod_4,
            "consequence": "impossible modulo 4",
        },
        "middle_interval_exact_check": middle,
        "proved_integral_points": expected,
        "nondegenerate_integral_points": [],
        "bounded_search_used": False,
        "status": "PROVED_COMPLETE_BY_INTEGRAL_TRANSLATION_AND_INDEPENDENT_GCD_ARGUMENT",
    }


def pattern_impact() -> dict[str, object]:
    rows = input_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == MASK for item in row["occurrences"]
    ))
    assert affected == [33, 83, 257, 268, 283]
    survivors = sorted(set(row["pattern_id"] for row in rows) - set(affected))
    assert survivors == [12, 31, 43, 59, 134, 214, 230, 251, 276, 281]
    return {
        "input_remaining_count": 15,
        "selected_mask": MASK,
        "affected_pattern_ids": affected,
        "strictly_excluded": 5,
        "remaining_count": 10,
        "remaining_pattern_ids": survivors,
        "reason": "mask 51 has no nondegenerate integral parameter",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-square-mask51-v1",
        "semantic_version": "1.0.0",
        "input_sha256": {
            MASK99_CERT.name: sha256(MASK99_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
        },
        "genus1_inventory": genus1_inventory(),
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
