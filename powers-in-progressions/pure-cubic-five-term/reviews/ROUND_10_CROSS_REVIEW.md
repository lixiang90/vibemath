# Round 10 cross-review: second $3+1$ cubic

Date: 2026-09-04
Reviewer: elliptic-line cross-review
Verdict: **PASS**

I reviewed the Round-10 additions concerning

\[
C':3X^3-4Y^3+Z^3=0
\]

and the two models `((0,1,2,4),0010)` and
`((0,1,3,4),0010)`.  I checked the standalone Round-10 note, its exact
script, frozen JSON certificate and tests, and the corresponding claims
propagated to the main paper, README, novelty audit, and submission material.
No blocking mathematical error was found.

## 1. The covering identity and the target curve

With

\[
\begin{aligned}
N'&=12X^3Y^3+4Y^3Z^3-3Z^3X^3,\\
T'&=(3X^3+4Y^3)(-4Y^3-Z^3)(Z^3-3X^3),
\end{aligned}
\]

independent exact polynomial division gives

\[
(T')^2-4(N')^3+3888X^6Y^6Z^6
=(3X^3-4Y^3+Z^3)H'
\]

with zero remainder.  The computed quotient is nonzero (total degree 15,
12 terms).  Dividing the identity on $C'$ by
$4X^6Y^6Z^6$ verifies, term for term, that

\[
u=\frac{N'}{X^2Y^2Z^2},\qquad
v=-\frac{T'}{2X^3Y^3Z^3}
\]

satisfy $v^2=u^3-972$.  Thus the sign and the factor $3888=4\cdot972$
in the manuscript are correct.

The displayed formula is defined at both points used in the proof.  The
three coordinate-zero cases on $C'(\mathbf Q)$ would respectively require
$4$, $-3$, or $4/3$ to be rational cubes, so no rational point is lost
in the later arithmetic argument.  More generally, the rational map extends
from the smooth projective curve $C'$ to the proper curve $E'$; this is
the standard extension theorem for maps from nonsingular curves and is used
correctly.

## 2. Point images and the Mordell calculation

Direct substitution gives

\[
\phi'(1:1:1)=(13,-35)=-Q',\qquad Q'=(13,35).
\]

For $P'=(5:2:-7)$, the numerator and denominator of the first coordinate
are $129649$ and $4900$, and exact substitution gives

\[
\phi'(P')=
\left(\frac{129649}{4900},
-\frac{45441143}{343000}\right).
\]

Doubling $Q'$ on $v^2=u^3-972$ uses slope
$3\cdot13^2/(2\cdot35)=507/70$ and produces exactly this point.  Hence the
two asserted images and the equality $\phi'(P')=2Q'$ are correct.

## 3. Nagell--Lutz and the meaning of $P'-O'\mapsto3Q'$

For the integral short Weierstrass equation $v^2=u^3-972$,

\[
\Delta=-16\cdot27\cdot972^2=-2^8 3^{13}=-408146688.
\]

The point $Q'=(13,35)$ is integral and lies on the curve.  It has nonzero
second coordinate, while $35^2=5^2 7^2\nmid\Delta$.  The Nagell--Lutz
torsion criterion therefore proves that $Q'$ is non-torsion.  No
minimal-model assumption is needed for this exclusion: the theorem applies
to the displayed nonsingular integral short Weierstrass equation, and the
divisibility by its discriminant is a necessary condition for integral
torsion points with nonzero second coordinate.

The phrase “$P'-O'$ maps to $2Q'-(-Q')=3Q'$” is also correct.  It does
not mean coordinate subtraction on the plane cubic.  Translating the target
map by $-\phi'(O')=Q'$ produces an origin-preserving nonconstant morphism

