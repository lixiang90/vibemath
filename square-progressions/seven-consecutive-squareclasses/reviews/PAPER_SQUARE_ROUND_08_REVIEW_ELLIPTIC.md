# Elliptic-line cross-review of the mask-51 gate

Date: 2026-09-03

## Decision: PASS

No mathematical or reproducibility blocker was found.  The mask-51 integral
point theorem, its use as a same-parameter exclusion, and the reduction from
15 patterns to 10 are supported by two complete proofs and by the recorded
upstream occurrence data.  No change to the author's paper, code, or
certificate is required.

## Independent verification

### 1. Translation to mask 102

For

```text
C51: y^2=t(t+1)(t+4)(t+5),
```

putting `s=t-1` gives

```text
(s+1)(s+2)(s+5)(s+6)=t(t+1)(t+4)(t+5).
```

The maps `(t,y) -> (s,y)=(t-1,y)` and `(s,y) -> (t,y)=(s+1,y)`
are mutually inverse on integral points.  The already proved mask-102 points

```text
s=-6,-5,-2,-1
```

therefore map exactly to

```text
t=-5,-4,-1,0.
```

This is an actual integral-point bijection, not merely an isomorphism over
the rationals or a bounded check.

### 2. Independent squarefree-kernel proof

Let

```text
A=t(t+5),  B=(t+1)(t+4)=A+4.
```

For `t<=-6` or `t>=1`, both `A` and `B` are strictly positive.  Also
`gcd(A,B)=gcd(A,4)`, so their gcd divides 4.  If `AB` is a square, the
positive squarefree kernels of `A` and `B` coincide: writing
`A=d*U^2`, `B=d*V^2`, the squarefree integer `d` divides the gcd and hence
is exactly `1` or `2`.

- For `d=1`, `(V-U)(V+U)=4`.  Positivity gives `V>U>=1`; both factors
  have the same parity.  The only positive same-parity factorization is
  `(2,2)`, which instead gives `U=0`, contradicting `A>0`.
- For `d=2`, `V^2-U^2=2`, impossible modulo 4 because a difference of two
  square residues modulo 4 lies in `{0,1,3}`.

Thus the exterior ranges contain no points.  The complementary interval is
exactly the six integers `-5<=t<=0`; direct evaluation gives

```text
0, 0, 12, 12, 0, 0.
```

Only the four zero values are squares.  This partition of the integer line
also handles all signs and all zero cases: no negative-`A` branch or endpoint
is omitted.

### 3. Inventory and pattern impact

I independently parsed `PAPER_SQUARE_MASK99_CERTIFICATE.json` and
`STUDENT_SQUARE_ROUND_04_CERTIFICATE.json`, without importing the mask-51
module.  The recomputation gives:

```text
input rows                         15
characters per row                15, all distinct in every row
total character occurrences       225
distinct masks                    53
distinct genus-one four-root masks 26
genus-one occurrences             113
pairable ranking
  (51,5,4), (90,5,6), (54,4,3),
  (27,3,3), (45,3,6), (85,2,8)
```

Mask 51 occurs precisely in pattern IDs

```text
33, 83, 257, 268, 283.
```

Removing those five from the certified 15 inputs leaves exactly

```text
12, 31, 43, 59, 134, 214, 230, 251, 276, 281.
```

Hence `15 -> 10` is exact.  Because the mask-51 curve has no nondegenerate
integral parameter at all, this is a legitimate same-parameter exclusion;
it does not combine witnesses from different parameter values.

### 4. Regression and certificate audit

With the repository `code/` directory on `PYTHONPATH`, all seven dedicated
tests pass.  The disk certificate is exactly regenerated, and both upstream
SHA-256 values match the files read during the independent calculation.

## Required fixes

None.

The only scope boundary to retain is already stated correctly in the paper:
the ten patterns are necessary candidates only; the theorem neither realizes
one nor decides `R_2(7)`.
