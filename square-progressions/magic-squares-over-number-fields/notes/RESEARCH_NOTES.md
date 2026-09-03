# Research note: a targeted attack on Boyer's open sub-problem 2

Date: 2026-08-29

## Selection

The most promising still-open item on the cited pages is the `3 x 3`
near-square problem (open sub-problem 2): construct a magic square with
eight distinct square entries, or another inequivalent example with seven
square entries.  This is more tractable than demanding all nine entries at
once, retains the elliptic-curve structure, and is the problem to which
Christian Boyer attached champagne and a monetary prize.

The old pages disagree on the amount: the 2005 lecture says EUR 100, while
later summaries and the 2025 literature say EUR 1,000.  The continued
availability and exact terms must therefore be confirmed with Boyer before
treating the prize as current.

Open problem 4 from the 2005 list is not a valid target anymore: Boyer found
an order-11 prime bimagic square in 2006, and order-8 examples followed.

## Exact reduction used here

Bremner writes every rational `3 x 3` magic square as

```text
a-b       a+b+c     a-c
a+b-c     a         a-b+c
a+c       a-b-c     a+b
```

Fix `c=n` and the congruent-number curve

```text
E_n: y^2 = x(x^2-n^2).
```

For a rational point `P`, if `X=x(2P)`, then `X-n`, `X`, and `X+n`
are rational squares.  Consequently:

- three certified centers `a-b, a, a+b` in arithmetic progression give
  nine rational squares;
- two certified centers contribute six square cells; if one of the three
  cells attached to the inferred third center is square, the result has at
  least seven square cells;
- multiplying all entries by a common rational square clears denominators
  while preserving which entries are rational squares.

This is the bridge from the full elliptic statement to the prize-bearing
7/8/9-square search.

## Literature update: arithmetic progressions on elliptic curves

The literature separates four conditions that should not be conflated:

1. arbitrary rational points whose `x`-coordinates are in arithmetic
   progression;
2. integral points whose `x`-coordinates are in arithmetic progression;
3. points in the identity coset `2E(Q)`;
4. the magic-square condition, which requires three points satisfying both
   (1) and (3), with the associated nine square values positive and distinct.

The following results are the most relevant.

### Rank at least two is necessary for the full nine-square problem

Bremner--Silverman--Tzanakis (2000) prove that, for squarefree `n`, a
rank-one subgroup of

```text
E_n: y^2 = x^3 - n^2 x
```

contains no non-trivial arithmetic progression of integral points.  Their
paper explicitly records Robertson's equivalence between a square magic
square and an integral arithmetic progression of three points in `2E(Q)`.
Cilleruelo--Granville subsequently give the rational `3 x 3` GAP formulation
in terms of `x(2P_i)` and state the resulting necessary condition:

```text
a non-trivial 3 x 3 GAP of squares forces rank(E_n(Q)) >= 2.
```

Thus excluding rank zero and rank one curves is theoretically justified for
the complete magic square of nine squares, not merely a search heuristic.
This does not imply that rank two is sufficient.  It also does not rule out
rank-zero or rank-one curves for the weaker seven- or eight-square partial
configurations searched here.

### The squarefree integral model contains no doubled integral point

Chan (Transactions of the AMS, 2022) studies integral points one coset at a
time in `E_D(Q)/2E_D(Q)`.  Her Theorem 1.4 includes the exact statement

```text
E_D(Z) intersect 2E_D(Q) = empty set
```

for positive squarefree `D`.  Therefore a magic-square search on the
squarefree model must retain rational denominators.  Clearing denominators
moves the points to the non-minimal isomorphic model `E_(D m^2)`, so results
about integral points on `E_D` cannot simply be applied after scaling.

There is also an elementary denominator consequence.  Write a non-torsion
point `Q in 2E_D(Q)` as

```text
x(Q) = (a/b)^2,  gcd(a,b)=1, b>0.
```

The 2-descent criterion gives integers `c,e` with

```text
c^2, a^2, e^2 in arithmetic progression,
common difference = D b^2.
```

This progression is primitive.  Primitive three-term progressions of integer
squares have common difference divisible by 24 (all three roots are odd and
nonzero modulo 3).  Hence

```text
24 divides D b^2.
```

In particular, `2|b` when `D` is even, `4|b` when `D` is odd, and `3|b`
unless `3|D`.  These are rigorous, inexpensive denominator checks for future
searches.

Chan also proves

