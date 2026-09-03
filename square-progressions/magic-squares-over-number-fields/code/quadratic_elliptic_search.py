"""Exact rank-two subgroup searches on congruent-number curves over Q(sqrt(d)).

Given rational points on E_n and its quadratic twist E_(dn), the twist point
is transported to E_n(Q(sqrt(d))).  The program enumerates x(2(aP+bQ)) and
looks for exact three-term arithmetic progressions.  Any hit automatically
gives the nine square entries required for a 3 by 3 magic square.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import numpy as np
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from number_field_magic import (
    QElt,
    clear_root_denominators,
    qadd,
    qdiv,
    qmul,
    qneg,
    qresidue,
    qscale,
    qsub,
)


QPoint = tuple[QElt, QElt] | None
RationalPoint = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class QuadraticCenter:
    x: QElt
    coefficients: tuple[int, int]


@dataclass(frozen=True)
class QuadraticMagicCandidate:
    n: int
    d: int
    centers: tuple[QElt, QElt, QElt]
    roots: tuple[QElt, ...]
    scale: int
    coefficients: tuple[tuple[int, int], ...]

    @property
    def values(self) -> tuple[QElt, ...]:
        return tuple(qmul(root, root, self.d) for root in self.roots)


def rational_square_root(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator:
        return None
    if denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def quadratic_square_root(value: QElt, d: int) -> QElt | None:
    """Return one exact square root of value in Q(sqrt(d)), if it exists."""

    a, b = value
    norm_root = rational_square_root(a * a - d * b * b)
    if norm_root is None:
        return None
    for signed_norm_root in (norm_root, -norm_root):
        u = rational_square_root((a + signed_norm_root) / 2)
        if u is not None and u != 0:
            candidate = (u, b / (2 * u))
            if qmul(candidate, candidate, d) == value:
                return candidate
        if u == 0 and b == 0:
            v = rational_square_root(a / d)
            if v is not None:
                candidate = (Fraction(0), v)
                if qmul(candidate, candidate, d) == value:
                    return candidate
    return None


def add_points(p: QPoint, q: QPoint, n: int, d: int) -> QPoint:
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and y1 == qneg(y2):
        return None
    if p == q:
        if y1 == (Fraction(0), Fraction(0)):
            return None
        numerator = qsub(qscale(qmul(x1, x1, d), 3), (Fraction(n * n), Fraction(0)))
        denominator = qscale(y1, 2)
    else:
        numerator = qsub(y2, y1)
        denominator = qsub(x2, x1)
    slope = qdiv(numerator, denominator, d)
    x3 = qsub(qsub(qmul(slope, slope, d), x1), x2)
    y3 = qsub(qmul(slope, qsub(x1, x3), d), y1)
    return x3, y3


def multiply_point(k: int, point: QPoint, n: int, d: int) -> QPoint:
    if k < 0:
        if point is None:
            return None
        return multiply_point(-k, (point[0], qneg(point[1])), n, d)
    result: QPoint = None
    addend = point
    while k:
        if k & 1:
            result = add_points(result, addend, n, d)
        addend = add_points(addend, addend, n, d)
        k >>= 1
    return result


def point_is_on_curve(point: QPoint, n: int, d: int) -> bool:
    if point is None:
        return True
    x, y = point
    return qmul(y, y, d) == qsub(qmul(qmul(x, x, d), x, d), qscale(x, n * n))


def lift_rational_point(point: RationalPoint) -> QPoint:
    return (point[0], Fraction(0)), (point[1], Fraction(0))


def transport_twist_point(point: RationalPoint, d: int) -> QPoint:
    """Map E_(dn)(Q) to the anti-invariant part of E_n(Q(sqrt(d)))."""

    x, y = point
    return (x / d, Fraction(0)), (Fraction(0), y / (d * d))


def enumerate_centers(
    n: int, d: int, generators: Sequence[QPoint], box: int
) -> list[QuadraticCenter]:
    if len(generators) != 2:
        raise ValueError("this search expects exactly two generators")
    if not all(point_is_on_curve(point, n, d) for point in generators):
        raise ValueError("a supplied generator is not on E_n over Q(sqrt(d))")

    coefficient_range = range(-box, box + 1)
    tables = [
        {coefficient: multiply_point(coefficient, point, n, d) for coefficient in coefficient_range}
        for point in generators
    ]
    by_x: dict[QElt, tuple[int, int]] = {}
    for a, b in itertools.product(coefficient_range, repeat=2):
        if a == b == 0:
            continue
        if next(value for value in (a, b) if value) < 0:
            continue
        point = add_points(tables[0][a], tables[1][b], n, d)
        doubled = add_points(point, point, n, d)
        if doubled is not None:
            by_x.setdefault(doubled[0], (a, b))
    return [QuadraticCenter(x, coefficients) for x, coefficients in by_x.items()]


def magic_values(centers: tuple[QElt, QElt, QElt], n: int) -> tuple[QElt, ...]:
    left, middle, right = centers
    if qadd(left, right) != qscale(middle, 2):
        raise ValueError("centers are not in arithmetic progression")
    b = qsub(middle, left)
    n_element = (Fraction(n), Fraction(0))
    return (
        qsub(middle, b),
        qadd(qadd(middle, b), n_element),
        qsub(middle, n_element),
        qsub(qadd(middle, b), n_element),
        middle,
        qadd(qsub(middle, b), n_element),
        qadd(middle, n_element),
        qsub(qsub(middle, b), n_element),
        qadd(middle, b),
    )


def verify_magic_values(values: tuple[QElt, ...]) -> bool:
    if len(set(values)) != 9:
        return False
    rows = (values[:3], values[3:6], values[6:])
    target = (Fraction(0), Fraction(0))
    for value in rows[0]:
        target = qadd(target, value)
    lines = [*rows]
    lines.extend(tuple(rows[row][column] for row in range(3)) for column in range(3))
    lines.append(tuple(rows[i][i] for i in range(3)))
    lines.append(tuple(rows[i][2 - i] for i in range(3)))
    return all(
        sum((value[0] for value in line), Fraction(0)) == target[0]
        and sum((value[1] for value in line), Fraction(0)) == target[1]
        for line in lines
    )


def search_progression(
    n: int, d: int, centers: Sequence[QuadraticCenter], modulus: int = 10_007
) -> QuadraticMagicCandidate | None:
    by_x = {center.x: center for center in centers}
    residues = {x: qresidue(x, modulus) for x in by_x}
    inverse_two = pow(2, -1, modulus)
    center_list = list(centers)

    def exact_candidate(left_index: int, right_index: int) -> QuadraticMagicCandidate | None:
        left = center_list[left_index]
        right = center_list[right_index]
        midpoint = qscale(qadd(left.x, right.x), Fraction(1, 2))
        middle = by_x.get(midpoint)
        if middle is None or len({left.x, middle.x, right.x}) != 3:
            return None
        values = magic_values((left.x, middle.x, right.x), n)
        if not verify_magic_values(values):
            return None
        roots = tuple(quadratic_square_root(value, d) for value in values)
        if any(root is None for root in roots):
            raise ArithmeticError("a doubled-point Kummer certificate failed")
        exact_roots = tuple(root for root in roots if root is not None)
        scale, integral_roots = clear_root_denominators(exact_roots)
        candidate = QuadraticMagicCandidate(
            n=n,
            d=d,
            centers=(left.x, middle.x, right.x),
            roots=integral_roots,
            scale=scale,
            coefficients=(left.coefficients, middle.coefficients, right.coefficients),
        )
        if verify_magic_values(candidate.values):
            return candidate
        raise ArithmeticError("denominator clearing damaged the magic square")

    # Work only with good reductions in the vectorized main sieve.  A modulus
    # around 10^4 makes its two-coordinate image sparse, while NumPy evaluates
    # millions of midpoint residues without a Python-level pair loop.
    good_indices = [
        index for index, center in enumerate(center_list) if residues[center.x] is not None
    ]
    bad_indices = [
        index for index, center in enumerate(center_list) if residues[center.x] is None
    ]
    good_residues = np.array(
        [residues[center_list[index].x] for index in good_indices], dtype=np.int64
    ).reshape((-1, 2))
    residue_codes = np.unique(good_residues[:, 0] * modulus + good_residues[:, 1])
    column_indices = np.arange(len(good_indices), dtype=np.int64)[None, :]
    block_size = 128
    for start in range(0, len(good_indices), block_size):
        end = min(start + block_size, len(good_indices))
        midpoint_first = (
            (good_residues[start:end, 0, None] + good_residues[None, :, 0])
            * inverse_two
            % modulus
        )
        midpoint_second = (
            (good_residues[start:end, 1, None] + good_residues[None, :, 1])
            * inverse_two
            % modulus
        )
        midpoint_codes = midpoint_first * modulus + midpoint_second
        row_indices = np.arange(start, end, dtype=np.int64)[:, None]
        mask = np.isin(midpoint_codes, residue_codes) & (column_indices > row_indices)
        for local_row, local_column in np.argwhere(mask):
            candidate = exact_candidate(
                good_indices[start + int(local_row)],
                good_indices[int(local_column)],
            )
            if candidate is not None:
                return candidate

    # Denominators divisible by the sieve prime have no affine reduction.  All
    # pairs involving them are checked exactly, so the vectorized sieve cannot
    # hide a genuine progression.
    checked_bad_pairs: set[tuple[int, int]] = set()
    for bad_index in bad_indices:
        for other_index in range(len(center_list)):
            if bad_index == other_index:
                continue
            pair = tuple(sorted((bad_index, other_index)))
            if pair in checked_bad_pairs:
                continue
            checked_bad_pairs.add(pair)
            candidate = exact_candidate(*pair)
            if candidate is not None:
                return candidate
    return None


def parse_point(text: str) -> RationalPoint:
    x, y = text.split(",", maxsplit=1)
    return Fraction(x), Fraction(y)


def qtext(value: QElt, d: int) -> str:
    a, b = value
    if b == 0:
        return str(a)
    return f"{a}+({b})*sqrt({d})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--d", type=int, required=True)
    parser.add_argument("--generator", required=True, help="rational point x,y on E_n")
    parser.add_argument("--twist-generator", required=True, help="rational point x,y on E_(dn)")
    parser.add_argument("--box", type=int, default=20)
    args = parser.parse_args()

    generators = (
        lift_rational_point(parse_point(args.generator)),
        transport_twist_point(parse_point(args.twist_generator), args.d),
    )
    centers = enumerate_centers(args.n, args.d, generators, args.box)
    candidate = search_progression(args.n, args.d, centers)
    payload: dict[str, object] = {
        "n": args.n,
        "d": args.d,
        "box": args.box,
        "centers": len(centers),
        "candidate": None,
    }
    if candidate is not None:
        payload["candidate"] = {
            "scale": candidate.scale,
            "coefficients": candidate.coefficients,
            "centers": [qtext(value, args.d) for value in candidate.centers],
            "roots": [qtext(value, args.d) for value in candidate.roots],
            "values": [qtext(value, args.d) for value in candidate.values],
        }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
