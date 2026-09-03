# Pure-cubic five-term problem: mathematical and novelty audit

Date: 2026-09-04
Audited tree: `vibemath/powers-in-progressions/pure-cubic-five-term/`
Decision: **mathematics ACCEPT; novelty wording ACCEPT only in the narrow form stated in Section 4 below.**

This is an adversarial audit of the mathematical claim, not a submission-format
review.  The documents in the audited tree were treated as claims to check, not
as instructions.

## 1. Exact claim and normalization

For a nonconstant rational five-term arithmetic progression

\[
A_i=a+id\quad(0\leq i<5),\qquad d\ne0,
\]

the paper counts only nonzero positions and asks for one common
`lambda in Q*` and one nontrivial pure cubic field
`K_D=Q(cuberoot(D))` such that every counted `lambda A_i` is a cube in
`K_D`.  Under this definition the asserted equality

\[
R^\times_{(3,1)}(5)=4
\]

is correct.

The qualifications are essential and are handled correctly.

- A rational-cube radicand gives the degree-one field `Q`, so it is excluded.
- The sign of `D` is immaterial because `-1=(-1)^3`; a rational cube factor is
  immaterial; and `D` and `D^2` generate the same field.  Conversely, the
  kernel lemma itself shows that two nontrivial radicands defining the same
  pure cubic field span the same line in `Q*/Q*3`, so no additional field
  identifications are missing.
- A common rational scaling of the progression changes only the affine origin
  of its cube classes, not the radicand direction.  Reversal changes the sign
  of the common difference and is legitimate.
- Zero is deliberately not counted.  If it were counted,
  `(-2,-1,0,1,2)` over `Q(cuberoot(2))` would make the five-term statement
  false.  The superscript `times` is therefore substantive.

## 2. Proof-chain audit

### 2.1 Kummer kernel

For noncube `D`, `X^3-D` is irreducible over `Q`, so
`1, alpha, alpha^2` is a basis of `K_D`, where `alpha^3=D`.  Expanding
`(a+b alpha+c alpha^2)^3`, the two nonrational coefficients are exactly

\[
3(a^2b+Da c^2+Db^2c),\qquad
3(a^2c+ab^2+Dbc^2).
\]

If `a=0`, their simultaneous vanishing gives `bc=0`, and a nonzero element is
on the `Q alpha` or `Q alpha^2` axis.  If `a != 0`, put `B=b/a`, `C=c/a`.
The independently checked resultants are

\[
B D(B^3D-1)^2,\qquad C(C^3D^2-1)^2.
\]

The alternative `B^3D=1` would make `D` a rational cube; hence `B=0`, then
`C=0`.  Cubing the three axes yields precisely the classes
`1,[D],[D]^2`.  Thus

\[
\ker(\Q^*/\Q^{*3}\to K_D^*/K_D^{*3})=\langle[D]\rangle.
\]

There is no missing unit, integrality, or normal-closure hypothesis: this is a
statement about elements of the degree-three field and follows from the basis
calculation.

### 2.2 Colors and the 25 orbits

After one common scale, each of five nonzero hits has a unique color in
`F_3`.  The relevant action is translation of all colors, color inversion
(`D <-> D^2`), and reversal of the five positions.  It has 12 elements.
Independent enumeration agrees with the stored computation:

- all `3^5=243` words are covered exactly once;
- Burnside fixed-point counts are
  `243,27,9,9,9,1,1,1,0,0,0,0`, whose sum is 300;
- hence there are exactly 25 orbits;
- 9 contain a monochromatic index three-term AP;
- one further orbit is represented by `00100` and has four equal-color
  positions `0,1,3,4`;
- the remaining 15 representatives are exactly those printed in the paper.

The quotient is correctly by an **affine color action**, not by a fixed
linear subspace containing color zero.

### 2.3 The ten externally excluded orbits

The nine monochromatic-index-AP cases give, after clearing denominators of
the rational cube roots and dividing by their common gcd, a primitive integer
solution of

\[
X^3+Z^3=2Y^3.
\]

