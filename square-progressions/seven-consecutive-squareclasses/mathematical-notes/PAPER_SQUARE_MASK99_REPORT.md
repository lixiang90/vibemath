# Seventh-round squareclass gate: mask 99

Date: 2026-09-03

## Result

The final 23 necessary patterns have `23*15=345` character occurrences and 55
distinct character masks.  The complete per-mask list, including support,
degree, genus, hit count and every affected pattern ID, is stored in
`PAPER_SQUARE_MASK99_CERTIFICATE.json` under `occurrence_inventory.all_masks`.

Among genus-one masks admitting a pairing of their four linear factors into
quadratics with the same linear coefficient, the exact ranking is:

| mask | support | patterns hit | constant difference |
|---:|---|---:|---:|
| 99 | `{0,1,5,6}` | 8 | 5 |
| 54 | `{1,2,4,5}` | 7 | 3 |
| 45 | `{0,2,3,5}` | 7 | 6 |
| 90 | `{1,3,4,6}` | 7 | 6 |
| 51 | `{0,1,4,5}` | 5 | 4 |
| 85 | `{0,2,4,6}` | 5 | 8 |
| 27 | `{0,1,3,4}` | 3 | 3 |

The most frequent masks overall are 53 (12 patterns), 105, 92 and 33 (10
each).  The first three do not have the constant quadratic pairing used by the
elementary gates, while mask 33 has degree two.  Hence mask 99 is the
maximum-impact mask inside the explicitly selected elementary genus-one class.

## Complete integral-point theorem

Let

\[
 C_{99}: y^2=t(t+1)(t+5)(t+6).
\]

Then

\[
 C_{99}(\mathbb Z)=
 \{(-6,0),(-5,0),(-3,-6),(-3,6),(-1,0),(0,0)\}.
\]

Indeed, set

\[
 A=t(t+6),\qquad B=(t+1)(t+5)=A+5.
\]

For `t<=-7` or `t>=1`, both `A` and `B` are positive and
`gcd(A,B)=gcd(A,5)` divides 5.  If `AB` is a square, the positive squarefree
parts of `A` and `B` agree, so

\[
 A=dU^2,\qquad B=dV^2,\qquad d\in\{1,5\}.
\]

- If `d=1`, then `(V-U)(V+U)=5`.  The only positive same-parity factor pair
  is `(1,5)`, giving `(U,V)=(2,3)`.  Thus `A=4`, so
  `(t+3)^2=13`, impossible modulo 8.
- If `d=5`, then `(V-U)(V+U)=1`, forcing `U=0`, contrary to `A>0`.

Direct evaluation of the seven integers `-6<=t<=0` gives right sides
`0,0,24,36,24,0,0`, proving the list.  Every listed parameter has a zero in
the original block `t,...,t+6`; therefore there is no nondegenerate integral
parameter on this character quotient.

No bounded search is present in this proof or certificate.

## Pattern impact

Mask 99 occurs in exactly the eight final-23 patterns

`9, 26, 50, 188, 210, 212, 266, 271`.

They are strictly excluded.  The remaining 15 IDs are

`12, 31, 33, 43, 59, 83, 134, 214, 230, 251, 257, 268, 276, 281, 283`.

Thus the rigorous necessary-pattern chain is now

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15`.

This remains only a necessary classification: it neither proves that any of
the 15 patterns is realizable nor decides `R_2(7)`.

## Artifacts and verification

- Generator: `PAPER_SQUARE_MASK99.py`
- Exact certificate: `PAPER_SQUARE_MASK99_CERTIFICATE.json`
- Regression test: `PAPER_SQUARE_MASK99_test.py`
- Mathematical paper: new Proposition `prop:99`, updated summary theorem and
  15-row table
- Supplement manifest: version `0.6.0`, now binding the three mask-99
  artifacts and the expanded test command

The mask-99 module has six dedicated tests.  The full square-line suite has 63
tests after this gate.
