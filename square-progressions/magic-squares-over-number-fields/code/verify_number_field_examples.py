"""Exact certificates for degree-four magic squares of algebraic squares."""

from __future__ import annotations

import sympy as sp


def lines(matrix: sp.Matrix) -> list[list[sp.Expr]]:
    result = [[matrix[r, c] for c in range(3)] for r in range(3)]
    result.extend([[matrix[r, c] for r in range(3)] for c in range(3)])
    result.append([matrix[i, i] for i in range(3)])
    result.append([matrix[i, 2 - i] for i in range(3)])
    return result


def certify(roots: sp.Matrix, primitive_element: sp.Expr) -> dict[str, object]:
    values = roots.applyfunc(lambda root: sp.expand(root**2))
    sums = [sp.simplify(sum(line)) for line in lines(values)]
    distinct = all(
        sp.simplify(values[i] - values[j]) != 0
        for i in range(9)
        for j in range(i)
    )
    polynomial = sp.Poly(sp.minpoly(primitive_element))
    return {
        "roots": roots,
        "values": values,
        "line_sums": sums,
        "distinct": distinct,
        "primitive_minpoly": polynomial,
        "field_degree": polynomial.degree(),
    }


def pythagorean_example() -> dict[str, object]:
    """The center-zero example over Q(i,sqrt(7))."""
    i = sp.I
    r7 = sp.sqrt(7)
    roots = sp.Matrix(
        [
            [4, 5 * i, 3],
            [i * r7, 0, r7],
            [3 * i, 5, 4 * i],
        ]
    )
    return certify(roots, i + r7)


def bremner_real_example() -> dict[str, object]:
    """Bremner's totally real example over Q(sqrt(3),sqrt(133))."""
    r3 = sp.sqrt(3)
    r133 = sp.sqrt(133)
    roots = sp.Matrix(
        [
            [5 - 13 * r3, 17 + 9 * r3, 22 - 4 * r3],
            [23 - r3, 2 * r133, 23 + r3],
            [22 + 4 * r3, 17 - 9 * r3, 5 + 13 * r3],
        ]
    )
    return certify(roots, r3 + r133)


def main() -> None:
    for name, example in (
        ("Pythagorean Q(i,sqrt(7))", pythagorean_example()),
        ("Bremner Q(sqrt(3),sqrt(133))", bremner_real_example()),
    ):
        print(name)
        print("roots:")
        print(example["roots"])
        print("values:")
        print(example["values"])
        print("line sums:", example["line_sums"])
        print("distinct:", example["distinct"])
        print("primitive minpoly:", example["primitive_minpoly"].as_expr())
        print("field degree:", example["field_degree"])


if __name__ == "__main__":
    main()
