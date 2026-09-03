# Round 09: exact clustering of 29 four-hit models

Date: 2026-09-04.  Status: **two further models proved to have infinite
families; all 29 input models reconstructed and permutation-clustered**.

This round uses no bounded rational-point search and no heuristic rank.  The
only isomorphisms claimed are explicit permutations of coordinates or of the
two `P1` factors.  Failure of two canonical keys to agree is not claimed to
prove non-isomorphism over `Q`.

## 1. Exact 405 -> 38 -> 31 -> 29 reconstruction

There are five choices of omitted position and `3^4` partial color words,
hence 405 inputs.  Quotienting by `AGL(1,F3)` on colors and reversal gives 38
orbits.  Three one-color orbits and four containing a monochromatic
three-term index AP are removed by the already proved rational-cube bounds,
leaving 31.  Removing the previously settled `0001` and endpoint-omitted
`0010` models gives exactly 29 inputs.

Their color multiplicities are

```text
3+1:       4
2+2:       9
2+1+1:    16
total:    29.
```

The generator recomputes all four counts from the original 405 inputs.

## 2. Curves attached to every model

Write `A_i=a+id`.

### 2.1 Type 3+1

If equal-color positions are `i<j<k`, scale that color to rational cubes
`X^3,Y^3,Z^3`.  The exact AP relation is the smooth diagonal cubic

```text
(k-j)X^3-(k-i)Y^3+(j-i)Z^3=0.                 (1)
```

It has genus one.  The four current models form two explicit coordinate-
permutation clusters, each of size two:

```text
coefficient key (1,-3,2):
  ((0,1,2,3),0100), ((0,1,2,4),0111)

coefficient key (1,-4,3):
  ((0,1,2,4),0010), ((0,1,3,4),0010).
```

The first key is the curve `2X^3-3Y^3+Z^3=0` after permuting coordinates.
The second is `3X^3-4Y^3+Z^3=0`; no rank or rational-point classification is
claimed for it.

### 2.2 Type 2+2

Let one color occur at `p<q` and put `A_p=X^3`, `A_q=Y^3`.  Define

```text
L_k=(q-k)X^3+(k-p)Y^3,
```

so `(q-p)A_k=L_k`.  If the other color occurs at `r,s`, eliminating its
common Kummer class gives

```text
L_r V^3-L_s U^3=0.                             (2)
```

This is a bidegree `(3,3)` curve in `P1 x P1`.  All four coefficients in
the two binomials are nonzero, and their coefficient determinant is nonzero,
so numerator and denominator have six distinct simple geometric zeros.  The
degree-three cover of `P1` is totally ramified at those six points;
Riemann--Hurwitz gives genus four.  Exact row/column swaps and transposition
of the two factors yield nine certified permutation keys for the nine
models; no additional coincidence occurs under this explicitly stated
action.

### 2.3 Type 2+1+1

Let the repeated color occur at `p<q` and normalize it to color zero.  If
the singleton positions are `r,s`, their colors can be normalized to one
and two.  The Kummer condition is equivalent to `A_r A_s` being a rational
cube.  Hence the exact weighted model is

```text
(q-p)^2 W^3=L_r L_s                              (3)
```

in `P(1,1,2)`.  The product has six distinct simple roots.  The smooth
normalization of the cubic cover has

```text
g=((3-1)(6-1)-(gcd(3,6)-1))/2=4.
```

Swapping `X,Y` gives 14 certified permutation keys for the 16 models.  The
two nontrivial pairs are

```text
((0,1,2,3),0121)  <-> ((0,1,2,3),0102),
((0,1,2,3),0122)  <-> ((0,1,2,3),0012).
```

Thus the complete 29-model list has 25 clusters under the precise
permutation action used here: `2+9+14`.  This is a strict reuse theorem, not
a complete classification under arbitrary `Q`-isomorphisms.

## 3. Two new positive-rank models

Let

```text
C: 2X^3-3Y^3+Z^3=0,
O=(1:1:1), P=(4:1:-5).
```

The Round07 exact Mordell map sends `O` to `-Q` and `P` to `2Q` on
`v^2=u^3-243`, where `Q=(7,10)` is non-torsion by Nagell--Lutz.  After
translation the image of `P` is the exact point

```text
3Q=(2838722167/174477681,
    146917312265870/2304675688329).
```

Therefore `P_n=O+n(P-O)` supplies infinitely many rational points of `C`.

### 3.1 Orbit ((0,1,2,3),0100)

For `(X:Y:Z) in C`, use

```text
(Z^3,(Z^3+Y^3)/2,Y^3,X^3,2Y^3-Z^3).             (4)
```

This is an AP because swapping `X,Z` changes `C` into
`X^3-3Y^3+2Z^3=0`.  Positions 0,2,3 are rational cubes.  The singleton
`A1` is nonzero: if `A1=0`, then `Z=-Y` and `C` forces `X^3=2Y^3`.
The missing term `A4` is nonzero because its vanishing forces
`Z^3=2Y^3`.  If `A1` were a rational cube, positions 0,1,2,3 would
contradict `P_5(3)=3`.  Its positive cube-free class therefore defines a
genuinely cubic field, and the five-hit theorem excludes the missing term
from being a cube in that same field.

At `P`, (4) is

```text
(-125,-62,1,64,127),
```

with singleton `-62=62*(-1)^3`, over `Q(cuberoot(62))`.

### 3.2 Orbit ((0,1,2,4),0111)

Use instead

```text
(2X^3-Y^3,X^3,Y^3,2Y^3-X^3,Z^3).                (5)
```

Positions 1,2,4 are rational cubes.  The singleton `A0` and missing term
`A3` cannot vanish, since either equality would make 2 a rational cube.
The singleton is not a rational cube by `P_5(3)=3`.  Its raw word is `1000`;
the permitted color map `c -> 2c+1` gives the canonical representative
`0111`.  The five-hit theorem again excludes the remaining position.

At `P`, (5) is

```text
(127,64,1,-62,-125),
```

over `Q(cuberoot(127))`.

For both constructions the common difference vanishes only at `O`.
Comparison at a fixed nonzero rational-cube position proves injectivity up
to common rational scaling; reversal has fibers of size at most two.  Thus
each model contains infinitely many equivalence classes.  Exact orbit
enumeration proves that the four models settled through Round09 are pairwise
distinct.

## 4. Reproducibility and boundary

- `code/PAPER_CUBE_FOURHIT_CLUSTER_ROUND09.py` reconstructs every model,
  canonicalizes only explicit coordinate permutations, rechecks the
  inherited Mordell identity, and freezes the two new lifts.
- `code/PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_test.py` contains six tests of the
  complete partition, curve data/genus hypotheses, every recorded
  permutation, exact samples, positive-rank dependency, and stored JSON.
- `code/PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_CERTIFICATE.json` has SHA-256
  `4217f170ce6cd27d488811119289dd1cccb480b47c536c23bd10be99b1193662`.

Round09 proves two new infinite families and leaves **27** models open.  It
does not infer rank from a search, does not call different permutation keys
non-isomorphic, and makes no rational-point assertion for the other 27
models.
