"""Exact structural clustering of the 29 four-hit models open after Round 08.

This is a symbolic reconstruction, not a bounded point search.  Every model
is expressed as a plane diagonal cubic, a bidegree-(3,3) cyclic curve, or a
weighted superelliptic curve.  Only variable permutations are used for the
Q-isomorphism clusters claimed here.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_CERTIFICATE.json"


def _load(name, filename):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


km = _load("round09_kummer5", "PAPER_CUBE_KUMMER5.py")
base = _load("round09_0001", "PAPER_CUBE_FOURHIT_0001.py")
lift = _load("round09_0010", "PAPER_CUBE_FOURHIT_0010.py")

SOLVED_BEFORE_ROUND09 = {
    ((0, 1, 3, 4), (0, 0, 0, 1)),
    ((0, 1, 2, 3), (0, 0, 1, 0)),
}
NEWLY_SOLVED = {
    ((0, 1, 2, 3), (0, 1, 0, 0)),
    ((0, 1, 2, 4), (0, 1, 1, 1)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gate_unresolved_models():
    out = []
    triples = ((0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4))
    for indices, word in km.four_hit_orbit_representatives():
        if len(set(word)) == 1:
            continue
        if any(
            all(i in indices for i in triple)
            and len({word[indices.index(i)] for i in triple}) == 1
            for triple in triples
        ):
            continue
        out.append((tuple(indices), tuple(word)))
    assert len(out) == 31
    return tuple(out)


def current_models():
    out = tuple(m for m in gate_unresolved_models() if m not in SOLVED_BEFORE_ROUND09)
    assert len(out) == 29
    return out


def multiplicity_type(word):
    counts = sorted(Counter(word).values(), reverse=True)
    return "+".join(map(str, counts))


def linear_numerator(p, q, k):
    """Numerator of A_k from A_p=X^3,A_q=Y^3, denominator q-p."""
    assert p != q
    return (q-k, k-p)


def normalize_tuple(values):
    values = tuple(int(v) for v in values)
    g = 0
    for value in values:
        g = math.gcd(g, abs(value))
    values = tuple(v//g for v in values)
    first = next(v for v in values if v)
    if first < 0:
        values = tuple(-v for v in values)
    return values


def canonical_diagonal(coefficients):
    candidates = []
    for perm in permutations(range(3)):
        candidate = normalize_tuple(coefficients[i] for i in perm)
        candidates.append((candidate, perm))
    return min(candidates)


def matrix_action(matrix, transpose, row_swap, col_swap):
    m = tuple(tuple(row) for row in matrix)
    if transpose:
        m = ((m[0][0], m[1][0]), (m[0][1], m[1][1]))
    if row_swap:
        m = (m[1], m[0])
    if col_swap:
        m = tuple((row[1], row[0]) for row in m)
    return m


def canonical_matrix(matrix):
    candidates = []
    for transpose in (False, True):
        for row_swap in (False, True):
            for col_swap in (False, True):
                m = matrix_action(matrix, transpose, row_swap, col_swap)
                key = normalize_tuple(m[0] + m[1])
                candidates.append((key, {
                    "transpose_factors": transpose,
                    "swap_first_factor": row_swap,
                    "swap_second_factor": col_swap,
                }))
    return min(candidates, key=lambda item: (item[0], str(item[1])))


def canonical_superelliptic(coefficients):
    a, b, c, w = coefficients
    candidates = [
        (normalize_tuple((a, b, c, w)), {"swap_X_Y": False}),
        (normalize_tuple((c, b, a, w)), {"swap_X_Y": True}),
    ]
    return min(candidates, key=lambda item: item[0])


def reconstruct_model(indices, word):
    positions_by_color = defaultdict(list)
    for i, color in zip(indices, word):
        positions_by_color[color].append(i)
    kind = multiplicity_type(word)
    result = {
        "indices": list(indices),
        "word": "".join(map(str, word)),
        "multiplicity_type": kind,
    }

    if kind == "3+1":
        repeated = next(c for c, pos in positions_by_color.items() if len(pos) == 3)
        triple = tuple(sorted(positions_by_color[repeated]))
        i, j, k = triple
        coefficients = (k-j, -(k-i), j-i)
        key, permutation = canonical_diagonal(coefficients)
        result["curve"] = {
            "model": "plane diagonal cubic",
            "variables_follow_positions": list(triple),
            "coefficient_vector": list(coefficients),
            "equation": f"{coefficients[0]}X^3+({coefficients[1]})Y^3+{coefficients[2]}Z^3=0",
            "smooth": True,
            "genus": 1,
            "canonical_permutation_key": list(key),
            "map_to_canonical_coordinate_permutation": list(permutation),
        }
        result["cluster_key"] = [kind, *key]
        return result

    if kind == "2+2":
        colors = sorted(positions_by_color)
        p, q = sorted(positions_by_color[colors[0]])
        r, s = sorted(positions_by_color[colors[1]])
        lr, ls = linear_numerator(p, q, r), linear_numerator(p, q, s)
        # F=(lr_X X^3+lr_Y Y^3)V^3-(ls_X X^3+ls_Y Y^3)U^3.
        matrix = ((-ls[0], lr[0]), (-ls[1], lr[1]))
        key, action = canonical_matrix(matrix)
        result["curve"] = {
            "model": "smooth bidegree-(3,3) curve in P1xP1",
            "first_color_positions": [p, q],
            "second_color_positions": [r, s],
            "coefficient_matrix_rows_XY_columns_UV": [list(row) for row in matrix],
            "equation_template": "L_r(X^3,Y^3)V^3-L_s(X^3,Y^3)U^3=0",
            "six_simple_branch_points": True,
            "genus": 4,
            "canonical_permutation_key": list(key),
            "map_to_canonical_factor_action": action,
        }
        result["cluster_key"] = [kind, *key]
        return result

    assert kind == "2+1+1"
    repeated = next(c for c, pos in positions_by_color.items() if len(pos) == 2)
    p, q = sorted(positions_by_color[repeated])
    singleton_positions = sorted(i for i in indices if i not in (p, q))
    r, s = singleton_positions
    lr, ls = linear_numerator(p, q, r), linear_numerator(p, q, s)
    coefficients = (
        lr[0]*ls[0],
        lr[0]*ls[1]+lr[1]*ls[0],
        lr[1]*ls[1],
        -(q-p)**2,
    )
    key, action = canonical_superelliptic(coefficients)
    result["curve"] = {
        "model": "normalization of W^3=A_r*A_s in P(1,1,2)",
        "repeated_color_positions": [p, q],
        "singleton_positions": [r, s],
        "coefficient_vector_X6_X3Y3_Y6_W3": list(coefficients),
        "equation_template": "L_r(X^3,Y^3)L_s(X^3,Y^3)-(q-p)^2W^3=0",
        "six_simple_branch_points": True,
        "genus": 4,
        "canonical_permutation_key": list(key),
        "map_to_canonical_coordinate_action": action,
    }
    result["cluster_key"] = [kind, *key]
    return result


def all_model_data():
    return tuple(reconstruct_model(*model) for model in current_models())


def clusters():
    grouped = defaultdict(list)
    for model in all_model_data():
        grouped[tuple(model["cluster_key"])].append([model["indices"], model["word"]])
    return {"|".join(map(str, key)): members for key, members in sorted(grouped.items())}


def progression_from_pair(p, q, x3, y3):
    return tuple(
        Fraction((q-k)*x3+(k-p)*y3, q-p)
        for k in range(5)
    )


def zero_boundary_data_0100():
    """Exact symbolic audit of the two nontrivial zero coordinates in (4)."""
    X, Y, Z = sp.symbols("X Y Z")
    curve = 2*X**3 - 3*Y**3 + Z**3
    twice_A1 = Z**3 + Y**3
    A4 = 2*Y**3 - Z**3
    a1_factorization = (Z + Y) * (Z**2 - Z*Y + Y**2)
    curve_at_Z_minus_Y = 2 * (X**3 - 2*Y**3)

    # A1=0: over Q the second homogeneous factor has discriminant -3 and
    # hence vanishes only at Y=Z=0; that projective possibility is excluded
    # by the curve.  Thus Z=-Y, and the curve gives X^3=2Y^3.
    assert sp.expand(twice_A1 - a1_factorization) == 0
    assert sp.discriminant((Z**2 - Z*Y + Y**2).subs(Y, 1), Z) == -3
    assert sp.expand(curve.subs(Z, -Y) - curve_at_Z_minus_Y) == 0

    # A4=0 is exactly Z^3=2Y^3.
    assert sp.expand(-A4 - (Z**3 - 2*Y**3)) == 0

    return {
        "A1=0": {
            "twice_AP_coordinate": str(twice_A1),
            "factorization": str(a1_factorization),
            "other_factor_dehomogenized_discriminant": -3,
            "forced_linear_relation_over_Q": "Z=-Y",
            "curve_after_substitution": str(curve_at_Z_minus_Y),
            "forced_cube_relation": "X^3=2Y^3",
        },
        "A4=0": {
            "AP_coordinate": str(A4),
            "equivalent_cube_relation": "Z^3=2Y^3",
        },
    }


def new_family_data():
    X, Y, Z = base.GENERATOR
    # 0100: source cubic coordinates are (Z,Y,X), at positions 0,2,3.
    ap_0100 = progression_from_pair(0, 2, Z**3, Y**3)
    assert ap_0100[3] == X**3
    # 0111: base coordinates are cube positions 1,2,4.
    ap_0111 = progression_from_pair(1, 2, X**3, Y**3)
    assert ap_0111[4] == Z**3
    D0100, w0100 = lift.cube_free_representative(ap_0100[1])
    D0111, w0111 = lift.cube_free_representative(ap_0111[0])
    assert (D0100, w0100) == (62, Fraction(-1))
    assert (D0111, w0111) == (127, Fraction(1))
    three_Q = base.ec_add(base.ec_add(base.Q, base.Q), base.Q)
    return {
        "shared_curve": "2X^3-3Y^3+Z^3=0",
        "base_source_sha256": sha256(HERE / "PAPER_CUBE_FOURHIT_0001.py"),
        "base_symbolic_mordell_identity_recomputed": base.symbolic_map_identity() != 0,
        "translated_generator_image_3Q": [str(v) for v in three_Q],
        "models": [
            {
                "indices": [0, 1, 2, 3],
                "word": "0100",
                "source_cubic": "X^3-3Y^3+2Z^3=0",
                "map_source_to_shared": ["U=Z", "V=Y", "W=X"],
                "sample_AP": [str(v) for v in ap_0100],
                "singleton_index": 1,
                "D": D0100,
                "singleton_scale": str(w0100),
                "zero_checks": zero_boundary_data_0100(),
            },
            {
                "indices": [0, 1, 2, 4],
                "word": "0111",
                "source_cubic": "2X^3-3Y^3+Z^3=0",
                "map_source_to_shared": ["U=X", "V=Y", "W=Z"],
                "sample_AP": [str(v) for v in ap_0111],
                "singleton_index": 0,
                "raw_colors": "1000",
                "canonical_color_map": "c -> 2c+1 gives 0111",
                "D": D0111,
                "singleton_scale": str(w0111),
                "zero_checks": {
                    "A0=0": "Y^3=2X^3",
                    "A3=0": "X^3=2Y^3",
                },
            },
        ],
        "boundary": {
            "constant_only_at": [1, 1, 1],
            "singleton_rational_cube_contradicts": "P_5(3)=3",
            "fifth_hit_contradicts": "R^times_(3,1)(5)=4",
            "equivalence": "common rational scaling and reversal; reversal fibres have size at most two",
        },
    }


def certificate_data():
    data = all_model_data()
    counts = Counter(model["multiplicity_type"] for model in data)
    cls = clusters()
    assert counts == Counter({"2+1+1": 16, "2+2": 9, "3+1": 4})
    return {
        "schema": "paper-cube-fourhit-round09-clusters-v1",
        "source_sha256": sha256(Path(__file__)),
        "input_counts": {
            "all_partial_words": 405,
            "affine_color_reversal_orbits": 38,
            "gate_unresolved": 31,
            "solved_before_round09": 2,
            "round09_input": 29,
        },
        "structural_type_counts": dict(sorted(counts.items())),
        "models": list(data),
        "proven_coordinate_permutation_clusters": cls,
        "new_positive_rank_families": new_family_data(),
        "round09_conclusion": {
            "newly_solved": 2,
            "newly_solved_models": [
                {"indices": list(i), "word": "".join(map(str, w))}
                for i, w in sorted(NEWLY_SOLVED)
            ],
            "remaining_after_round09": 27,
            "no_claim": "No rank or rational-point classification is claimed for the other 27 models",
        },
    }


def write_certificate(path=OUTPUT):
    path.write_text(json.dumps(certificate_data(), indent=2) + "\n", encoding="utf-8", newline="\n")
    return sha256(path)


if __name__ == "__main__":
    print(write_certificate())
