"""Exact small-height search over pure cubic fields Q(theta), theta^3=m."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce


CElt = tuple[Fraction, Fraction, Fraction]


def cadd(x: CElt, y: CElt) -> CElt:
    return x[0] + y[0], x[1] + y[1], x[2] + y[2]


def cneg(x: CElt) -> CElt:
    return -x[0], -x[1], -x[2]


def csub(x: CElt, y: CElt) -> CElt:
    return cadd(x, cneg(y))


def cscale(x: CElt, scalar: int | Fraction) -> CElt:
    return scalar * x[0], scalar * x[1], scalar * x[2]


def cmul(x: CElt, y: CElt, m: int) -> CElt:
    a, b, c = x
    p, q, r = y
    return (
        a * p + m * (b * r + c * q),
        a * q + b * p + m * c * r,
        a * r + b * q + c * p,
    )


def cinv(x: CElt, m: int) -> CElt:
    a, b, c = x
    norm = a**3 + m * b**3 + m * m * c**3 - 3 * m * a * b * c
    if norm == 0:
        raise ZeroDivisionError
    return (
        (a * a - m * b * c) / norm,
        (m * c * c - a * b) / norm,
        (b * b - a * c) / norm,
    )


def cdiv(x: CElt, y: CElt, m: int) -> CElt:
    return cmul(x, cinv(y, m), m)


def cformat(x: CElt, m: int) -> str:
    labels = ("", f"*cuberoot({m})", f"*cuberoot({m})^2")
    terms: list[str] = []
    for coefficient, label in zip(x, labels):
        if coefficient:
            terms.append(f"{coefficient}{label}")
    return " + ".join(terms).replace("+ -", "- ") if terms else "0"


def is_nontrivial_pure_cubic(m: int) -> bool:
    if m in (-1, 0, 1):
        return False
    root = round(abs(m) ** (1 / 3))
    return all(candidate**3 != abs(m) for candidate in range(max(0, root - 2), root + 3))


def parameter_grid(bound: int, denominator_bound: int) -> set[CElt]:
    parameters: set[CElt] = set()
    for denominator in range(1, denominator_bound + 1):
        for a in range(-bound, bound + 1):
            for b in range(-bound, bound + 1):
                for c in range(-bound, bound + 1):
                    if math.gcd(math.gcd(math.gcd(abs(a), abs(b)), abs(c)), denominator) != 1:
                        continue
                    parameters.add(
                        (
                            Fraction(a, denominator),
                            Fraction(b, denominator),
                            Fraction(c, denominator),
                        )
                    )
    return parameters


def circle_data(t: CElt, m: int) -> tuple[CElt, CElt, CElt] | None:
    one: CElt = (Fraction(1), Fraction(0), Fraction(0))
    t2 = cmul(t, t, m)
    denominator = cadd(one, t2)
    try:
        plus_root = cdiv(csub(cadd(one, cscale(t, 2)), t2), denominator, m)
        minus_root = cdiv(csub(csub(one, cscale(t, 2)), t2), denominator, m)
    except ZeroDivisionError:
        return None
    offset = csub(cmul(plus_root, plus_root, m), one)
    if cmul(minus_root, minus_root, m) != csub(one, offset):
        raise AssertionError("circle identity failed")
    return offset, plus_root, minus_root


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def clear_denominators(roots: tuple[CElt, ...]) -> tuple[int, tuple[CElt, ...]]:
    scale = reduce(
        lcm, (coordinate.denominator for root in roots for coordinate in root), 1
    )
    return scale, tuple(cscale(root, scale) for root in roots)


@dataclass(frozen=True)
class PureCubicMagicSquare:
    m: int
    roots: tuple[CElt, ...]
    scale: int

    @property
    def values(self) -> tuple[CElt, ...]:
        return tuple(cmul(root, root, self.m) for root in self.roots)


def verify(square: PureCubicMagicSquare) -> bool:
    values = square.values
    if len(set(values)) != 9:
        return False
    rows = (values[0:3], values[3:6], values[6:9])
    zero: CElt = (Fraction(0), Fraction(0), Fraction(0))
    target = reduce(cadd, rows[0], zero)
    lines = [*rows]
    lines.extend(tuple(rows[r][col] for r in range(3)) for col in range(3))
    lines.append(tuple(rows[i][i] for i in range(3)))
    lines.append(tuple(rows[i][2 - i] for i in range(3)))
    return all(reduce(cadd, line, zero) == target for line in lines)


def search(m: int, bound: int, denominator_bound: int) -> PureCubicMagicSquare | None:
    if not is_nontrivial_pure_cubic(m):
        raise ValueError("x^3-m must define a nontrivial cubic field")
    data: dict[CElt, tuple[CElt, CElt]] = {}
    for t in parameter_grid(bound, denominator_bound):
        result = circle_data(t, m)
        if result is None:
            continue
        offset, plus_root, minus_root = result
        data.setdefault(offset, (plus_root, minus_root))
    offsets = set(data)
    one: CElt = (Fraction(1), Fraction(0), Fraction(0))
    for b in offsets:
        for c in offsets:
            bp = cadd(b, c)
            bm = csub(b, c)
            if bp not in offsets or bm not in offsets:
                continue
            roots = (
                data[b][1],
                data[bp][0],
                data[c][1],
                data[bm][0],
                one,
                data[bm][1],
                data[c][0],
                data[bp][1],
                data[b][0],
            )
            scale, integral_roots = clear_denominators(roots)
            candidate = PureCubicMagicSquare(m, integral_roots, scale)
            if verify(candidate):
                return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, nargs="+", required=True)
    parser.add_argument("--parameter-bound", type=int, default=3)
    parser.add_argument("--denominator-bound", type=int, default=2)
    args = parser.parse_args()
    for m in args.m:
        result = search(m, args.parameter_bound, args.denominator_bound)
        if result is None:
            print(
                f"m={m}: no example through parameter bound {args.parameter_bound}, "
                f"denominator bound {args.denominator_bound}"
            )
            continue
        print(f"m={m}: FOUND, denominator-clearing scale={result.scale}")
        for index in range(0, 9, 3):
            print(
                "  roots:",
                " | ".join(cformat(root, m) for root in result.roots[index : index + 3]),
            )
            print(
                "  values:",
                " | ".join(cformat(value, m) for value in result.values[index : index + 3]),
            )


if __name__ == "__main__":
    main()
