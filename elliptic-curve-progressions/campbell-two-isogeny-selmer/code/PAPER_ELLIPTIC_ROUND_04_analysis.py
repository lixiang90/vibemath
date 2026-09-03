"""Exact fourth-round certificate for the Campbell 2-isogeny descent.

This module upgrades the previously complete bad-place matrix to the two
isogeny Selmer groups by recording the standard support/good-prime lemma.  It
also represents the Q x quadratic-field component of z(H) structurally.

This clean certificate contains no proposed Cassels--Tate pairing input.  The
superseded opposite-side proposal is retained only in the separate Round-05
negative audit.  Nothing here decides C_H(Q).
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import sympy as sp

import PAPER_ELLIPTIC_CAMPBELL_analysis as old
import PAPER_ELLIPTIC_NEXT_analysis as nxt


ROOT = Path(__file__).resolve().parent
SCRIPT_PATH = ROOT / "PAPER_ELLIPTIC_ROUND_04_analysis.py"
CERTIFICATE_PATH = ROOT / "PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json"

D_FIELD = 1434501462453361
RESOLVENT_ROOT = 269378023424
QUADRATIC_CONSTANT = -36009487121810563530752
SQRT_DISC_FACTOR = 12288

A_Z = 943720940177342464
B_Z = 3400316

E_A = -591895071
E_B = 58536289153843200
EP_A = -2 * E_A
EP_B = E_A * E_A - 4 * E_B


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def squarefree_part(value: int) -> int:
    answer = -1 if value < 0 else 1
    for prime, exponent in sp.factorint(abs(value)).items():
        if exponent % 2:
            answer *= int(prime)
    return answer


def squareclass_product(left: int, right: int) -> int:
    return squarefree_part(left * right)


def quadratic_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Multiply coefficient pairs for u+v*w, where w^2=D_FIELD."""
    u, v = left
    x, y = right
    return u*x + D_FIELD*v*y, u*y + v*x


def quadratic_norm(pair: tuple[int, int]) -> int:
    u, v = pair
    return u*u - D_FIELD*v*v


