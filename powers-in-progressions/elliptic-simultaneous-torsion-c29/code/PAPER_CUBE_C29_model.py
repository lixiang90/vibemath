"""Exact algebra certificate for the C29 genus-two model.

Only polynomial arithmetic over QQ and QQ(sqrt(-3)) is used.  This file does
not compute a Mordell--Weil rank and must not be used as such evidence.
"""

from __future__ import annotations

import json
import sympy as sp


r, s, k, X, p, z, d = sp.symbols("r s k X p z d")


def red_d(expr):
    """Reduce a polynomial expression modulo d^2+3."""
    return sp.rem(sp.Poly(sp.expand(expr), d), sp.Poly(d**2 + 3, d)).as_expr()


def assert_zero_in_L(expr):
    """Assert a rational identity in QQ(d)(variables), d^2=-3."""
    numerator = sp.fraction(sp.together(expr))[0]
    assert sp.factor(red_d(numerator)) == 0


def D(v): return v**3 - 3*v**2 + 1
def Q(v): return v**2 - v + 1
def H(v): return v**3 - 6*v**2 + 3*v + 1


f = z**6 + 2*z**5 + 15*z**4 - 20*z**3 + 15*z**2 + 18*z + 33


def main_open_denominators():
    """All denominators in the direct Q-birational charts."""
    return {
        "source_C29_to_rk_to_H29": (D(r), s+2, k, r+2*k),
        "target_H29_to_rk_to_C29": (z**2-1, 4*k-z+1, 1+4*k**3),
    }


def check_original_rs_rk_freeze():
    """Freeze the original C29 (r,s) <-> normalized (r,k) passage."""
    hh = sp.symbols("hh")
    Gsh = sp.expand(s**2*(s+3)+108*hh**3-4)
    F_rk = sp.expand(k*D(r)-(1+4*k**3)*r*(r-1))
    original = sp.expand(s**2*(s+3)*D(r)**3-4*Q(r)**3*H(r))

    # Exact bridge from the original Kubert polynomials to the singular cubic.
    assert sp.factor(D(r)**3-Q(r)**3*H(r)-27*r**3*(r-1)**3) == 0
    h_r = r*(r-1)/D(r)
    original_sh_num = sp.fraction(sp.together(
        original/D(r)**3-Gsh.subs(hh, h_r)
    ))[0]
    assert sp.factor(original_sh_num) == 0

    # Forward and backward normalization maps in the coordinate ring of Gsh.
    k_from_sh = 3*hh/(s+2)
    s_from_k = (1-8*k**3)/(1+4*k**3)
    h_from_k = k/(1+4*k**3)
    s_back_num = sp.fraction(sp.together(
        s_from_k.subs(k, k_from_sh)-s
    ))[0]
    h_back_num = sp.fraction(sp.together(
        h_from_k.subs(k, k_from_sh)-hh
    ))[0]
    assert sp.factor(sp.rem(s_back_num, Gsh, s)) == 0
    assert sp.factor(sp.rem(h_back_num, Gsh, s)) == 0
    assert sp.factor(3*h_from_k/(s_from_k+2)-k) == 0

    # Compose all the way between the original (r,s) model and F(r,k)=0.
    k_from_rs = sp.cancel(3*r*(r-1)/((s+2)*D(r)))
    forward_num = sp.fraction(sp.together(F_rk.subs(k, k_from_rs)))[0]
    assert sp.factor(sp.rem(forward_num, original, s)) == 0
    original_back_num = sp.fraction(sp.together(original.subs(s, s_from_k)))[0]
    assert sp.factor(sp.rem(original_back_num, F_rk, r)) == 0
    k_roundtrip_num = sp.fraction(sp.together(
        k_from_rs.subs(s, s_from_k)-k
    ))[0]
    assert sp.factor(sp.rem(k_roundtrip_num, F_rk, r)) == 0

    # No finite affine source point lies over D=0, even geometrically.
    assert sp.gcd(D(r), Q(r)) == 1
    assert sp.gcd(D(r), H(r)) == 1

    # Homogeneous normalization of the singular cubic, with k=K/L.
    K, L = sp.symbols("K L")
    Sproj = L**3-8*K**3
    Hproj = K*L**2
    Wproj = L**3+4*K**3
    projective_cubic = sp.expand(
        Sproj**2*(Sproj+3*Wproj)+108*Hproj**3-4*Wproj**3
    )
    assert sp.factor(projective_cubic) == 0
    assert [q.subs({K: 1, L: 0}) for q in (Sproj, Hproj, Wproj)] == [-8, 0, 4]

    return {
        "schema": "paper-cube-c29-rs-rk-freeze-v1",
        "original_equation": "s^2(s+3)D(r)^3=4Q(r)^3H(r)",
        "normalized_equation": "kD(r)=(1+4k^3)r(r-1)",
        "forward": "k=3r(r-1)/((s+2)D(r))",
        "backward": "s=(1-8k^3)/(1+4k^3)",
        "forward_denominators": ["D(r)", "s+2"],
        "backward_denominators": ["1+4k^3"],
        "exceptional_fibres": {
            "D(r)=0": "no finite affine source point (gcd(D,Q)=gcd(D,H)=1)",
            "s=-2": "h=0 cusp; normalization value k=infinity",
            "1+4k^3=0": "three geometric points at infinity; none Q-rational",
            "h=0": "r=0,1,infinity over each of s=1,-2 after normalization",
        },
        "status": "EXACT_POLYNOMIAL_CERTIFICATE",
    }


