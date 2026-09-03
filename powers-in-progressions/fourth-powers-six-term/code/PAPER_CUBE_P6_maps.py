"""Exact maps and the first finite covering collection for the P_6(4) gate.

Everything here is symbolic over QQ or elementary integral arithmetic.  The
finite-field trace checks live in PAPER_CUBE_P6_gate.py and are regression
tests only; no rank or rational-point completeness is asserted here.
"""

from __future__ import annotations

import json
import math
import sympy as sp


X, Y, Z = sp.symbols("X Y Z")
x, v, u, w = sp.symbols("x v u w")


CURVE_EQUATIONS = {
    "C1": 4*X**4+Z**4-5*Y**4,
    "C2": 3*X**4+2*Z**4-5*Y**4,
}

# (curve, involution): (quartic a,b,c, quotient x, quotient v, lift scale)
# The quotient is v^2=a*x^4+b, (1,c) is its selected rational base point,
# and v/lift_scale must be a square to lift to the original plane quartic.
QUOTIENTS = {
    ("C1", "flip_X"): (-1, 5, 2, Z/Y, 2*X**2/Y**2, 2),
    ("C1", "flip_Z"): (-4, 5, 1, X/Y, Z**2/Y**2, 1),
    ("C1", "flip_Y"): (5, 20, 5, Z/X, 5*Y**2/X**2, 5),
    ("C2", "flip_X"): (-6, 15, 3, Z/Y, 3*X**2/Y**2, 3),
    ("C2", "flip_Z"): (-6, 10, 2, X/Y, 2*Z**2/Y**2, 2),
    ("C2", "flip_Y"): (10, 15, 5, Z/X, 5*Y**2/X**2, 5),
}


def quartic_to_jacobian(x0, v0, a, b, c):
    """Birational main chart v^2=a*x^4+b -> w^2=u^3-4ab*u."""
    assert c*c == a+b
    T = sp.cancel((v0+c+sp.Rational(2)*a*(x0-1)/c)/(x0-1)**2)
    u0 = sp.cancel(2*(c*T+a))
    w0 = sp.cancel(2*c*(T**2-a)*(x0-1)-4*a*(T+c))
    return u0, w0, T


def jacobian_to_quartic(u0, w0, a, b, c):
    """Inverse main chart; the input must lie on w^2=u^3-4ab*u."""
    assert c*c == a+b
    T = sp.cancel((u0/sp.Integer(2)-a)/c)
    q = sp.cancel((w0+4*a*(T+c))/(2*c*(T**2-a)))
    x0 = sp.cancel(1+q)
    v0 = sp.cancel(T*q**2-c-sp.Rational(2)*a*q/c)
    return x0, v0, T


def exact_fourth_root(n):
    """Return the non-negative integral fourth root, or None."""
    if n < 0:
        return None
    r = math.isqrt(math.isqrt(n))
    for q in range(max(0, r-2), r+3):
        if q**4 == n:
            return q
    return None


