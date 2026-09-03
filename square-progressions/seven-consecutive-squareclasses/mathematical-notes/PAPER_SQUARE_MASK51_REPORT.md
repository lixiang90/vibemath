# Eighth-round squareclass gate: mask 51

Date: 2026-09-03

## Authoritative input and exact inventory

The input is exactly the 15 IDs certified after mask 99:

`12, 31, 33, 43, 59, 83, 134, 214, 230, 251, 257, 268, 276, 281, 283`.

They contain 225 character occurrences, 53 distinct masks and 26 distinct
genus-one four-factor masks.  The genus-one masks account for 113 occurrences.
`PAPER_SQUARE_MASK51_CERTIFICATE.json` records every one of the 26 masks with
its support, gap signature, affected IDs, constant pairing and gcd bound.

The pairable ranking is:

| mask | patterns hit | gcd bound | already proved integral translate |
|---:|---:|---:|---|
| 51 | 5 | 4 | mask 102 family |
| 90 | 5 | 6 | no |
| 54 | 4 | 3 | mask 108 family |
| 27 | 3 | 3 | mask 108 family |
| 45 | 3 | 6 | no |
| 85 | 2 | 8 | no |

Although mask 90 ties the maximum hit count, mask 51 has both the smaller gcd
constant and a bijective integral translation to an already closed curve.
Among candidates whose complete integral point set is therefore already
available, mask 51 uniquely maximizes impact.

## Complete point theorem

For

\[
 C_{51}: y^2=t(t+1)(t+4)(t+5),
\]

one has

\[
 C_{51}(\mathbb Z)=\{(-5,0),(-4,0),(-1,0),(0,0)\}.
\]

There are two independent checks.

First, putting `s=t-1` gives the identity

\[
 (s+1)(s+2)(s+5)(s+6)=t(t+1)(t+4)(t+5).
\]

Translation by one is a bijection on integer parameters, so this is exactly
the previously proved mask-102 curve.

Second, put

\[
 A=t(t+5),\qquad B=(t+1)(t+4)=A+4.
\]

For `t<=-6` or `t>=1`, both factors are positive and
`gcd(A,B)=gcd(A,4)` divides 4.  If `AB` is a square, its common positive
squarefree kernel is `d=1` or `2`.

- For `d=1`, `V^2-U^2=4`.  The only positive same-parity factor pair is
  `(V-U,V+U)=(2,2)`, which forces `U=0`, contradicting `A>0`.
- For `d=2`, `V^2-U^2=2`, impossible modulo 4.

For the remaining integers `-5<=t<=0`, the right sides are
`0,0,12,12,0,0`.  This proves the displayed list.  Every point is a branch
point and every parameter is degenerate for the original seven-term block.
No bounded search or Mordell--Weil assertion is used.

## Exact impact

Mask 51 occurs in precisely the five IDs

`33, 83, 257, 268, 283`.

All five are strictly excluded. The ten remaining necessary IDs are

`12, 31, 43, 59, 134, 214, 230, 251, 276, 281`.

The rigorous chain is therefore

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10`.

This is still a necessary-pattern classification only. It neither realizes a
survivor nor decides `R_2(7)`.

## Artifacts and verification

- `PAPER_SQUARE_MASK51.py`: inventory, selection, proof data and impact.
- `PAPER_SQUARE_MASK51_CERTIFICATE.json`: exact machine certificate.
- `PAPER_SQUARE_MASK51_test.py`: seven dedicated regression tests.
- Paper and README: integrated only after the complete proof passed.
- Mathematical supplement manifest: advanced to version 0.7.0 and binds the
  three new artifacts.

After this gate the full square-line suite contains 70 tests.