def transvectant(F, G, order, xv, zv):
    """Unnormalised binary transvectant, with its convention explicit."""
    return sp.expand(sum(
        (-1)**i * sp.binomial(order, i)
        * sp.diff(F, xv, order-i, zv, i)
        * sp.diff(G, xv, i, zv, order-i)
        for i in range(order+1)
    ))


def check_kubert_coordinates():
    # Old Tate coordinates and the exact affine change putting 3P at (0,0)
    # and its tangent at Y=0.
    xo, yo, xx, yy = sp.symbols("xo yo xx yy")
    c = r**2*(r-1)
    b = c*(r**2-r+1)
    m = (r-1)*(r+1)
    old = yo**2 + (1-c)*xo*yo - b*yo - xo**3 + b*xo**2
    moved = sp.expand(old.subs({xo: xx+c, yo: yy+m*xx+(b-c)}))
    A1 = -D(r)
    A3 = -r**3*(r-1)**3
    target = yy**2 + A1*xx*yy + A3*yy - xx**3
    assert sp.expand(moved-target) == 0
    assert sp.factor(108*A3/A1**3) == 108*r**3*(r-1)**3/D(r)**3
    return {"A1": str(A1), "A3": str(A3), "change": "xo=xx+c; yo=yy+m*xx+(b-c)"}


