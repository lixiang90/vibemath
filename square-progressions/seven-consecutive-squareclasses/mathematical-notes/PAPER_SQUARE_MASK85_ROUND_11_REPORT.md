# Round 11: the mask-85 integral-point gate

Date: 2026-09-04

## Result

Among the four necessary patterns left by mask 54, mask 85 occurs exactly in
IDs 31 and 276.  The direct character curve at the original normalized
integer parameter is

```text
C_85: y^2=t(t+2)(t+4)(t+6).
```

Its complete integral-point set is

```text
(-6,0), (-4,0), (-3,-3), (-3,3), (-2,0), (0,0).
```

Every point makes one of `t,...,t+6` zero.  Thus both affected patterns are
excluded and the exact necessary-pattern chain becomes

```text
651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7 -> 4 -> 2.
```

The two remaining IDs and partition words are

```text
12   0012202
134  0012131.
```

This is a necessary classification only.  It neither realizes nor excludes
either survivor and does not decide `R_2(7)`.

## Complete integer-point proof

Put `x=t+3`.  Then

```text
t(t+2)(t+4)(t+6)=(x^2-9)(x^2-1).
```

For `t<=-7` or `t>=1`, equivalently `|x|>=4`, set

```text
A=x^2-9,  B=x^2-1=A+8.
```

Both factors are positive and `gcd(A,B)=gcd(A,8)`.  If `AB` is a square,
the positive integers `A,B` have a common positive squarefree kernel `d`.
Since `d` divides the gcd, `d` is a squarefree divisor of 8, hence
`d in {1,2}`.  Write `A=dU^2`, `B=dV^2` with positive integers `U,V`.
Then

```text
d(V^2-U^2)=8.
```

- For `d=1`, the only positive same-parity factorization of 8 is
  `(V-U,V+U)=(2,4)`.  Thus `(U,V)=(1,3)`, so `A=1` and `x^2=10`, impossible
  modulo 8.
- For `d=2`, the only positive same-parity factorization of 4 is `(2,2)`.
  It forces `(U,V)=(0,2)`, contrary to `A>0`.

This excludes both infinite outer intervals.  On the complementary interval
`-6<=t<=0`, the seven right-hand sides are

```text
0, -15, 0, 9, 0, -15, 0,
```

giving exactly the six displayed points.  Finally, if rational `y` has
integer square `y^2`, writing `y` in lowest terms shows that its denominator
is one, so the proof also covers the rational ordinate used by the character
quotient.

## Occurrence and same-parameter audit

The input is the exact four-row output of the mask-54 certificate.  Rebuilding
the Round-04 occurrence table gives 60 occurrences, 37 distinct masks and 19
distinct genus-one masks.  The constant-pairable ranking is

```text
(mask, patterns hit, |constant|)
(85,2,8), (27,1,3), (45,1,6).
```

The exact records are `P31:m85` and `P276:m85`.  Both record representative
mask 15, class 0, and the map `t=2u`; the proof above is conducted directly in
their common original integer parameter `t`.  No points from different
quotients or different parameters are combined.

## Artifacts and boundary

- Generator: `code/PAPER_SQUARE_MASK85.py`.
- Certificate: `certificates/PAPER_SQUARE_MASK85_CERTIFICATE.json`.
- Tests: `reproducibility/tests/PAPER_SQUARE_MASK85_test.py`.

The certificate SHA-256 is
`c0f7597c6eaad87c735a0a3356992dd83c8c610ac9d8884c8d4fcf48d34d3d22`.
The flat supplement is version `paper-square-supplement-v0.10.1`; its manifest
SHA-256 is
`deb3eade7c9f25c6e0c8da019f21f7a0943bdd50fcf263f7add6ed8b3ed0309e`.

The certificate contains the complete occurrence inventory, centered
polynomial identity, both squarefree-kernel branches, exact middle interval,
all integral points, degeneracy positions and exact `4 -> 2` impact.  No
bounded search, rank heuristic or unproved CAS computation enters the proof.
