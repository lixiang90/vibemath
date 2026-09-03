"""Exact minimal-model and isomorphism invariants for the Campbell Jacobian.

This module uses only integer arithmetic and SymPy factorisation.  The
minimality and conductor deductions use the elementary criterion that an
integral model with v_p(c4)=0<v_p(Delta) has multiplicative reduction and is
p-minimal.  No rank or Selmer computation is performed here.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import sympy as sp


CODE_ROOT = Path(__file__).resolve().parent
CERT_ROOT = CODE_ROOT.parent / "certificates"
OUTPUT = CERT_ROOT / "minimal_model_identity.json"

ORIGINAL_AINVS = (0, -591_895_071, 0, 58_536_289_153_843_200, 0)
TRANSFORMATION = {"u": 6, "r": 0, "s": 3, "t": 0}
MINIMAL_AINVS = (1, -16_441_530, 0, 45_166_889_779_200, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform_ainvs(ainvs: tuple[int, ...], u: int, r: int, s: int, t: int) -> tuple[int, ...]:
    """Coefficients after x=u^2*x'+r, y=u^3*y'+s*u^2*x'+t."""
    a1, a2, a3, a4, a6 = ainvs
    numerators = (
        a1 + 2*s,
        a2 - s*a1 + 3*r - s*s,
        a3 + r*a1 + 2*t,
        a4 - s*a3 + 2*r*a2 - (t+r*s)*a1 + 3*r*r - 2*s*t,
        a6 + r*a4 + r*r*a2 + r**3 - t*a3 - r*t*a1 - t*t,
    )
    divisors = (u, u**2, u**3, u**4, u**6)
    assert all(n % d == 0 for n, d in zip(numerators, divisors))
    return tuple(n // d for n, d in zip(numerators, divisors))


def invariants(ainvs: tuple[int, ...]) -> dict[str, int]:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1*a1 + 4*a2
    b4 = a1*a3 + 2*a4
    b6 = a3*a3 + 4*a6
    b8 = a1*a1*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3*a3 - a4*a4
    c4 = b2*b2 - 24*b4
    c6 = -b2**3 + 36*b2*b4 - 216*b6
    delta = -b2*b2*b8 - 8*b4**3 - 27*b6*b6 + 9*b2*b4*b6
    assert c4**3 - c6**2 == 1728*delta
    return {"b2": b2, "b4": b4, "b6": b6, "b8": b8,
            "c4": c4, "c6": c6, "discriminant": delta}


def factor_dict(n: int) -> dict[str, int]:
    return {str(p): int(e) for p, e in sp.factorint(abs(n)).items()}


def certificate() -> dict[str, object]:
    u, r, s, t = (TRANSFORMATION[k] for k in ("u", "r", "s", "t"))
    assert transform_ainvs(ORIGINAL_AINVS, u, r, s, t) == MINIMAL_AINVS
    old = invariants(ORIGINAL_AINVS)
    new = invariants(MINIMAL_AINVS)
    assert old["c4"] == u**4 * new["c4"]
    assert old["c6"] == u**6 * new["c6"]
    assert old["discriminant"] == u**12 * new["discriminant"]

    delta_primes = sorted(int(p) for p in sp.factorint(new["discriminant"]))
    assert math.gcd(new["c4"], new["discriminant"]) == 1
    conductor = math.prod(delta_primes)
    j = sp.Rational(new["c4"]**3, new["discriminant"])
    assert sp.Rational(old["c4"]**3, old["discriminant"]) == j

    reduction = {
        str(p): {
            "v_discriminant": int(sp.factorint(new["discriminant"])[p]),
            "v_c4": 0,
            "reduction": "multiplicative",
            "kodaira_symbol": f"I_{int(sp.factorint(new['discriminant'])[p])}",
            "conductor_exponent": 1,
        }
        for p in delta_primes
    }
    return {
        "schema": "campbell-jacobian-minimal-model-identity-v1",
        "source_sha256": {Path(__file__).name: sha256(Path(__file__))},
        "original_model": {
            "ainvs": list(ORIGINAL_AINVS),
            "equation": "y^2=x^3-591895071*x^2+58536289153843200*x",
        },
        "Q_isomorphism": {
            "direction": "original coordinates in terms of minimal coordinates",
            "x": "x_original=36*x_minimal",
            "y": "y_original=216*y_minimal+108*x_minimal",
            "parameters_u_r_s_t": [u, r, s, t],
        },
        "global_minimal_model": {
            "ainvs": list(MINIMAL_AINVS),
            "equation": "y^2+x*y=x^3-16441530*x^2+45166889779200*x",
            "proof": (
                "The displayed integral change has u=6.  On the resulting model "
                "gcd(c4,Delta)=1, so at every bad prime v_p(c4)=0; hence the "
                "model is p-minimal with multiplicative reduction.  At every "
                "other prime Delta is a unit."
            ),
        },
        "invariants": new,
        "factorizations": {
            "c4": factor_dict(new["c4"]),
            "abs_c6": factor_dict(new["c6"]),
            "minimal_discriminant": factor_dict(new["discriminant"]),
        },
        "j_invariant": {
            "numerator": int(sp.numer(j)),
            "denominator": int(sp.denom(j)),
            "fraction": str(j),
        },
        "local_reduction": reduction,
        "conductor": conductor,
        "conductor_factorization": {str(p): 1 for p in delta_primes},
        "semistable": True,
        "claim_boundary": {
            "proved": [
                "the explicit Q-isomorphism and integral global minimal model",
                "c4, c6, minimal discriminant, j-invariant, multiplicative local types and conductor",
            ],
            "not_inferred": [
                "an LMFDB label (the conductor is outside the complete range)",
                "Mordell-Weil rank or any new Selmer result",
                "priority from a no-match search",
            ],
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
