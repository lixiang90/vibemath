"""Exact elliptic-curve search for 3x3 magic squares with many squares.

The curve is E_n: y^2 = x^3 - n^2 x.  If P is rational, the
x-coordinate X of 2P has the property that X-n, X, X+n are rational
squares.  Three such X-coordinates in arithmetic progression give a
3x3 magic square of nine rational squares.  Two certified centers and
one additional square in the third triple give a seven-square candidate.

All arithmetic in this module is exact (fractions.Fraction).
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import urllib.parse
import urllib.request
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from typing import Iterable, Iterator, Sequence


Point = tuple[Fraction, Fraction] | None

_SQUARE_RESIDUE_FILTERS = tuple(
    (modulus, frozenset((value * value) % modulus for value in range(modulus)))
    for modulus in (256, 63, 65, 11, 17, 19, 23, 29, 31)
)
_LOCAL_SIEVE_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67)
_LOCAL_SQUARES = {
    prime: frozenset((value * value) % prime for value in range(prime))
    for prime in _LOCAL_SIEVE_PRIMES
}


def add_points(p: Point, q: Point, n: int) -> Point:
    """Add two points on y^2 = x^3 - n^2*x."""
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and y1 == -y2:
        return None
    if p == q:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1 - n * n) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope * slope - x1 - x2
    y3 = slope * (x1 - x3) - y1
    return x3, y3


def multiply_point(k: int, p: Point, n: int) -> Point:
    """Multiply a curve point by an integer using double-and-add."""
    if k < 0:
        if p is None:
            return None
        return multiply_point(-k, (p[0], -p[1]), n)
    result: Point = None
    addend = p
    while k:
        if k & 1:
            result = add_points(result, addend, n)
        addend = add_points(addend, addend, n)
        k >>= 1
    return result


def linear_combination(coefficients: Sequence[int], generators: Sequence[Point], n: int) -> Point:
    result: Point = None
    for coefficient, generator in zip(coefficients, generators, strict=True):
        result = add_points(result, multiply_point(coefficient, generator, n), n)
    return result


def point_is_on_curve(point: Point, n: int) -> bool:
    if point is None:
        return True
    x, y = point
    return y * y == x * x * x - n * n * x


def rational_square_root(value: Fraction) -> Fraction | None:
    """Return the nonnegative rational square root, or None."""
    if value < 0:
        return None
    for modulus, residues in _SQUARE_RESIDUE_FILTERS:
        if value.numerator % modulus not in residues:
            return None
        if value.denominator % modulus not in residues:
            return None
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator:
        return None
    if denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def is_rational_square(value: Fraction) -> bool:
    return rational_square_root(value) is not None


@dataclass(frozen=True)
class CertifiedCenter:
    x: Fraction
    coefficients: tuple[int, ...]


@dataclass(frozen=True)
class Candidate:
    n: int
    centers: tuple[Fraction, Fraction, Fraction]
    rational_grid: tuple[tuple[Fraction, Fraction, Fraction], ...]
    integer_grid: tuple[tuple[int, int, int], ...]
    square_count: int
    certified_coefficients: tuple[tuple[int, ...], tuple[int, ...]]

    @property
    def magic_sum(self) -> int:
        return sum(self.integer_grid[0])

    def as_dict(self) -> dict[str, object]:
        def fraction_text(value: Fraction) -> str:
            return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

        return {
            "n": self.n,
            "centers": [fraction_text(value) for value in self.centers],
            "integer_grid": [list(row) for row in self.integer_grid],
            "magic_sum": self.magic_sum,
            "square_count": self.square_count,
            "certified_coefficients": [list(item) for item in self.certified_coefficients],
        }


def enumerate_certified_centers(
    n: int,
    generators: Sequence[Point],
    box: int,
) -> list[CertifiedCenter]:
    """Enumerate distinct x(2P) for generator coefficients in [-box, box]."""
    for generator in generators:
        if not point_is_on_curve(generator, n):
            raise ValueError(f"Generator {generator!r} is not on E_{n}")

    by_x: dict[Fraction, tuple[int, ...]] = {}
    coefficient_range = tuple(range(-box, box + 1))
    multiple_tables = [
        {coefficient: multiply_point(coefficient, generator, n) for coefficient in coefficient_range}
        for generator in generators
    ]
    for coefficients in itertools.product(coefficient_range, repeat=len(generators)):
        if all(coefficient == 0 for coefficient in coefficients):
            continue
        # P and -P have the same x(2P), so keep one sign representative.
        first_nonzero = next(coefficient for coefficient in coefficients if coefficient)
        if first_nonzero < 0:
            continue
        point: Point = None
        for coefficient, table in zip(coefficients, multiple_tables, strict=True):
            point = add_points(point, table[coefficient], n)
        doubled = add_points(point, point, n)
        if doubled is None:
            continue
        x = doubled[0]
        if x <= n:
            continue
        if not all(is_rational_square(value) for value in (x - n, x, x + n)):
            raise ArithmeticError(f"Doubling certificate failed for E_{n}, x={x}")
        by_x.setdefault(x, tuple(coefficients))
    return [CertifiedCenter(x, by_x[x]) for x in sorted(by_x)]


def certified_center_progressions(
    centers: Sequence[CertifiedCenter],
) -> list[tuple[CertifiedCenter, CertifiedCenter, CertifiedCenter]]:
    """Find exact three-term APs consisting entirely of certified centers."""
    ordered = sorted(centers, key=lambda center: center.x)
    by_x = {center.x: center for center in ordered}
    # A large-prime residue filter avoids constructing millions of enormous
    # Fraction midpoints.  It cannot reject a rational AP: reduction modulo a
    # prime preserves 2*middle=left+right whenever denominators are invertible.
    filter_prime = 1_000_003
    residues = {center.x: fraction_mod(center.x, filter_prime) for center in ordered}
    residue_set = {residue for residue in residues.values() if residue is not None}
    inverse_two = pow(2, -1, filter_prime)
    progressions: list[tuple[CertifiedCenter, CertifiedCenter, CertifiedCenter]] = []
    for left_index, left in enumerate(ordered):
        for right in ordered[left_index + 1 :]:
            left_residue = residues[left.x]
            right_residue = residues[right.x]
            if left_residue is not None and right_residue is not None:
                midpoint_residue = (left_residue + right_residue) * inverse_two % filter_prime
                if midpoint_residue not in residue_set:
                    continue
            total = left.x + right.x
            middle = by_x.get(total / 2)
            if middle is not None:
                progressions.append((left, middle, right))
    return progressions


def magic_grid_from_centers(n: int, centers: Sequence[Fraction]) -> tuple[tuple[Fraction, Fraction, Fraction], ...]:
    """Build Bremner's magic-square form from an increasing 3-term AP."""
    if len(centers) != 3:
        raise ValueError("Exactly three centers are required")
    low, middle, high = sorted(centers)
    if low + high != 2 * middle:
        raise ValueError("Centers are not in arithmetic progression")
    a = middle
    b = high - middle
    c = Fraction(n)
    return (
        (a - b, a + b + c, a - c),
        (a + b - c, a, a - b + c),
        (a + c, a - b - c, a + b),
    )


