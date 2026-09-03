# Round 09 cross-review: the 29 four-hit models

Date: 2026-09-04.

## Verdict

**Mathematical result: PASS.  Frozen certificate: FAIL pending one local
correction (major but non-blocking for the theorem).**

I found no error in the `405 -> 38 -> 31 -> 29` reconstruction, the three
geometric model types, the 25 clusters under the explicitly stated
coordinate-permutation action, or the two new positive-rank families.  The
report and manuscript correctly avoid calling the 25 keys a complete list of
arbitrary `Q`-isomorphism classes.

There is, however, a definite variable-name error in the generated JSON's
`0100` boundary data.  The prose proof is correct, so this does not invalidate
the theorem, but the source, JSON, and test coverage must be repaired before
the certificate is frozen again.

## Independent reconstruction

I used a separate exact-arithmetic enumerator, without importing the Round-09
module.  It regenerated all `5*3^4=405` partial words, their
`AGL(1,F_3)`-plus-reversal orbits, and the stated arithmetic gate:

```text
raw inputs                         405
orbits                              38
one-colour exclusions                3
monochromatic index-3-AP exclusions  4
gate survivors                      31
previously solved removed             2
Round-09 inputs                      29
```

The 29 models split independently as

```text
3+1       4
2+2       9
2+1+1    16
```

For every `3+1` model I recomputed
`(k-j)X^3-(k-i)Y^3+(j-i)Z^3=0`; all three coefficients are nonzero, so the
diagonal cubic is smooth of genus one.

For every `2+2` model I recomputed the coefficient matrix of
`L_r V^3-L_s U^3`.  Every entry is nonzero and every determinant is nonzero.
Thus the two binary cubics have six distinct simple zeros.  The degree-three
cyclic cover is totally ramified over those six points, and
`2g-2=3(-2)+6(3-1)=6`, hence `g=4`.

For every `2+1+1` model I independently formed
`L_r L_s-(q-p)^2W^3`.  Its two binomial factors have nonzero endpoints and
nonzero determinant.  The degree-six polynomial is squarefree, and the
standard superelliptic formula gives
`g=((3-1)(6-1)-(gcd(3,6)-1))/2=4`.

## Permutation clusters

Independent canonicalization under exactly the advertised actions gave

```text
3+1 clusters       2
2+2 clusters       9
2+1+1 clusters    14
total              25
```

The only clusters with more than one model are

```text
3+1, key (1,-3,2):
  ((0,1,2,3),0100), ((0,1,2,4),0111)
3+1, key (1,-4,3):
  ((0,1,2,4),0010), ((0,1,3,4),0010)
2+1+1, key (1,-2,-3,4):
  ((0,1,2,3),0121), ((0,1,2,3),0102)
2+1+1, key (2,-7,6,-1):
  ((0,1,2,3),0122), ((0,1,2,3),0012)
```

All remaining keys are singletons.  Row/column exchange and matrix
transposition really are coordinate swaps on `P1 x P1`; `X,Y` exchange is
the claimed swap on the weighted model.  Agreement of keys therefore proves
the displayed isomorphisms.  Disagreement is only absence of an isomorphism
inside this small action, not a `Q`-isomorphism invariant.  Both the Round-09
report and `paper/main.tex` state this boundary correctly.  **PASS.**

## Two new orbits and samples

For `C: 2X^3-3Y^3+Z^3=0`, independent substitution gives

```text
O=(1:1:1),       P=(4:1:-5),
phi(O)=(7,-10),  phi(P)=(16009/400,-2021723/8000)=2Q,
Q=(7,10),
3Q=(2838722167/174477681,
    146917312265870/2304675688329).
```

Since `100` does not divide `2^4*3^13`, Nagell--Lutz proves that `Q` is
non-torsion.  Translation sends `P-O` to `3Q`, so the positive-rank reuse is
rigorous and is not a rank-search inference.

At `P`, the two new constructions give respectively

```text
0100: (-125,-62,1,64,127),  common difference 63,
0111: (127,64,1,-62,-125),  common difference -63.
```

Both are nonzero APs.  The singleton decompositions are
`-62=62*(-1)^3` and `127=127*1^3`.  For the second model the raw word is
`1000`, and `c -> 2c+1` indeed gives `0111`.  A fresh orbit computation also
shows that `0001`, `0010`, `0100`, and `0111` are pairwise disjoint under
affine colour change and reversal.  **PASS.**

The zero and constant-difference boundaries in the report/manuscript also
check directly: on `C`, rational points have `XYZ != 0`; the common
difference in either new construction vanishes only at `O`.  The
`P_5(3)=3` and five-hit theorem implications are applied only after all five
terms have been shown nonzero.  **PASS.**

## Required certificate correction

In `PAPER_CUBE_FOURHIT_CLUSTER_ROUND09.py`, and consequently in
`PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_CERTIFICATE.json`, the `0100`
`zero_checks` strings currently say

```text
A1=0: X=-Y, then Z^3=2Y^3
A4=0: X^3=2Y^3
```

For the actual formula

```text
(Z^3,(Z^3+Y^3)/2,Y^3,X^3,2Y^3-Z^3),
```

the correct implications are

```text
A1=0: Z=-Y, then X^3=2Y^3
A4=0: Z^3=2Y^3.
```

The Round-09 report and manuscript already contain the correct statements.
The error is confined to certificate metadata, but the current stored-JSON
test merely compares the JSON to the same generating function, so it cannot
detect this semantic mistake.  Regenerate the JSON after fixing the two
strings and add exact algebraic assertions for both zero implications.
**FAIL until repaired.**

## Reproduction

The author tests were run with warnings promoted to errors:

```text
python -W error -m unittest -v \
  PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_test.py \
  PAPER_CUBE_FOURHIT_0001_test.py \
  PAPER_CUBE_FOURHIT_0010_test.py \
  PAPER_CUBE_KUMMER5_test.py
Ran 29 tests: OK
```

The current Round-09 certificate SHA-256 is
`9625C8DF80BE3180CCA6B9DB68E09FF40F42340E6F45E388AFE747AF8C3215F2`.
It should be superseded after the correction above.

## Final itemized decision

- 29-model exhaustive reconstruction: **PASS**.
- Geometric equations, smoothness/branch hypotheses, and genera: **PASS**.
- All 25 explicit coordinate-permutation clusters: **PASS**.
- Claim boundary versus arbitrary `Q`-isomorphism: **PASS**.
- Positive-rank reuse and the two displayed examples: **PASS**.
- Nonzero, nonconstant, noncube, fifth-hit, and inequivalence boundaries in
  the prose theorem: **PASS**.
- Frozen JSON boundary metadata and its semantic regression coverage:
  **FAIL; major correction required, theorem unaffected**.
