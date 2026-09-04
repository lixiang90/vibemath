"""Round-11 audit upgrading the local survivor rows to isogeny Selmer groups.

The old 512-cell certificate intentionally called its output an ambient local
set.  This module supplies the missing convention/support audit: it checks the
two isogenies and the covering map symbolically, verifies the complete set of
places, revalidates every finite positive witness for the surviving rows, and
then applies the standard local definition of an isogeny Selmer group.

It proves only an upper bound for the Mordell--Weil rank.  It does not compute
the exact rank, the full 2-Selmer group, or a rational ninth point.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUTPUT = PROJECT / "certificates" / "round11_isogeny_selmer_audit.json"
LOCAL_MATRIX = PROJECT / "certificates" / "local_matrix_512.json"
ROUND09 = PROJECT / "certificates" / "round09_two_place_gate.json"
ROUND10 = PROJECT / "certificates" / "round10_eprime_two_three_gate.json"

E_A = -591_895_071
E_B = 58_536_289_153_843_200
EP_A = 1_183_790_142
EP_B = 116_194_618_458_722_241
Q = 339_106_321
R = 59 * 71_699
D = R * Q

SIDES = {
    "E": {"a": E_A, "b": E_B, "support": (2, 3, 5, 7)},
    "E_dual": {"a": EP_A, "b": EP_B, "support": (3, 59, 71_699, Q)},
}
BAD_FINITE_PLACES = (2, 3, 5, 7, 59, 71_699, Q)
E_REAL_CANDIDATES = tuple(
    math.prod(subset)
    for size in range(5)
    for subset in itertools.combinations((2, 3, 5, 7), size)
)
E_SELMER = (1, 3, 5, 7, 15, 21, 35, 105)
EP_SELMER = (1, R, Q, D)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valuation(value: int, prime: int) -> int:
    assert value
    answer = 0
    value = abs(value)
    while value % prime == 0:
        value //= prime
        answer += 1
    return answer


def is_prime_trial(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def signed_squareclasses(support: tuple[int, ...]) -> tuple[int, ...]:
    positive = [
        math.prod(subset)
        for size in range(len(support) + 1)
        for subset in itertools.combinations(support, size)
    ]
    return tuple(sorted(positive + [-value for value in positive]))


def legendre(value: int, prime: int) -> int:
    assert is_prime_trial(prime) and value % prime
    residue = pow(value % prime, (prime - 1) // 2, prime)
    assert residue in (1, prime - 1)
    return 1 if residue == 1 else -1


def squarefree_part(value: int) -> int:
    sign = -1 if value < 0 else 1
    value = abs(value)
    answer = sign
    divisor = 2
    while divisor * divisor <= value:
        exponent = 0
        while value % divisor == 0:
            value //= divisor
            exponent += 1
        if exponent % 2:
            answer *= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        answer *= value
    return answer


def squareclass_product(left: int, right: int) -> int:
    return squarefree_part(left * right)


def is_squareclass_subgroup(classes: tuple[int, ...]) -> bool:
    values = set(classes)
    return 1 in values and all(
        squareclass_product(left, right) in values
        for left in values
        for right in values
    )


def q2_square(value: int) -> bool:
    if value == 0:
        return True
    exponent = valuation(value, 2)
    unit = value // 2**exponent
    return exponent % 2 == 0 and unit % 8 == 1


def odd_qp_square(value: int, prime: int) -> bool:
    if value == 0:
        return True
    exponent = valuation(value, prime)
    unit = value // prime**exponent
    return exponent % 2 == 0 and legendre(unit, prime) == 1


def quartic_rhs(side: str, d: int, U: int, V: int) -> int:
    data = SIDES[side]
    a, b = data["a"], data["b"]
    assert b % d == 0
    return d * U**4 + a * U**2 * V**2 + (b // d) * V**4


def symbolic_map_audit() -> dict[str, object]:
    x, y, a, b, d, u, n = sp.symbols("x y a b d u n")
    curve = x**3 + a*x**2 + b*x
    xp = y**2 / x**2
    yp = y*(b-x**2) / x**2
    target = xp**3 - 2*a*xp**2 + (a*a-4*b)*xp
    direct = sp.factor(sp.together(yp**2-target).subs(y**2, curve))

    xback = yp**2 / (4*xp**2)
    yback = yp*((a*a-4*b)-xp**2) / (8*xp**2)
    dual_target = xback**3 + a*xback**2 + b*xback
    dual = sp.factor(sp.together(yback**2-dual_target).subs(y**2, curve))

    slope = (3*x**2+2*a*x+b)/(2*y)
    doubled_x = slope**2-a-2*x
    composition = sp.factor(sp.together(xback-doubled_x).subs(y**2, curve))

    cover_left = d**2*u**2*n**2
    cover_relation = d*u**4+a*u**2+b/d
    cover_right = (d*u**2)**3+a*(d*u**2)**2+b*(d*u**2)
    cover = sp.factor(cover_left.subs(n**2, cover_relation)-cover_right)
    assert direct == dual == composition == cover == 0
    return {
        "E": "y^2=x^3+a*x^2+b*x",
        "E_prime": "Y^2=X^3-2*a*X^2+(a^2-4*b)*X",
        "phi": "(x,y)->(y^2/x^2, y*(b-x^2)/x^2)",
        "dual_phi": (
            "(X,Y)->(Y^2/(4*X^2), "
            "Y*((a^2-4*b)-X^2)/(8*X^2))"
        ),
        "composition_x_coordinate_equals_doubling": True,
        "cover": "N^2=d*U^4+a*U^2*V^2+(b/d)*V^4",
        "cover_to_same_side_affine": "x=d*(U/V)^2; y=d*U*N/V^3",
        "cover_map_identity": True,
        "Kummer_convention": (
            "alpha(O)=1, alpha((0,0))=[b], alpha((x,y))=[x] for x!=0"
        ),
    }


def support_and_places_audit() -> dict[str, object]:
    assert EP_A == -2*E_A and EP_B == E_A*E_A-4*E_B
    assert EP_A*EP_A-4*EP_B == 16*E_B
    assert E_B == 2**18 * 3**12 * 5**2 * 7**5
    assert EP_B == 3**4 * 59 * 71_699 * Q
    assert all(is_prime_trial(p) for p in (2, 3, 5, 7, 59, 71_699, Q))
    union = tuple(sorted({2, 3, 5, 7, 59, 71_699, Q}))
    assert union == BAD_FINITE_PLACES
    return {
        "support_lemma": (
            "A Selmer squareclass has a signed squarefree representative supported "
            "on b: if p does not divide b and v_p(d)=1, a primitive local solution "
            "is impossible by the unique odd-valuation term argument."
        ),
        "E_b_factorization": {"2": 18, "3": 12, "5": 2, "7": 5},
        "E_prime_b_factorization": {
            "3": 4, "59": 1, "71699": 1, str(Q): 1
        },
        "finite_places_requiring_checks": list(BAD_FINITE_PLACES),
        "real_place_required": True,
        "good_prime_bridge": (
            "For p outside the displayed set the quartic discriminant "
            "16*b*(a^2-4*b)^2 is a p-adic unit. The smooth proper genus-one "
            "reduction has an F_p-point by Hasse and it lifts by Hensel."
        ),
        "all_other_finite_places_automatic": True,
    }


def load_matrix() -> dict[str, object]:
    return json.loads(LOCAL_MATRIX.read_text(encoding="utf-8"))


def validate_finite_yes_cell(row: dict[str, object], prime: int) -> None:
    cell = row["places"][str(prime)]
    assert cell["status"] == "YES"
    witness = cell["witness"]
    U, V = int(witness["U"]), int(witness["V"])
    assert U % prime or V % prime
    rhs = quartic_rhs(row["side"], int(row["d"]), U, V)
    assert rhs == int(witness["rhs"])
    assert q2_square(rhs) if prime == 2 else odd_qp_square(rhs, prime)


def local_to_selmer_audit() -> dict[str, object]:
    matrix = load_matrix()
    assert matrix["checked_places"] == [
        "infinity", "2", "3", "5", "7", "59", "71699", str(Q)
    ]
    rows = {(row["side"], int(row["d"])): row for row in matrix["rows"]}
    assert len(rows) == 64
    assert set(d for side, d in rows if side == "E") == set(
        signed_squareclasses(SIDES["E"]["support"])
    )
    assert set(d for side, d in rows if side == "E_dual") == set(
        signed_squareclasses(SIDES["E_dual"]["support"])
    )

    # The 16 positive E-side classes pass the real condition.  Exactly the
    # eight even ones fail the uniform p=59 criterion (d/59)=1.
    assert set(E_REAL_CANDIDATES) == {
        d for side, d in rows if side == "E" and d > 0
    }
    e_rejected = tuple(d for d in E_REAL_CANDIDATES if legendre(d, 59) == -1)
    e_survivors = tuple(d for d in E_REAL_CANDIDATES if legendre(d, 59) == 1)
    assert e_rejected == (2, 6, 10, 14, 30, 42, 70, 210)
    assert e_survivors == E_SELMER
    for d in e_rejected:
        assert rows[("E", d)]["places"]["59"]["status"] == "NO"

    # Round 10 proves these iff criteria, so every other E'-side class is
    # excluded at 2 or 3 without interpreting a bounded search negatively.
    ep_candidates = signed_squareclasses(SIDES["E_dual"]["support"])
    ep_survivors = tuple(
        d for d in ep_candidates
        if d % 8 == 1 and valuation(d, 3) == 0 and d % 3 == 1
    )
    assert ep_survivors == EP_SELMER

    survivor_rows = [
        *(rows[("E", d)] for d in E_SELMER),
        *(rows[("E_dual", d)] for d in EP_SELMER),
    ]
    for row in survivor_rows:
        assert row["places"]["infinity"]["status"] == "YES"
        for prime in BAD_FINITE_PLACES:
            validate_finite_yes_cell(row, prime)

    assert is_squareclass_subgroup(E_SELMER)
    assert is_squareclass_subgroup(EP_SELMER)
    assert len(E_SELMER) == 2**3 and len(EP_SELMER) == 2**2
    return {
        "matrix_path": "certificates/local_matrix_512.json",
        "matrix_sha256": sha256(LOCAL_MATRIX),
        "round09_path": "certificates/round09_two_place_gate.json",
        "round09_sha256": sha256(ROUND09),
        "round10_path": "certificates/round10_eprime_two_three_gate.json",
        "round10_sha256": sha256(ROUND10),
        "E_side": {
            "conventional_name": "Sel^(dual_phi)(E'/Q)",
            "real_survivors_before_finite_gate": list(E_REAL_CANDIDATES),
            "rejected_at_Q_59": list(e_rejected),
            "classes": list(E_SELMER),
            "generators": [3, 5, 7],
            "F2_dimension": 3,
        },
        "E_prime_side": {
            "conventional_name": "Sel^phi(E/Q)",
            "classes_after_Q2_and_Q3": list(EP_SELMER),
            "classes": list(EP_SELMER),
            "generators": [R, Q],
            "F2_dimension": 2,
        },
        "surviving_rows_checked_at_infinity": len(survivor_rows),
        "finite_positive_witnesses_revalidated": (
            len(survivor_rows) * len(BAD_FINITE_PLACES)
        ),
        "every_surviving_class_everywhere_locally_soluble": True,
        "every_other_supported_class_has_a_uniform_proved_obstruction": True,
        "conclusion": "the two displayed sets are the exact isogeny Selmer groups",
    }


def rank_bound_audit() -> dict[str, object]:
    numerator_bound = len(E_SELMER) * len(EP_SELMER)
    kernel_product = 2 * 2
    quotient_bound = numerator_bound // kernel_product
    assert numerator_bound == 32 and kernel_product == 4 and quotient_bound == 8
    assert quotient_bound == 2**3
    return {
        "exact_sequence_identity": (
            "2^rank = |E'(Q)/phi E(Q)|*|E(Q)/dual_phi E'(Q)| / "
            "(|E(Q)[phi]|*|E'(Q)[dual_phi]|)"
        ),
        "quotient_injections": [
            "E'(Q)/phi E(Q) injects into Sel^phi(E/Q)",
            "E(Q)/dual_phi E'(Q) injects into Sel^(dual_phi)(E'/Q)",
        ],
        "Selmer_size_product": numerator_bound,
        "kernel_orders": [2, 2],
        "rank_power_upper_bound": quotient_bound,
        "rank_upper_bound": 3,
        "exact_rank_claimed": False,
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "campbell-round11-isogeny-selmer-audit-v1",
        "source_sha256": {Path(__file__).name: sha256(Path(__file__))},
        "mapping_conventions": symbolic_map_audit(),
        "support_and_places": support_and_places_audit(),
        "local_to_selmer": local_to_selmer_audit(),
        "rank_bound": rank_bound_audit(),
        "claim_boundary": {
            "proved": [
                "the E-side 16 real-soluble classes reduce to eight at Q_59",
                "the E-side eight and E-prime-side four classes are exact isogeny Selmer groups",
                "the two Selmer dimensions are 3 and 2",
                "rank E(Q) is at most 3",
            ],
            "not_proved": [
                "the exact Mordell-Weil rank or generators",
                "the full 2-Selmer group or a Cassels-Tate value",
                "existence or nonexistence of a rational ninth point",
                "an independent second-CAS reproduction",
            ],
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {OUTPUT.name}")


if __name__ == "__main__":
    main()