def check_normalization_and_descent():
    # The singular cubic in (X,R), normalized by k.
    R = sp.symbols("R")
    Xk = 2*(1-2*k**3)/(1+4*k**3)
    Rk = 3*k/(1+4*k**3)
    assert sp.factor((X**3-3*X+4*R**3-2).subs({X:Xk, R:Rk})) == 0
    sk = (1-8*k**3)/(1+4*k**3)
    h = r*(r-1)/D(r)
    assert sp.factor(sk**2*(sk+3) - (4-108*(k/(1+4*k**3))**3)) == 0

    # The r-cover is k D(r)=(1+4k^3)r(r-1).  Its branch divisor is A*B.
    A = k**2-k+1
    B = 4*k**2+2*k+1
    branch = 9*k**2+3*k*(1+4*k**3)+(1+4*k**3)**2
    assert sp.factor(branch-A*B**2) == 0

    # Kummer description of (3), including the full r <-> w conversion.
    alpha = (1+d)/2
    alphab = (1-d)/2
    beta = (-1-d)/4
    betab = (-1+d)/4
    w = (r-alpha)/(r-alphab)
    f_kummer_h = (2-3*h*(d-1))/(2+3*h*(d+1))
    assert_zero_in_L(w**3-f_kummer_h)

    # After h=k/(1+4k^3), the same Kummer class factors into one simple
    # and one double branch on each conjugate side.
    nk = 8*k**3+3*k+2-3*d*k
    nkbar = 8*k**3+3*k+2+3*d*k
    assert_zero_in_L(nk-8*(k-alpha)*(k-beta)**2)
    assert_zero_in_L(nkbar-8*(k-alphab)*(k-betab)**2)

    # Over L=Q(d), d^2=-3, the hyperelliptic involution is obtained from
    # k -> -1/(2k).  Its quotient coordinate p gives the following conic
    # normalization; eliminating X then gives a sextic over L.
    A0 = (1-3*d)/4
    B0 = (1+3*d)/4
    Lk = (k-alphab)*(k-betab)/k
    Xkummer = k-1/(2*k)
    # Z=Lk*w and p=Z/(X-A0): cubing eliminates w and proves exactly
    # p^3=(X-B0)/(X-A0).  This audits the nontrivial middle of (4)-(5).
    assert_zero_in_L(
        Lk**3*(nk/nkbar)-(Xkummer-A0)**2*(Xkummer-B0)
    )
    Xp = (A0*p**3-B0)/(p**3-1)
    assert red_d((p**3-1)*Xp-(A0*p**3-B0)) == 0
    FL = red_d((A0*p**3-B0)**2 + 2*(p**3-1)**2)
    expected_FL = sp.Rational(3,8)*((1-d)*p**6-20*p**3+(1+d))
    assert red_d(FL-expected_FL) == 0

    # Galois descent p=(z-d)/(z+d), with the anti-invariant ordinate divided
    # by d.  This is the exact identity producing y^2=f(z).
    descent = red_d((1-d)*(z-d)**6 - 20*(z-d)**3*(z+d)**3 + (1+d)*(z+d)**6)
    assert sp.expand(descent + 18*f) == 0

    # The descended birational maps simplify completely over QQ.  On the
    # cubic F(r,k)=0 the forward map is (r,k)->(z,y); conversely (z,y)
    # recovers k,r.  Polynomial remainders independently audit both sides.
    yy = sp.symbols("yy")
    F_rk = sp.expand(k*D(r)-(1+4*k**3)*r*(r-1))
    z_forward = sp.cancel((4*k*r+r-2*k-2)/(r+2*k))
    y_forward = sp.cancel(4*(1-z_forward**2)*(k+1/(2*k)))
    forward_error_num = sp.fraction(sp.together(
        y_forward**2-f.subs(z, z_forward)
    ))[0]
    assert sp.factor(sp.rem(forward_error_num, F_rk, r)) == 0

    k_inverse = sp.cancel(
        (z**3+z**2-9*z-1-yy)/(8*(z**2-1))
    )
    r_inverse = sp.cancel(
        2*(k_inverse*z+k_inverse+1)/(4*k_inverse-z+1)
    )
    inverse_error_num = sp.fraction(sp.together(
        k_inverse*D(r_inverse)
        -(1+4*k_inverse**3)*r_inverse*(r_inverse-1)
    ))[0]
    assert sp.factor(sp.rem(inverse_error_num, yy**2-f, yy)) == 0

    k_roundtrip = k_inverse.subs({z: z_forward, yy: y_forward})
    r_roundtrip = r_inverse.subs({z: z_forward, yy: y_forward})
    assert sp.factor(sp.rem(
        sp.fraction(sp.together(k_roundtrip-k))[0], F_rk, r
    )) == 0
    assert sp.factor(sp.rem(
        sp.fraction(sp.together(r_roundtrip-r))[0], F_rk, r
    )) == 0


    # Target-side compositions: start on H29, return through (r,k), and
    # compare the new (z,y) with the original pair modulo y^2=f(z).
    z_target = sp.cancel(
        (4*k_inverse*r_inverse+r_inverse-2*k_inverse-2)
        /(r_inverse+2*k_inverse)
    )
    y_target = sp.cancel(
        4*(1-z_target**2)*(k_inverse+1/(2*k_inverse))
    )
    assert sp.factor(sp.rem(
        sp.fraction(sp.together(z_target-z))[0], yy**2-f, yy
    )) == 0
    assert sp.factor(sp.rem(
        sp.fraction(sp.together(y_target-yy))[0], yy**2-f, yy
    )) == 0

    disc = sp.discriminant(f, z)
    assert disc == -(2**45)*(3**4)
    ff5 = sp.factor_list(f, modulus=5)
    # A single degree-six factor of exponent one is the actual criterion;
    # no string/rendering comparison is used.
    assert ff5[0] % 5 != 0
    assert len(ff5[1]) == 1
    assert sp.degree(ff5[1][0][0], z) == 6
    assert ff5[1][0][1] == 1
    return {
        "hyperelliptic_model": "Y^2=z^6+2z^5+15z^4-20z^3+15z^2+18z+33",
        "sextic_discriminant": str(disc),
        "discriminant_factorization": "-2^45*3^4",
        "certified_good_primes": "all p not in {2,3}",
        "rational_2_torsion": "0 (sextic irreducible modulo 5)",
        "forward_Q_map": {
            "z": "(4*k*r+r-2*k-2)/(r+2*k)",
            "Y": "4*(1-z^2)*(k+1/(2*k))",
        },
        "inverse_Q_map": {
            "k": "(z^3+z^2-9*z-1-Y)/(8*(z^2-1))",
            "r": "2*(k*z+k+1)/(4*k-z+1)",
            "s": "(1-8*k^3)/(1+4*k^3)",
        },
        "visible_points": ["(-1,8)", "(-1,-8)", "(1,8)", "(1,-8)", "infinity+", "infinity-"],
    }


