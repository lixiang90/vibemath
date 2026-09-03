# Round 09: independent-CAS gate and a closed two-place theorem

Date: 2026-09-04.

## 1. Fail-closed environment audit

The host was queried for application binaries `sage.exe`, `magma.exe`,
`gp.exe`, `pari-gp.exe`, and `mwrank.exe`, and for Python modules
`sageall`, `sage`, `cypari2`, `cypari`, and `eclib`.  Every query
returned not found.  In PowerShell, the bare token `gp` is the
`Get-ItemProperty` alias, not PARI/GP.

The only relevant installed arithmetic runtime is

```text
Python executable: C:\Python314\python.exe
Python version:    3.14.5
Python SHA-256:    3adbbf2af609e206e3ca18cd55fc7c4b52f5c8bb8218dd99fd5a9e50d7a193cd
SymPy version:     1.14.0
platform:          Windows-11-10.0.26200-SP0
```

Python/SymPy is the runtime of the first implementation.  It is not an
independent elliptic-curve CAS, so this round does **not** claim a second
reproduction of the minimal model, Kodaira symbols, split types, or
conductor.  No synthetic transcript or unavailable command is promoted to
evidence.

## 2. Replacement task: exact two-place classification

For

```text
E: y^2=x^3+a*x^2+b*x,
a=-591895071,
b=58536289153843200,
```

and a signed squarefree `d` supported on `{2,3,5,7}`, let

```text
C_d: N^2=F_d(U,V)
F_d=d*U^4+a*U^2*V^2+(b/d)*V^4.
```

The following theorem is now proved in the paper.

### Theorem

At either `p=59` or `p=71699`,

```text
C_d(Q_p) is nonempty
```

if and only if

```text
d in {-210,-70,-42,-30,-14,-10,-6,-2,
       1,3,5,7,15,21,35,105}.
```

Over the reals, `C_d(R)` is nonempty if and only if `d>0`.
Consequently, the real place together with either one of these finite places
reduces all 32 E-side support candidates to exactly

```text
{1,3,5,7,15,21,35,105}.
```

### Exact proof

Put

```text
delta=a^2-4*b=3^4*59*71699*339106321.
```

At `p=59,71699`, one has `v_p(delta)=1` and `p` does not divide
`2*d*b`.  Direct coefficient comparison proves

```text
4*d*F_d=(2*d*U^2+a*V^2)^2-delta*V^4.             (1)
```

If `(d/p)=1`, the point `(U:V)=(1:0)` works because `d` has a square
root in `Q_p`.  If `(d/p)=-1`, take a primitive p-adic pair `(U,V)`.

1. If `p|V`, then `F_d=d*U^4 mod p` is a nonsquare unit.
2. If `V` and `2*d*U^2+a*V^2` are units, (1) makes `F_d` have the
   nonsquare residue class of `d`.
3. If `V` is a unit and `p|(2*d*U^2+a*V^2)`, the right side of (1) has
   valuation exactly one, hence so does `F_d`.

These cases exhaust primitive pairs and prove necessity.  Quadratic
reciprocity gives at both primes

```text
(-1/p)=(2/p)=-1,   (3/p)=(5/p)=(7/p)=+1,
```

which gives the displayed 16 local classes.  At the real place, `d>0`
again has the `(1:0)` point.  When `d<0`, all coefficients `d,a,b/d`
are negative, so `F_d<0` off the excluded zero pair.  The intersection is
the eight positive odd divisors of 105.

This is a complete local theorem, not a bounded witness search.  It also
explains structurally why the E-side survivor set in the 512-cell
certificate is already forced by only two places.

## 3. Artifacts

- `code/NEXT_ELLIPTIC_ROUND_09.py`: standard-library-only environment audit,
  trial-division primality, exact Legendre classifications, and all 32
  support classes.
- `certificates/round09_two_place_gate.json`: frozen environment and theorem
  certificate.
- `code/NEXT_ELLIPTIC_ROUND_09_test.py`: six exact tests, including the
  manuscript statement.
- `paper/main.tex`: the fully proved two-place proposition.

Hashes:

```text
NEXT_ELLIPTIC_ROUND_09.py
  9334298cb02926d496622401a74d74712f8cc2081e4c03ff2612d6cd7ac0cf6b
round09_two_place_gate.json
  68f00a435d7ecf7a127746f4fe668fad791c6dab1ac295a8c8f16c05677cc75f
```

The certificate hash above precedes only later test-string cleanup; its
bound source script is unchanged.

## 4. Claim boundaries

Proved:

- complete real, Q_59, and Q_71699 classification of the 32 E-side support
  classes;
- exact two-place reduction to eight classes.

Not proved:

- an independent CAS verification of the minimal model or conductor;
- a new rational point on, or global obstruction to, the Campbell ninth
  curve;
- Mordell-Weil rank equality or a Cassels--Tate value;
- novelty from any database no-match.

The earlier isomorphism-class searches remain a dated, bounded search report.
This theorem rests only on the displayed exact local calculation, not on
database absence.

## 5. Verification and final paper artifact

The Round-09 module was run with warnings promoted to errors:

```text
python -W error -m unittest -v NEXT_ELLIPTIC_ROUND_09_test.py
Ran 6 tests: OK
```

The joint Campbell regression command ran 56 tests, including all earlier
same-parameter, clean-certificate, manuscript, and isomorphism-audit tests:

```text
python -W error -m unittest -q PAPER_ELLIPTIC_NEXT_test.py \
  PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py \
  PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py \
  test_same_m_local.py NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py \
  NEXT_ELLIPTIC_ROUND_09_test.py
Ran 56 tests: OK
```

The rebuilt `paper/main.pdf` has 10 A4 pages and 290546 bytes.  All ten
rendered pages were visually inspected; after correcting the purely
typographical token `-1,qquad` to `-1,\qquad`, the affected page was rendered
and inspected again.  No clipping, overlap, or malformed display was found.
The exact corrected token and absence of the malformed token are regression
tested.  The final LaTeX log contains no warning, overfull-box, or
underfull-box message.  Its SHA-256 is

```text
5509f6763f92416ddd37a318a2f46f1971e34ba31dc54784a61f037b6de57b36
```