All three entries are nonzero, and equality of all three cubes would force
`d=0`.  Thus the solution is nontrivial in the precise sense required by
Darmon--Merel.  Part 1 of their Main Theorem states that
`x^n+y^n=2z^n` has no nontrivial primitive solution for every `n>=3`.
The application at `n=3` is unconditional.  See the authors' paper,
pp. 1--3: [Darmon--Merel, *Winding quotients and some variants of Fermat's
Last Theorem*](https://www.math.mcgill.ca/darmon/pub/Articles/Research/18.Merel/paper.pdf).

For the `00100` orbit, one color at positions `0,1,3,4` becomes four
rational cubes in a rational five-term AP.  Multiplication by a common cube
clears both progression and root denominators; reversal makes the integer
common difference positive if necessary.  Hajdu--Tengely define
`P_{a,b;N}(3)` for `a>0`, `b in Z`, and their Theorem 2 proves the exact
upper bound 3 for `N=5` (indeed for `4<=N<=9`).  They allow arbitrary
integer `b`, so negative cubes and progressions crossing zero are covered;
allowing zero only makes their upper bound stronger than needed here.  See
pp. 15--18 of [Hajdu--Tengely, *Powers in arithmetic
progressions*](https://d-nb.info/1229902422/34), especially Theorem 2.

Conclusion: both cited results are used within their stated hypotheses.  No
BSD, modularity conjecture, positivity assumption, or unexecuted CAS result is
imported into the present theorem.

### 2.4 Prime support and four radicands

After clearing denominators and making the integer AP primitive,
`gcd(A_i,A_j)` divides `|i-j|`.  Hence any prime `p>3` divides at most one of
the five terms.  At such a prime, the valuation residues are the values of an
affine function `g_p+c_i delta_p` on the color blocks.

For every one of the 15 words, the block sizes are one of
`(3,2)`, `(3,1,1)`, `(2,2,1)`.  A two-color word has neither used color in a
singleton block; for a three-color word an affine function on `F_3` that
vanishes on two colors vanishes everywhere.  A singleton nonzero valuation
support is therefore impossible.  Thus both `g` and `delta` are supported at
2 and 3.  Removing `g` by a common rational scale leaves a nonzero direction
in `F_3^2`; the four projective directions are represented exactly by
`D=2,3,6,18`.

This argument is only invoked after the ten exceptional color orbits have
been removed, so `delta=0` and the one-color degeneration are not silently
included.

### 2.5 The 60 models and finite-field obstruction

The Cartesian product of 15 color representatives and 4 radicand directions
gives exactly 60 models, each the projective complete intersection

\[
D^{c_i}x_i^3-2D^{c_{i+1}}x_{i+1}^3+D^{c_{i+2}}x_{i+2}^3=0
\quad(i=0,1,2).
\]

For a listed prime `p`, a projective point is equivalent to a nonzero pair
`(a,d) in F_p^2` for which all five `a+id` lie in the corresponding weighted
cube images `D^{c_i} F_p^3`; zero coordinates are included.  The scan is
therefore exhaustive, rather than a search up to an arbitrary height.

The certificate and live recomputation agree on all 60 cells:

- certificate SHA-256:
  `7c5ff0bd36ebfc3bace0ca5898625b2fd7f03d318c754c6650d3a2483dd83977`;
- obstruction primes: `7,13,19,31,43,61`;
- every prime is coprime to `3D`;
- all 60 compatible-pair counts are zero;
- total nonzero parameter pairs scanned: 23,520.

The printed Jacobian-minor argument correctly proves smooth reduction at
these primes.  For the implication actually used, even smoothness is more
than necessary: a rational projective point has primitive integral
coordinates, whose reduction modulo any prime cannot be the all-zero vector.
It would therefore give an `F_p`-point.  Hence an empty projective special
fiber rigorously implies no rational point.

### 2.6 Lower bound

In `K=Q(alpha)`, `alpha^3=3`, the nonconstant AP

\[
(-3,-1,1,3,5)
\]

has its first four nonzero terms equal to
`(-alpha)^3,(-1)^3,1^3,alpha^3`.  It uses `lambda=1` and a genuinely cubic
field.  This proves the lower bound 4, while Sections 2.1--2.5 prove the upper
bound 4.

### 2.7 Four-hit extension through Round 09

The four-hit gate starts with 31 color/position models.  Four pairwise
distinct affine-color/reversal orbits are now proved to contain infinitely
many inequivalent maximizers:

    ((0,1,3,4),0001), ((0,1,2,3),0010),
    ((0,1,2,3),0100), ((0,1,2,4),0111).

All four constructions are obtained from the positive-rank smooth plane cubic
\(2X^3-3Y^3+Z^3=0\); the exact map to \(v^2=u^3-243\) and the Nagell--Lutz
certificate supply the non-torsion point.  Thus 27 of the initial 31
rational-point models remain open.

After removing the two models closed before Round 09, the generator
reconstructs all 29 inputs as 4 diagonal cubics, 9 bidegree \((3,3)\) curves,
and 16 weighted superelliptic curves.  Exact coordinate permutations give
\(2+9+14=25\) clusters.  This is only a reuse theorem under the displayed
coordinate and factor permutations: unequal keys are not asserted to be
non-isomorphic over \(\Q\), and the computation is not a complete
classification under arbitrary \(\Q\)-isomorphisms.

## 3. Reproducibility result

Command run from the repository root:

```text
python -m unittest discover -s vibemath/powers-in-progressions/pure-cubic-five-term/code -p "*_test.py" -v
```

Result after Round 09: **29/29 tests passed**.  They cover the kernel elimination, radicand
normalization, all color orbits and their partition, Burnside counts, all 60
good-prime obstructions, Jacobian minors, the lower witness, certificate/live
equality, the fail-closed four-hit-classification boundary, the first two
positive-rank constructions, the complete 29-model reconstruction, all 25
explicit permutation clusters, and the two further positive-rank lifts.

Round-09 cross-review found a deterministic metadata error in the 0100
boundary record: its two zero checks had interchanged variables although the
report and manuscript proof were correct.  The generator now verifies
symbolically that \(A_1=0\) gives \(Z=-Y\) and then \(X^3=2Y^3\), while
\(A_4=0\) gives \(Z^3=2Y^3\); the test independently checks the
factorization, discriminant and substitutions.  The regenerated Round-09
certificate has SHA-256
4217f170ce6cd27d488811119289dd1cccb480b47c536c23bd10be99b1193662.

## 4. Prior art and the narrow publishable claim

### 4.1 Nearest work found

Searches used the exact three diagonal-cubic equations, the phrases “common
rational scaling,” “pure cubic field,” “five-term arithmetic progression,”
and the Kummer/color formulation, together with broader citation searches.
No accessible paper through 2026-09-03 was found that states the present
five-term maximum or its 25-orbit/60-model reduction.  This is evidence from
search, not a proof of novelty.

The closest primary literature treats materially different problems:

- Darmon--Merel solve the equal-exponent rational obstruction
  `x^n+y^n=2z^n`; this supplies one ingredient, not the common-field
  five-position theorem.
- Hajdu--Tengely determine the number of ordinary integer cubes among short
  rational/integer APs.  Their `P_5(3)=3` has no varying pure-cubic Kummer
  class: [published paper](https://d-nb.info/1229902422/34).
- Hajdu--Tengely and Bruin--Gyory--Hajdu--Tengely study primitive integer APs
  with assigned ordinary perfect-power exponents, not rational entries that
  become cubes in one field after a common scale:
  [Hajdu--Tengely 2007](https://arxiv.org/abs/0707.0593),
  [Bruin et al. 2005](https://arxiv.org/abs/math/0512419).
- Gonzalez-Jimenez studies three terms that are themselves cubes of elements
  of a quadratic field, parameterized by an elliptic curve.  The field degree,
  length, and rational-entry/common-scaling condition all differ:
  [*Three cubes in arithmetic progression over quadratic fields*](https://arxiv.org/abs/0909.0227).
- Xarles proves qualitative degree-dependent bounds for APs all of whose terms
  are `k`-th powers in a number field; he does not determine this partial-hit,
  common-scale pure-cubic maximum:
  [*Squares in arithmetic progression over number fields*](https://arxiv.org/abs/0909.1642).
- Bremner--Siksek prove that no cubic field contains five squares in AP.  This
  is close in field degree and length but concerns squares of field elements,
  not cubes of rational entries after a rational scale:
  [*Squares in arithmetic progression over cubic fields*](https://arxiv.org/abs/1505.06424).
- Finite-field work counting APs among cubes is methodologically adjacent to
  the local certificate but does not address the global Kummer maximum:
  [*Arithmetic progressions in certain subsets of finite fields*](https://doi.org/10.1016/j.ffa.2023.102264).

### 4.2 Safest main novelty sentence

The narrow claim supported by both the proof and the search is:

> We determine the exact maximum for nonzero entries of a rational five-term
> nonconstant arithmetic progression that, after one common rational scaling,
> become cubes in one nontrivial pure cubic field: the maximum is four.  We
> also exhaust all five-hit Kummer color classes by a 25-orbit reduction and
> 60 certified finite-field obstructions.

Use “we determine,” not “for the first time,” “the first result,” or “complete
classification of maximizers.”  The paper classifies and excludes all
**five-hit color/position classes**.  Of the initial 31 four-hit
arithmetic-point models, four distinct orbits have positive-rank infinite
families and 27 remain open.  The 25 Round-09 clusters on the 29-model input
are proved only under explicit coordinate permutations and are not an
arbitrary-\(\Q\)-isomorphism classification.  The work must not be advertised as a
general theorem about cubes in cubic fields, because the rational-entry and
common-rational-scale restrictions are central.

### 4.3 Residual novelty risk

The remaining risk is bibliographic, not mathematical: the exact formulation
could occur under different notation in a thesis, non-English source, or an
unindexed computation.  Before asserting novelty, a human author should run
equation-level and citation-forward searches in MathSciNet and zbMATH and ask
a specialist in perfect powers in progressions.  Pending that check, the
narrow descriptive sentence above is publishable; any priority claim is not.

## 5. Final verdict

- **Mathematical correctness:** accept.  No blocking or major gap found.
- **External theorem applicability:** accept; hypotheses match after the
  explicit denominator-clearing/primitivity/reversal reductions.
- **Finite computation:** accept as exhaustive and reproducible, not heuristic.
- **Novelty:** plausibly distinct from accessible prior art, but only the
  narrowly defined exact maximum and exhaustive five-hit color-class
  elimination, together with the four explicitly proved positive-rank
  four-hit orbits, should be claimed.
- **Four-hit boundary:** four of 31 models are closed and 27 remain open; the
  25 permutation clusters are a strict reuse result, not a complete
  \(\Q\)-isomorphism classification.
- **Cross-review repair:** the 0100 certificate metadata was corrected and
  upgraded to symbolic semantic assertions; the mathematical theorem was
  unaffected.
