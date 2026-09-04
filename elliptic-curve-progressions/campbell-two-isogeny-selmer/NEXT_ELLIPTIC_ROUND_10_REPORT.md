# Round 10: a uniform two-/three-adic gate on the E-prime side

Date: 2026-09-04.

## Result

For

```text
E': y^2=x^3+A*x^2+B*x,
A=1183790142,
B=116194618458722241=3^4*59*71699*339106321,
```

and

```text
C'_d: N^2=d*U^4+A*U^2*V^2+(B/d)*V^4,
```

where `d` runs through the 32 signed squarefree classes supported on
`{3,59,71699,339106321}`, the following equivalences are proved:

```text
C'_d(Q_2) is nonempty  iff  d = 1 (mod 8),
C'_d(Q_3) is nonempty  iff  v_3(d)=0 and d = 1 (mod 3).
```

The two-adic survivors are

```text
{1,q} * {1,3*59,3*71699,59*71699},  q=339106321,
```

and the three-adic survivors are

```text
{1,q} * {1,59*71699,-59,-71699}.
```

Their intersection is exactly

```text
{1,4230241,339106321,1434501462453361}.
```

An audit of the existing 512-cell certificate shows that no single finite
place leaves only these four rows.  The only two-place combinations doing so
are `{2,3}` and `{2,5}`.  We choose `{2,3}` because both columns admit short
uniform proofs.

## Proof, independent of the old enumeration

Put `A=2c`, with `c=591895071=7 (mod 8)`.  Since

```text
A^2-4B=2^22*k,  k=223298222175 odd,
```

coefficient comparison gives

```text
d*N^2=T^2-2^20*k*V^4,  T=d*U^2+c*V^2.               (1)
```

For a primitive 2-adic pair, `T` is odd when `U,V` have opposite parity.  If
both are odd and `d` is `3,5,7 (mod 8)`, then `v_2(T)` is respectively
`1,2,1`.  Thus the correction divided by `T^2` has valuation at least 16,
and the right side of (1) is a nonzero square because `1+8 Z_2` consists of
squares.  Hence `d` would be a 2-adic square, a contradiction.  Conversely,
`d=1 (mod 8)` is a 2-adic square by the strengthened Hensel criterion applied
at `1`, and `(U:V:N)=(1:0:sqrt(d))` is a point.

At 3, `v_3(A)=2`, `A/9=1 (mod 3)`, and `B/3^4=1 (mod 3)`.  If `v_3(d)=1`,
the unique lowest term has valuation 1 when `U` is a unit and valuation 3
when `3|U`; neither is a square valuation.  If `v_3(d)=0`, a unit `U` reduces
the quartic to `d*U^4`.  For `U=3^r*u`, divide by `3^4`: at `r>=2` the unit
is `d^(-1)`, while at `r=1` it is `d+1+d^(-1)`.  Both are `-1 (mod 3)` when
`d=-1 (mod 3)`.  The remaining class `d=1 (mod 3)` is a 3-adic square by
ordinary Hensel lifting and again gives the point at `V=0`.

This proves both `iff` statements without a finite residue enumeration.  The
old matrix is used only for compatibility and minimal-place auditing.

## Artifacts and boundaries

- `code/NEXT_ELLIPTIC_ROUND_10.py`: standard-library generator and exact
  compatibility/minimality audit.
- `certificates/round10_eprime_two_three_gate.json`: structured theorem,
  proof constants, Hensel conditions, survivor sets, and the SHA-256 of the
  old matrix.
- `code/NEXT_ELLIPTIC_ROUND_10_test.py`: exact regression tests.
- `paper/main.tex`: proposition and full valuation/residue/Hensel proof.

The result proves a complete local theorem and supplies a non-enumerative
proof of the E-prime-side four-class reduction.  It does not produce or
exclude a rational ninth point, compute a Cassels--Tate value, or provide an
independent second-CAS reproduction.  A database no-match remains
insufficient for priority or novelty.