def check_exceptional_charts():
    """Exact generic audit of the base points and T^2=a divisor."""
    e, aa, cc, tau = sp.symbols("e aa cc tau", nonzero=True)
    bb = cc**2-aa

    # The implicit Taylor coefficients of v at x=1 are obtained from
    # v^2=a(1+e)^4+b, not inserted from the target elliptic curve.
    A1, A2 = sp.symbols("A1 A2")
    vm = -cc+A1*e+A2*e**2
    coeff = sp.Poly(sp.expand(vm**2-aa*(1+e)**4-bb), e)
    sol1 = sp.solve(sp.Eq(coeff.coeff_monomial(e), 0), A1)[0]
    sol2 = sp.solve(
        sp.Eq(coeff.coeff_monomial(e**2).subs(A1, sol1), 0), A2
    )[0]
    assert sp.factor(sol1+2*aa/cc) == 0
    Tminus = sp.factor(sol2)
    assert sp.factor(Tminus-aa*(2*aa-3*cc**2)/cc**3) == 0

    Tminus_from_branch = sp.cancel(
        (vm.subs({A1: sol1, A2: sol2})+cc+2*aa*e/cc)/e**2
    )
    assert sp.factor(sp.limit(Tminus_from_branch, e, 0)-Tminus) == 0

    # Independently solve the positive branch through second order.  Its T
    # numerator has nonzero constant 2c, hence T and u have double poles.
    B1, B2 = sp.symbols("B1 B2")
    vp = cc+B1*e+B2*e**2
    coeffp = sp.Poly(sp.expand(vp**2-aa*(1+e)**4-bb), e)
    psol1 = sp.solve(sp.Eq(coeffp.coeff_monomial(e), 0), B1)[0]
    psol2 = sp.solve(
        sp.Eq(coeffp.coeff_monomial(e**2).subs(B1, psol1), 0), B2
    )[0]
    Tplus_numerator = sp.expand(
        vp.subs({B1: psol1, B2: psol2})+cc+2*aa*e/cc
    )
    assert Tplus_numerator.subs(e, 0) == 2*cc

    # At infinity put a=alpha^2 and e=1/x.  A Laurent expansion of the
    # quartic branch through order e^2 proves all three target limits.
    alpha = sp.symbols("alpha", nonzero=True)
    for sign in (1, -1):
        xinf = 1/e
        vinf = sign*alpha/e**2 + sign*(cc**2-alpha**2)*e**2/(2*alpha)
        Tinf_expr = sp.cancel(
            (vinf+cc+2*alpha**2*(xinf-1)/cc)/(xinf-1)**2
        )
        uinf_expr = 2*(cc*Tinf_expr+alpha**2)
        winf_expr = (
            2*cc*(Tinf_expr**2-alpha**2)*(xinf-1)
            -4*alpha**2*(Tinf_expr+cc)
        )
        Tinf = sign*alpha
        uinf = 2*(cc*Tinf+alpha**2)
        winf = 4*alpha**2*(Tinf+cc)
        assert sp.factor(sp.limit(Tinf_expr, e, 0)-Tinf) == 0
        assert sp.factor(sp.limit(uinf_expr, e, 0)-uinf) == 0
        assert sp.factor(sp.limit(winf_expr, e, 0)-winf) == 0
        assert sp.factor(winf**2-uinf**3+4*alpha**2*(cc**2-alpha**2)*uinf) == 0

    # The other two points over T^2=a are finite quartic points.  Work over
    # Q(tau,c), put a=tau^2, and verify both landing and round trip.
    qminus = -(
        2*tau*cc**3-4*tau**4+6*tau**2*cc**2
    )/(4*tau**2*cc*(tau+cc))
    xminus = sp.cancel(1+qminus)
    vminus = sp.cancel(tau*qminus**2-cc-2*tau**2*qminus/cc)
    assert sp.factor(vminus**2-tau**2*xminus**4-(cc**2-tau**2)) == 0
    uu = 2*(cc*tau+tau**2)
    ww = -4*tau**2*(tau+cc)
    uf, wf, Tf = quartic_to_jacobian(
        xminus, vminus, tau**2, cc**2-tau**2, cc
    )
    assert all(sp.factor(z) == 0 for z in (uf-uu, wf-ww, Tf-tau))
    return {
        "P_plus": "(1,c) -> O (u has a double pole)",
        "P_minus_T_limit": str(Tminus),
        "T2_equals_a_plus_sign": "two quartic points at infinity",
        "T2_equals_a_minus_sign": "two finite quartic points recovered by qminus",
        "qminus": str(sp.factor(qminus)),
    }


