# Four-hit branch `0001`: a certified infinite family

Date: 2026-09-03
Status: **one of the 31 open color/position models is proved to have positive
rank and infinitely many inequivalent rational APs.**  The exact
Mordell--Weil group is not claimed.

## 1. Selected model

Among the 31 unresolved four-hit orbits, take

```text
counted positions = (0,1,3,4),  colors = 0001.
```

Write the first three same-color entries as

\[
A_0=X^3,\qquad A_1=Y^3,\qquad A_3=Z^3.
\]

The condition that they occupy positions `0,1,3` of one arithmetic
progression is exactly

\[
C:\quad 2X^3-3Y^3+Z^3=0.                         \tag{1}
\]

The full progression determined by a point of `C` is

\[
(A_0,\ldots,A_4)=
(X^3,Y^3,2Y^3-X^3,Z^3,4Y^3-3X^3).                \tag{2}
\]

Equation (1) makes all four consecutive differences in (2) equal to
`Y^3-X^3`.  Conversely every progression in this color/position model gives
a point of (1).  Thus no information is lost in the reduction.

The curve is smooth over `Q`: its partial derivatives are
`6X^2,-9Y^2,3Z^2`, which cannot vanish simultaneously at a projective point.
It is therefore a genus-one curve.  We use

\[
O=(1:1:1)
\]

as origin.  This point gives the constant progression and is the unique
point giving common difference zero.

## 2. A rational map to a Mordell curve

For a point `(X:Y:Z)` of `C`, put

\[
\begin{aligned}
N={}&6X^3Y^3+3Y^3Z^3-2Z^3X^3,\\
T={}&(2X^3+3Y^3)(-3Y^3-Z^3)(Z^3-2X^3).
\end{aligned}
\]

On `XYZ != 0`, define

\[
\phi(X:Y:Z)=
\left(\frac{N}{X^2Y^2Z^2},
-\frac{T}{2X^3Y^3Z^3}\right)=(u,v).              \tag{3}
\]

Exact polynomial division verifies

\[
T^2-4N^3+972X^6Y^6Z^6
=(2X^3-3Y^3+Z^3)H(X,Y,Z)                         \tag{4}
\]

for the explicit polynomial `H` computed by the accompanying script.
Hence (3) maps to

\[
E:\quad v^2=u^3-243.                              \tag{5}
\]

Formula (3) is the specialization of the classical diagonal-cubic
3-covering map, followed by the standard diagonal-to-Mordell change of
variables; identity (4) makes the present use self-contained.  As a rational
map from the smooth projective curve `C` to the proper curve `E`, it extends
across the finitely many apparent denominator points.  In fact there are no
rational points of `C` with `XYZ=0`, as such a point would make one of
`3,-2,3/2` a rational cube.

Two exact evaluations are

\[
\phi(O)=(7,-10)=-Q,
\]

and, for

\[
P=(4:1:-5)\in C(\Q),\qquad Q=(7,10)\in E(\Q),
\]

\[
\phi(P)=
\left(\frac{16009}{400},-\frac{2021723}{8000}\right)=2Q. \tag{6}
\]

The last equality follows directly from the tangent slope `147/20` at `Q`.

The integral Weierstrass equation (5) has discriminant

\[
\Delta=-16\cdot27\cdot243^2=-2^4 3^{13}.
\]

Since the integer point `Q=(7,10)` has nonzero `y` and
`10^2=100` does not divide the discriminant, Nagell--Lutz proves that `Q`
has infinite order.

Translate (3) by `-phi(O)`.  Any nonconstant morphism between genus-one
curves that sends origins to origins is an isogeny.  Its value at `P` is

\[
\phi(P)-\phi(O)=2Q-(-Q)=3Q,
\]

which is non-torsion.  Therefore `P` itself has infinite order in `C(Q)`.
In particular `C(Q)` has positive rank.

## 3. The infinite family and an explicit new example

Let

\[
P_n=O+n(P-O)\in C(\Q),\qquad n\in\mathbf Z.       \tag{7}
\]

Because `P-O` has infinite order, the points `P_n` are pairwise distinct.
For every `n != 0`, substitute `P_n=(X_n:Y_n:Z_n)` in (2).

No zero boundary is hidden here:

- `X_n,Y_n,Z_n` cannot vanish, by the cube-class observations above;
- `A_2=0` would make `2` a rational cube;
- `A_4=0` would make `4/3` a rational cube;
- the AP is constant only at `P_n=O`, hence only for `n=0`.

