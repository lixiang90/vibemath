"""Exact searches for 3x3 magic squares over quadratic fields.

The main search implemented here looks for a particularly transparent kind of
quadratic-field example: all nine *values* are rational integers in the two
square classes 1 and d.  Thus every value is either x^2 or d*x^2 and is the
square of the algebraic integer x or x*sqrt(d) in Q(sqrt(d)).

This is only a subsearch of all squares in a quadratic field: a general square
of a+b*sqrt(d) need not be rational.
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce


@dataclass(frozen=True)
class QuadraticMagicSquare:
    d: int
    center: int
    b: int
    c: int
    entries: tuple[int, ...]

    @property
    def rows(self) -> tuple[tuple[int, int, int], ...]:
        return (
            self.entries[0:3],
            self.entries[3:6],
            self.entries[6:9],
        )

    @property
    def magic_sum(self) -> int:
        return 3 * self.center


QElt = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class GeneralQuadraticMagicSquare:
    """A square represented by its nine roots in Q(sqrt(d))."""

    d: int
    roots: tuple[QElt, ...]
    scale: int = 1

    @property
    def values(self) -> tuple[QElt, ...]:
        return tuple(qmul(root, root, self.d) for root in self.roots)


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def is_squarefree(n: int) -> bool:
    n = abs(n)
    if n < 2:
        return True
    p = 2
    while p * p <= n:
        if n % (p * p) == 0:
            return False
        p += 1
    return True


def qadd(x: QElt, y: QElt) -> QElt:
    return x[0] + y[0], x[1] + y[1]


def qneg(x: QElt) -> QElt:
    return -x[0], -x[1]


def qsub(x: QElt, y: QElt) -> QElt:
    return qadd(x, qneg(y))


def qmul(x: QElt, y: QElt, d: int) -> QElt:
    return x[0] * y[0] + d * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def qinv(x: QElt, d: int) -> QElt:
    norm = x[0] * x[0] - d * x[1] * x[1]
    if norm == 0:
        raise ZeroDivisionError
    return x[0] / norm, -x[1] / norm


def qdiv(x: QElt, y: QElt, d: int) -> QElt:
    return qmul(x, qinv(y, d), d)


def qscale(x: QElt, scalar: int | Fraction) -> QElt:
    return scalar * x[0], scalar * x[1]


def qformat(x: QElt, d: int) -> str:
    a, b = x
    if b == 0:
        return str(a)
    if a == 0:
        return f"{b}*sqrt({d})"
    sign = "+" if b > 0 else "-"
    return f"{a}{sign}{abs(b)}*sqrt({d})"


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def clear_root_denominators(roots: tuple[QElt, ...]) -> tuple[int, tuple[QElt, ...]]:
    denominators = [coordinate.denominator for root in roots for coordinate in root]
    scale = reduce(lcm, denominators, 1)
    return scale, tuple(qscale(root, scale) for root in roots)


def circle_data(t: QElt, d: int) -> tuple[QElt, QElt, QElt] | None:
    """Return (offset, plus-root, minus-root) for squares centered at 1.

    The identities are
        x=(1+2t-t^2)/(1+t^2), y=(1-2t-t^2)/(1+t^2),
        x^2=1+offset, y^2=1-offset.
    """
    one: QElt = (Fraction(1), Fraction(0))
    two_t = qscale(t, 2)
    t2 = qmul(t, t, d)
    denominator = qadd(one, t2)
    try:
        plus_root = qdiv(qsub(qadd(one, two_t), t2), denominator, d)
        minus_root = qdiv(qsub(qsub(one, two_t), t2), denominator, d)
    except ZeroDivisionError:
        return None
    offset = qsub(qmul(plus_root, plus_root, d), one)
    if qmul(minus_root, minus_root, d) != qsub(one, offset):
        raise AssertionError("circle parametrization identity failed")
    return offset, plus_root, minus_root


def parameter_grid(bound: int, denominator_bound: int) -> set[QElt]:
    parameters: set[QElt] = set()
    for denominator in range(1, denominator_bound + 1):
        for a in range(-bound, bound + 1):
            for b in range(-bound, bound + 1):
                if math.gcd(math.gcd(abs(a), abs(b)), denominator) != 1:
                    continue
                parameters.add((Fraction(a, denominator), Fraction(b, denominator)))
    return parameters


def qresidue(x: QElt, modulus: int) -> tuple[int, int] | None:
    """Reduce a quadratic-field element modulo a prime.

    A coordinate whose denominator is divisible by ``modulus`` has no affine
    reduction.  Returning ``None`` is intentional: such elements are retained
    by the modular sieve rather than discarded, so the sieve remains exact.
    Only the additive structure is used, hence no condition on ``d`` is needed.
    """

    residues: list[int] = []
    for coordinate in x:
        denominator = coordinate.denominator % modulus
        if denominator == 0:
            return None
        try:
            inverse = pow(denominator, -1, modulus)
        except ValueError:
            return None
        residues.append((coordinate.numerator % modulus) * inverse % modulus)
    return residues[0], residues[1]


def find_offset_configuration(
    offsets: set[QElt],
    modulus: int = 31,
    secondary_modulus: int | None = None,
    tertiary_modulus: int | None = None,
) -> tuple[QElt, QElt] | None:
    """Find ``b,c`` with ``b,c,b+c,b-c`` in ``offsets``.

    The modular stage is only a necessary-condition sieve.  Every surviving
    pair is checked using exact ``Fraction`` arithmetic.  Elements without a
    reduction modulo ``modulus`` are always searched, preserving completeness.
    """

    if modulus < 2:
        raise ValueError("modulus must be at least 2")

    buckets: dict[tuple[int, int], list[QElt]] = {}
    bad_reduction: list[QElt] = []
    for offset in offsets:
        residue = qresidue(offset, modulus)
        if residue is None:
            bad_reduction.append(offset)
        else:
            buckets.setdefault(residue, []).append(offset)

    residues = set(buckets)
    secondary_sieves: list[
        tuple[
            int,
            dict[QElt, tuple[int, int] | None],
            set[tuple[int, int]],
        ]
    ] = []
    for extra_modulus in (secondary_modulus, tertiary_modulus):
        if extra_modulus is None:
            continue
        by_offset: dict[QElt, tuple[int, int] | None] = {}
        extra_residues: set[tuple[int, int]] = set()
        for offset in offsets:
            residue = qresidue(offset, extra_modulus)
            by_offset[offset] = residue
            if residue is not None:
                extra_residues.add(residue)
        secondary_sieves.append((extra_modulus, by_offset, extra_residues))

    def survives_secondary(b: QElt, c: QElt) -> bool:
        for extra_modulus, by_offset, extra_residues in secondary_sieves:
            b_residue = by_offset[b]
            c_residue = by_offset[c]
            if b_residue is None or c_residue is None:
                continue
            b0, b1 = b_residue
            c0, c1 = c_residue
            if (
                (b0 + c0) % extra_modulus,
                (b1 + c1) % extra_modulus,
            ) not in extra_residues or (
                (b0 - c0) % extra_modulus,
                (b1 - c1) % extra_modulus,
            ) not in extra_residues:
                return False
        return True

    allowed_cache: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
    zero: QElt = (Fraction(0), Fraction(0))
    for b in offsets:
        if b == zero:
            continue
        b_residue = qresidue(b, modulus)
        if b_residue is None:
            candidates = offsets
        else:
            allowed = allowed_cache.get(b_residue)
            if allowed is None:
                b0, b1 = b_residue
                allowed = tuple(
                    c_residue
                    for c_residue in residues
                    if (
                        (b0 + c_residue[0]) % modulus,
                        (b1 + c_residue[1]) % modulus,
                    )
                    in residues
                    and (
                        (b0 - c_residue[0]) % modulus,
                        (b1 - c_residue[1]) % modulus,
                    )
                    in residues
                )
                allowed_cache[b_residue] = allowed
            candidates = (
                candidate
                for residue in allowed
                for candidate in buckets[residue]
            )

        for c in candidates:
            if c == zero or c == b or c == qneg(b):
                continue
            if not survives_secondary(b, c):
                continue
            bp = qadd(b, c)
            bm = qsub(b, c)
            signed_offsets = {zero, b, qneg(b), c, qneg(c), bp, qneg(bp), bm, qneg(bm)}
            if len(signed_offsets) != 9:
                continue
            if bp in offsets and bm in offsets:
                return b, c

        # Bad-reduction c values do not occur in the residue buckets above.
        if b_residue is not None:
            for c in bad_reduction:
                if c == zero or c == b or c == qneg(b):
                    continue
                if not survives_secondary(b, c):
                    continue
                bp = qadd(b, c)
                bm = qsub(b, c)
                signed_offsets = {
                    zero,
                    b,
                    qneg(b),
                    c,
                    qneg(c),
                    bp,
                    qneg(bp),
                    bm,
                    qneg(bm),
                }
                if len(signed_offsets) != 9:
                    continue
                if bp in offsets and bm in offsets:
                    return b, c
    return None


def verify_general(square: GeneralQuadraticMagicSquare) -> bool:
    values = square.values
    if len(set(values)) != 9:
        return False
    rows = (values[0:3], values[3:6], values[6:9])
    target = reduce(qadd, rows[0], (Fraction(0), Fraction(0)))
    lines = [*rows]
    lines.extend(tuple(rows[r][col] for r in range(3)) for col in range(3))
    lines.append(tuple(rows[i][i] for i in range(3)))
    lines.append(tuple(rows[i][2 - i] for i in range(3)))
    return all(reduce(qadd, line, (Fraction(0), Fraction(0))) == target for line in lines)


def search_general_quadratic(
    d: int,
    parameter_bound: int,
    denominator_bound: int,
    *,
    modulus: int = 31,
    secondary_modulus: int | None = 43,
    tertiary_modulus: int | None = 47,
    verbose: bool = False,
) -> GeneralQuadraticMagicSquare | None:
    """Search the full Q(sqrt(d)) circle parametrization with center 1."""
    if d in (0, 1) or not is_squarefree(d):
        raise ValueError("d must be a nonzero squarefree integer other than 1")
    data: dict[QElt, tuple[QElt, QElt]] = {}
    parameters = parameter_grid(parameter_bound, denominator_bound)
    for t in parameters:
        result = circle_data(t, d)
        if result is None:
            continue
        offset, plus_root, minus_root = result
        data.setdefault(offset, (plus_root, minus_root))

    offsets = set(data)
    if verbose:
        print(
            f"d={d}: {len(data)} distinct offsets from "
            f"{len(parameters)} parameters"
        )
    configuration = find_offset_configuration(
        offsets, modulus, secondary_modulus, tertiary_modulus
    )
    if configuration is not None:
        b, c = configuration
        bp = qadd(b, c)
        bm = qsub(b, c)
        one: QElt = (Fraction(1), Fraction(0))
        # Positions follow magic_entries(1,b,c).  For each offset t,
        # data[t] stores roots of 1+t and 1-t respectively.
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
        scale, integral_roots = clear_root_denominators(roots)
        candidate = GeneralQuadraticMagicSquare(d, integral_roots, scale)
        if verify_general(candidate):
            return candidate
    return None


def two_square_class_values(d: int, root_bound: int) -> set[int]:
    if d in (0, 1) or not is_squarefree(d):
        raise ValueError("d must be a nonzero squarefree integer other than 1")
    values: set[int] = set()
    for root in range(root_bound + 1):
        q = root * root
        values.add(q)
        values.add(d * q)
    return values


def magic_entries(center: int, b: int, c: int) -> tuple[int, ...]:
    """Return the standard 3-parameter order-3 magic square."""
    a = center
    return (
        a - b,
        a + b + c,
        a - c,
        a + b - c,
        a,
        a - b + c,
        a + c,
        a - b - c,
        a + b,
    )


def verify(square: QuadraticMagicSquare) -> bool:
    entries = square.entries
    if len(set(entries)) != 9:
        return False
    values = two_square_class_values(
        square.d,
        max(
            math.isqrt(abs(x))
            if x >= 0
            else math.isqrt(abs(x // square.d)) if square.d and x % square.d == 0 else 0
            for x in entries
        )
        + 1,
    )
    if any(x not in values for x in entries):
        return False
    rows = square.rows
    target = sum(rows[0])
    lines = [*rows]
    lines.extend(tuple(rows[r][col] for r in range(3)) for col in range(3))
    lines.append(tuple(rows[i][i] for i in range(3)))
    lines.append(tuple(rows[i][2 - i] for i in range(3)))
    return all(sum(line) == target for line in lines)


def search_two_square_classes(
    d: int, root_bound: int, *, nonzero_center: bool = False
) -> QuadraticMagicSquare | None:
    """Search exact integer-valued squares from square classes 1 and d.

    For a fixed center a, an offset t is admissible precisely when both a+t
    and a-t belong to the allowed value set.  A full square needs admissible
    offsets b, c, b+c, and b-c.
    """
    values = two_square_class_values(d, root_bound)
    ordered_values = sorted(values)
    for center in ordered_values:
        if nonzero_center and center == 0:
            continue
        # With d>0 all allowed values are nonnegative; center zero would force
        # every opposite pair to be (0,0), contradicting distinctness.
        if d > 0 and center == 0:
            continue
        offsets = {value - center for value in ordered_values if 2 * center - value in values}
        for b in offsets:
            for c in offsets:
                if b + c not in offsets or b - c not in offsets:
                    continue
                entries = magic_entries(center, b, c)
                if len(set(entries)) != 9:
                    continue
                candidate = QuadraticMagicSquare(d, center, b, c, entries)
                if verify(candidate):
                    return candidate
    return None


def format_root(value: int, d: int) -> str:
    if is_square(value):
        return str(math.isqrt(value))
    if value % d == 0 and is_square(value // d):
        coefficient = math.isqrt(value // d)
        return f"{coefficient}*sqrt({d})"
    raise ValueError(f"{value} is in neither square class 1 nor {d}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=int, nargs="+", required=True)
    parser.add_argument("--root-bound", type=int, default=500)
    parser.add_argument("--nonzero-center", action="store_true")
    parser.add_argument("--general", action="store_true")
    parser.add_argument("--parameter-bound", type=int, default=5)
    parser.add_argument("--denominator-bound", type=int, default=3)
    parser.add_argument("--modulus", type=int, default=31)
    parser.add_argument("--secondary-modulus", type=int, default=43)
    parser.add_argument("--tertiary-modulus", type=int, default=47)
    args = parser.parse_args()
    for d in args.d:
        if args.general:
            started = time.perf_counter()
            result = search_general_quadratic(
                d,
                args.parameter_bound,
                args.denominator_bound,
                modulus=args.modulus,
                secondary_modulus=args.secondary_modulus,
                tertiary_modulus=args.tertiary_modulus,
                verbose=True,
            )
            elapsed = time.perf_counter() - started
            if result is None:
                print(
                    f"d={d}: no general example through parameter bound "
                    f"{args.parameter_bound}, denominator bound {args.denominator_bound} "
                    f"({elapsed:.2f}s)"
                )
                continue
            print(f"d={d}: FOUND, denominator-clearing scale={result.scale}")
            for index in range(0, 9, 3):
                print(
                    "  roots: ",
                    " | ".join(qformat(root, d) for root in result.roots[index : index + 3]),
                )
                print(
                    "  values:",
                    " | ".join(qformat(value, d) for value in result.values[index : index + 3]),
                )
            continue
        result = search_two_square_classes(
            d, args.root_bound, nonzero_center=args.nonzero_center
        )
        if result is None:
            print(f"d={d}: no example through root bound {args.root_bound}")
            continue
        print(f"d={d}: center={result.center}, magic sum={result.magic_sum}")
        for row in result.rows:
            print("  values:", " ".join(str(x) for x in row))
            print("  roots: ", " ".join(format_root(x, d) for x in row))


if __name__ == "__main__":
    main()
