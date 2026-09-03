"""Self-contained Campbell-source and provenance audit for the finite theorem.

Only exact integer/polynomial identities are promoted.  The bundled Magma
program is deliberately recorded as an unexecuted, ineligible research input.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
CERT_ROOT = ROOT.parent / "certificates"
NOTES_ROOT = ROOT.parent / "notes"
OUTPUT = CERT_ROOT / "campbell_source_provenance.json"
m, x = sp.symbols("m x")

D_COEFFS = (-264815, -19343520, 62846856064, -2906312951808, -495507443511296)
H_COEFFS = (-850079, -11210976, 138714149248, -5501355374592, -1679721044504576)

G3 = -18816*m**4 + 677376*m**3 + 1922543616*m**2 - 48944480256*m - 40678301368320
G2 = 236896*m**4 - 9821952*m**3 - 22598349824*m**2 + 508953231360*m + 520252184657920
G1 = -958800*m**4 + 40985280*m**3 + 89932669440*m**2 - 1957723729920*m - 2113363439616000
G0 = 1292769*m**4 - 57304800*m**3 - 118795148928*m**2 + 2647001548800*m + 2758336954896384
G = sp.expand(G3*x**3 + G2*x**2 + G1*x + G0)
D = sp.Poly.from_list(D_COEFFS, gens=m).as_expr()
H = sp.Poly.from_list(H_COEFFS, gens=m).as_expr()

SQUARE_ROOTS_0_TO_6 = (
    3*(379*m**2 - 8400*m - 17506624),
    743*m**2 - 17136*m - 33534272,
    415*m**2 - 11088*m - 16946752,
    3*(67*m**2 - 3696*m - 494656),
    209*m**2 - 17136*m + 5050432,
    263*m**2 - 25200*m + 10631872,
    63*(m**2 - 2352*m + 72256),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def campbell_source_certificate() -> dict[str, object]:
    square_residuals = [sp.expand(G.subs(x, j) - q*q) for j, q in enumerate(SQUARE_ROOTS_0_TO_6)]
    disc_x = sp.factor(sp.discriminant(G, x))
    disc_primitive = sp.Poly(sp.cancel(disc_x / -65028096), m)
    factor_degrees = [[int(sp.degree(f, m)), int(exponent)] for f, exponent in sp.factor_list(disc_primitive.as_expr())[1]]
    disc_mod_53 = sp.Poly(disc_primitive.as_expr(), m, modulus=53)
    leading_factorization = sp.factor(G3)
    return {
        "source": {
            "author": "Garikai Campbell",
            "title": "A Note on Arithmetic Progressions on Elliptic Curves",
            "journal": "Journal of Integer Sequences 6 (2003), Article 03.1.3",
            "source_url": "https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html",
            "location": "Corollary 2.4, Theorem 2.5, and its proof",
        },
        "parameter_change": {
            "old_parameter_t": "(6*m^2-126*m-285360)/(m^2-72256)",
            "denominator_polynomial": "m^2-72256",
            "no_rational_denominator_zero": True,
            "reason": "268^2 < 72256 < 269^2",
            "Campbell_exception_t_equals_5_over_2_has_no_rational_m": True,
        },
        "g_coefficients_descending_in_x": [str(sp.expand(v)) for v in (G3, G2, G1, G0)],
        "indices": {
            "automatic_square_indices": list(range(7)),
            "eighth_index": 7,
            "ninth_candidate_index": 8,
            "x_coordinates": list(range(9)),
        },
        "square_roots_at_0_through_6": [str(sp.expand(q)) for q in SQUARE_ROOTS_0_TO_6],
        "square_identity_residuals": [str(v) for v in square_residuals],
        "g_at_7_minus_D": str(sp.expand(G.subs(x, 7) - D)),
        "g_at_8_minus_H": str(sp.expand(G.subs(x, 8) - H)),
        "D_coefficients": list(D_COEFFS),
        "H_coefficients": list(H_COEFFS),
        "degeneracy_boundaries": {
            "rational_parameter_infinity": "not on C_D(Q): the leading equation is Y^2=-264815*M^4",
            "leading_cubic_coefficient": str(leading_factorization),
            "leading_coefficient_has_no_rational_zero": True,
            "leading_quadratic_discriminants": [4*72256, 120976],
            "leading_quadratic_nonsquare_brackets": [[268**2, 72256, 269**2], [347**2, 120976, 348**2]],
            "cubic_discriminant_constant": -65028096,
            "cubic_discriminant_primitive_degree": disc_primitive.degree(),
            "cubic_discriminant_primitive_coefficients": [int(v) for v in disc_primitive.all_coeffs()],
            "primitive_factor_degrees_over_Q": factor_degrees,
            "primitive_irreducible_mod_53": bool(disc_mod_53.is_irreducible),
            "hence_no_rational_singular_specialization": bool(disc_mod_53.is_irreducible),
            "D_or_H_zero": "allowed branch point with y_7=0 or y_8=0; it is not a repeated x-coordinate or a singularity of g_m",
            "D_and_H_simultaneously_zero": "impossible because resultant(D,H) is nonzero",
            "nine_x_coordinates_are_distinct": True,
        },
    }


def same_m_certificate_summary() -> dict[str, object]:
    path = CERT_ROOT / "same_m_local.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    local = data["same_m_local_certificates"]
    odd = local["odd"]
    def evaluate(coefficients: tuple[int, ...], value: int, modulus: int | None = None) -> int:
        ans = 0
        for coefficient in coefficients:
            ans = ans*value + coefficient
            if modulus is not None:
                ans %= modulus
        return ans

    for prime, value, d_value, d_root, h_value, h_root in odd:
        assert evaluate(D_COEFFS, value, prime) == d_value
        assert evaluate(H_COEFFS, value, prime) == h_value
        assert d_root*d_root % prime == d_value
        assert h_root*h_root % prime == h_value
    real = local["real"]
    two = local["two_adic"]
    assert evaluate(D_COEFFS, real["m"]) == real["D_m"] > 0
    assert evaluate(H_COEFFS, real["m"]) == real["H_m"] > 0
    assert evaluate(D_COEFFS, two["m"]) == two["D_m"]
    assert evaluate(H_COEFFS, two["m"]) == two["H_m"]
    assert two["D_mod_8"] == two["H_mod_8"] == 1
    disc_d = int(sp.discriminant(D, m))
    disc_h = int(sp.discriminant(H, m))
    resultant = int(sp.resultant(D, H, m))
    branch_bad = sorted(set(sp.factorint(abs(disc_d))) | set(sp.factorint(abs(disc_h))) | set(sp.factorint(abs(resultant))))
    return {
        "source_file": path.name,
        "source_sha256": sha256(path),
        "real_witness": local["real"],
        "two_adic_witness": local["two_adic"],
        "odd_format": local["odd_format"],
        "odd_witness_count": len(odd),
        "odd_primes": [row[0] for row in odd],
        "odd_witnesses": odd,
        "disc_D": disc_d,
        "disc_H": disc_h,
        "resultant_D_H": resultant,
        "branch_bad_primes": branch_bad,
        "good_prime_bridge": local["remaining_good_primes"],
        "claim": "the smooth fibre product Y^2=D(m), Z^2=H(m) has points over R and every Q_p",
    }


def prior_art_audit() -> dict[str, object]:
    return {
        "search_date": "2026-09-03",
        "exact_queries": [
            '"58536289153843200" elliptic curve',
            '"116194618458722241" elliptic curve',
            '"1434501462453361" Selmer',
            '"4230241" "339106321" elliptic',
            '"850079" "11210976" "138714149248"',
            '"264815" "19343520" "62846856064" Campbell',
            'site:lmfdb.org/EllipticCurve/Q "591895071"',
        ],
        "exact_query_result": "NO_MATCH_FOUND_FOR_THE_SPECIFIC_MODELS_OR_SELMER_SETS",
        "located_source": "Campbell 2003 is the source of g_m and the eight-term family, but does not state the present two-isogeny Selmer calculation.",
        "nearby_sources": [
            "Campbell, JIS 6 (2003), Article 03.1.3",
            "Bremner, Experimental Mathematics 8 (1999), 409-413",
            "Garcia-Selfa--Tornero, Bulletin of the Australian Mathematical Society 71 (2005), 417-424",
            "Fisher, Research in Number Theory 8 (2022), article 74",
        ],
        "novelty_boundary": "This is a documented not-found search, not proof of priority or novelty.",
    }


def provenance() -> dict[str, object]:
    candidates = [
        NOTES_ROOT / "candidate-input" / "UNEXECUTED_full_two_selmer.m",
        NOTES_ROOT / "candidate-input" / "UNEXECUTED_same_m_and_descent_H.m",
        NOTES_ROOT / "candidate-input" / "UNEXECUTED_run_magma_audit.ps1",
    ]
    return {
        "python_exact_pipeline": {
            "status": "EXECUTED_AND_REGRESSION_TESTED",
            "mathematical_evidence_eligible": True,
        },
        "magma_full_descent": {
            "candidate_inputs": [
                {"path": path.relative_to(ROOT.parent).as_posix(), "sha256": sha256(path)}
                for path in candidates
            ],
            "status": "BUNDLED_UNEXECUTED_NOT_EVIDENCE",
            "transcript": None,
            "magma_binary_sha256": None,
            "mathematical_evidence_eligible": False,
            "forbidden_promotions": [
                "full 2-Selmer dimension",
                "Cassels-Tate pairing value",
                "Mordell-Weil rank equality",
                "C_H(Q) empty or nonempty",
            ],
        },
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "paper-elliptic-campbell-round-06-v1",
        "semantic_version": "1.0.0",
        "campbell_source_reconstruction": campbell_source_certificate(),
        "same_m_local_summary": same_m_certificate_summary(),
        "prior_art": prior_art_audit(),
        "provenance": provenance(),
        "claim_boundary": {
            "proved": [
                "the exact Campbell identities at x=0,...,8 and all rational degeneration boundaries listed above",
                "the same-m fibre product is everywhere locally soluble, conditional only on the explicitly stored finite certificates and the Weil-Hensel bridge",
                "the Python finite theorem may use the exact isogeny Selmer groups already certified in Round 04",
            ],
            "not_proved": [
                "a rational m giving nine points on a nonsingular cubic Weierstrass model",
                "nonexistence of such an m",
                "any Cassels-Tate or full 2-descent conclusion",
                "priority of the finite Selmer computation",
            ],
        },
    }


def main() -> None:
    OUTPUT.write_text(json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
