"""Round 4: Jacobian j-certificates and strict Magma-result ingestion.

No external computation is performed here.  Simulated rank/point files exercise
the same strict parser and same-t compatibility pipeline used for future Magma
output; simulated conclusions are labelled as fixtures, never as mathematics.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import STUDENT_SQUARE_ROUND_02_patterns as round2
import STUDENT_SQUARE_ROUND_03_isomorphisms as round3


ROOT = Path(__file__).resolve().parent
CERTIFICATE_PATH = ROOT / "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json"
SIM_RANK_PATH = ROOT / "STUDENT_SQUARE_ROUND_04_SIMULATED_RANK.csv"
SIM_POINT_PATH = ROOT / "STUDENT_SQUARE_ROUND_04_SIMULATED_POINTS.csv"
SIM_OUTCOME_PATH = ROOT / "STUDENT_SQUARE_ROUND_04_SIMULATED_OUTCOMES.json"


def polynomial_coefficients(mask: int) -> list[int]:
    coefficients = [1]
    for i in range(7):
        if not (mask >> i & 1):
            continue
        result = [0] * (len(coefficients) + 1)
        for j, value in enumerate(coefficients):
            result[j] += i * value
            result[j + 1] += value
        coefficients = result
    return coefficients


def quartic_invariants(mask: int) -> dict[str, Any]:
    coefficients = polynomial_coefficients(mask)
    if len(coefficients) != 5:
        raise ValueError("quartic mask required")
    # Coefficients are stored constant first; binary quartic is
    # a*x^4+b*x^3*z+c*x^2*z^2+d*x*z^3+e*z^4.
    e, d, c, b, a = coefficients
    I = 12 * a * e - 3 * b * d + c * c
    J = 72 * a * c * e + 9 * b * c * d - 27 * a * d * d - 27 * b * b * e - 2 * c**3
    delta27 = 4 * I**3 - J**2
    if delta27 == 0:
        raise ValueError("singular quartic")
    j = Fraction(6912 * I**3, delta27)
    return {
        "representative_mask": mask,
        "polynomial_coefficients_constant_first": coefficients,
        "binary_quartic_I": I,
        "binary_quartic_J": J,
        "27_times_binary_quartic_discriminant": delta27,
        "jacobian_model": f"Y^2=X^3-27*({I})*X-27*({J})",
        "j_invariant": [j.numerator, j.denominator],
        "proof_status": "exact binary-quartic invariant calculation; distinct j implies non-isomorphic Jacobians over Qbar",
    }


def pgl_lookup(round3_certificate: dict[str, Any]) -> dict[int, dict[str, Any]]:
    lookup = {}
    for class_id, row in enumerate(round3_certificate["pgl2_Q_classes"]):
        for mask, transform in zip(row["members"], row["maps_from_representative_to_member"]):
            lookup[mask] = {
                "class_id": class_id,
                "representative_mask": row["representative_mask"],
                "transform": transform,
            }
    return lookup


def occurrence_records(
    round2_certificate: dict[str, Any], round3_certificate: dict[str, Any]
) -> list[dict[str, Any]]:
    lookup = pgl_lookup(round3_certificate)
    result = []
    for pattern_id, pattern in enumerate(round2_certificate["unresolved_patterns_ranked"]):
        occurrences = []
        for quotient in pattern["quotients"]:
            mask = quotient["relation_mask"]
            genus = quotient["genus"]
            machine_variable = f"u_P{pattern_id}_m{mask}"
            if genus == 0:
                occurrences.append(
                    {
                        "occurrence_id": f"P{pattern_id}:m{mask}",
                        "character_mask_m": mask,
                        "genus": genus,
                        "local_notation": "u_m",
                        "machine_variable": machine_variable,
                        "representative_mask": mask,
                        "class_id": None,
                        "t_numerator_homogeneous": [1, 0],
                        "t_denominator_homogeneous": [0, 1],
                        "same_t_map": f"t={machine_variable}",
                        "finite_constraint": "Z != 0",
                        "nonbranch_constraint": "nonbranch: t not in {0,-1,-2,-3,-4,-5,-6}",
                        "note": "genus-0 character is checked directly at candidate t",
                    }
                )
                continue
            item = lookup[mask]
            transform = item["transform"]
            a, b, c, d = transform["matrix"]
            occurrences.append(
                {
                    "occurrence_id": f"P{pattern_id}:m{mask}",
                    "character_mask_m": mask,
                    "genus": genus,
                    "local_notation": "u_m",
                    "machine_variable": machine_variable,
                    "representative_mask": item["representative_mask"],
                    "class_id": item["class_id"],
                    "mobius_matrix_rep_to_occurrence": [a, b, c, d],
                    "t_numerator_homogeneous": [a, b],
                    "t_denominator_homogeneous": [c, d],
                    "same_t_map": f"t=({a}*U_m+({b})*Z_m)/({c}*U_m+({d})*Z_m)",
                    "finite_constraint": f"{c}*U_m+({d})*Z_m != 0",
                    "nonbranch_constraint": "nonbranch: t not in {0,-1,-2,-3,-4,-5,-6}",
                    "coordinate_note": (
                        "u_m is a fresh copy of the representative parameter for this character mask m; "
                        "different masks in one class do not share a point variable"
                    ),
                }
            )
        result.append(
            {
                "pattern_id": pattern_id,
                "partition": pattern["partition"],
                "occurrences": occurrences,
                "compatibility": "all fifteen occurrence maps must yield one identical finite nonbranch t",
            }
        )
    return result


@dataclass(frozen=True)
class RankRecord:
    class_id: int
    representative_mask: int
    degree: int
    genus: int
    rank_lo: int
    rank_hi: int


@dataclass(frozen=True)
class ProjectivePoint:
    U: Fraction
    V: Fraction
    Z: Fraction


@dataclass
class PointSetRecord:
    class_id: int
    complete: bool
    points: list[ProjectivePoint]


RANK_HEADER = ["class_id", "representative_mask", "degree", "genus", "rank_lo", "rank_hi"]
POINT_HEADER = [
    "class_id",
    "complete",
    "U_num",
    "U_den",
    "V_num",
    "V_den",
    "Z_num",
    "Z_den",
]


def strict_int(text: str, field: str) -> int:
    if text.strip() != text or not text or (text[0] == "-" and not text[1:].isdigit()) or (
        text[0] != "-" and not text.isdigit()
    ):
        raise ValueError(f"invalid integer in {field}: {text!r}")
    return int(text)


def strict_bool(text: str) -> bool:
    if text == "true":
        return True
    if text == "false":
        return False
    raise ValueError(f"invalid boolean: {text!r}")


def parse_rank_csv(text: str, certificate: dict[str, Any]) -> dict[int, RankRecord]:
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != RANK_HEADER:
        raise ValueError(f"rank header mismatch: {reader.fieldnames}")
    expected = {
        class_id: row["representative_mask"]
        for class_id, row in enumerate(certificate["pgl2_Q_classes"])
    }
    records = {}
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("malformed rank row")
        values = {name: strict_int(row[name], name) for name in RANK_HEADER}
        class_id = values["class_id"]
        if class_id in records or class_id not in expected:
            raise ValueError(f"duplicate or unknown class_id {class_id}")
        mask = values["representative_mask"]
        if mask != expected[class_id]:
            raise ValueError(f"mask mismatch for class {class_id}")
        degree = mask.bit_count()
        genus = (degree - 2) // 2
        if values["degree"] != degree or values["genus"] != genus:
            raise ValueError(f"degree/genus mismatch for class {class_id}")
        if not (0 <= values["rank_lo"] <= values["rank_hi"]):
            raise ValueError(f"invalid rank bounds for class {class_id}")
        records[class_id] = RankRecord(**values)
    if set(records) != set(expected):
        raise ValueError("rank output does not cover exactly all 16 representatives")
    return records


def projective_point_is_on_curve(mask: int, point: ProjectivePoint) -> bool:
    degree = mask.bit_count()
    if point.U == point.V == point.Z == 0:
        return False
    rhs = Fraction(1)
    for i in range(7):
        if mask >> i & 1:
            rhs *= point.U + i * point.Z
    return point.V * point.V == rhs


def parse_point_csv(text: str, certificate: dict[str, Any]) -> dict[int, PointSetRecord]:
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != POINT_HEADER:
        raise ValueError(f"point header mismatch: {reader.fieldnames}")
    expected = {
        class_id: row["representative_mask"]
        for class_id, row in enumerate(certificate["pgl2_Q_classes"])
    }
    records: dict[int, PointSetRecord] = {}
    seen_points: dict[int, set[tuple[Fraction, Fraction, Fraction]]] = {}
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("malformed point row")
        class_id = strict_int(row["class_id"], "class_id")
        if class_id not in expected:
            raise ValueError(f"unknown class_id {class_id}")
        complete = strict_bool(row["complete"])
        fractions = []
        for coordinate in ("U", "V", "Z"):
            numerator = strict_int(row[f"{coordinate}_num"], f"{coordinate}_num")
            denominator = strict_int(row[f"{coordinate}_den"], f"{coordinate}_den")
            if denominator <= 0:
                raise ValueError("coordinate denominator must be positive")
            fractions.append(Fraction(numerator, denominator))
        point = ProjectivePoint(*fractions)
        if not projective_point_is_on_curve(expected[class_id], point):
            raise ValueError(f"point is not on representative class {class_id}")
        if class_id not in records:
            records[class_id] = PointSetRecord(class_id, complete, [])
            seen_points[class_id] = set()
        elif records[class_id].complete != complete:
            raise ValueError(f"inconsistent complete flag for class {class_id}")
        key = (point.U, point.V, point.Z)
        if key in seen_points[class_id]:
            raise ValueError(f"duplicate literal point for class {class_id}")
        seen_points[class_id].add(key)
        records[class_id].points.append(point)
    if set(records) != set(expected):
        raise ValueError("point output does not cover exactly all 16 representatives")
    return records


def mapped_t(point: ProjectivePoint, occurrence: dict[str, Any]) -> Fraction | None:
    a, b = occurrence["t_numerator_homogeneous"]
    c, d = occurrence["t_denominator_homogeneous"]
    numerator = a * point.U + b * point.Z
    denominator = c * point.U + d * point.Z
    if denominator == 0:
        return None
    t = Fraction(numerator, denominator)
    if t in {Fraction(-i) for i in range(7)}:
        return None
    return t


def rational_is_square(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        math.isqrt(value.numerator) ** 2 == value.numerator
        and math.isqrt(value.denominator) ** 2 == value.denominator
    )


def character_rhs(mask: int, t: Fraction) -> Fraction:
    result = Fraction(1)
    for i in range(7):
        if mask >> i & 1:
            result *= t + i
    return result


def evaluate_same_t(
    certificate: dict[str, Any],
    ranks: dict[int, RankRecord],
    point_sets: dict[int, PointSetRecord],
) -> list[dict[str, Any]]:
    # Rank records are required for audit completeness even though exact point
    # sets, not ranks alone, drive the t-intersection.
    if set(ranks) != set(point_sets):
        raise ValueError("rank and point class sets differ")
    results = []
    for pattern in certificate["pattern_occurrences"]:
        candidate_sets = []
        complete = True
        genus0_masks = []
        occurrence_counts = []
        for occurrence in pattern["occurrences"]:
            mask = occurrence["character_mask_m"]
            if occurrence["genus"] == 0:
                genus0_masks.append(mask)
                continue
            point_set = point_sets[occurrence["class_id"]]
            complete = complete and point_set.complete
            values = {
                t
                for point in point_set.points
                if (t := mapped_t(point, occurrence)) is not None
            }
            candidate_sets.append(values)
            occurrence_counts.append(
                {"occurrence_id": occurrence["occurrence_id"], "finite_nonbranch_t_count": len(values)}
            )
        if not candidate_sets:
            results.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "status": "unresolved_no_positive_genus_occurrence",
                }
            )
            continue
        common = set.intersection(*candidate_sets)
        common = {
            t
            for t in common
            if all(rational_is_square(character_rhs(mask, t)) for mask in genus0_masks)
        }
        serialized = [[t.numerator, t.denominator] for t in sorted(common)]
        if not complete:
            status = "unresolved_incomplete_representative_point_sets"
        elif not common:
            status = "excluded_by_complete_same_t_intersection"
        else:
            # All positive characters have points at t and all genus-0
            # characters were checked directly.  Recheck every character as a
            # fail-closed assertion before reporting a full-cover candidate.
            all_masks = [item["character_mask_m"] for item in pattern["occurrences"]]
            if not all(all(rational_is_square(character_rhs(mask, t)) for mask in all_masks) for t in common):
                raise AssertionError("same-t candidate failed a character equation")
            status = "valid_full_cover_candidates_require_independent_AP_certificate"
        results.append(
            {
                "pattern_id": pattern["pattern_id"],
                "partition": pattern["partition"],
                "status": status,
                "all_positive_genus_point_sets_complete": complete,
                "occurrence_candidate_counts": occurrence_counts,
                "common_finite_nonbranch_t": serialized,
            }
        )
    return results


def simulated_csv(certificate: dict[str, Any]) -> tuple[str, str]:
    rank_stream = io.StringIO(newline="")
    rank_writer = csv.writer(rank_stream, lineterminator="\n")
    rank_writer.writerow(RANK_HEADER)
    point_stream = io.StringIO(newline="")
    point_writer = csv.writer(point_stream, lineterminator="\n")
    point_writer.writerow(POINT_HEADER)
    for class_id, row in enumerate(certificate["pgl2_Q_classes"]):
        mask = row["representative_mask"]
        degree = mask.bit_count()
        genus = (degree - 2) // 2
        rank_writer.writerow([class_id, mask, degree, genus, 0, 0])
        points = [ProjectivePoint(Fraction(-i), Fraction(0), Fraction(1)) for i in range(7) if mask >> i & 1]
        points.extend(
            [ProjectivePoint(Fraction(1), Fraction(1), Fraction(0)), ProjectivePoint(Fraction(1), Fraction(-1), Fraction(0))]
        )
        for point in points:
            point_writer.writerow(
                [
                    class_id,
                    "true",
                    point.U.numerator,
                    point.U.denominator,
                    point.V.numerator,
                    point.V.denominator,
                    point.Z.numerator,
                    point.Z.denominator,
                ]
            )
    return rank_stream.getvalue(), point_stream.getvalue()


def build_certificate() -> dict[str, Any]:
    r2 = round2.build_certificate((11, 13, 17, 19, 23, 29, 31))
    r3 = round3.build_certificate()
    quartic_representatives = [
        row["representative_mask"]
        for row in r3["pgl2_Q_classes"]
        if row["representative_mask"].bit_count() == 4
    ]
    j_records = [quartic_invariants(mask) for mask in quartic_representatives]
    if len({tuple(row["j_invariant"]) for row in j_records}) != 12:
        raise AssertionError("quartic representative j-invariants are not distinct")
    affine_partition = [sorted(row["members"]) for row in r3["affine_classes"]]
    pgl_partition = [sorted(row["members"]) for row in r3["pgl2_Q_classes"]]
    nonaffine = [
        transform
        for row in r3["pgl2_Q_classes"]
        for transform in row["maps_from_representative_to_member"]
        if not transform["affine"]
    ]
    certificate: dict[str, Any] = {
        "version": "2026-09-01-r4",
        "j_invariant_proof": {
            "binary_quartic_invariants": "I=12ae-3bd+c^2; J=72ace+9bcd-27ad^2-27b^2e-2c^3",
            "jacobian": "Y^2=X^3-27IX-27J",
            "j_formula": "j=6912 I^3/(4I^3-J^2)",
            "scope": "abstract Jacobians; separate from PGL2 cover-isomorphism data",
            "all_12_distinct": True,
        },
        "quartic_j_invariants": j_records,
        "pgl2_Q_classes": r3["pgl2_Q_classes"],
        "affine_and_pgl_member_partitions_equal": affine_partition == pgl_partition,
        "nonaffine_transform_count": len(nonaffine),
        "nonaffine_transforms": nonaffine,
        "pattern_occurrences": occurrence_records(r2, r3),
        "parser_schema": {"rank_header": RANK_HEADER, "point_header": POINT_HEADER},
        "simulation_warning": "rank0/complete flags and trivial points in SIMULATED files are pipeline fixtures, not Magma results",
    }
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    certificate["sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    return certificate


def main() -> None:
    certificate = build_certificate()
    CERTIFICATE_PATH.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rank_text, point_text = simulated_csv(certificate)
    SIM_RANK_PATH.write_text(rank_text, encoding="utf-8")
    SIM_POINT_PATH.write_text(point_text, encoding="utf-8")
    ranks = parse_rank_csv(rank_text, certificate)
    points = parse_point_csv(point_text, certificate)
    outcomes = evaluate_same_t(certificate, ranks, points)
    counts: dict[str, int] = {}
    for row in outcomes:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    SIM_OUTCOME_PATH.write_text(
        json.dumps(
            {
                "warning": certificate["simulation_warning"],
                "status_counts": counts,
                "outcomes": outcomes,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("j invariants:", len(certificate["quartic_j_invariants"]))
    print("nonaffine transforms:", certificate["nonaffine_transform_count"])
    print("simulated outcomes (not mathematics):", counts)
    print("certificate:", CERTIFICATE_PATH.name)


if __name__ == "__main__":
    main()
