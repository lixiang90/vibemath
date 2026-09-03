# Four-hit branch `0010`: a second certified infinite family

Status: **proved**.  This closes a second one of the original 31 unresolved
four-hit color/position models.  It uses the same positive-rank genus-one
curve as the `0001` branch, but it is a different orbit under affine color
change and reversal.  The remaining 29 models are not addressed here.

## 1. Model and exact derivation

Take counted positions and colors

```text
indices = (0,1,2,3),  colors = 0010.
```

After the permitted common rational scaling, write the color-zero entries
at positions 0, 1 and 3 as

```text
A0=X^3,  A1=Y^3,  A3=Z^3.
```

The AP identity `A3=3*A1-2*A0` is therefore exactly

```text
C: 2X^3-3Y^3+Z^3=0.                         (1)
```

Conversely, every rational point on (1) gives the rational five-term AP

```text
(A0,...,A4)=(X^3,Y^3,2Y^3-X^3,Z^3,4Y^3-3X^3).   (2)
```

Choosing the cube class of `A2` as the singleton color makes positions
0,1,2,3 have colors `0010` in one pure cubic field.

This is not the earlier `((0,1,3,4),0001)` orbit.  The latter omits the
central position 2; the present model omits an endpoint, position 4 (or 0
after reversal).  Direct enumeration of all 12 affine-color/reversal images
finds the two orbits disjoint.

## 2. Positive rank

Curve (1), with origin `O=(1:1:1)`, is the curve already certified in Round
07.  Its partial derivatives have no common projective zero.  On `XYZ != 0`
the exact map

```text
N = 6X^3Y^3+3Y^3Z^3-2Z^3X^3,
T = (2X^3+3Y^3)(-3Y^3-Z^3)(Z^3-2X^3),
(u,v) = (N/(X^2Y^2Z^2), -T/(2X^3Y^3Z^3))
```

lands on `E: v^2=u^3-243`.  The symbolic cleared identity is exact.  For

```text
P=(4:1:-5),  Q=(7,10) in E(Q),
```

the images are `phi(O)=-Q` and `phi(P)=2Q`.  The integral discriminant of
`E` is `-2^4*3^13`, and `10^2` does not divide it.  Nagell--Lutz therefore
shows that `Q` is non-torsion.  Translating the nonconstant genus-one map by
`-phi(O)` gives an isogeny sending `P` to `3Q`; hence `P` is non-torsion on
`C`.  Thus `P_n=O+n(P-O)` gives infinitely many distinct rational points.

## 3. Pure-cubic lift and all boundaries

For `n != 0`, insert `P_n=(X_n:Y_n:Z_n)` into (2).

- `X_n Y_n Z_n` cannot vanish: (1) would make one of `3,-2,3/2` a rational
  cube.
- `A2=0` would make `2` a rational cube; `A4=0` would make `4/3` a rational
  cube.  Thus all five AP terms are nonzero.
- The AP is constant only if `X_n=Y_n=Z_n`, namely at the origin `O`, which
  is excluded by `n != 0`.
- `A2` is not a rational cube.  Otherwise positions 0,1,2,3 would be four
  rational cubes in a nonconstant five-term AP, contradicting
  Hajdu--Tengely's strict bound `P_5(3)=3`.

Let `D_n` be the positive cube-free representative of `[A2]` in
`Q*/Q*3`.  Then `A2=D_n*w_n^3`, with `w_n in Q*`, and `D_n != 1`; hence
`Q(cuberoot(D_n))` is genuinely cubic.  Positions 0,1,2,3 are therefore
cubes in that field with colors `0010`.  The already proved theorem
`R^times_(3,1)(5)=4` excludes `A4` from being a fifth hit in the same field.

Distinct projective points of `C(Q)` give distinct APs up to common rational
scaling: comparison of `A0` makes the scaling a rational cube, and rational
cubing is injective.  Reversal has fibers of size at most two.  Consequently
infinitely many equivalence classes remain.

## 4. First exact member

At `P=(4:1:-5)`, (2) is

```text
(64,1,-62,-125,-188).
```

For `beta^3=62`, positions 0,1,2,3 are the cubes of
`4,1,-beta,-5` in `Q(beta)`.  This is the new `0010` model.  The same AP also
realizes the earlier `0001` model over `Q(cuberoot(188))`, but the two
color/position orbits are disjoint as explained above.

## 5. Reproducibility and claim boundary

- `code/PAPER_CUBE_FOURHIT_0010.py` freezes the orbit action, curve/AP
  correspondence, rational cube-free normalization, Mordell image, example,
  and boundary identities.  Certificate schema v2 records the coefficient
  vectors for `A2=0` and `A4=0`, all three possible fifth-hit Kummer colors,
  and recomputes these assertions rather than storing prose alone.
- `code/PAPER_CUBE_FOURHIT_0010_test.py` contains seven exact tests.
- `code/PAPER_CUBE_FOURHIT_0010_CERTIFICATE.json` is the stored certificate;
  SHA-256:
  `24f6a36c5d3b899c2d45f2088dc0d32b75881cfd89a852fcf51d374e056bfeb2`.
- The certificate binds the inherited Mordell identity to exact SHA-256
  values of `PAPER_CUBE_FOURHIT_0001.py`, its test, and its certificate, and
  reruns `symbolic_map_identity()`.  It also stores and tests
  `3Q=(2838722167/174477681,146917312265870/2304675688329)` rather than only
  the label `3Q`.

No bounded rational-point search, external CAS, or unproved rank assertion is
used.  The result proves positive rank and an infinite family in precisely
the additional orbit `((0,1,2,3),0010)`.  It does not determine the exact
rank or classify any of the other 29 models.

Combined command:

```powershell
python -m unittest discover -s code -p "*_test.py" -v
```

Expected status after this round: **23/23 tests pass**.
