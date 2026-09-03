"""Exact first gate for the two diagonal quartics controlling P_6(4).

This is finite arithmetic only: identities, residue classes, quotient equations,
and small-prime point-count checks.  It does not determine all rational points.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
import sympy as sp


X, Y, Z, U = sp.symbols("X Y Z U")

CURVES = {
    "C1": (4, 1),  # 4 X^4 + Z^4 = 5 Y^4
    "C2": (3, 2),  # 3 X^4 + 2 Z^4 = 5 Y^4
}


def equation(a, b):
    return sp.expand(a*X**4+b*Z**4-5*Y**4)


def is_rational_fourth_power(q):
    q = Fraction(q)
    if q < 0:
        return False
    if q == 0:
        return True
    for integer in (q.numerator, q.denominator):
        n = integer
        prime = 2
        while prime*prime <= n:
            valuation = 0
            while n % prime == 0:
                valuation += 1
                n //= prime
            if valuation % 4:
                return False
            prime += 1
        # The remaining prime, if any, has valuation one.
        if n != 1:
            return False
    return True


def check_ap_equivalence():
    # For positions 0,i,5 the eliminated common-difference equation is
    # (5-i)X^4+iZ^4=5Y^4.  Reflection i<->5-i leaves i=1,2.
    out = {}
    for i, name in [(1, "C1"), (2, "C2")]:
        a, b = CURVES[name]
        assert (a, b) == (5-i, i)
        step = (Z**4-X**4)/5
        assert sp.expand(X**4+i*step-Y**4) == equation(a, b)/5
        out[name] = {"positions": [0, i, 5], "step": "(Z^4-X^4)/5"}
    return out


def check_geometry_and_obvious_points():
    result = {}
    for name, (a, b) in CURVES.items():
        F = equation(a, b)
        # In characteristic zero all three partials vanish only at the
        # forbidden projective origin, hence the plane quartic is smooth g=3.
        partials = [sp.factor(sp.diff(F, v)) for v in (X, Y, Z)]
        assert partials == [4*a*X**3, -20*Y**3, 4*b*Z**3]
        for signs in itertools.product((-1, 1), repeat=3):
            assert F.subs(dict(zip((X, Y, Z), signs))) == 0
        # X=0 and Z=0 would require the displayed rational ratios to be
        # fourth powers; Y=0 has no nonzero real solution.
        assert not is_rational_fourth_power(Fraction(5, b))
        assert not is_rational_fourth_power(Fraction(5, a))
        assert a > 0 and b > 0
        result[name] = {
            "smooth_plane_genus": 3,
            "rational_trivial_projective_points": 4,
            "zero_coordinate_Q_points": 0,
            "rational_points_at_Y_infinity": 0,
        }
    return result


def primitive_residue_solutions(a, b, modulus):
    sol = []
    for xv, yv, zv in itertools.product(range(modulus), repeat=3):
        if math.gcd(math.gcd(math.gcd(xv, yv), zv), modulus) != 1:
            continue
        if (a*xv**4+b*zv**4-5*yv**4) % modulus == 0:
            sol.append((xv, yv, zv))
    return sol


def check_local_classes():
    out = {}
    for name, (a, b) in CURVES.items():
        mod16 = primitive_residue_solutions(a, b, 16)
        assert mod16
        assert {tuple(v % 2 for v in row) for row in mod16} == {(1, 1, 1)}
        # Mod 5 forces X and Z to vanish together or both be units.  The
        # first case is excluded over Q_5 by valuations in a primitive lift.
        mod5 = primitive_residue_solutions(a, b, 5)
        assert all((xv == 0) == (zv == 0) for xv, _, zv in mod5)
        out[name] = {
            "at_2": "primitive integral solutions have X,Y,Z odd",
            "at_5": "X and Z are 5-adic units (valuation argument after mod 5)",
        }
    mod3_c2 = primitive_residue_solutions(*CURVES["C2"], 3)
    assert all((yv == 0) == (zv == 0) for _, yv, zv in mod3_c2)
    out["C2"]["at_3"] = "Y and Z are 3-adic units; X may be divisible by 3"
    return out


def quotient_data():
    # For V^2=a4*x^4+b0, the Jacobian is v^2=u^3-4*a4*b0*u.
    data = {
        "C1": [
            ("flip_X", "V^2=5-Z^4", 20),
            ("flip_Z", "V^2=5-4X^4", 80),
            ("flip_Y", "V^2=20+5Z^4", -400),
        ],
        "C2": [
            ("flip_X", "V^2=15-6Z^4", 360),
            ("flip_Z", "V^2=10-6X^4", 240),
            ("flip_Y", "V^2=15+10Z^4", -600),
        ],
    }
    return {
        name: [
            {"involution": inv, "genus_one_quartic": quartic,
             "jacobian": f"v^2=u^3+({A})u"}
            for inv, quartic, A in rows
        ] for name, rows in data.items()
    }


def count_projective_quartic(a, b, prime):
    affine_nonzero = 0
    for xv, yv, zv in itertools.product(range(prime), repeat=3):
        if xv == yv == zv == 0:
            continue
        if (a*xv**4+b*zv**4-5*yv**4) % prime == 0:
            affine_nonzero += 1
    return affine_nonzero // (prime-1)


def count_elliptic(A, prime):
    return 1 + sum(
        1 for xv, yv in itertools.product(range(prime), repeat=2)
        if (yv*yv-xv**3-A*xv) % prime == 0
    )


def check_jacobian_split_traces():
    # Kani--Rosen for the three commuting sign involutions gives the candidate
    # Q-isogeny J(C)~E1*E2*E3.  These point counts independently catch signs
    # or twists in the displayed quotient Jacobians; they are not the proof.
    elliptic_As = {"C1": [20, 80, -400], "C2": [360, 240, -600]}
    audit = {}
    for name, (a, b) in CURVES.items():
        rows = []
        for prime in (7, 11, 13, 17, 19):
            nc = count_projective_quartic(a, b, prime)
            ne = [count_elliptic(A, prime) for A in elliptic_As[name]]
            assert nc == sum(ne)-2*(prime+1)
            rows.append((prime, nc, tuple(ne)))
        audit[name] = rows
    return audit


def build_certificate():
    return {
        "schema": "paper-cube-p6-fourth-power-gate-v1",
        "ap_equivalence": check_ap_equivalence(),
        "geometry": check_geometry_and_obvious_points(),
        "local_classes": check_local_classes(),
        "elliptic_quotients": quotient_data(),
        "split_trace_audit": check_jacobian_split_traces(),
        "rational_points_status": "UNKNOWN_FAIL_CLOSED",
    }


if __name__ == "__main__":
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
