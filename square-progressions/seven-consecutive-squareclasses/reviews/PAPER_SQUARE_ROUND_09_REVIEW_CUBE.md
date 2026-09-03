# Independent review of the Round-09 mask-90 gate

Date: 2026-09-04

## Decision

**PASS.** I found no mathematical or certificate-integrity defect in the
mask-90 gate.  The complete integral-point argument, the occurrence audit,
and the resulting reduction from ten patterns to seven are valid.  The claim
boundary in the manuscript is also correct: none of the seven survivors is
proved realizable or impossible, and the result does not decide \(R_2(7)\).

## Independent occurrence recomputation

I used the ten IDs stored by the preceding mask-51 certificate and recomputed
membership from the Round-02 quotient lists.  This does not call any function
from `PAPER_SQUARE_MASK90.py`.  As a second independent check, I read each
restricted-growth partition as labels in
\(\mathbf F_2^2=\{0,(1,0),(0,1),(1,1)\}\) and tested the character support
\(\{1,3,4,6\}\) directly: its cardinality is even and its selected label sum
must vanish.

| ID | partition | labels at positions 1,3,4,6 | mask 90 in relation space? |
|---:|:---:|:---:|:---:|
| 12 | 0012202 | 0,2,2,2 | no |
| 31 | 0001202 | 0,1,2,2 | no |
| 43 | 0100021 | 1,0,0,1 | yes |
| 59 | 0012231 | 0,2,2,1 | no |
| 134 | 0012131 | 0,2,1,1 | no |
| 214 | 0122213 | 1,2,2,3 | no |
| 230 | 0012102 | 0,2,1,2 | no |
| 251 | 0102221 | 1,2,2,1 | yes |
| 276 | 0010203 | 0,0,2,3 | no |
| 281 | 0102003 | 1,2,0,3 | yes |

Thus the affected IDs are exactly \(43,251,281\), and subtraction from the
frozen ten-ID input gives exactly

\[
  12,31,59,134,214,230,276.
\]

The independent result agrees with the Round-04 occurrence records.  Their
only mask-90 rows are `P43:m90`, `P251:m90`, and `P281:m90`; all have
representative mask 45, class 5, and the affine map \(t=u-1\).  Each source
row has 15 distinct character masks.  Therefore the asserted \(10\to7\)
count is **PASS**.

## Independent arithmetic proof audit

Set

\[
 A=(t+1)(t+6),\qquad B=(t+3)(t+4).
\]

Direct expansion gives \(B-A=6\), whence
\(\gcd(A,B)=\gcd(A,6)\).  For \(t\le-7\) or \(t\ge0\), both \(A\) and \(B\)
are positive.  If \(AB\) is a square, the parity of every prime valuation in
\(A\) equals that in \(B\).  Hence their squarefree parts are the same positive
integer \(d\); moreover \(d\mid\gcd(A,B)\mid6\).  This proves, rather than
assumes, the complete list \(d\in\{1,2,3,6\}\), with

\[
 A=dU^2,\quad B=dV^2,\quad d(V^2-U^2)=6,
\]

where \(U,V>0\) and \(V>U\).

- \(d=1\): \(V^2-U^2=6\equiv2\pmod4\), impossible.
- \(d=2\): \((V-U)(V+U)=3\).  Positivity and equal parity leave only
  \((1,3)\), so \((U,V)=(1,2)\) and \(A=2\).  But the exact identity
  \((2t+7)^2=4A+25\) would give a square equal to 33, impossible.
- \(d=3\): \(V^2-U^2=2\equiv2\pmod4\), impossible.
- \(d=6\): \((V-U)(V+U)=1\) forces \(U=0,V=1\), contradicting \(A>0\).

This covers both unbounded sign regions and all four squarefree branches:
**PASS**.

The complementary integer interval is exactly \(-6\le t\le-1\).  Direct
substitution gives \(0,-8,0,0,-8,0\), hence precisely

\[
(-6,0),(-4,0),(-3,0),(-1,0).
\]

There are no omitted rational ordinates: if \(y\in\mathbf Q\) and
\(y^2\in\mathbf Z\), a reduced denominator argument gives \(y\in\mathbf Z\).
The four points are branch points and each parameter makes one of
\(t,t+1,\ldots,t+6\) zero.  The other zero-boundary parameters
\(t=-5,-2,0\) have respectively right sides \(-8,-8,72\), so none yields an
additional rational point.  Middle interval, sign, and zero boundaries are
all **PASS**.

## Artifact and manuscript checks

- Certificate SHA-256 independently recomputed as
  `2d07dcf9c1b237001e7e25cf2af0e6e3baa7f3b7fee3662fb6568e5caffa5c28`:
  **PASS**.
- The certificate's three input hashes match the files on disk: **PASS**.
- The eight dedicated mask-90 tests pass: **8/8**.
- The complete squareclasses suite passes: **78/78**.
- `paper/main.tex` states the same curve, proof, exact reduction chain and
  seven-row table, and explicitly retains the unresolved claim boundary:
  **PASS**.

## Non-blocking observation

The shipped tests mainly check regeneration through the author generator;
they are not by themselves an independent proof of occurrence completeness.
The direct partition-label recomputation above supplies that missing
review-level independence.  No source change is required for correctness.
