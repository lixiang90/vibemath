"""Exact certificate for a 3-term x-AP in the Moody--Juyal family.

No network or external CAS is used.  SymPy is used only for exact polynomial
identities; the finite-field group law is implemented independently below.
"""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp


q, u, x, t = sp.symbols("q u x t")


def a2(tt):
    return sp.cancel(tt**2 / 4 - 2)


def cubic(xx, tt):
    """Right side of E_t: y^2=x(x^2+(t^2/4-2)x+1)."""
    return sp.factor(xx * (xx**2 + a2(tt) * xx + 1))


def first_point_parameterization(uu=u, qq=q):
    """Birational conic chart forcing x=uu to be a rational point."""
    tt = sp.factor((uu * qq**2 - 4 * (uu - 1) ** 2) / (2 * uu * qq))
    yy = sp.factor(-(uu * qq**2 + 4 * (uu - 1) ** 2) / (4 * qq))
    return tt, yy


T_UQ, Y1_UQ = first_point_parameterization()


# After the first point is parameterized, x=2u and x=-u are square iff
# these binary quartics (in u, over Q(q)) are squares.
Q_ENDPOINT = (
    16 * u**4
    + (24 * q**2 - 64) * u**3
    + (q**4 - 16 * q**2 + 96) * u**2
    - 64 * u
    + 16
)

Q_CENTER = (
    16 * u**4
    - (64 + 24 * q**2) * u**3
    + (q**4 - 16 * q**2 + 96) * u**2
    - (64 + 24 * q**2) * u
    + 16
)


def endpoint_section():
    """The nontrivial third intersection on z^2=Q_ENDPOINT."""
    uu = sp.factor((4 - q**2) / (q**2 + 2))
    zz = sp.factor(4 * uu**2 + (q**2 - 12) * uu + 4)
    tt, yy1 = first_point_parameterization(uu, q)
    yy2 = sp.factor(zz / (2 * q))
    return uu, sp.factor(tt), sp.factor(yy1), yy2, zz


U_SECTION, T_SECTION, Y1_SECTION, Y2_SECTION, Z_SECTION = endpoint_section()


CENTER_SLICE_QUARTIC = u**4 + 14 * u**2 + 1


def center_slice_to_jacobian(uu=u, zz=sp.symbols("z")):
    """Birational map to Y^2=X(X-12)(X-16), valid away from u=0."""
    big_u = sp.cancel((zz + 1) / uu**2)
    XX = sp.factor(2 * big_u + 14)
    YY = sp.factor(2 * uu * (big_u**2 - 1))
    return XX, YY


def rational_ec_add(P, Q, aa=Fraction(-28), bb=Fraction(192)):
    """Group law on y^2=x^3+aa*x^2+bb*x over Q."""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == -y2:
        return None
    if P == Q:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1 + 2 * aa * x1 + bb) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope * slope - aa - x1 - x2
    y3 = -y1 + slope * (x1 - x3)
    return x3, y3


def symbolic_certificate():
    """Return exact zero/factor identities used in the proof."""
    parabola = 4 * u**2 + (q**2 - 12) * u + 4
    inverse_q = sp.factor(T_UQ - 2 * Y1_UQ / u)
    center_s = sp.symbols("center_s")
    center_z = sp.symbols("center_z")
    center_X, center_Y = center_slice_to_jacobian(u, center_z)
    center_map_numerator = sp.together(
        center_Y**2 - center_X * (center_X - 12) * (center_X - 16)
    ).as_numer_denom()[0]
    return {
        "first_point": sp.factor(Y1_UQ**2 - cubic(u, T_UQ)),
        "endpoint_elimination": sp.factor(
            cubic(2 * u, T_UQ) - Q_ENDPOINT / (4 * q**2)
        ),
        "center_elimination": sp.factor(
            cubic(-u, T_UQ) - Q_CENTER / (16 * q**2)
        ),
        "birational_inverse": sp.factor(inverse_q - q),
        "chord_factorization": sp.factor(Q_ENDPOINT - parabola**2),
        "endpoint_quartic_discriminant": sp.factor(sp.discriminant(Q_ENDPOINT, u)),
        "center_quartic_discriminant": sp.factor(sp.discriminant(Q_CENTER, u)),
        "center_genus_zero_quotient": sp.factor(
            Q_CENTER / u**2
            - (
                16 * center_s**2
                - (64 + 24 * q**2) * center_s
                + q**4
                - 16 * q**2
                + 64
            ).subs(center_s, u + 1 / u)
        ),
        "section_curve_discriminant": sp.factor(
            T_SECTION**2 * (T_SECTION**2 - 16)
        ),
        "center_slice_jacobian_map": sp.factor(
            sp.rem(
                center_map_numerator,
                center_z**2 - CENTER_SLICE_QUARTIC,
                center_z,
            )
        ),
        "section_on_first_x": sp.factor(
            Y1_SECTION**2 - cubic(U_SECTION, T_SECTION)
        ),
        "section_on_second_x": sp.factor(
            Y2_SECTION**2 - cubic(2 * U_SECTION, T_SECTION)
        ),
    }


