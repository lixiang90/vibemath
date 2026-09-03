# Three-by-three magic squares of squares over number fields

## Result: an unconditional degree-four record

Let `K = Q(i, sqrt(7))`.  The matrix of algebraic-integer roots

```text
       4       5i        3
 i sqrt(7)      0    sqrt(7)
      3i        5       4i
```

has the entrywise square

```text
 16  -25    9
 -7    0    7
 -9   25  -16
```

The nine values are pairwise distinct and every row, column, and main
diagonal has sum zero.  Every displayed root is an algebraic integer.  The
element `i + sqrt(7)` has minimal polynomial

```text
x^4 - 12*x^2 + 64,
```

so `K` has degree four.

This belongs to an elementary infinite family.  Given a nondegenerate integer
Pythagorean triple `x^2 + y^2 = z^2`, with `y > x`, put
`delta = y^2 - x^2`.  The roots

```text
             y          zi              x
 i sqrt(delta)           0     sqrt(delta)
            xi           z             yi
```

give a magic square with zero line sum over `Q(i, sqrt(delta))`.  Fermat's
right-triangle theorem implies that `delta` cannot be a rational square: if it
were, three rational squares would be in arithmetic progression with square
common difference, equivalently 1 would be a congruent number.  Thus this
family genuinely has degree four, not two.

There is also a totally real degree-four certificate, due to Bremner, over
`Q(sqrt(3), sqrt(133))`:

```text
  (5-13 sqrt(3))^2   (17+9 sqrt(3))^2  (22-4 sqrt(3))^2
     (23-sqrt(3))^2       (2 sqrt(133))^2     (23+sqrt(3))^2
  (22+4 sqrt(3))^2   (17-9 sqrt(3))^2  (5+13 sqrt(3))^2
```

All eight line sums are 1596.  Its nine roots are algebraic integers and its
nine squared values are distinct.  The values themselves lie in `Q(sqrt(3))`,
but the central value 532 has no square root there; adjoining `sqrt(133)` is
essential for this certificate.  The primitive element `sqrt(3)+sqrt(133)`
has minimal polynomial `x^4 - 272*x^2 + 16900`.

Both certificates are checked exactly by `verify_number_field_examples.py`.

## Two rigorous restrictions on degree two and degree three

1. **A zero center rules out every odd-degree field.**  Opposite entries in an
   order-three magic square sum to twice the center.  If the center is zero
   and a nonzero opposite pair is `u^2, v^2`, then `v^2 = -u^2`, hence
   `(v/u)^2 = -1`.  The field contains `Q(i)` and therefore has even degree.
   In particular, a cubic example must have nonzero center.

2. **Rational-valued entries give no shortcut in odd degree.**  If `K/Q` has
   odd degree and `alpha in K` satisfies `alpha^2 in Q`, then `Q(alpha)` has
   degree at most two and divides `[K:Q]`; consequently `alpha in Q`.  Thus a
   cubic-field square whose nine *values* are rational would already be a
   rational magic square of nine squares.  A genuinely cubic construction
   must use nonrational values as well as a nonzero center.

For a quadratic field `Q(sqrt(d))`, a rational number is a square in the field
exactly when its rational square class is `1` or `d`.  This makes a search for
rational-valued quadratic examples equivalent to looking for a magic square
whose entries occupy only those two square classes.

## Full quadratic-field reduction used by the search

For a nonzero center, scale so that the center value is 1.  Every pair of
squares symmetric about 1 can be parametrized by `t in K`:

```text
x = (1 + 2t - t^2)/(1 + t^2)
y = (1 - 2t - t^2)/(1 + t^2)
f(t) = 4t(1-t^2)/(1+t^2)^2
x^2 = 1 + f(t),   y^2 = 1 - f(t).
```

Therefore a full order-three square is equivalent to finding `b,c in K` for
which all four elements

```text
b, c, b+c, b-c
```

belong to `f(K)`, subject to the nine resulting values being distinct.  This
is the number-field analogue of the four coupled three-term progressions of
squares.  Once a quadratic solution is found, one common integer scaling
clears all root denominators and produces algebraic integers.

The exact implementation is in `number_field_magic.py`.  It has two modes:

- rational values in the square classes `1,d`;
- the unrestricted parametrization above for `t in Q(sqrt(d))`.

Current negative search results (not nonexistence proofs):