def quadratic_field_and_z_certificate() -> dict[str, object]:
    # The quadratic factor is phi^2+r*phi+c.  Its discriminant is
    # (12288)^2*D_FIELD, hence phi=-r/2 +/- 6144*w.
    r = RESOLVENT_ROOT
    c = QUADRATIC_CONSTANT
    discriminant = r*r - 4*c
    assert discriminant == SQRT_DISC_FACTOR**2 * D_FIELD
    assert sp.factorint(D_FIELD) == {59: 1, 71699: 1, 339106321: 1}
    assert D_FIELD % 4 == 1

    phi_plus = (-r // 2, SQRT_DISC_FACTOR // 2)
    phi_minus = (phi_plus[0], -phi_plus[1])
    assert quadratic_multiply(phi_plus, phi_plus)[0] + r*phi_plus[0] + c == 0
    assert quadratic_multiply(phi_plus, phi_plus)[1] + r*phi_plus[1] == 0

    z_q = (A_Z - B_Z*RESOLVENT_ROOT) // 3
    assert 3*z_q == A_Z - B_Z*RESOLVENT_ROOT
    z_k_raw = ((A_Z - B_Z*phi_plus[0]) // 3, (-B_Z*phi_plus[1]) // 3)
    assert z_k_raw == (467235380575281152, -6963847168)
    z_k_conjugate = (z_k_raw[0], -z_k_raw[1])

    # Divide the K component by 64^2, a square in K.  This gives a much
    # smaller representative of the same K*/K*2 class.
    z_k_reduced = (2*57035568917881, -2*850079)
    assert z_k_raw == (64**2*z_k_reduced[0], 64**2*z_k_reduced[1])

    norm_k_raw = quadratic_norm(z_k_raw)
    norm_k_reduced = quadratic_norm(z_k_reduced)
    assert norm_k_raw == 64**4 * norm_k_reduced
    norm_k_square_root_after_35 = 15915620907648
    assert norm_k_reduced == 35 * norm_k_square_root_after_35**2

    z_q_square_root_after_35 = 16257024
    assert z_q == 35 * z_q_square_root_after_35**2
    full_norm = z_q * norm_k_raw
    full_norm_root = 37093056870271943410974720
    assert full_norm == full_norm_root**2

    return {
        "field": {
            "name": "K",
            "definition": f"Q(w)/(w^2-{D_FIELD})",
            "D": D_FIELD,
            "D_factorization": {str(p): int(e) for p, e in sp.factorint(D_FIELD).items()},
            "D_squarefree": True,
            "integral_basis_note": "D=1 mod 4, so O_K=Z[(1+w)/2]; computations use the Q-basis (1,w)",
            "basis": ["1", "w"],
            "multiplication": "(u,v)*(x,y)=(u*x+D*v*y, u*y+v*x)",
            "conjugation": "(u,v)->(u,-v)",
            "norm": "N_K/Q(u,v)=u^2-D*v^2",
        },
        "quadratic_resolvent_factor": {
            "coefficients": [1, r, c],
            "discriminant": discriminant,
            "discriminant_identity": f"{SQRT_DISC_FACTOR}^2*{D_FIELD}",
            "phi_plus_coefficients_in_basis_1_w": list(phi_plus),
            "phi_minus_coefficients_in_basis_1_w": list(phi_minus),
        },
        "etale_algebra": "Q x K",
        "z_components": {
            "Q": {
                "raw": z_q,
                "square_equivalent_representative": 35,
                "identity": f"raw=35*{z_q_square_root_after_35}^2",
            },
            "K": {
                "raw_coefficients_in_basis_1_w": list(z_k_raw),
                "conjugate_coefficients_in_basis_1_w": list(z_k_conjugate),
                "square_equivalent_reduced_coefficients": list(z_k_reduced),
                "scaling_identity": "z_K_raw=64^2*z_K_reduced",
                "raw_norm": norm_k_raw,
                "reduced_norm": norm_k_reduced,
                "reduced_norm_identity": f"N(z_K_reduced)=35*{norm_k_square_root_after_35}^2",
                "norm_squareclass": 35,
            },
        },
        "full_etale_norm": {
            "value": full_norm,
            "square_root": full_norm_root,
            "is_square": True,
            "compatibility": "[N_K/Q(z_K)]=[z_Q]=35, so z_Q*N_K/Q(z_K) is a square",
        },
    }


def scaling_certificate() -> dict[str, object]:
    I, J = old.binary_quartic_invariants()
    u = 64
    small_A = (-27*I) // u**4
    small_B = (-27*J) // u**6
    assert -27*I == u**4*small_A
    assert -27*J == u**6*small_B
    assert small_A == -58243635870855147
    assert small_B == -3811211217040595260188186

    x, X = sp.symbols("x X")
    small_cubic = x**3 + small_A*x + small_B
    translated = sp.expand(small_cubic.subs(x, X-197298357))
    assert translated == X**3 + E_A*X**2 + E_B*X
    assert -3*RESOLVENT_ROOT == u**2*(-197298357)
    return {
        "large_jacobian": "y_big^2=x_big^3-27*I*x_big-27*J",
        "weierstrass_scaling": {
            "u": u,
            "x_big": "64^2*x_small",
            "y_big": "64^3*y_small",
        },
        "small_short_model": {
            "A": small_A,
            "B": small_B,
            "equation": f"y^2=x^3+({small_A})*x+({small_B})",
        },
        "translation": "X=x_small+197298357",
        "translated_E": {
            "a": E_A,
            "b": E_B,
            "equation": f"y^2=X^3+({E_A})*X^2+({E_B})*X",
        },
        "rational_2_torsion_scaling": "-3*phi_0=64^2*(-197298357), hence x_big+3*phi_0=64^2*X",
    }


def is_subgroup(classes: list[int]) -> bool:
    values = set(classes)
    return 1 in values and all(squareclass_product(x, y) in values for x in values for y in values)


def isogeny_selmer_certificate() -> dict[str, object]:
    assert EP_A == 1183790142
    assert EP_B == 116194618458722241
    assert EP_A*EP_A - 4*EP_B == 16*E_B

    rows = old.complete_local_matrix()
    summary = old.matrix_summary(rows)
    survivors_E = summary["surviving_ambient_classes"]["E"]
    survivors_EP = summary["surviving_ambient_classes"]["E_dual"]
    assert survivors_E == [1, 3, 5, 7, 15, 21, 35, 105]
    assert survivors_EP == [1, 4230241, 339106321, D_FIELD]
    assert is_subgroup(survivors_E) and is_subgroup(survivors_EP)

    support_E = sorted(sp.factorint(E_B))
    support_EP = sorted(sp.factorint(EP_B))
    bad_union = sorted(set([2]) | set(support_E) | set(support_EP))
    assert support_E == [2, 3, 5, 7]
    assert support_EP == [3, 59, 71699, 339106321]
    assert bad_union == nxt.BAD_PRIMES
    t, ds, aa, bb = sp.symbols("t ds aa bb")
    generic_quartic = ds*t**4 + aa*t**2 + bb/ds
    generic_discriminant = sp.factor(sp.discriminant(generic_quartic, t))
    assert generic_discriminant == 16*bb*(aa*aa-4*bb)**2
    assert all(
        set(row["places"]) == {"infinity"} | {str(p) for p in bad_union}
        for row in rows
    )

    # Every survivor has an actual Q_v point at every checked finite place;
    # the real-place status is also YES.  Non-survivors have at least one
    # rigorous local obstruction and hence are not Selmer classes.
    for row in rows:
        all_yes = all(cell["status"] == "YES" for cell in row["places"].values())
        if row["d"] in (survivors_E if row["side"] == "E" else survivors_EP):
            assert all_yes

    return {
        "curves_and_isogeny": {
            "E": {"a": E_A, "b": E_B, "kernel": ["O", "(0,0)"]},
            "E_prime": {"a": EP_A, "b": EP_B, "kernel": ["O", "(0,0)"]},
            "phi": "E -> E' has kernel {O,(0,0)}",
            "dual_phi": "E' -> E has kernel {O,(0,0)}",
        },
        "support_lemma": {
            "statement": (
                "For y^2=x^3+a*x^2+b*x, every class in the x-Kummer/isogeny "
                "Selmer group has a squarefree representative supported on primes dividing b. "
                "It is represented by C_d: N^2=dU^4+aU^2V^2+(b/d)V^4."
            ),
            "valuation_proof": (
                "If p does not divide b and v_p(d)=1, first use the original equation. "
                "If V were a unit, (b/d)V^4 would be its unique term of valuation -1, so "
                "the right side could not be a square; hence p divides V.  Primitivity then "
                "makes U a unit, and the original right side has valuation exactly 1, again "
                "not a square.  This argument never assumes that N is p-integral."
            ),
            "candidate_support_E": support_E,
            "candidate_support_E_prime": support_EP,
            "number_of_signed_candidate_classes_on_each_side": 32,
        },
        "good_prime_lemma": {
            "S": ["infinity"] + bad_union,
            "statement": (
                "For p not in S, p>=5 and C_d has smooth genus-one reduction. "
                "Hasse gives #C_d(F_p)>=p+1-2*sqrt(p)>0; every F_p point is smooth "
                "and Hensel lifts to Q_p.  Thus only S must be checked."
            ),
            "quartic_polynomial_discriminant": "16*b*(a^2-4*b)^2",
            "smoothness_discriminant_support": "divides 2*b*(a^2-4b)",
            "all_S_places_checked": True,
        },
        "exact_selmer_groups": {
            "E_side_conventional_name": "Sel^(dual_phi)(E'/Q), identified with locally soluble x-Kummer classes on E",
            "E_side_classes": survivors_E,
            "E_side_generators": [3, 5, 7],
            "E_side_F2_dimension": 3,
            "E_prime_side_conventional_name": "Sel^phi(E/Q), identified with locally soluble x-Kummer classes on E'",
            "E_prime_side_classes": survivors_EP,
            "E_prime_side_generators": [4230241, 339106321],
            "E_prime_side_F2_dimension": 2,
            "rank_upper_bound": 3,
            "rank_formula": "rank(E(Q)) <= dim Sel^(dual_phi)+dim Sel^phi-2 = 3+2-2",
        },
    }


def known_mordell_weil_images() -> dict[str, object]:
    # Only O and the visibly rational 2-torsion points are asserted here.
    assert 0 == 0**3 + E_A*0**2 + E_B*0
    assert 0 == 0**3 + EP_A*0**2 + EP_B*0
    assert squarefree_part(E_B) == 7
    assert squarefree_part(EP_B) == D_FIELD
    return {
        "Kummer_map": "alpha(O)=1; alpha((0,0))=[b]; alpha((x,y))=[x] for x!=0",
        "proved_points_only": {
            "E": [
                {"point": "O", "image": 1},
                {"point": "(0,0)", "image": 7, "identity": "[b]=[7]"},
            ],
            "E_prime": [
                {"point": "O", "image": 1},
                {"point": "(0,0)", "image": D_FIELD, "identity": "[b']=[D]"},
            ],
        },
        "proved_MW_image_subgroups": {
            "E": [1, 7],
            "E_prime": [1, D_FIELD],
        },
        "unexplained_selmer_cosets_not_yet_Sha": {
            "E_mod_known": [[1, 7], [3, 21], [5, 35], [15, 105]],
            "E_prime_mod_known": [[1, D_FIELD], [4230241, 339106321]],
            "warning": "Unknown non-torsion rational points may account for these cosets; they are Sha candidates, not proved Sha classes.",
        },
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-elliptic-campbell-round-04-clean-v2",
        "semantic_version": "2.0.0",
        "source_sha256": {
            SCRIPT_PATH.name: sha256(SCRIPT_PATH),
            old.SCRIPT_PATH.name: sha256(old.SCRIPT_PATH),
            old.NEXT_PATH.name: sha256(old.NEXT_PATH),
        },
        "quadratic_field_and_z": quadratic_field_and_z_certificate(),
        "scaling": scaling_certificate(),
        "isogeny_descent": isogeny_selmer_certificate(),
        "known_mordell_weil_images": known_mordell_weil_images(),
        "supersession": {
            "excluded_fields": [
                "d35_cassels_tate_setup",
                "pairing_bits_to_compute",
                "decisive_outcome",
            ],
            "reason": (
                "The former proposal paired classes from opposite isogeny Selmer groups. "
                "It is not a defined Cassels--Tate pairing and is excluded from this clean "
                "mathematical certificate."
            ),
            "negative_audit": "PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json",
        },
        "claim_boundary": {
            "proved": [
                "the full Q x K coefficient representation, norms, and square scalings of z(H)",
                "the 8 and 4 survivor sets are the exact two isogeny Selmer groups",
                "their F2 dimensions are 3 and 2, giving rank(E(Q)) <= 3",
                "the Kummer images of O and the visible rational 2-torsion points",
            ],
            "not_proved": [
                "the Mordell-Weil rank or full Mordell-Weil Kummer images",
                "that any unexplained Selmer coset is a nonzero Sha class",
                "either Cassels--Tate pairing bit for d=35",
                "C_H(Q) is empty or nonempty",
            ],
        },
    }


def main() -> None:
    certificate = build_certificate()
    CERTIFICATE_PATH.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "selmer": certificate["isogeny_descent"]["exact_selmer_groups"],
        "certificate_status": "CLEAN_NO_PAIRING_FIELDS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
