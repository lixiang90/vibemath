# Prior-art audit for the square-class-pattern paper

Search date: 2026-09-03.  This note records a reproducible literature audit; it
does **not** claim novelty from absence of a search hit.

## 1. Objects searched

The two exact integral quartics are

\[
H_{77}: y^2=t(t+2)(t+3)(t+6),\qquad
H_{102}: y^2=(t+1)(t+2)(t+5)(t+6).
\]

Queries included the quoted polynomials in both `t` and `x`, the exact elliptic
model `Y^2=X^3-36X`, `576h2`, `576.c3`, `S-integral`, `simultaneous Pell`,
`square classes consecutive integers`, and the names/DOIs below.  Searches were
run against general web indices, arXiv, journal/author pages, and the LMFDB
entry.  No refereed source located in this audit states either exact integral
point set above or the 284/186/98/44/19 pattern reductions.  This is only a
negative search report, not proof that no such source exists.

## 2. Exact elliptic model and the S-integral distinction

The Jacobian model for `H_77` is the congruent-number curve
`Y^2=X^3-36X`, identified as Cremona 576h2 / LMFDB 576.c3.  Sources:

- [LMFDB elliptic curve 576.c3](https://www.lmfdb.org/EllipticCurve/Q/576/c/3)
- [Noam Elkies, Harvard Math 223 course page](https://people.math.harvard.edu/~elkies/M223.24/index.html)

An integral-point list for the Weierstrass model is not enough for our theorem:
the inverse map has `t=36/(X-12)`, so integral `t` imposes a specific
S-integral/divisibility condition rather than `X,Y` integral.  The general
algorithmic context is Pethő--Zimmer--Gebel--Herrmann,
[Computing all S-integral points on elliptic curves](https://arxiv.org/abs/math/9711227),
but that article does not by itself certify this particular point set.

## 3. Simultaneous Pell and arithmetic-progression neighbours

The squarefree-kernel branches are close in form to simultaneous Pell systems.
Relevant general sources are:

- Masser--Rickert, [Simultaneous Pell Equations](https://www.sciencedirect.com/science/article/pii/S0022314X96901377), JNT 61 (1996), 52--66, DOI 10.1006/jnth.1996.0137.
- Tzanakis, [Effective solution of two simultaneous Pell equations by the elliptic logarithm method](https://www.impan.pl/shop/en/publication/transaction/download/product/82953), Acta Arith. 103 (2002), 119--135.
- Bremner--Silverman--Tzanakis, [Integral points in arithmetic progression on y²=x(x²-n²)](https://asu.elsevierpure.com/en/publications/integral-points-in-arithmetic-progression-on-ysup2sup-xxsup2sup-n/), JNT 80 (2000), 187--208.

These establish broad methods or a different arithmetic-progression problem;
none of the located statements closes our eighteen `H_77` branches or the two
`H_102` kernel branches verbatim.  A
[MathOverflow/Math.SE-style discussion of the same 576h2 curve](https://math.stackexchange.com/questions/2765146/a-system-of-simultaneous-pell-equations)
was useful as a lead to quartic-Thue reductions, but is not used as authority in
the proof.

## 4. Consecutive squares and low-degree number fields

The finite screens and collision-risk audit used the following primary papers:

- González-Jiménez--Xarles, [On a conjecture of Rudin on squares in arithmetic progressions](https://arxiv.org/abs/1301.5122).
- Xarles, [Squares in arithmetic progression over number fields](https://arxiv.org/abs/0909.1642).
- González-Jiménez--Xarles, [Five squares in arithmetic progression over quadratic fields](https://arxiv.org/abs/0909.1663).
- Bremner--Siksek, [Squares in arithmetic progression over cubic fields](https://arxiv.org/abs/1505.06424), International Journal of Number Theory 12 (2016), 1409--1414.
- González-Jiménez, [Arithmetic progressions of squares over quadratic fields](https://arxiv.org/abs/2602.03251) (2026).
- González-Jiménez--Tho, [Arithmetic progressions of squares over quartic fields](https://arxiv.org/abs/2602.01380) (2026).

The 2026 papers create a **high collision risk for broad claims** about squares
over quadratic or quartic fields.  Their stated objects are actual square
progressions over prescribed extensions, whereas the present paper classifies
finite affine square-class labels of rational consecutive integers under a
common rational scaling and proves two integral-quartic exclusions.  The audit
found no theorem in those papers that obviously subsumes these finite pattern
counts, but the introduction must say “we did not locate” rather than “first”.

## 5. Products of subsets of intervals and progressions

This audit originally underweighted the literature closest to the character
equations. The following sources study square products of terms selected from
intervals or arithmetic progressions:

- N. Saradha, [Squares in products with terms in an arithmetic progression](https://doi.org/10.4064/aa-86-1-27-43), Acta Arith. 86 (1998), 27--43. Its principal theorem treats products of complete arithmetic-progression blocks (and related almost-square equations), rather than affine squareclass rank of a fixed seven-term interval.
- Granville--Selfridge, [Product of integers in an interval, modulo squares](https://doi.org/10.37236/1549), Electron. J. Combin. 8 (2001), R5. It studies when an interval contains a subproduct in a prescribed squareclass.
- Bui--Pratt--Zaharescu, [A problem of Erdős--Graham--Granville--Selfridge on integral points on hyperelliptic curves](https://doi.org/10.1017/S0305004123000488), Math. Proc. Camb. Phil. Soc. 176 (2024), 309--323. It connects interval subproducts to integral points on curves such as $y^2=x\prod(x+j_i)$ and proves distributional results for the least endpoint.

These are genuine conceptual predecessors for the character quotients
$y^2=\prod_{i\in S}(t+i)$. The located statements do not classify seven-term
affine-rank-two equality partitions, impose all fifteen character equations at
one parameter, or state the reduction `651 -> 23`. Therefore the safe unit of
claimed contribution is the combined finite classification, not the general
use of subset-product curves and not the three elementary quartic point lists
in isolation.

## 6. Safe wording

Permitted wording: “In the sources and exact-equation searches above, we did not
locate the seven-term affine-squareclass classification and simultaneous
same-parameter reductions stated here.” The elementary quartic point lists
should not be advertised as independently new. Forbidden without a stronger bibliographic review:
“new”, “first”, “previously unknown”, or “complete prior-art search”.