def verify_magic_grid(grid: Sequence[Sequence[Fraction]]) -> bool:
    target = sum(grid[0])
    lines = [
        *grid,
        *zip(*grid),
        (grid[0][0], grid[1][1], grid[2][2]),
        (grid[0][2], grid[1][1], grid[2][0]),
    ]
    return all(sum(line) == target for line in lines)


def scale_grid_to_integers(
    grid: Sequence[Sequence[Fraction]],
) -> tuple[tuple[int, int, int], ...]:
    """Multiply by the smallest obvious common square clearing denominators."""
    denominator_roots: list[int] = []
    for value in itertools.chain.from_iterable(grid):
        root = math.isqrt(value.denominator)
        if root * root != value.denominator:
            raise ValueError(f"Non-square denominator {value.denominator} in {value}")
        denominator_roots.append(root)
    scale_root = math.lcm(*denominator_roots)
    scale = scale_root * scale_root
    integer_grid = tuple(
        tuple(int(value * scale) for value in row)
        for row in grid
    )
    common = reduce(math.gcd, itertools.chain.from_iterable(integer_grid))
    square_divisor_root = 1
    factor = 2
    remainder = common
    while factor * factor <= remainder:
        exponent = 0
        while remainder % factor == 0:
            remainder //= factor
            exponent += 1
        square_divisor_root *= factor ** (exponent // 2)
        factor += 1 if factor == 2 else 2
    square_divisor = square_divisor_root * square_divisor_root
    if square_divisor > 1:
        integer_grid = tuple(
            tuple(value // square_divisor for value in row)
            for row in integer_grid
        )
    return integer_grid


def closure_values(x: Fraction, y: Fraction) -> Iterator[Fraction]:
    """All third terms of an AP containing x and y."""
    yield 2 * y - x
    yield 2 * x - y
    yield (x + y) / 2


def fraction_mod(value: Fraction, prime: int) -> int | None:
    denominator = value.denominator % prime
    if denominator == 0:
        return None
    return (value.numerator % prime) * pow(denominator, -1, prime) % prime


def local_third_square_mask(
    left_residues: Sequence[int | None],
    right_residues: Sequence[int | None],
    n: int,
    closure_index: int,
) -> int:
    """Return bits for third-n, third, third+n surviving local square tests."""
    mask = 0b111
    for prime, left, right in zip(
        _LOCAL_SIEVE_PRIMES, left_residues, right_residues, strict=True
    ):
        if left is None or right is None:
            continue
        if closure_index == 0:
            third = (2 * right - left) % prime
        elif closure_index == 1:
            third = (2 * left - right) % prime
        else:
            third = (left + right) * pow(2, -1, prime) % prime
        residues = _LOCAL_SQUARES[prime]
        for bit, offset in enumerate((-n, 0, n)):
            if mask & (1 << bit) and (third + offset) % prime not in residues:
                mask &= ~(1 << bit)
        if mask == 0:
            break
    return mask


def search_curve(
    n: int,
    generators: Sequence[Point],
    box: int = 10,
    minimum_squares: int = 7,
) -> tuple[list[CertifiedCenter], list[Candidate]]:
    centers = enumerate_certified_centers(n, generators, box)
    local_residues = {
        center.x: tuple(fraction_mod(center.x, prime) for prime in _LOCAL_SIEVE_PRIMES)
        for center in centers
    }
    candidates: dict[tuple[int, ...], Candidate] = {}
    for left, right in itertools.combinations(centers, 2):
        for closure_index, third in enumerate(closure_values(left.x, right.x)):
            if local_third_square_mask(
                local_residues[left.x],
                local_residues[right.x],
                n,
                closure_index,
            ) == 0:
                continue
            ordered = tuple(sorted((left.x, right.x, third)))
            if ordered[0] <= 0 or ordered[0] + ordered[2] != 2 * ordered[1]:
                continue
            third_square_count = sum(
                is_rational_square(value)
                for value in (third - n, third, third + n)
            )
            # The two enumerated doubled points already certify six cells.
            # Avoid constructing and testing the full grid unless the inferred
            # third center can contribute enough additional square cells.
            if 6 + third_square_count < minimum_squares:
                continue
            grid = magic_grid_from_centers(n, ordered)
            flat = tuple(itertools.chain.from_iterable(grid))
            if any(value <= 0 for value in flat) or len(set(flat)) != 9:
                continue
            square_count = sum(is_rational_square(value) for value in flat)
            if square_count < minimum_squares:
                continue
            if not verify_magic_grid(grid):
                raise ArithmeticError("Internal magic-grid reconstruction failed")
            integer_grid = scale_grid_to_integers(grid)
            normalized_key = tuple(sorted(integer_grid[0] + integer_grid[1] + integer_grid[2]))
            candidates.setdefault(
                normalized_key,
                Candidate(
                    n=n,
                    centers=ordered,
                    rational_grid=grid,
                    integer_grid=integer_grid,
                    square_count=square_count,
                    certified_coefficients=(left.coefficients, right.coefficients),
                ),
            )
    return centers, sorted(candidates.values(), key=lambda item: (item.square_count, item.magic_sum))


def fetch_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": "magic-square-research/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def fetch_lmfdb_generators(label: str) -> list[Point]:
    query = urllib.parse.urlencode({"lmfdb_label": label, "_format": "json"})
    payload = fetch_json(f"https://www.lmfdb.org/api/ec_mwbsd/?{query}")
    rows = payload.get("data", [])
    if not rows:
        raise LookupError(f"No Mordell-Weil data returned for {label}")
    generators: list[Point] = []
    for x_projective, y_projective, z_projective in rows[0]["gens"]:
        if z_projective == 0:
            raise ValueError("The point at infinity cannot be a generator")
        generators.append(
            (Fraction(x_projective, z_projective), Fraction(y_projective, z_projective))
        )
    return generators


def parse_generator(text: str) -> Point:
    x_text, y_text = text.split(",", maxsplit=1)
    return Fraction(x_text), Fraction(y_text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True, help="squarefree congruent-curve parameter")
    parser.add_argument("--box", type=int, default=10, help="coefficient box [-B,B]")
    parser.add_argument("--minimum-squares", type=int, default=7, choices=(7, 8, 9))
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--lmfdb-label", help="fetch generators from LMFDB ec_mwbsd")
    source.add_argument(
        "--generator",
        action="append",
        help="affine generator x,y; repeat once per generator",
    )
    args = parser.parse_args()

    if args.lmfdb_label:
        generators = fetch_lmfdb_generators(args.lmfdb_label)
    else:
        generators = [parse_generator(text) for text in args.generator]
    centers, candidates = search_curve(
        args.n,
        generators,
        box=args.box,
        minimum_squares=args.minimum_squares,
    )
    output = {
        "n": args.n,
        "box": args.box,
        "generators": [None if point is None else [str(point[0]), str(point[1])] for point in generators],
        "certified_centers": len(centers),
        "candidates": [candidate.as_dict() for candidate in candidates],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
