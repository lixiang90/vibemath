# Round 8: minimal model, conductor, and isomorphism-class audit

Date: 2026-09-03.

## Integrated theorem

The manuscript now proves that the Campbell-Jacobian equation is
Q-isomorphic, by

```text
X=36*x,  y_original=216*y_minimal+108*x,
```

to the global minimal equation

```text
y^2+x*y=x^3-16441530*x^2+45166889779200*x
[a1,a2,a3,a4,a6]=[1,-16441530,0,45166889779200,0].
```

The exact invariants are

```text
c4 = 2157171698920561,
c6 = 70577985500751764077559,
Delta_min = 2^28*3^16*5^4*7^10*59*71699*339106321,
N = 301245307115205810,
j = 10038160648206649953061393462836377818780518481
    /2926451742397178075653974744686961623040000.
```

Since `gcd(c4,Delta_min)=1`, every bad prime has `v_p(c4)=0`.
If an integral equation is nonminimal at `p`, its `c4` is divisible by
`p^4`; hence the displayed equation is minimal at every bad prime.
The criterion `v_p(Delta)>0`, `v_p(c4)=0` gives multiplicative reduction
of type `I_vp(Delta)` and conductor exponent one.  This proves semistability
and the displayed conductor.

### Independent check at 2 and 3

The proof is sufficient at residue characteristics 2 and 3.  It does not
invoke an odd-prime simplification of Tate's algorithm: the invariant-scaling
obstruction to nonminimality and the `v(c4)=0` multiplicative criterion hold
over every local field.  There is also a direct reduction certificate.  At
both primes the reduced affine equation is

```text
F(x,y)=y^2+x*y-x^3=0.
```

Its partial derivatives are `(y+x^2,x)` modulo 2 and `(y,2*y+x)` modulo 3,
so `(0,0)` is the unique affine singular point; the point at infinity is
smooth.  The tangent cone is `y(y+x)`, with two distinct rational factors
over both residue fields.  Thus the reduction at 2 and 3 is split
multiplicative, and no additional wild conductor term occurs.
This is also why the manuscript cites Silverman, *The Arithmetic of Elliptic
Curves*, Chapter VII, Section 5, rather than claiming an unaudited software
Tate-algorithm output.

## Prior-art and database search

The exact `a`-invariants, discriminant, conductor, `c4`, `j` numerator and
bad-prime support were searched on 2026-09-03.  Campbell's JIS article and
PDF, the accessible 1999 dissertation, its surviving author-page mirror,
EuDML metadata, arXiv-facing search, and the LMFDB completeness statement
were checked.  No indexed record of this Q-isomorphism class or these two
isogeny-Selmer computations was located.  Exact queries and URLs are frozen
in `notes/isomorphism-prior-art-search.md`.

This is a bounded no-match result, not a proof of novelty.  In particular,
the conductor is outside every complete LMFDB family stated at
https://www.lmfdb.org/EllipticCurve/Q/Completeness.  The safe claim remains
the manuscript's explicitly reproducible finite computation.  Absolute
priority would require a fuller human citation-graph and non-indexed-literature
audit.

## Verification

From `code/`:

```powershell
python -m unittest -q PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py test_same_m_local.py NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py
```

passes 50/50 tests.  The six minimal-model tests cover the coordinate
change, invariant scaling, factorization, minimality/reduction data,
conductor and `j`, disk certificate, exact manuscript formulas, and the
modulo-2/modulo-3 singular-locus and split-tangent-cone calculation.

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed in
three passes.  The nine-page PDF has no TeX warnings, overfull/underfull
boxes, undefined references, or multiply-defined labels.  All nine rendered
pages were visually checked.  Final PDF SHA-256:

```text
0C874FA9DC125BE37286DBE9C7A01E85824105D249D7817264BB7F9BCFBF4E44
```

The repository-wide `vibemath/tools/run_all_checks.py` currently stops in an
unrelated square-progressions manifest equality test before reaching this
package.  This round therefore claims the 50-test Campbell result only, not
a clean whole-repository run.

## Changed files

- `paper/main.tex`: theorem, proof, scope boundary, abstract/theorem summary.
- `paper/main.pdf`: rebuilt and visually audited nine-page paper.
- `code/NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py`: manuscript-formula regression.
- `NEXT_ELLIPTIC_MATH_NOVELTY_AUDIT.md`: resolved stale risk wording and test count.
- `notes/isomorphism-prior-art-search.md`: exact queries, author/publication/database scope.
- `NEXT_ELLIPTIC_ROUND_08_REPORT.md`: this audit record.

No withdrawn cross-isogeny Cassels--Tate expression was reintroduced or used
in the minimal-model, conductor, Selmer, or novelty conclusions.