def check_six_quotient_maps():
    rows = []
    for (curve, involution), (a, b, c, xq, vq, scale) in QUOTIENTS.items():
        F = CURVE_EQUATIONS[curve]
        quartic_error = sp.cancel(vq**2-a*xq**4-b)
        num = sp.factor(sp.fraction(sp.together(quartic_error))[0])
        assert sp.rem(num, F, X) == 0

        uq, wq, _ = quartic_to_jacobian(x, v, a, b, c)
        elliptic_error = sp.factor(sp.fraction(sp.together(
            wq**2-uq**3+4*a*b*uq
        ))[0])
        assert sp.rem(elliptic_error, v**2-a*x**4-b, v) == 0

        # Both rational-map compositions are exact on their main charts.
        xb, vb, _ = jacobian_to_quartic(uq, wq, a, b, c)
        assert sp.factor(xb-x) == 0
        assert sp.factor(vb-v) == 0
        xj, vj, _ = jacobian_to_quartic(u, w, a, b, c)
        inverse_error = sp.factor(sp.fraction(sp.together(
            vj**2-a*xj**4-b
        ))[0])
        assert sp.rem(inverse_error, w**2-u**3+4*a*b*u, w) == 0
        ub, wb, _ = quartic_to_jacobian(xj, vj, a, b, c)
        assert sp.factor(ub-u) == 0
        assert sp.factor(wb-w) == 0

        # The omitted base point (1,-c) has this finite limiting image;
        # (1,c) is the selected origin and maps to infinity.
        Tminus = sp.Rational(a*(2*a-3*c*c), c**3)
        minus_image = (
            sp.factor(2*(c*Tminus+a)),
            sp.factor(-4*a*(Tminus+c)),
        )
        assert sp.factor(minus_image[1]**2-
                         minus_image[0]**3+4*a*b*minus_image[0]) == 0

        rows.append({
            "curve": curve,
            "involution": involution,
            "quotient": f"v^2={a}*x^4+{b}",
            "plane_to_quartic": {"x": str(xq), "v": str(vq)},
            "lift_condition": f"v/{scale} is a rational square",
            "jacobian": f"w^2=u^3+({-4*a*b})u",
            "quartic_basepoints": {
                "origin": f"(1,{c}) -> O",
                "other": f"(1,{-c}) -> ({minus_image[0]},{minus_image[1]})",
            },
        })
    assert len(rows) == 6
    return rows


def check_total_quotient_conics():
    A, B, C = sp.symbols("A B C")
    conics = {
        "C1": 4*A**2+C**2-5*B**2,
        "C2": 3*A**2+2*C**2-5*B**2,
    }
    for name, conic in conics.items():
        assert conic.subs({A: 1, B: 1, C: 1}) == 0
        assert sp.expand(conic.subs({A: X**2, B: Y**2, C: Z**2})-
                         CURVE_EQUATIONS[name]) == 0
        # A diagonal conic is smooth iff all three gradient coefficients are
        # nonzero: simultaneous vanishing then forces A=B=C=0.
        gradients = [sp.diff(conic, q) for q in (A, B, C)]
        diagonal_coefficients = [sp.diff(g, q) for g, q in zip(gradients, (A, B, C))]
        assert all(co != 0 for co in diagonal_coefficients)
    return {
        "C1": "4A^2+C^2=5B^2, [A:B:C]=[X^2:Y^2:Z^2]",
        "C2": "3A^2+2C^2=5B^2, [A:B:C]=[X^2:Y^2:Z^2]",
        "common_Q_point": "[1:1:1]",
        "genus": 0,
    }


def c1_cover_values(X0, Z0):
    return Z0*Z0-2*X0*Z0+2*X0*X0, Z0*Z0+2*X0*Z0+2*X0*X0