```text
#E_D(Z) << 3.8^rank(E_D(Q))
```

and a 2024 sequel shows that the average number of non-torsion integral
points tends to zero as squarefree `D` varies.  These statistics reinforce
that an integral-only search on the minimal model is the wrong search space.

### Three-term progressions are finite on each fixed curve

Caro--Garcia-Fritz (Journal of Number Theory, 2025) classify the
positive-dimensional exceptional loci for

```text
c1*x(P1) + c2*x(P2) + c3*x(P3) = 0.
```

For the arithmetic-progression coefficients `(1,-2,1)` on the CM curve
`E_D` (which has `j=1728`), their list leaves only:

- constant triples coming from `P_i = +/- P`; and
- over the complex numbers, the CM symmetry `x([i]P)=-x(P)` with the
  middle point `(0,0)`.  Its rational instances reduce to the torsion
  progression `(-D,0,D)`.

After removing these degenerate cases, Uniform Mordell--Lang bounds the
number of triples in a finite-rank subgroup.  Applying their theorem to
`(2E_D(Q))^3`, whose rank is `3r`, gives a bound of the form

```text
number of non-degenerate doubled-point AP triples <= C^(3r+1)
```

with an absolute constant `C`.  This proves that every fixed curve has only
finitely many admissible triples, although the published constant/height
range is not practical enough to certify completion of a coefficient-box
search.

### What the long-progression rank theorems do and do not say

Garcia-Fritz--Pasten (IMRN, 2021) prove, for fixed `j`,

```text
1 + rank(E(Q)) >= c(j) * log(max AP length).
```

All congruent-number curves have `j=1728`, so the theorem applies uniformly
to the family.  It is important structurally, but a magic square asks for
only three terms; at length three it yields no useful numerical filter beyond
the sharper rank-at-least-two result above.  It constrains the length of an
AP, not the number or height of isolated three-term APs.

Two very recent preprints broaden this picture:

- Choi, *Additive Rigidity for x-Coordinates of Rational Points on Elliptic
  Curves* (arXiv v4, May 2026), gives effective rank-exponential bounds for
  rational points occupying a positive proportion of a generalized AP.
- Garcia-Fritz--Pasten, *Patterns on elliptic curves beyond Bremner's
  conjecture* (May 2026), treats APs, shifts, geometric progressions, and
  other patterns uniformly.

These support rank/height based enumeration, but neither yet supplies a
small explicit stopping bound for the three doubled points needed here.

### Constructive AP families are input data, not solutions

Spearman (2011) constructs infinitely many congruent-number curves with a
non-trivial rational `x`-arithmetic progression and rank at least three.
This is a promising source of test curves, but the three displayed points
must still pass the Kummer/2-descent test

```text
x-D, x, x+D are all rational squares
```

separately.  Generic AP constructions do not impose this identity-coset
condition.

That symbolic project has now been carried out for Spearman's displayed
triple.  Put

```text
A = 3u^4 - 4u^2v^2 + 12v^4
B = 3u^4 + 4u^2v^2 + 12v^4
n = 6AB,                  t = u/v
w^2 = 9t^4 + 4t^2 + 36.
```

The three x-coordinates from Spearman's Theorem 1 are

```text
x1 = -18(u^2-2v^2)^2 A
x2 = -3A^2
x3 = -48u^2v^2 A.
```

They satisfy `x1-2*x2+x3=0`, but `A>0`, so all three are strictly negative
for every admissible rational parameter.  Since the middle Kummer component
of a point in `2E_n(Q)` is its x-coordinate modulo squares, none of these
three AP points is a rational double.  Their alpha squareclasses are

```text
-2A,  -3,  -3A,
```

and Spearman's own descent lemmas show that these are outside the four alpha
classes of rational 2-torsion.  Thus adding a rational 2-torsion point cannot
move any of the displayed points into `2E_n(Q)` either.

Doubling the three points does not rescue the progression.  Exact symbolic
simplification gives

```text
x(2P1)-2x(2P2)+x(2P3)
  = v^8 (t^2-6)^2 (3t^2-2)^2 (3t^4+4t^2+12)^2
      (9t^8+88t^4+144)
    / [8t^2 (t^2-2)^2 (t^2+2)^2 (9t^4+4t^2+36)].
```

