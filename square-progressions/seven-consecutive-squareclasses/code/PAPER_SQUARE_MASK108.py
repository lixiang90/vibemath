"""Exact mask-108 integral-point gate on the 35 remaining patterns."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NEXT_CERT = ROOT / "PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json"
ROUND4_CERT = ROOT / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
OUTPUT = ROOT / "PAPER_SQUARE_MASK108_CERTIFICATE.json"
MASK = 108
SUPPORT = [2, 3, 5, 6]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rhs(t: int) -> int:
    return (t + 2) * (t + 3) * (t + 5) * (t + 6)


def integral_point_certificate() -> dict[str, object]:
    middle = []
    for t in range(-6, -1):
        value = rhs(t)
        square = value >= 0 and math.isqrt(value) ** 2 == value
        ys = [0] if value == 0 else ([-math.isqrt(value), math.isqrt(value)] if square else [])
        middle.append({"t": t, "rhs": value, "ys": ys})
    assert middle == [
        {"t": -6, "rhs": 0, "ys": [0]},
        {"t": -5, "rhs": 0, "ys": [0]},
        {"t": -4, "rhs": 4, "ys": [-2, 2]},
        {"t": -3, "rhs": 0, "ys": [0]},
        {"t": -2, "rhs": 0, "ys": [0]},
    ]

    # Outside the middle interval A=(t+2)(t+6), B=(t+3)(t+5)
    # are positive and B-A=3.  If AB is a square, their common positive
    # squarefree kernel divides 3.
    d1_pairs = [(1, 3)]
    # (V-U,V+U)=(1,3) gives U=1,V=2; A=1 would imply (t+4)^2=5.
    assert (1 + 4) == 5
    # The impossibility (t+4)^2=5 is certified modulo 8.
    squares_mod_8 = sorted({x*x % 8 for x in range(8)})
    assert 5 % 8 not in squares_mod_8

    # d=3 gives V^2-U^2=1.  The only nonnegative factor pair is (1,1), U=0.
    d3_pairs = [(1, 1)]
    points = [[-6, 0], [-5, 0], [-4, -2], [-4, 2], [-3, 0], [-2, 0]]
    return {
        "curve": "y^2=(t+2)(t+3)(t+5)(t+6)",
        "A": "(t+2)(t+6)",
        "B": "(t+3)(t+5)",
        "B_minus_A": 3,
        "positive_regions": ["t<=-7", "t>=-1"],
        "common_positive_squarefree_kernels": [1, 3],
        "d=1": {
            "equation": "V^2-U^2=3",
            "positive_same_parity_factor_pairs": [list(p) for p in d1_pairs],
            "consequence": "U=1,V=2, then A=1 and (t+4)^2=5, impossible modulo 8",
            "squares_mod_8": squares_mod_8,
        },
        "d=3": {
            "equation": "V^2-U^2=1",
            "nonnegative_factor_pairs": [list(p) for p in d3_pairs],
            "consequence": "U=0,V=1, hence A=0, impossible in the positive regions",
        },
        "middle_interval_exact_check": middle,
        "proved_integral_points": points,
        "nondegenerate_integral_points": [],
        "status": "PROVED_COMPLETE_BY_GCD_AND_FINITE_MIDDLE_INTERVAL",
    }


def remaining_rows() -> list[dict[str, object]]:
    next_data = json.loads(NEXT_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    ids = set(next_data["pattern_impact"]["remaining_pattern_ids"])
    rows = [row for row in round4["pattern_occurrences"] if row["pattern_id"] in ids]
    assert len(rows) == len(ids) == 35
    for row in rows:
        masks = [item["character_mask_m"] for item in row["occurrences"]]
        assert len(masks) == len(set(masks)) == 15
    return rows


def pattern_impact() -> dict[str, object]:
    rows = remaining_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == MASK for item in row["occurrences"]
    ))
    assert len(affected) == 12
    survivors = sorted(set(row["pattern_id"] for row in rows) - set(affected))
    assert len(survivors) == 23
    return {
        "input_remaining_count": 35,
        "selected_mask": MASK,
        "support": SUPPORT,
        "affected_pattern_ids": affected,
        "strictly_excluded": len(affected),
        "remaining_count": len(survivors),
        "remaining_pattern_ids": survivors,
        "reason": "mask 108 has no nondegenerate integral parameter",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-square-mask108-v1",
        "semantic_version": "1.0.0",
        "input_sha256": {
            NEXT_CERT.name: sha256(NEXT_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
        },
        "integral_points": integral_point_certificate(),
        "pattern_impact": pattern_impact(),
    }


def main() -> None:
    OUTPUT.write_text(json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