\[
f(R)=\phi'(R)-\phi'(O').
\]

An origin-preserving nonconstant morphism of genus-one curves is an
isogeny/group homomorphism, and

\[
f(P')=\phi'(P')-\phi'(O')=2Q'-(-Q')=3Q'.
\]

Since $3Q'$ is non-torsion, $P'-O'$ cannot be torsion.  This proves
positive rank; the finite list of chord-law multiples is only a regression
check and is not being substituted for the infinite-order proof.

## 4. The two cubic fields and exact four-hit property

The progression attached to a point of $C'$ is

\[
(X^3,Y^3,2Y^3-X^3,3Y^3-2X^3,Z^3).
\]

Its common-difference identity is exact.  For every nonidentity point in
the Mordell--Weil orbit it is nonconstant: $X^3=Y^3$ over $\mathbf Q$
forces $X=Y$, and the curve then forces $Z=X$, giving $O'$.  Its three
repeated-color terms are nonzero by the coordinate-zero check.  The two
middle terms cannot vanish, since that would make $2$ or $3/2$ a
rational cube.

If either middle term were a rational cube, positions $0,1,4$ together
with that term would be four rational cubes in a nonconstant rational
five-term AP.  The earlier denominator-clearing reduction puts this within
the hypotheses of the cited Hajdu--Tengely equality $P_5(3)=3$.  Therefore
both middle rational cube classes are nontrivial.  A positive cube-free
representative $D$ of either class is consequently not a rational cube,
so $x^3-D$ is irreducible over $\mathbf Q$ by the rational-root criterion;
both fields used in the construction have degree exactly three.

For the first point the AP is

\[
(125,8,-109,-226,-343),\qquad d=-117.
\]

The two exact cube-class vectors are

\[
\begin{array}{c|ccccc}
D&0&1&2&3&4\\ \hline
109&0&0&1&\ast&0\\
226&0&0&\ast&1&0,
\end{array}
\]

where $\ast$ is a non-hit.  Here $109$ is prime and
$226=2\cdot113$, so both radicands are positive, cube-free, noncubes and
define cubic fields.  The omitted term is also independently excluded in
the example: $v_{113}(-226)=1$ but every class in
$\langle109\rangle\subset\mathbf Q^*/\mathbf Q^{*3}$ has
$113$-valuation $0$, and $v_{109}(-109)=1$ but every class in
$\langle226\rangle$ has $109$-valuation $0$.

Uniformly in the infinite families, the Kummer-kernel lemma gives the four
claimed hits, while the proved global theorem
$R^\times_{(3,1)}(5)=4$ excludes the remaining term.  Thus “exactly four
hits” is justified and is not inferred merely from the sample certificate.

## 5. Infinitely many inequivalent progressions

The points $O'+n(P'-O')$ are pairwise distinct because $P'-O'$ is
non-torsion.  Suppose two progressions arising from points
$(X:Y:Z)$ and $(X':Y':Z')$ are related by common rational scaling
$\lambda$.  Comparing position 0 gives
$\lambda=(X'/X)^3=\mu^3$ with $\mu\in\mathbf Q^*$.  Positions 1 and 4
then give $Y'=\mu Y$ and $Z'=\mu Z$, because cubing is injective over
$\mathbf Q$.  The projective points are therefore equal.  Consequently
common scaling has singleton fibers on this family, and adding reversal
enlarges a fiber by at most a factor of two.  Infinitely many equivalence
classes remain.  The inference in the paper is valid.

## 6. Computational reproduction and boundary

The complete cube-line test suite was run from the repository root with

```text
python -W error -m unittest discover \
  -s powers-in-progressions/pure-cubic-five-term/code -p "*_test.py" -v
```

Result: **36 tests run, 36 passed**, including all seven new Round-10 tests.
The stored Round-10 JSON agrees exactly with live certificate generation.

The verdict is mathematical **PASS**.  This review does not certify an exact
rank, a full Mordell--Weil basis, database-level novelty/priority, or any of
the 25 remaining four-hit models; the author files make none of those
claims.  There is still no independent second-CAS reproduction of the large
polynomial division.  That is a nonblocking reproducibility limitation,
because the identity is exact, deterministic, test-covered, and its
mathematical consequences were independently checked above.  As optional
release hardening, the JSON could later record the generator-script hash and
software versions; this does not affect the present correctness verdict.