def _mod_fraction(value: Fraction, p: int) -> int:
    if value.denominator % p == 0:
        raise ZeroDivisionError("denominator vanishes modulo p")
    return value.numerator * pow(value.denominator, -1, p) % p


def ff_add(P, Q, p: int, aa: int):
    """Group law on y^2=x^3+aa*x^2+x over F_p."""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        if y1 % p == 0:
            return None
        slope = (3 * x1 * x1 + 2 * aa * x1 + 1) * pow(2 * y1, -1, p)
    else:
        slope = (y2 - y1) * pow((x2 - x1) % p, -1, p)
    slope %= p
    x3 = (slope * slope - aa - x1 - x2) % p
    y3 = (-y1 + slope * (x1 - x3)) % p
    return x3, y3


def ff_mul(n: int, P, p: int, aa: int):
    R = None
    while n:
        if n & 1:
            R = ff_add(R, P, p, aa)
        P = ff_add(P, P, p, aa)
        n //= 2
    return R


def ff_cardinality(p: int, aa: int) -> int:
    total = 1  # point at infinity
    for xx in range(p):
        rhs = (xx**3 + aa * xx**2 + xx) % p
        if rhs == 0:
            total += 1
        elif pow(rhs, (p - 1) // 2, p) == 1:
            total += 2
    return total


def specialization_3_certificate():
    """Exact q=3 and mod-37 certificate proving both sections non-torsion."""
    qq = Fraction(3)
    uu = Fraction(-5, 11)
    tt = Fraction(1519, 330)
    yy1 = Fraction(-529, 1452)
    yy2 = Fraction(749, 726)
    aa = tt * tt / 4 - 2
    delta = tt * tt * (tt * tt - 16)
    p = 37
    aa_p = _mod_fraction(aa, p)
    P = (_mod_fraction(uu, p), _mod_fraction(yy1, p))
    Q = (_mod_fraction(2 * uu, p), _mod_fraction(yy2, p))
    return {
        "q": str(qq),
        "u": str(uu),
        "t": str(tt),
        "P": [str(uu), str(yy1)],
        "Q": [str(2 * uu), str(yy2)],
        "a2": str(aa),
        "prime": p,
        "delta_mod_p": _mod_fraction(delta, p),
        "a2_mod_p": aa_p,
        "P_mod_p": P,
        "Q_mod_p": Q,
        "cardinality": ff_cardinality(p, aa_p),
        "P_multiples": {str(n): ff_mul(n, P, p, aa_p) for n in (8, 20, 40)},
        "Q_multiples": {str(n): ff_mul(n, Q, p, aa_p) for n in (4, 10, 20)},
    }


def validate_all():
    identities = symbolic_certificate()
    zero_keys = {
        "first_point",
        "endpoint_elimination",
        "center_elimination",
        "birational_inverse",
        "center_genus_zero_quotient",
        "section_on_first_x",
        "section_on_second_x",
        "center_slice_jacobian_map",
    }
    assert all(identities[key] == 0 for key in zero_keys)
    assert identities["chord_factorization"] == sp.factor(
        8 * u * (2 * u - 1) * (q**2 * u + q**2 + 2 * u - 4)
    )
    assert identities["endpoint_quartic_discriminant"] == sp.factor(
        -32768 * q**6 * (q**2 - 2) ** 2 * (q**6 - 48 * q**4 + 984 * q**2 - 4096)
    )
    assert identities["center_quartic_discriminant"] == sp.factor(
        262144 * q**6 * (q - 8) * (q + 8) * (q**2 + 8) ** 2 * (q**2 + 16) ** 2
    )

    # The eight displayed points form Z/2 x Z/4 on the Jacobian.
    R = (Fraction(8), Fraction(16))
    S = (Fraction(24), Fraction(48))
    assert rational_ec_add(R, R) == (Fraction(16), Fraction(0))
    assert rational_ec_add(S, S) == (Fraction(16), Fraction(0))

    cert = specialization_3_certificate()
    assert cert["delta_mod_p"] != 0
    assert cert["cardinality"] == 40
    assert cert["P_mod_p"] == (13, 7)
    assert cert["Q_mod_p"] == (26, 2)
    assert cert["P_multiples"] == {
        "8": (34, 29),
        "20": (0, 0),
        "40": None,
    }
    assert cert["Q_multiples"] == {
        "4": (28, 16),
        "10": (0, 0),
        "20": None,
    }
    return identities, cert


if __name__ == "__main__":
    identities, cert = validate_all()
    payload = {
        "sympy_version": sp.__version__,
        "identities": {key: str(value) for key, value in identities.items()},
        "specialization": cert,
        "status": "exact_certificate_passed",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