Every factor is positive for nonzero rational `t`: the possible zeros
`t^2=6` and `t^2=2/3` are not rational squares.  Hence the defect is always
strictly positive.  This rules out the displayed Spearman triple and its
doubles for the magic-square construction over the entire family, not just
at tested specializations.

The displayed progression is now also excluded over every quadratic and
cubic number field, even if the Spearman parameter itself is algebraic.  The
first two points have Kummer squareclasses

```text
P1: (-3, -2A, 6A),
P2: (-3A, -3, A),
```

where the parameter quartic makes
`9u^4+4u^2v^2+36v^4` a square.  The fixed class `-3` forces any quadratic
field of definition to be `Q(sqrt(-3))`.  In this field `P1` would require
`[A]=[-2]`, while `P2` would require `[A]=[1]`; these contradict because
`-2` is not a square in `Q(sqrt(-3))`.  A cubic field cannot contain the
quadratic subfield `Q(sqrt(-3))`, so the fixed class already excludes it.

Campbell's explicit seven-term cubic family has also been intersected with
the required CM locus.  For a cubic `y^2=a*x^3+b*x^2+c*x+d`, the condition
`j=1728` is

```text
2*b^3 - 9*a*b*c + 27*a^2*d = 0.
```

Substitution of Campbell's coefficient polynomials gives one irreducible
degree-12 polynomial over `Q`.  Thus this family has no `j=1728`
specialization with its parameter in a quadratic or cubic field.  The exact
calculation is in `campbell_j1728.py`, and the broader literature comparison
is in `AP_FAMILY_LITERATURE.md`.

The full-2-torsion test strengthens this exclusion.  On the degree-12
`j=1728` field, the short coefficient is `p(m)`.  Although the field norm of
`-p(m)` is a rational square, eliminating `H12(m)=0` and `z^2=-p(m)` gives
an irreducible degree-24 polynomial.  Hence the degree-12 curve does not yet
have full 2-torsion; the congruent-number model requires a degree-24 field.

Bremner's long Weierstrass family has now been treated similarly.  Its main
seven-term family has

```text
B = 324 r^2(r-1)^2(r-2)^2(r^2-2r+2)^2.
```

The only nondegenerate `j=1728` parameters are `r=1+-i`.  At `r=1+i` the
model has `d=-12i`, `A=1008`, and `B=0`; full 2-torsion needs `sqrt(7)`.
The eighth-point equations reduce to `+-48i`, whose square root has the
irreducible polynomial `z^4+2304`, so eight points plus full 2-torsion live
naturally over `Q(i,sqrt(6),sqrt(7))`, of degree 8.  None of the eight
displayed points passes the full Kummer test there.  Bremner's second
seven-term family has an irreducible degree-24 `j=1728` parameter divisor.
The proof and scripts are in `BREMNER_CAMPBELL_RESULTS.md` and
`bremner_j1728.py`.

There is also a parameter redundancy:

```text
(t,w) -> (2/t, 2w/t^2)
```

preserves the quartic and replaces `(A,B,n)` by `(4A,4B,16n)`.  The two
congruent-number models are related by the square scaling
`(x,y)->(16x,64y)`.  Searches should therefore identify `t` with `2/t` and
normalize `n` to its squarefree part before spending a coefficient box.

The rank-three subgroup remains useful even though its displayed AP is
excluded: other even linear combinations can still supply centers.  On the
first specialization `(t,w)=(1,7)`, it gives `n=1254` and the classical AP
`-528,-363,-198`.  Exact searches using the three displayed independent
points found no seven-square candidate in coefficient boxes `[-3,3]^3`
(171 distinct doubled centers) or `[-6,6]^3` (1098 centers).  This is finite
computational evidence, not a proof for the whole rank-three subgroup.  The
next small quartic specialization, represented by `(t,w)=(9/14,1227/196)`,
normalizes to the distinct squarefree curve `D=151343798406`; its box
`[-6,6]^3` likewise has 1098 doubled centers and no seven-square candidate.
The points `(2,14)` and `(28/9,818/27)` give only the square-scaled partners
of these two curves under the involution above, so they were not counted as
new cases.

### Exact generation and subgroup screening inside the Spearman family

The parameter quartic is now explored without a denominator grid.  If three
points `(t_i,w_i)` with distinct `t_i` are given, interpolate the unique
quadratic

```text
q(t) = a t^2 + b t + c,       q(t_i)=w_i.
```

The polynomial `q(t)^2-(9t^4+4t^2+36)` already has the three known roots.
Vieta's formula gives the fourth intersection exactly as

