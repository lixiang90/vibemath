# Elliptic-curve AP families and the magic-square filter

Date: 2026-08-31

## The filter specific to this problem

A useful family must pass three successively stronger tests.

1. Its displayed points have `x`-coordinates in a nonconstant arithmetic
   progression.
2. After an affine Weierstrass change of `x`, the curve is a congruent-number
   curve

   ```text
   E_n: y^2 = x^3 - n^2 x,       j(E_n)=1728.
   ```

   An affine change `x -> u^2*x+r` preserves arithmetic progressions.
3. Each of the three points belongs to `2E_n(K)`. With the rational
   2-torsion roots `-n,0,n`, this is the full Kummer condition

   ```text
   x-n, x, x+n are all squares in K.
   ```

The first condition alone is common in the literature; the third is the
rare condition equivalent to a square magic square.

For a cubic model

```text
y^2 = a*x^3+b*x^2+c*x+d,
```

put `X=a*x`, `Y=a*y`. The monic equation is

```text
Y^2 = X^3+b*X^2+a*c*X+a^2*d.
```

Its `j=1728` condition is

```text
2*b^3 - 9*a*b*c + 27*a^2*d = 0.
```

This gives a direct elimination test for any published cubic AP family.

## Main constructive papers

### Spearman: the exact ambient family, but not its displayed triple

Blair K. Spearman, *Arithmetic Progressions on Congruent Number Elliptic
Curves*, Rocky Mountain Journal of Mathematics 41 (2011), 2033--2044,
DOI 10.1216/RMJ-2011-41-6-2033.

This is the closest paper to the target: it gives an infinite `j=1728`
family and three independent rational points in `x`-arithmetic progression.
Writing

```text
A = 3u^4-4u^2v^2+12v^4,
B = 3u^4+4u^2v^2+12v^4,
n = 6AB,
w^2 v^4 = 9u^4+4u^2v^2+36v^4,
```

the first two displayed coordinates have Kummer factors

```text
P1: x-n = -12 A^2,
    x   = -18(u^2-2v^2)^2 A,
    x+n =  96u^2v^2 A;

P2: x-n = -3A(9u^4+4u^2v^2+36v^4),
    x   = -3A^2,
    x+n =  9(u^2+2v^2)^2 A.
```

The quartic relation makes the second factor in `P2` a square. Both points
therefore contain the fixed nontrivial squareclass `-3`. This gives a proof
even when the Spearman parameter itself is algebraic. Over a quadratic
field, either point being a double forces `sqrt(-3)` into the field, hence
the field is `Q(sqrt(-3))`. There `P1` requires `[A]=[-2]`, while `P2`
requires `[A]=[1]`. Since `-2` is not a square in `Q(sqrt(-3))`, they cannot
both be doubles. A cubic field cannot contain `Q(sqrt(-3))` at all, by the
tower law, so already the fixed `-3` factor rules it out.

**Conclusion.** Spearman's displayed AP cannot produce a square magic
square over a quadratic or cubic field, even allowing algebraic parameter
specializations. Other even linear combinations in the rank-three subgroup
remain possible.

### Campbell: a general cubic AP family meets j=1728 only in degree 12

Garikai Campbell, *A Note on Arithmetic Progressions on Elliptic Curves*,
Journal of Integer Sequences 6 (2003), Article 03.1.3.

Campbell gives a one-parameter cubic family with seven points at
`x=0,1,...,6`; imposing one further square gives an auxiliary rank-two
elliptic curve and length eight. Applying the preceding invariant formula
to the explicit coefficients gives

```text
c6(m) = constant * H12(m),
```

where `H12` is irreducible over `Q` and has degree 12. The complete
polynomial and reproducible calculation are in `campbell_j1728.py`.

**Conclusion.** No parameter in a quadratic or cubic field specializes
this explicit family to `j=1728`. The remaining full-2-torsion test is now
also complete. Although the norm of `-p` is a rational square, eliminating
`H12(m)=0` with `z^2=-p(m)` gives an irreducible degree-24 polynomial in
`z`. Thus `-p` is not a square in the degree-12 field, and the field needed
for full 2-torsion has degree 24.

Campbell's quartic families are much less useful here. Their arithmetic
progression is in the quartic-model coordinate, and the birational map to a
Weierstrass model is nonlinear in that coordinate, so it normally destroys
the progression.

### Bremner: length-eight Weierstrass families

Andrew Bremner, *On Arithmetic Progressions on Elliptic Curves*,
Experimental Mathematics 8 (1999), 409--413,
DOI 10.1080/10586458.1999.10504629.

Bremner constructs infinitely many Weierstrass curves with eight rational
points in `x`-arithmetic progression; an auxiliary elliptic curve of rank
one parametrizes the construction. Because the allowed Weierstrass change
is affine in `x`, this is a legitimate source family.

The exact intersection is now computed. In the main seven-term family the
nondegenerate `j=1728` condition is `r^2-2r+2=0`, hence `r=1+-i`. The
specialized model has `A=1008`, so full 2-torsion also requires `sqrt(7)`.
Extending the progression to eight terms requires a root of the irreducible
polynomial `z^4+2304`, equivalently a `sqrt(6)` extension. The natural field
containing the eight points and full 2-torsion is therefore
`Q(i,sqrt(6),sqrt(7))`, of degree 8. A direct Kummer squareclass calculation
shows that none of the eight displayed points lies in `2E` over this field.

