"""PGL2/affine cover-isomorphism reduction for the R_2(7) character curves.

For an even subset S of {0,...,6}, the character curve is

    C_S: y^2 = product_{i in S} (t+i).

The code proves cover isomorphisms by an explicit rational Mobius substitution
and a rational square multiplier.  It intentionally does not identify abstract
genus-1 curves unless the isomorphism respects their displayed double covers.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import permutations
from pathlib import Path

import STUDENT_SQUARE_ROUND_02_patterns as round2


ROOT = Path(__file__).resolve().parent
CERTIFICATE_PATH = ROOT / "STUDENT_SQUARE_ROUND_03_CERTIFICATE.json"
MAGMA_PATH = ROOT / "STUDENT_SQUARE_ROUND_03_selmer.m"


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def null_vector_3x4(matrix: list[list[Fraction]]) -> tuple[Fraction, ...]:
    result = []
    for column in range(4):
        minor = [[row[j] for j in range(4) if j != column] for row in matrix]
        result.append(((-1) ** column) * determinant3(minor))
    return tuple(result)


def normalize_matrix(vector: tuple[Fraction, ...]) -> tuple[int, int, int, int]:
    lcm = 1
    for value in vector:
        lcm = math.lcm(lcm, value.denominator)
    integers = [int(value * lcm) for value in vector]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    integers = [value // common for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return tuple(integers)  # type: ignore[return-value]


def mobius_from_triples(
    target: tuple[Fraction, Fraction, Fraction],
    source: tuple[Fraction, Fraction, Fraction],
) -> tuple[int, int, int, int] | None:
    # Find t_source=(a*u_target+b)/(c*u_target+d).
    matrix = [
        [u, Fraction(1), -t * u, -t]
        for u, t in zip(target, source)
    ]
    vector = null_vector_3x4(matrix)
    if not any(vector):
        return None
    a, b, c, d = normalize_matrix(vector)
    if a * d - b * c == 0:
        return None
    return a, b, c, d


def apply_mobius(matrix: tuple[int, int, int, int], value: Fraction) -> Fraction | None:
    a, b, c, d = matrix
    denominator = c * value + d
    if denominator == 0:
        return None
    return Fraction(a * value + b, denominator)


def rational_square_root(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def roots(mask: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(-i) for i in range(7) if mask >> i & 1)


@dataclass(frozen=True)
class CoverIsomorphism:
    source_mask: int
    target_mask: int
    # Substitution into the source model: t_source=g(u_target).
    matrix: tuple[int, int, int, int]
    multiplier_K: tuple[int, int]
    sqrt_K: tuple[int, int]
    affine: bool
    point_map: str


def find_cover_isomorphism(
    source_mask: int, target_mask: int, *, affine_only: bool = False
) -> CoverIsomorphism | None:
    source_roots = roots(source_mask)
    target_roots = roots(target_mask)
    if len(source_roots) != len(target_roots):
        return None
    degree = len(source_roots)
    fixed_target = target_roots[:3]
    source_set = set(source_roots)
    for source_triple in permutations(source_roots, 3):
        matrix = mobius_from_triples(fixed_target, source_triple)
        if matrix is None:
            continue
        a, b, c, d = matrix
        if affine_only and c != 0:
            continue
        images = [apply_mobius(matrix, value) for value in target_roots]
        if None in images or set(images) != source_set or len(set(images)) != degree:
            continue
        K = Fraction(1)
        for root in source_roots:
            K *= a - root * c
        sqrt_K = rational_square_root(K)
        if sqrt_K is None:
            continue
        return CoverIsomorphism(
            source_mask=source_mask,
            target_mask=target_mask,
            matrix=matrix,
            multiplier_K=(K.numerator, K.denominator),
            sqrt_K=(sqrt_K.numerator, sqrt_K.denominator),
            affine=c == 0,
            point_map=(
                f"t_source=({a}*u_target+({b}))/({c}*u_target+({d})); "
                f"y_source=({sqrt_K})*v_target/({c}*u_target+({d}))^{degree // 2}"
            ),
        )
    return None


def classify_masks(masks: list[int], *, affine_only: bool) -> list[dict[str, object]]:
    classes: list[dict[str, object]] = []
    for mask in sorted(masks):
        placed = False
        for row in classes:
            representative = row["representative_mask"]
            iso = find_cover_isomorphism(mask, representative, affine_only=affine_only)
            if iso is not None:
                row["members"].append(mask)
                row["maps_from_representative_to_member"].append(asdict(iso))
                placed = True
                break
        if not placed:
            identity = find_cover_isomorphism(mask, mask, affine_only=affine_only)
            assert identity is not None
            classes.append(
                {
                    "representative_mask": mask,
                    "members": [mask],
                    "maps_from_representative_to_member": [asdict(identity)],
                }
            )
    return classes


def mask_polynomial_text(mask: int, variable: str = "t") -> str:
    factors = [f"({variable}+{i})" for i in range(7) if mask >> i & 1]
    return "*".join(factors)


def padic_witness(prime: int, m: int | None = None) -> dict[str, object]:
    if m is None:
        m = 2 if prime == 2 else 1
    if prime == 2 and m < 2:
        raise ValueError("for p=2 use m>=2")
    t = Fraction(1, prime ** (2 * m))
    checks = []
    modulus = 8 if prime == 2 else prime
    for i in range(7):
        unit = 1 + i * prime ** (2 * m)
        checks.append(
            {
                "i": i,
                "t_plus_i": [*(t + i).as_integer_ratio()],
                "square_prefactor": f"{prime}^(-{2*m})",
                "unit": unit,
                "unit_modulus": modulus,
                "unit_residue": unit % modulus,
                "hensel_square_criterion": unit % modulus == 1,
            }
        )
    return {
        "prime": prime,
        "m": m,
        "t": [t.numerator, t.denominator],
        "identity": f"t+i={prime}^(-{2*m})*(1+i*{prime}^{2*m})",
        "checks": checks,
        "all_certified_squares_in_Qp": all(row["hensel_square_criterion"] for row in checks),
    }


def attach_occurrences(
    classes: list[dict[str, object]], patterns: list[dict[str, object]]
) -> None:
    occurrences: dict[int, list[dict[str, object]]] = {}
    for pattern_id, pattern in enumerate(patterns):
        for quotient in pattern["quotients"]:
            mask = quotient["relation_mask"]
            if quotient["genus"] > 0:
                occurrences.setdefault(mask, []).append(
                    {"pattern_id": pattern_id, "partition": pattern["partition"]}
                )
    for row in classes:
        affected = []
        for mask in row["members"]:
            affected.extend({"mask": mask, **item} for item in occurrences.get(mask, []))
        row["affected_pattern_occurrences"] = affected


def class_lookup(classes: list[dict[str, object]]) -> dict[int, dict[str, object]]:
    result = {}
    for class_id, row in enumerate(classes):
        for mask, transform in zip(row["members"], row["maps_from_representative_to_member"]):
            result[mask] = {
                "class_id": class_id,
                "representative_mask": row["representative_mask"],
                "map_from_representative_to_mask": transform,
            }
    return result


def compatibility_records(
    patterns: list[dict[str, object]], pgl_lookup: dict[int, dict[str, object]]
) -> list[dict[str, object]]:
    records = []
    for pattern_id, pattern in enumerate(patterns):
        conditions = []
        for mask in pattern["relation_basis_masks"]:
            if mask in pgl_lookup:
                lookup = pgl_lookup[mask]
                transform = lookup["map_from_representative_to_mask"]
                a, b, c, d = transform["matrix"]
                conditions.append(
                    {
                        "basis_mask": mask,
                        "representative_mask": lookup["representative_mask"],
                        "representative_parameter": f"u_{mask}",
                        "same_t_condition": f"t=({a}*u_{mask}+({b}))/({c}*u_{mask}+({d}))",
                    }
                )
            else:
                conditions.append(
                    {
                        "basis_mask": mask,
                        "representative_mask": mask,
                        "representative_parameter": f"u_{mask}",
                        "same_t_condition": f"t=u_{mask}",
                        "note": "genus-0 basis character; not sent to Selmer script",
                    }
                )
        records.append(
            {
                "pattern_id": pattern_id,
                "partition": pattern["partition"],
                "basis_masks": pattern["relation_basis_masks"],
                "conditions": conditions,
                "compatibility_requirement": (
                    "all displayed rational functions must give one identical finite t; "
                    "the four square roots must then satisfy the basis equations simultaneously"
                ),
            }
        )
    return records


def build_certificate() -> dict[str, object]:
    round2_certificate = round2.build_certificate((11, 13, 17, 19, 23, 29, 31))
    patterns = round2_certificate["unresolved_patterns_ranked"]
    quartics = sorted(
        {q["relation_mask"] for p in patterns for q in p["quotients"] if q["genus"] == 1}
    )
    sextics = sorted(
        {q["relation_mask"] for p in patterns for q in p["quotients"] if q["genus"] == 2}
    )
    positive_genus_masks = quartics + sextics

    affine_classes = classify_masks(quartics, affine_only=True) + classify_masks(sextics, affine_only=True)
    pgl_classes = classify_masks(quartics, affine_only=False) + classify_masks(sextics, affine_only=False)
    attach_occurrences(affine_classes, patterns)
    attach_occurrences(pgl_classes, patterns)
    pgl_lookup = class_lookup(pgl_classes)

    certificate: dict[str, object] = {
        "version": "2026-09-01-r3",
        "theorem_correction": {
            "formula": "[t+i]=c+phi(ell_i)",
            "phi": "F_2-linear from F_2^2 to Q*/Q*2",
            "exact_blocks": (
                "labels are exactly the squareclass equality blocks iff phi is injective; "
                "for a finite nonzero R_2(7)=7 solution, R_1(6)=5 forces affine rank 2, hence phi injective"
            ),
        },
        "counts": {
            "quartic_masks": len(quartics),
            "sextic_masks": len(sextics),
            "positive_genus_masks": len(positive_genus_masks),
            "affine_cover_classes": len(affine_classes),
            "pgl2_Q_cover_classes": len(pgl_classes),
        },
        "quartic_masks": quartics,
        "sextic_masks": sextics,
        "affine_classes": affine_classes,
        "pgl2_Q_classes": pgl_classes,
        "padic_witnesses": [padic_witness(p) for p in (2, 3, 5, 7, 11)],
        "pattern_compatibility": compatibility_records(patterns, pgl_lookup),
        "magma_scope": (
            "RankBounds/Jacobian data are computed once per PGL2 cover representative; "
            "rational points must be pulled back with the recorded Mobius maps and matched at one common t"
        ),
    }
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    certificate["sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    return certificate


def write_magma(certificate: dict[str, object]) -> None:
    lines = [
        "// Generated by STUDENT_SQUARE_ROUND_03_isomorphisms.py",
        "// Auditable Selmer/Mordell--Weil handoff; no result is claimed until this runs.",
        "Q := Rationals();",
        "Qt<t> := PolynomialRing(Q);",
        'out := Open("STUDENT_SQUARE_ROUND_03_rank_output.csv", "w");',
        'fprintf out, "class_id,mask,degree,genus,rank_lo,rank_hi,members,patterns\\n";',
    ]
    for class_id, row in enumerate(certificate["pgl2_Q_classes"]):
        mask = row["representative_mask"]
        degree = mask.bit_count()
        genus = (degree - 2) // 2
        polynomial = mask_polynomial_text(mask)
        members = ";".join(str(value) for value in row["members"])
        pattern_ids = sorted({item["pattern_id"] for item in row["affected_pattern_occurrences"]})
        patterns = ";".join(str(value) for value in pattern_ids)
        lines.extend(
            [
                f"f := {polynomial};",
                "C := HyperellipticCurve(f);",
                "J := Jacobian(C);",
                "lo,hi := RankBounds(J);",
                (
                    f'fprintf out, "{class_id},{mask},{degree},{genus},%o,%o,'
                    f'{members},{patterns}\\n", lo,hi;'
                ),
                f'printf "class {class_id}, mask {mask}, rank bounds %o %o\\n", lo,hi;',
            ]
        )
    lines.extend(["delete out;", "quit;"])
    MAGMA_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    certificate = build_certificate()
    CERTIFICATE_PATH.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_magma(certificate)
    print(json.dumps(certificate["counts"], sort_keys=True))
    print("sha256:", certificate["sha256_without_this_field"])
    print("certificate:", CERTIFICATE_PATH.name)
    print("Magma:", MAGMA_PATH.name)


if __name__ == "__main__":
    main()