def check_cusp_branches():
    """Six exact Puiseux (in fact power-series) branch certificates."""
    e = sp.symbols("e")
    D0 = lambda v: v**3-3*v**2+1
    F0 = lambda kval, rval: sp.expand(
        kval*D0(rval)-(1+4*kval**3)*rval*(rval-1)
    )
    # R=1/r chart: this is exactly R^3*F(k,1/R), so it is the regular
    # local equation at r=infinity and must be used for valuation tests.
    F0_recip = lambda kval, Rval: sp.expand(
        kval*(1-3*Rval+Rval**3)
        -(1+4*kval**3)*Rval*(1-Rval)
    )
    zmap = lambda kval, rval: sp.cancel(
        (4*kval*rval+rval-2*kval-2)/(rval+2*kval)
    )
    ymap = lambda kval, zz: sp.cancel(4*(1-zz**2)*(kval+1/(2*kval)))

    branches = [
        # name, k, r or reciprocal r, is_reciprocal, expected z, expected y
        ("k0_r0", e, -e+e**2+e**3-2*e**4, False, sp.oo, 1),
        ("k0_r1", e, 1-e+2*e**2-2*e**3+e**4+e**5, False, -1, 8),
        ("k0_rinf", e, e-2*e**2+2*e**3-e**4-e**5, True, 1, -8),
        ("kinf_r0", 1/e, -e**2/4+e**4/16+e**5/16+e**6/64-e**7/32, False, -1, -8),
        ("kinf_r1", 1/e, 1-e**2/4+e**4/8+e**5/16-e**6/32-e**7/16, False, 1, 8),
        ("kinf_rinf", 1/e, e**2/4-e**4/8-e**5/16+e**6/32+e**7/16, True, sp.oo, -1),
    ]
    rows = []
    for name, kval, rval_or_R, reciprocal, expected_z, expected_y in branches:
        rval = 1/rval_or_R if reciprocal else rval_or_R
        local_equation = (
            F0_recip(kval, rval_or_R) if reciprocal else F0(kval, rval)
        )
        residual = sp.series(local_equation, e, 0, 3).removeO()
        assert residual == 0
        zz = zmap(kval, rval)
        yv = ymap(kval, zz)
        if expected_z is sp.oo:
            assert sp.limit(1/zz, e, 0) == 0
            # expected_y is the sign of Y/z^3 at the selected infinity.
            assert sp.limit(yv/zz**3, e, 0) == expected_y
            image = (sp.oo, expected_y)
        else:
            assert sp.limit(zz, e, 0) == expected_z
            assert sp.limit(yv, e, 0) == expected_y
            image = (expected_z, expected_y)
        rows.append((name, image))
    assert len({image for _, image in rows}) == 6
    return rows


def check_absolute_invariants():
    """A convention-explicit absolute binary-sextic fingerprint."""
    xv, zv = sp.symbols("xv zv")
    F6 = sp.expand(zv**6 * f.subs(z, xv/zv))
    G4 = transvectant(F6, F6, 4, xv, zv)
    H2 = transvectant(F6, G4, 4, xv, zv)
    I2 = transvectant(F6, F6, 6, xv, zv)
    I4 = transvectant(G4, G4, 4, xv, zv)
    I6 = transvectant(H2, H2, 2, xv, zv)
    I10 = sp.discriminant(f, z)
    assert all(not q.free_symbols for q in (I2, I4, I6, I10))
    absolute = tuple(sp.factor(q) for q in (
        I4/I2**2, I6/I2**3, I10/I2**5
    ))
    assert absolute == (
        sp.Integer(24), sp.Integer(24),
        -sp.Rational(1, 2**25*3**16*5**10),
    )
    return {
        "convention": "raw transvectants: I2=(F,F)_6; G=(F,F)_4; I4=(G,G)_4; H=(F,G)_4; I6=(H,H)_2; I10=disc(f)",
        "I2": str(I2), "I4": str(I4), "I6": str(I6), "I10": str(I10),
        "absolute_tuple": [str(v) for v in absolute],
    }


def build_certificate():
    cusp_rows = check_cusp_branches()
    return {
        "schema": "paper-cube-c29-exact-model-v1",
        "original_rs_rk_freeze": check_original_rs_rk_freeze(),
        "kubert": check_kubert_coordinates(),
        "c29": check_normalization_and_descent(),
        "cusps": [
            {
                "branch": name,
                "z": None if image[0] is sp.oo else int(image[0]),
                "Y_or_infinity_sign": int(image[1]),
            }
            for name, image in cusp_rows
        ],
        "absolute_invariants": check_absolute_invariants(),
        "rank_status": "UNKNOWN_FAIL_CLOSED",
        "bad_reduction_exact_status": "AWAITING_AUDITED_MAGMA",
    }


if __name__ == "__main__":
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
