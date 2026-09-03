# Seven consecutive squareclasses

## Proved

For an integer `t` such that `t,t+1,...,t+6` are nonzero and have affine
rational squareclass rank at most two, exact Kummer and finite-case arguments
reduce the possible equality patterns, modulo relabelling and reversal, by

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10`.

The paper proves the enumerative reductions and the integer-point gates for
masks 77/89, 102, 108, 99, and 51.  The code and JSON certificates expose every finite
branch used in those reductions.

## Not proved

The 10 remaining necessary patterns are not classified as realizable or
impossible.  The work does not decide `R_2(7)` and does not solve the rational
three-by-three magic square of squares.

`STUDENT_SQUARE_ROUND_04_CERTIFICATE.json` contains historical pipeline fields;
only the exact geometry and occurrence data consumed by the later SAFE and mask
certificates are evidence.  Simulated companion files are intentionally absent.

See `paper/`, `mathematical-notes/`, and `reviews/` before interpreting a JSON
field as a theorem.  `NEXT_SQUARE_MATH_NOVELTY_AUDIT.md` gives the current
claim-by-claim correctness and prior-art audit.