Bremner's second seven-term family meets `j=1728` on an irreducible
degree-24 parameter polynomial. The details and exact scripts are in
`BREMNER_CAMPBELL_RESULTS.md` and `bremner_j1728.py`.

### Bremner--Silverman--Tzanakis: explicit torsion AP branches

A. Bremner, J. H. Silverman, and N. Tzanakis, *Integral Points in
Arithmetic Progression on y^2=x(x^2-n^2)*, Journal of Number Theory 80
(2000), 187--208, DOI 10.1006/jnth.1999.2430.

Besides its rank-one exclusion theorem, this paper parametrizes three-term
integral progressions containing a rational 2-torsion point. This is a
genuine `j=1728` source, but the torsion point itself must be divisible by 2
for our problem. In a quadratic field this leaves only `Q(i)` for `(0,0)`
and `Q(sqrt(2))` for the endpoints. The nondegenerate endpoint family has

```text
n = 3(r^2+s^2)(r^2-2s^2)(2r^2-s^2)t^2.
```

Its 3-adic valuation is always odd, while halving the applicable endpoint
over `Q(sqrt(2))` requires the rational squareclass of `n` to be `1` or
`2`. Hence the whole displayed torsion family is excluded for quadratic
magic squares. A cubic field cannot halve rational 2-torsion because it has
no quadratic subfield.

### Ulas and Lee--Velez: explicit Mordell families, wrong CM type

J. B. Lee and W. Y. Velez, *Integral Solutions in Arithmetic Progression
for y^2=x^3+k*, Periodica Mathematica Hungarica 25 (1992), 31--49,
DOI 10.1007/BF02454382; and Maciej Ulas, *Rational Points in Arithmetic
Progression on y^2=x^n+k*, Canadian Mathematical Bulletin 55 (2012),
193--207, arXiv:0901.2076.

For `n=3`, these are Mordell curves `y^2=x^3+k`, and Ulas gives four
independent points in arithmetic progression over `Q(t)`. Every
nonsingular member has `j=0`, while a congruent-number curve has `j=1728`.
The families are therefore disjoint in characteristic zero and cannot be
converted into the required family by a change of Weierstrass coordinates.

### Garcia-Selfa--Tornero: simultaneous progressions

I. Garcia-Selfa and J. M. Tornero, *On Simultaneous Arithmetic Progressions
on Elliptic Curves*, Experimental Mathematics 15 (2006), 471--478,
arXiv:math/0604385; and *Searching for Simultaneous Arithmetic Progressions
on Elliptic Curves*, arXiv:math/0703624.

These papers construct and search general Weierstrass curves whose `x`
coordinates and permuted `y` coordinates are both arithmetic progressions.
The extra `y`-progression does not imply any of `x-n`, `x`, `x+n` is a
square. They are relevant only after intersecting their parameter spaces
with `j=1728`; the simultaneous condition itself gives no Kummer shortcut.

### Edwards, Huff, and quartic models

There are further constructions on Edwards, Huff, and quartic genus-one
models. Their stated arithmetic progression is model-coordinate dependent.
Only an affine Weierstrass `x`-change preserves the relation, whereas the
maps from these models usually use nonlinear rational functions. They
should be assigned low priority unless a paper explicitly tracks the
Weierstrass `x`-coordinate and lands at `j=1728`.

## Obstruction and finiteness papers

Garcia-Fritz and Pasten, *Elliptic Curves with Long Arithmetic Progressions
Have Large Rank* (arXiv:1910.14485), proves rank growth for long progressions
in fixed-`j` families. Their 2026 preprint *Patterns on Elliptic Curves
Beyond Bremner's Conjecture* (arXiv:2605.14962) gives more general
rank-dependent uniform pattern bounds. These are valuable structural
results, but length three is too short to produce an effective construction
or exclusion for the magic-square problem.

Bremner--Silverman--Tzanakis, *Integral Points in Arithmetic Progression on
y^2=x(x^2-n^2)*, Journal of Number Theory 80 (2000), 187--208, is directly
about congruent-number curves. Its height and integral-point arguments
restrict integral progressions, especially in rank one, but the magic-square
problem requires rational points in the particular coset `2E(K)`. Its main
use here is as a source of local, height, and descent filters rather than a
parameterization of the needed doubles.

## Recommended next computation

1. Recover Bremner's explicit length-eight coefficient functions and factor
   the `c6=0` divisor on his auxiliary rank-one curve.
2. Search that divisor for closed points of degree 2 and 3. If none exist,
   record a second rigorous low-degree exclusion; if they do, transform the
   curve and apply the three Kummer tests.
3. For Campbell's irreducible degree-12 field, determine whether `-p(m)` is
   a square. If so, test all consecutive triples among the seven displayed
   points. This is the current most concrete route to a finite-degree
   record above 3.
4. Continue searching non-displayed even combinations in Spearman's
   rank-three subgroup, but do not revisit its displayed triple.
