# Fourth-round next gate: mask 102

## Result

Starting from the 54 pattern IDs left after masks 77/89, the audited ranking of
four-root character masks with a constant quadratic pairing selects mask 102:

\[
H_{102}:y^2=(t+1)(t+2)(t+5)(t+6).
\]

It occurs in 19 of the 54 patterns.  The complete integral point set is

\[
H_{102}(\mathbb Z)=\{(-6,0),(-5,0),(-2,0),(-1,0)\}.
\]

All four parameters are degenerate for the original seven-term problem.
Consequently the 19 affected patterns are rigorously excluded and exactly 35
patterns remain.

## Proof gate

Set

\[
A=(t+1)(t+6),\qquad B=(t+2)(t+5)=A+4.
\]

Outside the finite middle interval `-6 <= t <= -1`, both `A` and `B` are
positive and `gcd(A,B)|4`.  If `AB` is a square, their common squarefree kernel
is therefore `d=1` or `d=2`, so `A=dU^2`, `B=dV^2`.

- For `d=1`, `(V-U)(V+U)=4`.  The only nonnegative same-parity factor pair is
  `(2,2)`, hence `U=0`, a boundary point.
- For `d=2`, `V^2-U^2=2`, impossible modulo 4.
- Direct evaluation at the six middle integers gives RHS
  `0,0,12,12,0,0`.

This is a global proof, not a bounded search and not a Mordell--Weil
calculation.

## Pattern impact

Affected IDs:

`2, 10, 11, 19, 20, 28, 37, 41, 47, 56, 116, 138, 165, 199, 202, 213, 234, 267, 279`.

Remaining 35 IDs:

`9, 12, 26, 31, 32, 33, 43, 50, 59, 70, 71, 83, 84, 134, 188, 193, 195, 197, 210, 212, 214, 229, 230, 237, 248, 251, 256, 257, 264, 266, 268, 271, 276, 281, 283`.

The occurrence claim is same-parameter safe: a pattern is removed only because
its own fifteen-character packet contains mask 102, whose integral curve has no
nondegenerate parameter at all.

## Reproducibility and next choice

- Generator: `PAPER_SQUARE_NEXT_GATE.py`
- Tests: `PAPER_SQUARE_NEXT_GATE_test.py` (5/5)
- Certificate: `PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json`
- Upstream certificate hashes are embedded in the certificate.

The deterministic ranking rule maximizes the number of remaining patterns hit,
breaking ties by the smaller gcd bound.  Recomputing it on the exact 35
survivors chooses **mask 108**, support `{2,3,5,6}`, which hits 12 rows and has
the pairing `(t+2)(t+6)` versus `(t+3)(t+5)` with constant difference 3.
This is the next-round choice; it is a selection result, not yet an integral-
point theorem.  Masks 54, 45 and 90 each hit 11 rows and are the fallbacks.