```text
t4 = -2ab/(a^2-9) - t1 - t2 - t3,
w4 = q(t4).
```

Starting with `(0, +/-6)`, `(1, +/-7)`, and `(2, +/-14)`, two closure rounds
produce 30 points and four essential nonzero parameter orbits after quotienting
by signs and `t <-> 2/t`:

```text
t=1                         D=1254
t=9/14                      D=151343798406
t=230/703                   D=3235718212535074888133094
t=206136/147103             D=4510914192331471444132821067497825254945286
```

All four curves have 171 distinct doubled centers in `[-3,3]^3` and no
seven-square candidate.  For each of the first two, the stronger seven-square
search through `[-6,6]^3` has 1098 centers and no candidate.  A direct
all-certified-center AP scan through `[-8,8]^3` gives 2456 centers and zero
three-term APs on **each of all four curves**.

Increasing the closure component bound from `10^12` to `10^30` adds two more
essential orbits:

```text
t=29662529/95793739
D=6148412284798866852021651273650987070783848221907786749722725749734

t=482976761260/730628799543
D=524510820405164156661512386553380031246438794003828570714629108935180129559409756254907487337606
```

Their `[-3,3]^3` searches likewise have 171 doubled centers, zero fully
certified center APs, and zero seven-square candidates.  These six cases are
not a proof about the family, but they show that the rank-three construction
does not have an immediately visible low-height doubled-point AP mechanism.

For the full-center scan, reduction modulo the large prime `1000003` is now
used before exact midpoint construction.  This is a necessary filter with no
false negatives and reduces millions of high-height `Fraction` additions to
only the residue-compatible pairs.

Mendoza Roca's 2019 master's thesis proves an explicit bound `d<=13` for
long integral APs on rank-two congruent curves under additional hypotheses
(`x(P_i)>=D`, coprimality, and height greater than 40).  It is useful evidence
for height-based methods but does not constrain a three-term rational magic
candidate.  The thesis also mistakenly labels the common `j`-invariant as
`0`; for `y^2=x^3-D^2x` it is `1728`.

### Revised search priorities from the literature

1. Keep the rigorous `rank >= 2` gate for the complete nine-square problem;
   retain rank-one curves when targeting only a seven- or eight-square partial
   configuration.  Do not assume rank-one rational progressions are
   impossible outside the integral setting.
2. Never enumerate only integral `x` on squarefree `E_D`; enumerate rational
   points in `2E_D(Q)` and enforce `24 | D b^2` on the denominator of every
   certified center.
3. Do not pursue Spearman's displayed AP triple further: its Kummer classes
   and doubled-AP defect exclude it identically.  Use the family only as a
   source of rank-three subgroups, searching other even linear combinations.
4. Treat each fixed curve as a finite problem in principle, while recording
   that no usable uniform height cutoff is currently known.
5. Prioritize curves by certified rank, small generator heights, and an
   unusually high density of trivial Kummer classes; rank alone is too weak.

## Implementation

`spearman_kummer.py` transcribes Spearman's Theorem 1 exactly, verifies the
curve equations and original AP, computes the full Kummer square tests,
checks the factorized doubled-AP defect, and optionally sends the three
independent points to the exact coefficient-box searcher.

`spearman_parameters.py` implements the exact fourth-intersection generator,
the sign and `t <-> 2/t` quotient, squarefree-model normalization, and optional
batch searches of every generated rank-three subgroup.

`magic_square_search.py` implements:

1. exact group law on `E_n` using `fractions.Fraction`;
2. generator combinations in a coefficient box;
3. certification of `x(2P)-n`, `x(2P)`, and `x(2P)+n` as rational squares;
4. all three arithmetic-progression closures determined by each pair;
5. a necessary local-square sieve at 16 small odd primes;
6. exact final square tests, distinctness, positivity, denominator clearing,
   and all eight magic-line checks.

The local sieve has no false negatives: a rational square must reduce to a
quadratic residue at every prime where its denominator is nonzero.

## Calibration: E_154

LMFDB label: `379456.ei3`

Certified rank: 2

Generators:

```text
G1 = (-98, 1176)
G2 = (350, 5880)
```

In the coefficient box `[-10,10]^2`, the program found 220 distinct
certified centers and recovered exactly the known Bremner class:

```text
139129  360721   42025
 83521  180625  277729
319225     529  222121
```