- all squarefree `d` with `2 <= |d| <= 31`, coefficient/root bound 500, in
  the rational two-square-class subsearch;
- `d=-1` through coefficient/root bound 3000 in that subsearch;
- `d=-3,-2,-1,2,3` with
  `t=(a+b sqrt(d))/q`, `|a|,|b| <= 10`, `1 <= q <= 5`; this is 1889
  normalized parameters and about 1600 distinct offsets per field.
- every squarefree `d` with `2 <= |d| <= 30`, together with `d=-1`, with
  `|a|,|b| <= 15` and `1 <= q <= 8`.  There are 6497 normalized parameters
  and 5555--6415 distinct offsets per field.  A complete additive search of
  every resulting `b,c,b+c,b-c` configuration found no example.
- `d=-1` was additionally searched through `|a|,|b| <= 20`, `1 <= q <= 10`:
  13985 normalized parameters and 12887 distinct offsets, again with no
  example.

The general search now uses two or three independent modular additive sieves
before exact `Fraction` operations.  Elements whose denominators are not
invertible modulo a sieve prime are retained and checked exactly, so this is
an acceleration of the same complete finite-box search, not a heuristic.

## Quadratic-twist rank-two subgroup searches

There is a second exact search in `quadratic_elliptic_search.py`.  Given
rational points `P in E_n(Q)` and `P' in E_(dn)(Q)`, it transports

```text
P'=(u,v)  ->  (u/d, (v/d^2)*sqrt(d)) in E_n(Q(sqrt(d)))
```

and enumerates every `x(2(aP+bP'))` for `|a|,|b| <= B`, modulo the unavoidable
`(a,b) -> (-a,-b)` duplication.  A vectorized modular midpoint sieve is
followed by exact quadratic-field verification.  The following independent
rank-two subgroups were searched with `B=30`; each produced 1860 distinct
doubled centers and no three-term `x`-arithmetic progression:

```text
(n,d) = (5,6), (6,5), (6,14), (6,35), (30,7), (30,11).
```

The rational points used come from the integer right triangles of areas
`5,6,30,84,210,330`.  These computations search the displayed rank-two
subgroups; without a full Mordell--Weil and saturation calculation they are
not claims about all of `E_n(Q(sqrt(d)))`.

No quadratic example occurred in these boxes.  These finite computations do
not settle the quadratic case.

The same normalized-circle method has also been implemented for pure cubic
fields `Q(theta)`, `theta^3=m`, in `cubic_field_magic.py`.  Exact searches for
`m=2,3,5,6,7,10` with

```text
t=(a+b theta+c theta^2)/q,
|a|,|b|,|c| <= 3,  1 <= q <= 2
```

found no example.  This represents 659 normalized parameters and 607--651
distinct offsets in each field.  It is again finite negative evidence, not a
nonexistence proof.

## Literature position

- [Bremner, *On squares of squares* (1999)](https://matwbn.icm.edu.pl/ksiazki/aa/aa88/aa8837.pdf)
  gives the degree-four real example and an odd-degree example of degree 27.
- [Bremner, *On squares of squares II* (2001)](https://www.impan.pl/shop/publication/transaction/download/product/82367)
  views the same configuration as an eight-square square over `Q(sqrt(3))`;
  the ninth root raises the field degree to four.
- [Michaud, *Magic Squares of Squares* (2019)](https://warwick.ac.uk/fac/sci/maths/people/staff/michaud/fourthyearproject.pdf)
  rederives the real quartic example geometrically and reports no known
  degree-below-four example at that time.
- [Cain, *Gaussian Integers, Rings, Finite Fields, and the Magic Square of
  Squares* (2019)](https://arxiv.org/abs/1908.03236) develops Gaussian and
  finite-field factorizations but does not supply a full Gaussian solution.
- [Jääskeläinen--Gebra Eyesus, *Complex Magic Squares and the Squared Gaussian
  Integer Lattice* (2026)](https://doi.org/10.1080/0025570X.2026.2627855)
  proves nonexistence for several geometric Gaussian subfamilies; it is not a
  general nonexistence theorem for quadratic fields.

The resulting record is therefore `k <= 4`; lowering it to 2 or 3 remains the
substantive problem.  Degree 2 is the first computational target because a
success would be optimal unless the original rational problem (`k=1`) is
solved.