For `n != 0`, `A_4` cannot be a rational cube.  Otherwise positions
`0,1,3,4` would be four rational cubes in a nonconstant rational five-term
AP, contradicting Hajdu--Tengely's exact bound `P_5(3)=3`.  Let `D_n` be a
positive cube-free representative of `[A_4]`.  Then

\[
A_4=D_n W_n^3
\]

for some rational `W_n`, and `Q(cuberoot(D_n))` is genuinely cubic.  Thus
positions `0,1,3,4` in (2) have colors `0001` after the permitted
normalizations.  The already proved five-hit theorem shows that the omitted
position cannot also hit in the same field.

Distinct projective points of `C(Q)` give inequivalent APs under common
rational scaling: if the two progressions differ by `mu in Q*`, comparison
at the nonzero zeroth position makes `mu` a rational cube, and injectivity of
the rational cube map then makes all three projective coordinates differ by
one common factor.  Reversal has fibers of size at most two, so (7) still
gives infinitely many equivalence classes after reversal.

The first nonconstant member is the especially small example

\[
P=(4:1:-5),\qquad
(A_0,\ldots,A_4)=(64,1,-62,-125,-188).            \tag{8}
\]

It has common difference `-63`.  With `alpha^3=188`, the four counted terms
are

\[
4^3,\quad1^3,\quad(-5)^3,\quad(-\alpha)^3.
\]

This is not the earlier lower-bound example `(-3,-1,1,3,5)`: that example
uses four consecutive counted positions and lies in the color orbit `0110`
over `Q(cuberoot(3))`, whereas (8) omits the middle position 2, lies in orbit
`0001`, and uses `Q(cuberoot(188))`.

The family (7) is a genuine integer-parameter family obtained from the group
law, not a bounded search.  It is not a rational-function parametrization by
`P^1`; such a parametrization cannot exist because `C` is a smooth genus-one
curve.  The script makes (7) explicit by a two-chord construction.  The
tangent at `O` meets `C` again at `P`; for arbitrary points `R,S`, take the
third point on the line `RS`, then the third point on the line joining that
point to `O`.  This is exactly the group sum with origin `O`.

## 4. Reproducibility

Files:

- `code/PAPER_CUBE_FOURHIT_0001.py`: exact symbolic map identity, rational
  chord law, AP construction, Mordell group-law checks, and certificate
  generator;
- `code/PAPER_CUBE_FOURHIT_0001_test.py`: seven independent regression tests;
- `code/PAPER_CUBE_FOURHIT_0001_CERTIFICATE.json`: frozen exact data and the
  first four multiples.

Certificate SHA-256:

```text
8c5251d8893d942580dc8f6704467be1761407dec299e8019da34ea6457edbd6
```

Command:

```text
python -m unittest vibemath/powers-in-progressions/pure-cubic-five-term/code/PAPER_CUBE_FOURHIT_0001_test.py -v
```

Result: **7/7 passed**.  The tests verify membership among the 31 models,
smooth-model points/tangent, the cleared symbolic map identity, both special
images, Nagell--Lutz data, seven exact chord multiples, the AP identity and
zero boundary, and stored/live certificate equality.

## 5. Proven result and fail-closed boundary

Proved in this round:

> The four-hit orbit `(positions 0,1,3,4; colors 0001)` is a smooth genus-one
> branch of positive rank.  It contains infinitely many rational points and
> yields infinitely many inequivalent nonzero rational five-term arithmetic
> progressions with four hits in nontrivial pure cubic fields.

Not proved:

- the exact rank, torsion subgroup, or a full generator set for `C(Q)`;
- a classification of all rational points of this branch;
- any conclusion about the other 30 unresolved four-hit models.

Closing the full Mordell--Weil structure requires a certified descent/rank
calculation.  No such computation is inferred from the sample points, and no
bounded search is used as a substitute.

## Reference for the classical map

The general diagonal cubic covering formula is recorded in Brendan Creutz,
“The obstruction to the local-global principle for divisibility,” Lemma 9
(attributed there to Selmer/Euler):
<https://www.maths.usyd.edu.au/u/pubs/publist/preprints/2013/creutz-15.pdf>.
Only the explicit identity (4), independently checked in the script, is
needed for the argument above.
