"""Fail-closed CAS audit and an exact two-place gate for the E-side covers.

No external CAS is used.  The local theorem is proved by integer arithmetic,
Euler symbols, and the identity

    4*d*F_d = (2*d*U^2+a*V^2)^2 - (a^2-4*b)*V^4.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import platform
import shutil
import sys


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUTPUT = PROJECT / "certificates" / "round09_two_place_gate.json"

A = -591_895_071
B = 58_536_289_153_843_200
DELTA = A*A - 4*B
SUPPORT = (2, 3, 5, 7)
MULTIPLICATIVE_PRIMES = (59, 71_699)
EXPECTED_COMBINED = (1, 3, 5, 7, 15, 21, 35, 105)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    q = 3
    while q*q <= n:
        if n % q == 0:
            return False
        q += 2
    return True


def valuation(n: int, p: int) -> int:
    assert n
    answer = 0
    while n % p == 0:
        n //= p
        answer += 1
    return answer


def legendre(a: int, p: int) -> int:
    assert is_prime_trial(p) and p % 2 == 1 and a % p
    value = pow(a % p, (p-1)//2, p)
    assert value in (1, p-1)
    return 1 if value == 1 else -1


def signed_candidates() -> tuple[int, ...]:
    positive = []
    for length in range(len(SUPPORT)+1):
        positive.extend(math.prod(s) for s in itertools.combinations(SUPPORT, length))
    return tuple(sorted(positive + [-d for d in positive]))


def real_soluble(d: int) -> bool:
    # If d>0, (U:V)=(1:0) gives F_d=d>0.  If d<0, all three
    # coefficients d,a,b/d are negative, so F_d<0 off (U,V)=(0,0).
    assert B % d == 0
    return d > 0


def local_soluble_at_multiplicative_prime(d: int, p: int) -> bool:
    """Complete Q_p classification for the listed d and p.

    A square d gives the point (U:V:N)=(1:0:sqrt(d)).  If d is a
    nonsquare, the valuation-normalized double-root argument proves that no
    point exists.
    """
    assert p in MULTIPLICATIVE_PRIMES
    assert valuation(DELTA, p) == 1
    assert math.gcd(2*d*B, p) == 1
    return legendre(d, p) == 1


def environment_audit() -> dict[str, object]:
    executables = ("sage.exe", "magma.exe", "gp.exe", "pari-gp.exe", "mwrank.exe")
    modules = ("sageall", "sage", "cypari2", "cypari", "eclib")
    located = {name: shutil.which(name) for name in executables}
    module_status = {name: importlib.util.find_spec(name) is not None for name in modules}
    sympy_available = importlib.util.find_spec("sympy") is not None
    return {
        "audit_date": "2026-09-04",
        "applications": located,
        "python_modules": module_status,
        "independent_elliptic_cas_available": any(located.values()) or any(module_status.values()),
        "powershell_gp_note": "gp is Get-ItemProperty alias, not a PARI/GP executable",
        "available_nonindependent_runtime": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "python_binary_sha256": sha256(Path(sys.executable)),
            "platform": platform.platform(),
            "sympy_available": sympy_available,
            "sympy_version": importlib.metadata.version("sympy") if sympy_available else None,
        },
        "claim_boundary": (
            "No second CAS is present.  Python/SymPy is the first implementation's "
            "runtime and is not counted as an independent reproduction."
        ),
    }


def local_gate_certificate() -> dict[str, object]:
    assert DELTA == 3**4 * 59 * 71_699 * 339_106_321
    candidates = signed_candidates()
    assert len(candidates) == 32
    local = {}
    for p in MULTIPLICATIVE_PRIMES:
        assert is_prime_trial(p)
        generators = {str(q): legendre(q, p) for q in (-1, 2, 3, 5, 7)}
        assert generators == {"-1": -1, "2": -1, "3": 1, "5": 1, "7": 1}
        soluble = tuple(d for d in candidates if local_soluble_at_multiplicative_prime(d, p))
        obstructed = tuple(d for d in candidates if d not in soluble)
        local[str(p)] = {
            "v_p_a2_minus_4b": valuation(DELTA, p),
            "legendre_generators": generators,
            "soluble_classes": list(soluble),
            "obstructed_classes": list(obstructed),
            "sufficiency": "if (d/p)=1, use (U,V)=(1,0) and N^2=d",
            "necessity_identity": "4*d*F_d=(2*d*U^2+a*V^2)^2-(a^2-4*b)*V^4",
        }
    assert local["59"]["soluble_classes"] == local["71699"]["soluble_classes"]

    real_yes = tuple(d for d in candidates if real_soluble(d))
    combined = tuple(
        d for d in candidates
        if real_soluble(d) and local_soluble_at_multiplicative_prime(d, 59)
    )
    assert combined == EXPECTED_COMBINED
    return {
        "curve": {
            "equation": "y^2=x^3-591895071*x^2+58536289153843200*x",
            "a": A,
            "b": B,
            "a2_minus_4b": DELTA,
            "a2_minus_4b_factorization": {"3": 4, "59": 1, "71699": 1, "339106321": 1},
        },
        "cover": "C_d: N^2=d*U^4+a*U^2*V^2+(b/d)*V^4",
        "signed_squarefree_support": list(SUPPORT),
        "all_32_candidates": list(candidates),
        "real_soluble_classes": list(real_yes),
        "local_classification": local,
        "real_and_Q59_survivors": list(combined),
        "real_and_Q71699_survivors": list(combined),
        "closed_theorem": (
            "Among the 32 signed squarefree classes supported on 2,3,5,7, "
            "simultaneous solubility over R and Q_59 (equivalently here R and "
            "Q_71699) leaves exactly 1,3,5,7,15,21,35,105."
        ),
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "campbell-round09-two-place-gate-v1",
        "source_sha256": {Path(__file__).name: sha256(Path(__file__))},
        "environment": environment_audit(),
        "two_place_gate": local_gate_certificate(),
        "claim_boundary": {
            "proved": [
                "the exact R, Q_59 and Q_71699 classification of all 32 E-side support classes",
                "the two-place reduction to the eight positive odd divisors of 105",
            ],
            "not_proved": [
                "an independent CAS reproduction of the minimal model or conductor",
                "a new rational point or an obstruction on C_H",
                "novelty from a database no-match",
            ],
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
