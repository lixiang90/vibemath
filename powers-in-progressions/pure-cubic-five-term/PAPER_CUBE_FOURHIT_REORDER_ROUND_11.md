# Round 11 four-hit queue after exact geometric and small-height triage

Date: 2026-09-04. Author: Codex (GPT-5.6-sol). This note ranks the 25
models left after Round 10. Search
results below are route-selection evidence only; an empty search is never a
rational-point theorem.

## A. Unreviewed rank-zero quotient candidates

A separate Round-11 draft claims a rank-zero quotient calculation for seven
explicit 2+1+1 models in five coordinate-permutation clusters:

- (0123,0120);
- (0123,0121) and (0123,0102);
- (0123,0122) and (0123,0012);
- (0124,0121);
- (0124,0112).

Here 0123 abbreviates the index set (0,1,2,3), and similarly for 0124.
That draft has not passed the required proof and independent-review gate.
Accordingly these seven remain in the authoritative open count and are not
part of a manuscript theorem.

## B. First new existence closure

The first remaining target is (0124,0102). Its genus-four curve is

\[
 (X^3+Y^3)(2Y^3-X^3)=2W^3.
\]

The point (2:1:-3) produces the proved four-hit AP
(64,36,8,-20,-48) over \(\mathbf Q(\sqrt[3]{6})\). Its image (6,15) on
\(y^2=x^3+9\) is non-torsion by Nagell--Lutz. The separate existence report,
script, independent test, and JSON certificate give the complete proof and
claim boundary.

## C. Other 2+1+1 covers in the geometric triage

Exact completion of the square shows that every one of the eight models not treated by the rank-zero candidate draft
2+1+1 covers maps to one of only two Mordell curves:

| indices, word | source coefficients (X6,X3Y3,Y6,W3) | normalized quotient |
|---|---:|---|
| 0123,0112 | (-2,5,-2,-1) | y2=x3+9 |
| 0124,0122 | (12,-10,2,-4) | y2=x3+36 |
| 0124,0120 | (6,8,2,-16) | y2=x3+9 |
| 0124,0012 | (3,-10,8,-1) | y2=x3+9 |
| 0134,0012 | (6,-17,12,-1) | y2=x3+9 |
| 0134,0102 | (-2,7,4,-9) | y2=x3+9 |
| 0134,0112 | (-3,10,-3,-4) | y2=x3+36 |
| 0134,0120 | (3,10,3,-16) | y2=x3+9 |

Both quotients have explicit non-torsion points, so quotient-rank-zero
classification is unavailable for this tier. Positive quotient rank does
not imply infinitely many rational lifts to a genus-four source.

A primitive signed search with \(|X|,|Y|\le100\) found only constant or
zero-boundary source points in this tier. This is not used as a proof and
does not lower the mathematical status of any model.

## D. The nine 2+2 covers

All nine are smooth bidegree-(3,3) curves in
\(\mathbf P^1\times\mathbf P^1\), hence genus four:

- (0123,0011), (0123,0101), (0123,0110);
- (0124,0011), (0124,0101), (0124,0110);
- (0134,0011), (0134,0101), (0134,0110).

For these models the exact condition is a fractional-linear function of
\((X/Y)^3\) being a rational cube. A primitive signed scan with
\(|X|,|Y|\le300\) found a legal nonzero point for (0123,0110):
\(X/Y=-1\), with the second cube ratio also -1. It yields

\[
 (-27,-9,9,27,45)
\]

over \(\mathbf Q(\sqrt[3]{3})\); the omitted value 45 is excluded by its
5-adic valuation. This is the next immediate existence-proof candidate.
Other hits in the scan had a zero source coordinate or a zero AP term.
Again, no non-hit is treated as a proof.

## E. Local-obstruction boundary and resulting priority

Every remaining model contains the rational point arising from a constant
AP. Consequently the whole projective curve is locally soluble at every
place, and a claim that an entire remaining curve is locally insoluble would
be false. A strict local obstruction can only close an explicitly separated
nonconstant covering branch or Mordell--Weil coset.

The revised priority is therefore:

1. freeze the proved (0124,0102) existence closure, moving the authoritative
   count from 6 closed/25 open to 7 closed/24 open;
2. audit the seven rank-zero candidate models before counting any of them;
3. certify the explicit (0123,0110) 2+2 existence point by a second
   implementation;
4. for the other positive-rank 2+1+1 covers, compute a genuine covering
   decomposition before applying local tests;
5. leave all search non-hits explicitly experimental until a covering,
   Chabauty, or descent argument closes them.
