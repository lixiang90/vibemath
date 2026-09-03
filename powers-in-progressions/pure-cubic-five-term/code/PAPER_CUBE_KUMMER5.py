"""Exact certificate for the nonzero pure-cubic Kummer problem at N=5.

No point search and no external CAS is used.  The final 60 curve exclusions
are exhaustive finite-field checks at primes of good reduction.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


INDEX_THREE_APS = ((0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4))
DIRECTION_REPRESENTATIVES = (2, 3, 6, 18)
GOOD_PRIMES = (7, 13, 19, 31, 37, 43, 61, 67)


def color_orbit(word):
    """AGL(1,F3) on colors, together with reversal of five positions."""
    out = set()
    for slope in (1, 2):
        for shift in range(3):
            transformed = tuple((slope*c+shift) % 3 for c in word)
            out.add(transformed)
            out.add(transformed[::-1])
    return out


def partial_color_orbit(indices, word):
    """Affine color/reversal orbit for four counted positions in a 5-window."""
    out = set()
    for slope in (1, 2):
        for shift in range(3):
            transformed = tuple((slope*c+shift) % 3 for c in word)
            out.add((tuple(indices), transformed))
            reflected = sorted((4-i, c) for i, c in zip(indices, transformed))
            out.add((
                tuple(i for i, _ in reflected),
                tuple(c for _, c in reflected),
            ))
    return out


def four_hit_orbit_representatives():
    seen, reps = set(), []
    for omitted in range(5):
        indices = tuple(i for i in range(5) if i != omitted)
        for word in product(range(3), repeat=4):
            item = (indices, word)
            if item in seen:
                continue
            orbit = partial_color_orbit(indices, word)
            seen.update(orbit)
            reps.append(min(orbit))
    assert len(seen) == 5*3**4
    assert len(reps) == 38
    return tuple(reps)


def four_hit_classification_gate():
    """State exactly how far the arithmetic maximizer classification is closed."""
    one_color, mono_three, unresolved = [], [], []
    for indices, word in four_hit_orbit_representatives():
        if len(set(word)) == 1:
            one_color.append((indices, word))
            continue
        bad = False
        for positions in ((0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4)):
            if all(i in indices for i in positions):
                colors = [word[indices.index(i)] for i in positions]
                if len(set(colors)) == 1:
                    bad = True
                    break
        (mono_three if bad else unresolved).append((indices, word))
    assert (len(one_color), len(mono_three), len(unresolved)) == (3, 4, 31)
    return {
        "all_four_hit_color_position_orbits": 38,
        "excluded_by_P5_ordinary": 3,
        "excluded_by_monochromatic_three_AP": 4,
        "arithmetic_point_classification_remaining": 31,
        "status": "FINITE_MODELS_DEFINED_BUT_RATIONAL_POINTS_NOT_CLASSIFIED",
    }


def five_color_orbit_representatives():
    seen = set()
    reps = []
    for word in product(range(3), repeat=5):
        if word in seen:
            continue
        orbit = color_orbit(word)
        seen.update(orbit)
        reps.append(min(orbit))
    assert len(seen) == 3**5
    assert len(reps) == 25
    return tuple(reps)


def monochromatic_index_three_ap(word):
    return tuple(
        triple for triple in INDEX_THREE_APS
        if len({word[i] for i in triple}) == 1
    )


def singleton_support_is_affine(word, position):
    """Whether an F3 affine function of the color can support one position."""
    for constant in range(3):
        for slope in range(3):
            values = tuple((constant+slope*c) % 3 for c in word)
            for nonzero in (1, 2):
                target = tuple(nonzero if i == position else 0 for i in range(5))
                if values == target:
                    return True
    return False


def candidate_partition():
    """Split the 25 orbits into known-theorem, four-same, and local cases."""
    mono, four_same, local = [], [], []
    for word in five_color_orbit_representatives():
        triples = monochromatic_index_three_ap(word)
        if triples:
            mono.append((word, triples))
        elif max(word.count(c) for c in range(3)) == 4:
            four_same.append(word)
        else:
            local.append(word)
    assert len(mono) == 9
    assert four_same == [(0, 0, 1, 0, 0)]
    assert len(local) == 15
    # Every local case is 3+2, 3+1+1, or 2+2+1.  In particular, for every
    # used color configuration the singleton-support valuation vector is not
    # an affine function of the colors.
    for word in local:
        counts = sorted((word.count(c) for c in set(word)), reverse=True)
        assert counts in ([3, 2], [3, 1, 1], [2, 2, 1])
        assert not any(singleton_support_is_affine(word, i) for i in range(5))
    return mono, four_same, local


def check_kernel_symbolics():
    """Coefficient calculation for y^3 in Q inside Q(alpha), alpha^3=D."""
    a, b, c, D, A = sp.symbols("a b c D A")
    raw = sp.expand((a+b*A+c*A**2)**3)
    coeff = [0, 0, 0]
    for (exponent,), value in sp.Poly(raw, A).terms():
        coeff[exponent % 3] += value*D**(exponent // 3)
    coeff = tuple(sp.factor(v) for v in coeff)
    expected = (
        a**3+D*b**3+D**2*c**3+6*D*a*b*c,
        3*(a**2*b+D*a*c**2+D*b**2*c),
        3*(a**2*c+a*b**2+D*b*c**2),
    )
    assert tuple(sp.expand(x-y) for x, y in zip(coeff, expected)) == (0, 0, 0)

    # If a != 0, put B=b/a,C=c/a.  Eliminating C or B gives the two
    # displayed factors.  For noncube D they force B=C=0.
    B, C = sp.symbols("B C")
    f = B+D*C**2+D*B**2*C
    g = C+B**2+D*B*C**2
    res_C = sp.factor(sp.resultant(f, g, C))
    res_B = sp.factor(sp.resultant(f, g, B))
    assert res_C == B*D*(B**3*D-1)**2
    assert res_B == C*(C**3*D**2-1)**2
    return {
        "alpha_coefficient": str(coeff[1]),
        "alpha2_coefficient": str(coeff[2]),
        "a_nonzero_resultant_C": str(res_C),
        "a_nonzero_resultant_B": str(res_B),
        "kernel": "{1,[D],[D]^2}",
    }


def _factor_integer(n):
    if n <= 0:
        raise ValueError("positive integer required")
    result = {}
    q = n
    p = 2
    while p*p <= q:
        while q % p == 0:
            result[p] = result.get(p, 0)+1
            q //= p
        p = 3 if p == 2 else p+2
    if q > 1:
        result[q] = result.get(q, 0)+1
    return result


def rational_cube_class(value):
    """Finite prime-exponent vector in Q*/Q*3; sign vanishes for cubes."""
    value = Fraction(value)
    if value == 0:
        raise ValueError("zero has no Kummer class")
    out = {}
    for p, e in _factor_integer(abs(value.numerator)).items():
        if e % 3:
            out[p] = e % 3
    for p, e in _factor_integer(value.denominator).items():
        residue = (-e) % 3
        if residue:
            out[p] = (out.get(p, 0)+residue) % 3
            if out[p] == 0:
                del out[p]
    return tuple(sorted(out.items()))


def canonical_pure_cubic_radicand(value):
    """Cube-free positive integer, modulo D <-> D^2 (same pure cubic field)."""
    cls = dict(rational_cube_class(value))
    if not cls:
        return 1

    def integer_for(multiplier):
        ans = 1
        for p, exponent in cls.items():
            ans *= p**((multiplier*exponent) % 3)
        return ans

    return min(integer_for(1), integer_for(2))


def curve_equations(word, D):
    """Three diagonal cubics in P^4 for a five-hit color pattern."""
    coeff = [D**c for c in word]
    return tuple(
        f"{coeff[i]}*x{i}^3-2*{coeff[i+1]}*x{i+1}^3+{coeff[i+2]}*x{i+2}^3=0"
        for i in range(3)
    )


def has_nonzero_projective_point_mod_p(word, D, p):
    """Equivalent O(p^2) search using the AP intercept and difference."""
    return local_scan_summary(word, D, p)["compatible_parameter_pairs"] > 0


def local_scan_summary(word, D, p):
    """Return a complete, auditable count for one finite-field obstruction.

    Every nonzero pair ``(a,d)`` in F_p^2 is scanned.  ``first_failure`` is a
    disjoint histogram: a pair is assigned to the first position whose value
    is not in the required weighted cube class.  Hence its sum plus the
    compatible count must be exactly ``p^2-1``.
    """
    cubes = {pow(x, 3, p) for x in range(p)}
    allowed = [
        {(pow(D, color, p)*cube) % p for cube in cubes}
        for color in word
    ]
    first_failure = [0] * 5
    compatible = 0
    pairs_with_zero_term = 0
    for intercept in range(p):
        for difference in range(p):
            if intercept == 0 and difference == 0:
                continue
            values = tuple((intercept+i*difference) % p for i in range(5))
            if 0 in values:
                pairs_with_zero_term += 1
            for i, value in enumerate(values):
                if value not in allowed[i]:
                    first_failure[i] += 1
                    break
            else:
                compatible += 1
    total = p*p-1
    assert sum(first_failure) + compatible == total
    return {
        "field": f"F_{p}",
        "parameterization": "A_i=a+i*d for i=0,...,4",
        "parameter_pairs_scanned": total,
        "excluded_zero_pair": [0, 0],
        "pairs_with_at_least_one_zero_term": pairs_with_zero_term,
        "cube_image_size_including_zero": len(cubes),
        "allowed_value_counts_by_position": [len(values) for values in allowed],
        "first_failure_counts_by_position": first_failure,
        "compatible_parameter_pairs": compatible,
        "count_identity_verified": sum(first_failure) + compatible == total,
        "good_prime_conditions": {
            "p_is_prime": bool(sp.isprime(p)),
            "p_does_not_divide_3D": math.gcd(p, 3*D) == 1,
            "condition_text": "p is prime and gcd(p,3D)=1",
        },
    }


def local_obstruction_table():
    _, _, local_words = candidate_partition()
    rows = []
    for word in local_words:
        for D in DIRECTION_REPRESENTATIVES:
            obstruction = next(
                (p for p in GOOD_PRIMES
                 if math.gcd(p, 3*D) == 1
                 and not has_nonzero_projective_point_mod_p(word, D, p)),
                None,
            )
            assert obstruction is not None
            summary = local_scan_summary(word, D, obstruction)
            assert summary["compatible_parameter_pairs"] == 0
            assert all(summary["good_prime_conditions"].values())
            rows.append({
                "word": "".join(map(str, word)),
                "D": D,
                "prime": obstruction,
                "equations": curve_equations(word, D),
                "good_prime_condition": "p is prime and gcd(p,3D)=1",
                "finite_field_count": summary,
            })
    assert len(rows) == 60
    return rows


def verify_lower_witness():
    values = (-3, -1, 1, 3, 5)
    assert all(values[i+1]-values[i] == 2 for i in range(4))
    # In Q(cuberoot(3)), the first four are cubes of -alpha,-1,1,alpha.
    return {
        "AP": list(values),
        "counted_positions": [0, 1, 2, 3],
        "radicand": 3,
        "cube_roots": ["-alpha", "-1", "1", "alpha"],
    }


def build_certificate():
    mono, four_same, local = candidate_partition()
    rows = local_obstruction_table()
    return {
        "schema": "paper-cube-pure-cubic-kummer-n5-v2",
        "definition": "nonzero terms; common rational scaling; nonconstant rational AP",
        "kernel_certificate": check_kernel_symbolics(),
        "D_normalization": {
            "degree_three": "[D] != 1 in Q*/Q*3",
            "negative": "K_D=K_-D because -1 is a rational cube",
            "same_field": "D and D^2 define the same line and the same field",
            "canonical_examples": [2, 3, 6, 18],
        },
        "orbit_counts": {
            "all_five_color_orbits": 25,
            "monochromatic_index_3AP": len(mono),
            "four_same_color_non_3AP": len(four_same),
            "local_cases": len(local),
        },
        "monochromatic_representatives": ["".join(map(str, w)) for w, _ in mono],
        "four_same_representative": "".join(map(str, four_same[0])),
        "local_representatives": ["".join(map(str, w)) for w in local],
        "local_obstructions": rows,
        "lower_witness": verify_lower_witness(),
        "theorem": "R_x_(3,1)(5)=4",
        "five_hit_status": "EXCLUDED_EXHAUSTIVELY",
        "four_hit_classification_gate": four_hit_classification_gate(),
        "maximizer_point_classification": "NOT_CLAIMED; only finite color/position models are classified",
    }


def write_certificate(path=None):
    """Write the canonical JSON certificate and return its content hash."""
    if path is None:
        path = Path(__file__).resolve().with_name("PAPER_CUBE_KUMMER5_CERTIFICATE.json")
    else:
        path = Path(path)
    payload = (json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(payload)
    return {"path": str(path), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(write_certificate(), indent=2, sort_keys=True))