Every row, column, and diagonal sums to 541875.  Exactly seven entries are
squares.  This is a rotation/reflection of the standard presentation.

## New bounded campaign: E_210

The current LMFDB CM=-4, rank-at-least-2 catalogue contains one exact model
`E_n` with `n>200`: `E_210`, label `705600.vn3`.

Certified rank: 2

Generators and canonical heights:

```text
G1 = (-84, 1764)    height 1.7702105785938859...
G2 = (294, 3528)    height 1.8636696426994850...
```

Result for the complete coefficient box `[-20,20]^2`:

```text
distinct certified centers: 840
center pairs:                352380
AP closures tested:          1057140
new >=7-square candidates:   0
```

Each closure was rejected either by a rigorous local nonresidue obstruction
or by the exact rational-square test.  This does **not** prove that `E_210`
has no solution outside the coefficient box, and says nothing global about
other `n` absent from the current LMFDB catalogue.

## Recommended next attack

Do not merely increase every coefficient box.  The useful next steps are:

1. obtain certified generators for squarefree `n>210` with rank at least 2,
   prioritizing low canonical height;
2. record which of the three third-center cells survives each local prime,
   then choose curves whose closure masks decay unusually slowly;
3. enlarge to `[-40,40]` only on those curves;
4. in parallel, study a parametrized elliptic fibration through the Bremner
   class, because uniform height growth on isolated curves has poor yield.

## Sources and status caveats

- Christian Boyer, [Magic squares of squares](https://www.multimagie.com/English/SquaresOfSquares.htm).
- Andrew Bremner, [On squares of squares](https://matwbn.icm.edu.pl/ksiazki/aa/aa88/aa8837.pdf), Acta Arithmetica 88 (1999), 289-297.
- Andrew Bremner, Joseph H. Silverman, and Nikos Tzanakis,
  [Integral points in arithmetic progression on y^2=x(x^2-n^2)](https://doi.org/10.1006/jnth.1999.2430),
  Journal of Number Theory 80 (2000), 187-208.
- Daniel M. Kane, Pär Kurlberg, and others' formulation is also discussed in
  [Lattice points on circles, squares in arithmetic progressions and sumsets of squares](https://matematicas.uam.es/~franciscojavier.cilleruelo/Papers/lattice%20points%20progressions.pdf).
- Blair K. Spearman,
  [Arithmetic progressions on congruent number elliptic curves](https://doi.org/10.1216/RMJ-2011-41-6-2033),
  Rocky Mountain Journal of Mathematics 41 (2011), 2033-2044.
- Natalia Garcia-Fritz and Hector Pasten,
  [Elliptic curves with long arithmetic progressions have large rank](https://arxiv.org/abs/1910.14485),
  International Mathematics Research Notices 2021, 7394-7414.
- Stephanie Chan,
  [Integral points on the congruent number curve](https://arxiv.org/abs/2004.03331),
  Transactions of the AMS 375 (2022), 6675-6700; and
  [The average number of integral points on the congruent number curves](https://arxiv.org/abs/2112.01615),
  Advances in Mathematics 457 (2024), 109946.
- Jerson Caro and Natalia Garcia-Fritz,
  [Linear x-coordinate relations of triples on elliptic curves](https://arxiv.org/abs/2310.17592),
  Journal of Number Theory 271 (2025), 109-121.
- Seokhyun Choi,
  [Additive Rigidity for x-Coordinates of Rational Points on Elliptic Curves](https://arxiv.org/abs/2510.03828),
  preprint, version 4 (2026).
- Natalia Garcia-Fritz and Hector Pasten,
  [Patterns on elliptic curves beyond Bremner's conjecture](https://arxiv.org/abs/2605.14962),
  preprint (2026).
- Matteo Rome and Shuntaro Yamagishi,
  [On the existence of magic squares of powers](https://link.springer.com/article/10.1007/s40993-025-00671-5),
  Research in Number Theory 11 (2025), confirms that the `3 x 3` square case
  remains outside the general existence theorem for orders at least 4.
- [LMFDB](https://www.lmfdb.org/) supplied the certified ranks, generators,
  and heights used in the two curve experiments.
- A July 2026 public repository reports searches through `n<=200`; it is an
  AI-generated, non-peer-reviewed working archive, so it was used only to
  choose a non-overlapping experiment, not as proof:
  [project status](https://github.com/mystimath/magic-square-of-squares-3x3/blob/main/STATUS.md).
