"""Intersect Campbell's seven-term AP family with the j=1728 locus.

Campbell's Theorem 2.5 writes

    y^2 = g3(m) x^3 + g2(m) x^2 + g1(m) x + g0(m).

Putting X=g3*x and Y=g3*y gives a monic Weierstrass equation

    Y^2 = X^3 + g2 X^2 + g3*g1 X + g3^2*g0.

For a model Y^2=X^3+a2*X^2+a4*X+a6, the condition j=1728
(away from singular models) is c6=0, equivalently

    2*a2^3 - 9*a2*a4 + 27*a6 = 0.

The computation below shows that the resulting degree-12 polynomial is
irreducible over Q. Therefore Campbell's parameter m cannot lie in a
quadratic or cubic number field when this family specializes to j=1728.
"""

from __future__ import annotations

from functools import lru_cache

from sympy import Poly, Rational, factor, factor_list, fraction, resultant, symbols


m = symbols("m")
z = symbols("z")

G3 = (
    -18816 * m**4
    + 677376 * m**3
    + 1922543616 * m**2
    - 48944480256 * m
    - 40678301368320
)
G2 = (
    236896 * m**4
    - 9821952 * m**3
    - 22598349824 * m**2
    + 508953231360 * m
    + 520252184657920
)
G1 = (
    -958800 * m**4
    + 40985280 * m**3
    + 89932669440 * m**2
    - 1957723729920 * m
    - 2113363439616000
)
G0 = (
    1292769 * m**4
    - 57304800 * m**3
    - 118795148928 * m**2
    + 2647001548800 * m
    + 2758336954896384
)


def c6_condition():
    """Return the polynomial proportional to c6 for Campbell's family."""
    return factor(2 * G2**3 - 9 * G2 * G3 * G1 + 27 * G3**2 * G0)


def primitive_j1728_polynomial() -> Poly:
    """Return the primitive degree-12 factor defining the j=1728 locus."""
    content, factors = factor_list(c6_condition())
    if content != 16384 or len(factors) != 1 or factors[0][1] != 1:
        raise ArithmeticError("Unexpected factorization of Campbell's c6 condition")
    return Poly(factors[0][0], m, domain="QQ")


def short_weierstrass_coefficient():
    """Coefficient p after shifting to Y^2=Z^3+pZ+q."""
    return factor(G3 * G1 - Rational(1, 3) * G2**2)


@lru_cache(maxsize=1)
def full_2_torsion_polynomial() -> Poly:
    """Minimal candidate polynomial for sqrt(-p(m)) on the j=1728 locus.

    A short j=1728 model Y^2=Z^3+pZ has full rational 2-torsion over its
    coefficient field exactly when -p is a square there.  Eliminating m
    from H12(m)=0 and z^2=-p(m) produces an irreducible degree-24
    polynomial.  Thus adjoining the missing 2-torsion doubles the degree.
    """
    h12 = primitive_j1728_polynomial().as_expr()
    numerator, denominator = fraction(-short_weierstrass_coefficient())
    elimination = resultant(h12, denominator * z**2 - numerator, m)
    _, primitive = Poly(elimination, z, domain="QQ").primitive()
    return primitive


def main() -> None:
    polynomial = primitive_j1728_polynomial()
    print(f"degree={polynomial.degree()}")
    print(f"irreducible over Q={polynomial.is_irreducible}")
    print(polynomial.as_expr())
    print(f"short coefficient p(m)={short_weierstrass_coefficient()}")
    torsion_polynomial = full_2_torsion_polynomial()
    print(f"full-2-torsion extension degree={torsion_polynomial.degree()}")
    print(f"full-2-torsion polynomial irreducible={torsion_polynomial.is_irreducible}")


if __name__ == "__main__":
    main()
