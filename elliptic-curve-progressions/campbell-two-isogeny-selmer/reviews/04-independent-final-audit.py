"""Independent exact-arithmetic audit for the Round-06 elliptic final review.

This reviewer-owned script does not import the submission's Python modules.
It verifies the central polynomial, local-support, Selmer-cardinality and
Q x K identities directly from integer data and frozen JSON certificates.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
m, x, T = sp.symbols("m x T")

DCS = (-264815, -19343520, 62846856064, -2906312951808, -495507443511296)
HCS = (-850079, -11210976, 138714149248, -5501355374592, -1679721044504576)
D = sp.Poly.from_list(DCS, m).as_expr()
H = sp.Poly.from_list(HCS, m).as_expr()

G3 = -18816*m**4 + 677376*m**3 + 1922543616*m**2 - 48944480256*m - 40678301368320
G2 = 236896*m**4 - 9821952*m**3 - 22598349824*m**2 + 508953231360*m + 520252184657920
G1 = -958800*m**4 + 40985280*m**3 + 89932669440*m**2 - 1957723729920*m - 2113363439616000
G0 = 1292769*m**4 - 57304800*m**3 - 118795148928*m**2 + 2647001548800*m + 2758336954896384
G = sp.expand(G3*x**3 + G2*x**2 + G1*x + G0)
QS = (
    3*(379*m**2 - 8400*m - 17506624),
    743*m**2 - 17136*m - 33534272,
    415*m**2 - 11088*m - 16946752,
    3*(67*m**2 - 3696*m - 494656),
    209*m**2 - 17136*m + 5050432,
    263*m**2 - 25200*m + 10631872,
    63*(m**2 - 2352*m + 72256),
)

EA, EB = -591895071, 58536289153843200
EPA, EPB = -2*EA, EA*EA - 4*EB
DF = 1434501462453361
SEL_E = {1, 3, 5, 7, 15, 21, 35, 105}
SEL_EP = {1, 4230241, 339106321, DF}


def sf(n: int) -> int:
    ans = -1 if n < 0 else 1
    for p, e in sp.factorint(abs(n)).items():
        if e & 1:
            ans *= int(p)
    return ans


def h(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # Campbell reconstruction, including the two new square conditions.
    assert all(sp.expand(G.subs(x, j) - q*q) == 0 for j, q in enumerate(QS))
    assert sp.expand(G.subs(x, 7) - D) == 0
    assert sp.expand(G.subs(x, 8) - H) == 0
    assert sp.resultant(D, H, m) != 0
    assert sp.expand(G3 + 18816*(m*m - 72256)*(m*m - 36*m - 29920)) == 0
    assert not sp.ntheory.primetest.is_square(4*72256)
    assert not sp.ntheory.primetest.is_square(36**2 + 4*29920)
    # Campbell's excluded t=5/2 gives 7m^2-252m-209440=0.
    assert not sp.ntheory.primetest.is_square(252**2 + 4*7*209440)
    disc_x = sp.Poly(sp.cancel(sp.discriminant(G, x) / -65028096), m)
    assert disc_x.degree() == 16 and sp.Poly(disc_x, m, modulus=53).is_irreducible
    assert sp.discriminant(D, m) != 0 and sp.discriminant(H, m) != 0

    disc_d = int(sp.discriminant(D, m))
    disc_h = int(sp.discriminant(H, m))
    res = int(sp.resultant(D, H, m))
    branch_bad = sorted(set(sp.factorint(abs(disc_d))) | set(sp.factorint(abs(disc_h))) | set(sp.factorint(abs(res))))
    r6 = json.loads((ROOT / "PAPER_ELLIPTIC_ROUND_06_CERTIFICATE.json").read_text(encoding="utf-8"))
    sm = r6["same_m_local_summary"]
    assert sm["disc_D"] == disc_d and sm["disc_H"] == disc_h and sm["resultant_D_H"] == res
    assert sm["branch_bad_primes"] == branch_bad
    small_odd = {p for p in range(3, 101, 2) if sp.isprime(p)}
    assert 2 in branch_bad and set(sm["odd_primes"]) == (set(branch_bad) - {2}) | small_odd
    assert 101 + 1 - 10*math.sqrt(101) > 0
    for p, mv, dv, dr, hv, hr in sm["odd_witnesses"]:
        assert int(sp.Poly(D, m).eval(mv)) % p == dv == dr*dr % p
        assert int(sp.Poly(H, m).eval(mv)) % p == hv == hr*hr % p
        assert dr % p and hr % p  # y-derivatives are units, so Hensel applies.
    assert sm["two_adic_witness"]["D_mod_8"] == sm["two_adic_witness"]["H_mod_8"] == 1

    # Two-isogeny equations and complete bad-prime support.
    assert EPA == 1183790142 and EPB == 116194618458722241
    assert EPA*EPA - 4*EPB == 16*EB
    assert sp.factorint(EB) == {2: 18, 3: 12, 5: 2, 7: 5}
    assert sp.factorint(EPB) == {3: 4, 59: 1, 71699: 1, 339106321: 1}
    assert sorted({2, *sp.factorint(EB), *sp.factorint(EPB)}) == [2, 3, 5, 7, 59, 71699, 339106321]
    a, b, d = sp.symbols("a b d")
    assert sp.factor(sp.discriminant(d*T**4 + a*T**2 + b/d, T)) == 16*b*(a*a - 4*b)**2
    assert not sp.ntheory.primetest.is_square(EA*EA - 4*EB)
    assert not sp.ntheory.primetest.is_square(EPA*EPA - 4*EPB)

    # The recorded sets really are F2 groups of the stated sizes.
    for S in (SEL_E, SEL_EP):
        assert 1 in S and all(sf(u*v) in S for u, v in itertools.product(S, repeat=2))
    assert len(SEL_E) == 2**3 and len(SEL_EP) == 2**2
    assert (len(SEL_E)*len(SEL_EP)) // 4 == 2**3  # upper bound 2^rank <= 8

    # Q x K resolvent and z identities, independently over Q(sqrt(DF)).
    I = 36191335541877218738176
    J = 9700164465385312324077552400334848
    phi0 = 269378023424
    resolvent = sp.Poly(T**3 - 3*I*T + J, T)
    assert resolvent.eval(phi0) == 0
    qfac = sp.div(resolvent, sp.Poly(T - phi0, T))[0]
    assert qfac.all_coeffs() == [1, phi0, -36009487121810563530752]
    assert int(sp.discriminant(qfac.as_expr(), T)) == 12288**2 * DF
    assert sp.factorint(DF) == {59: 1, 71699: 1, 339106321: 1}
    zq = 9250179026780160
    assert zq == 35 * 16257024**2
    u, v = 2*57035568917881, -2*850079
    nk = u*u - DF*v*v
    assert nk == 35 * 15915620907648**2
    assert zq * (64**4 * nk) == 37093056870271943410974720**2
    assert -3*phi0 == 64**2 * (-197298357)

    # Frozen manifest bytes are all bound; report the tests omitted by the
    # publication manifests even though the 45-test development command runs.
    sup = json.loads((ROOT / "PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json").read_text(encoding="utf-8"))
    for item in sup["files"]:
        p = ROOT / item["path"]
        assert p.stat().st_size == item["bytes"] and h(p) == item["sha256"]
    rel = json.loads((ROOT / "PAPER_ELLIPTIC_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    for item in rel["files"]:
        p = ROOT / item["path"]
        assert p.stat().st_size == item["bytes"] and h(p) == item["sha256"]
    test_paths = {item["path"] for item in sup["files"] if item["path"].endswith("_test.py")}
    assert "PAPER_ELLIPTIC_NEXT_test.py" not in test_paths
    assert "PAPER_ELLIPTIC_ROUND_05_test.py" not in test_paths

    print(json.dumps({
        "status": "PASS",
        "branch_bad_primes": branch_bad,
        "selmer_cardinalities": [len(SEL_E), len(SEL_EP)],
        "rank_upper_bound": 3,
        "manifest_omitted_development_tests": ["PAPER_ELLIPTIC_NEXT_test.py", "PAPER_ELLIPTIC_ROUND_05_test.py"],
    }, indent=2))


if __name__ == "__main__":
    main()