def classify_c1_primitive_cover(X0, Y0, Z0):
    """Classify a primitive odd integral C1 point into its two covers."""
    if math.gcd(math.gcd(abs(X0), abs(Y0)), abs(Z0)) != 1:
        raise ValueError("point is not primitive")
    if 4*X0**4+Z0**4 != 5*Y0**4:
        raise ValueError("point is not on C1")
    A0, B0 = c1_cover_values(X0, Z0)
    assert A0*B0 == 5*Y0**4
    assert math.gcd(A0, B0) == 1
    if A0 % 5:
        R0, S0 = exact_fourth_root(A0), exact_fourth_root(B0//5)
        if R0 is None or S0 is None:
            raise AssertionError("valuation lemma/certificate mismatch")
        return {"label": "A=R^4,B=5S^4", "R": R0, "S": S0}
    R0, S0 = exact_fourth_root(A0//5), exact_fourth_root(B0)
    if R0 is None or S0 is None:
        raise AssertionError("valuation lemma/certificate mismatch")
    return {"label": "A=5R^4,B=S^4", "R": R0, "S": S0}


def check_c1_finite_covering_collection():
    A0 = Z**2-2*X*Z+2*X**2
    B0 = Z**2+2*X*Z+2*X**2
    assert sp.expand(A0*B0-(Z**4+4*X**4)) == 0

    # Each cover implies C1 after Y=R*S.  Conversely, the written gcd lemma
    # puts every primitive integral point in exactly one of these two covers.
    R, S = sp.symbols("R S")
    assert sp.expand((R**4)*(5*S**4)-5*(R*S)**4) == 0
    assert sp.expand((5*R**4)*(S**4)-5*(R*S)**4) == 0

    # Both covers have a rational point, so are everywhere locally soluble;
    # these are the two sign charts of the visible C1 point.
    assert c1_cover_values(1, 1) == (1, 5)
    assert c1_cover_values(1, -1) == (5, 1)
    assert classify_c1_primitive_cover(1, 1, 1)["label"] == "A=R^4,B=5S^4"
    assert classify_c1_primitive_cover(1, 1, -1)["label"] == "A=5R^4,B=S^4"
    return {
        "factorization": "(Z^2-2XZ+2X^2)(Z^2+2XZ+2X^2)=5Y^4",
        "gcd_lemma": (
            "For a primitive C1 point X,Z are coprime; with X,Y,Z odd, "
            "the two positive factors are odd and coprime."
        ),
        "covers": [
            {
                "equations": ["Z^2-2XZ+2X^2=R^4", "Z^2+2XZ+2X^2=5S^4"],
                "map": "Y=+/-R*S",
                "local_status": "EVERYWHERE_LOCALLY_SOLUBLE_BY_POINT",
                "visible_point": "(X,Z,R,S)=(1,1,1,1)",
                "nontrivial_global_status": "UNKNOWN_FAIL_CLOSED",
            },
            {
                "equations": ["Z^2-2XZ+2X^2=5R^4", "Z^2+2XZ+2X^2=S^4"],
                "map": "Y=+/-R*S",
                "local_status": "EVERYWHERE_LOCALLY_SOLUBLE_BY_POINT",
                "visible_point": "(X,Z,R,S)=(1,-1,1,1)",
                "nontrivial_global_status": "UNKNOWN_FAIL_CLOSED",
            },
        ],
        "symmetry": "Z -> -Z exchanges the two covers",
    }


def check_fixed_fields_and_degrees():
    """Record the exact quadratic generators for all six quotient maps."""
    rows = []
    missing = {"flip_X": "X/Y", "flip_Z": "Z/Y", "flip_Y": "Y/X"}
    for (curve, involution), (_a, _b, _c, xq, vq, scale) in QUOTIENTS.items():
        # v/scale is the square of the sole coordinate ratio changed by the
        # involution.  The remaining ratios are generated by x.
        square = sp.cancel(vq/scale)
        expected = {
            "flip_X": X**2/Y**2,
            "flip_Z": Z**2/Y**2,
            "flip_Y": Y**2/X**2,
        }[involution]
        assert sp.cancel(square-expected) == 0
        rows.append({
            "curve": curve,
            "involution": involution,
            "quadratic_generator": missing[involution],
            "minimal_relation": f"q^2=v/{scale}",
            "generic_degree": 2,
            "deck_transformation": involution,
        })
    return rows


def check_dplus_reduction():
    """Reduce D_+ to one genus-one quotient plus a quadratic lift."""
    p, V, q = sp.symbols("p V q")
    xx = 2*p/(1+p**2)
    zz = (1+2*p-p**2)/(1+p**2)
    F = p**4-8*p**3+18*p**2+8*p+1
    assert sp.factor((zz-xx)**2+xx**2-1) == 0
    assert sp.factor((zz+xx)**2+xx**2-F/(1+p**2)**2) == 0
    # 5q^4=F/(1+p^2)^2 and V=q^2(1+p^2).
    assert sp.factor(5*V**2-F) == 5*V**2-F
    assert sp.discriminant(F, p) == 2**17
    assert sp.resultant(F, 1+p**2, p) == 2**9
    return {
        "conic_parameter": {"X/R^2": str(xx), "Z/R^2": str(zz)},
        "elliptic_quartic": "5*V^2=p^4-8p^3+18p^2+8p+1",
        "lift": "q^2=V/(1+p^2), q=S/R",
        "branch_count": 8,
        "cover_genus": 5,
        "status": "GLOBAL_RATIONAL_POINTS_UNKNOWN_FAIL_CLOSED",
    }


def check_dplus_three_elliptic_projections():
    """Give the three C1 elliptic projections and their exact D_+ lifts."""
    R, S = sp.symbols("R S", nonzero=True)
    xx, alpha, beta, gamma, eta = sp.symbols(
        "xx alpha beta gamma eta", nonzero=True
    )
    # Exact reverse-map audit.  After imposing the second square equation,
    # the unused D_+ equation reduces to the relevant quotient quartic.
    Lx = (xx-alpha)**2+alpha**2
    assert sp.factor(
        (eta**2*((xx+alpha)**2+alpha**2)-5).subs(eta**2, Lx)
    ) == 4*alpha**4+xx**4-5
    Lz = (beta-xx)**2+xx**2
    assert sp.factor(
        (eta**2*((beta+xx)**2+xx**2)-5).subs(eta**2, Lz)
    ) == beta**4+4*xx**4-5
    Ly = (xx-1)**2+1
    assert sp.factor(Ly*((xx+1)**2+1)-5*gamma**4) == xx**4+4-5*gamma**4
    rows = []
    lift2 = {
        "flip_X": {
            "equations": ["alpha^2=v/2", "eta^2=(x-alpha)^2+alpha^2"],
            "reconstruction": "(X,Z,R,S)=(alpha*eta,x*eta,eta,1)",
        },
        "flip_Z": {
            "equations": ["beta^2=v", "eta^2=(beta-x)^2+x^2"],
            "reconstruction": "(X,Z,R,S)=(x*eta,beta*eta,eta,1)",
        },
        "flip_Y": {
            "equations": ["gamma^2=v/5", "eta^2=(x-1)^2+1"],
            "reconstruction": "(X,Z,R,S)=(1/eta,x/eta,1,gamma/eta)",
        },
    }
    for involution in ("flip_X", "flip_Z", "flip_Y"):
        a, b, c, xq, vq, scale = QUOTIENTS[("C1", involution)]
        xD = sp.cancel(xq.subs(Y, R*S))
        vD = sp.cancel(vq.subs(Y, R*S))
        uD, wD, _ = quartic_to_jacobian(xD, vD, a, b, c)
        # Direct landing follows from C1, which is the product of the two
        # D_+ equations after Y=RS.  Check the numerator divisibility.
        err = sp.factor(sp.fraction(sp.together(wD**2-uD**3+4*a*b*uD))[0])
        c1D = 4*X**4+Z**4-5*(R*S)**4
        assert sp.rem(err, c1D, Z) == 0
        rows.append({
            "factor": f"E_{-4*a*b}",
            "quartic_coordinates": {"x": str(xD), "v": str(vD)},
            "elliptic_coordinates": {"u": str(sp.factor(uD)), "w": str(sp.factor(wD))},
            "C1_lift": f"v/{scale} is a square",
            "Dplus_lift_tower": lift2[involution],
        })
    assert len(rows) == 3
    return rows


def check_dplus_symmetry_loci():
    """Close the nonzero X=+-Z loci on D_+ by valuations."""
    # X=Z: A=X^2 and B=5X^2, so R^4=S^4=X^2.  A primitive
    # integral representative has |X|=|Y|=|Z|=1.
    # X=-Z: R^4=5X^2, impossible for X != 0 since 4v5(R)=1+2v5(X).
    return {
        "X=Z": "only primitive trivial points |X|=|Y|=|Z|=1",
        "X=-Z": "no nonzero rational point (5-adic parity obstruction)",
        "X=0_or_Z=0": "no nonzero rational point (R^4=5S^4)",
        "proof_status": "ELEMENTARY_COMPLETE_ON_THESE_LOCI",
    }


def build_certificate():
    return {
        "schema": "paper-cube-p6-explicit-maps-v1",
        "six_quotient_maps": check_six_quotient_maps(),
        "exceptional_charts": check_exceptional_charts(),
        "fixed_fields": check_fixed_fields_and_degrees(),
        "total_quotient": check_total_quotient_conics(),
        "c1_finite_covering_collection": check_c1_finite_covering_collection(),
        "dplus_reduction": check_dplus_reduction(),
        "dplus_three_elliptic_projections": check_dplus_three_elliptic_projections(),
        "dplus_symmetry_loci": check_dplus_symmetry_loci(),
        "kani_rosen_status": "PROVED_IN_REPORT_FROM_THREE_QUOTIENT_MAPS_AND_DIFFERENTIAL_CHARACTERS",
        "rank_status": "UNKNOWN_FAIL_CLOSED",
        "rational_points_status": "UNKNOWN_FAIL_CLOSED",
    }


if __name__ == "__main__":
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
