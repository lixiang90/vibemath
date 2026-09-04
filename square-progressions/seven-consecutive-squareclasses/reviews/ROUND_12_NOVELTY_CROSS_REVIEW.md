# Round 12 novelty integration cross-review

Date: 2026-09-04

Verdict: **FINAL PASS** for the Round 12 novelty integration.

This verdict is limited to claim calibration, literature comparison, and the
integer-parameter/common-scaling boundary.  It is not a priority certificate:
a negative search cannot establish priority, and the disclosed database and
2024-Tho gaps remain real.

## Scope reviewed

The review cross-checked the Round 12 novelty audit, the standing mathematical
audit, the prior-art note, the manuscript and its bibliography, and the
submission README, cover letter, limitations, and user-input checklist.  The
author files were treated as claims to audit and were not edited.

The exact result being positioned is a necessary equality-pattern
classification for a nonzero block of seven consecutive rational integers

    t, t+1, ..., t+6,    t in Z,

whose affine squareclass rank is at most two.  It leaves the two reversal
orbits represented by 0012202 and 0012131.  It does not prove that either
survivor is realizable, decide R_2(7), classify arbitrary rational starting
parameters, or classify all square progressions over quartic fields.

## Primary-source verification

1. González-Jiménez--Xarles, [Five squares in arithmetic progression over
   quadratic fields](https://arxiv.org/html/0909.1663), supports the stated
   quadratic-field comparison.  Its abstract and main theorem identify the
   Q(sqrt(409)) five-square progression, while its equivalence relation uses
   square scaling and reversal.  This is genuinely a degree-two/rank-at-most-one
   precedent, not the present seven-place affine-rank-two pattern theorem.

2. González-Jiménez--Xarles, [On a conjecture of Rudin on squares in arithmetic
   progressions](https://arxiv.org/html/1301.5122), defines subset equivalence
   using translation, rational dilation, and symmetry.  Proposition 5 gives
   the five exceptional four-subsets of {0,...,6}, and Corollary 6 gives
   Q(6)=Q(7)=4.  The manuscript accurately credits this four-position screen
   and does not claim to have invented that curve method.

3. González-Jiménez--Tho, [Squares in arithmetic progression over certain
   non-primitive quartic number
   fields](https://arxiv.org/html/2602.01380v1), defines equivalence by square
   scaling and reversal and imposes proper-definition, twist-rank, and
   class-number hypotheses.  Its D=409 discussion gives the six-term example
   over Q(sqrt(409),sqrt(649)).  The author files correctly use this as a close
   collision channel and correctly avoid a broad no-six-squares claim.

4. González-Jiménez, [Squares in arithmetic progression over quadratic
   extensions of number
   fields](https://arxiv.org/html/2602.03251v1), gives conditional,
   field-specific classifications under rank/degree and class-number
   hypotheses, again up to square scaling and reversal.  It also describes
   the Q(zeta_8) work of Tho as announced.  The stated difference from a
   universal necessary pattern theorem for integral t is supported.

5. Balasubramanian--Luca--Thangadurai, [On the exact degree of
   Q(sqrt(a_1),...,sqrt(a_l)) over
   Q](https://doi.org/10.1090/S0002-9939-10-10331-1), is the appropriate
   foundational citation for the square-product/multiquadratic-degree
   connection.  The manuscript does not attribute its seven-block
   classification to that general degree theorem.

The remaining short-interval product and hyperelliptic-curve references are
used only as broad conceptual predecessors.  Their titles, bibliographic
metadata, and the modest claims attached to them are consistent; the paper
does not state that they settle the simultaneous seven-block problem.

## Claim-language screen

No priority-bearing use of “first,” “new,” “previously unknown,” or “complete
classification” was found in the theorem statement, abstract, prior-work
discussion, cover letter, or limitations.  “Finite classification” and
“Summary classification” are theorem labels for the proved necessary
integer-pattern reduction; nearby text expressly denies realizability,
R_2(7), and arbitrary-rational-AP conclusions.  The occurrences of “first” in
venue ranking or positional mathematical prose are not novelty claims.

The audit's strongest suggested sentence is properly qualified: it says that
no equivalent theorem was located in the sources inspected and immediately
states that this is not proof of priority.  This is acceptable
high-caution wording.  Any later replacement by “first,” “new,” or “complete
prior-art search” would invalidate this pass.

## Integer t versus rational arithmetic progressions

The boundary is mathematically correct and consistently disclosed.  A
nonconstant rational progression a+di can be divided by d and written as
t+i with t=a/d, but t need not be integral.  Translation and rational
dilation in the Rudin subset problem therefore do not preserve the fixed
integral-parameter problem, and a quartic-curve isomorphism need not preserve
the single common t required by all fifteen characters.  The manuscript
claims only integral t and does not silently promote its theorem to all
rational progressions.

## Common scaling and the biquadratic formulation

The equivalence used for literature comparison is correct.  In
Q*/Q*2, affine rank at most two means that after multiplication by one common
rational squareclass, all seven classes lie in a vector space generated by at
most two independent classes.  Adjoining square roots of those generators
makes the commonly scaled seven terms squares in an extension of degree at
most four.  When the difference rank is exactly two, the generators may be
chosen independent and the field may be chosen biquadratic.

Conversely, the kernel of Q*/Q*2 to the squareclass group of a biquadratic
field is generated by the squareclasses of its three quadratic subfields, so
commonly scaled squares imply affine rank at most two.  The manuscript also
correctly warns that the unscaled affine offset may be independent and can
require an additional square root, giving degree up to eight.  It therefore
does not make the false claim that the unscaled seven terms are all squares in
one fixed biquadratic field.

## Search limitations

The limitations are conspicuous and repeated in the novelty audit, manuscript
prior-work section, submission limitations, and user-input checklist:

- stable complete MathSciNet result pages were unavailable;
- a subscription-level MathSciNet/zbMATH title, subject, and forward-citation
  search remains advisable;
- no authoritative full text of the 2024 Nguyen Xuan Tho item concerning
  quadratic extensions of Q(zeta_8) was available for theorem-level
  comparison;
- these absences are not evidence of priority and must be closed before any
  priority wording.

This disclosure is sufficient for the current submission-ready, no-actual-
submission boundary.  It does not turn the search into a comprehensive
bibliographic certification.

## Findings and executable follow-up

No blocking novelty or mathematical-boundary defect was found.

One nonblocking repository-state inconsistency lies outside the novelty
verdict: submission/README.md and submission/USER_INPUT_CHECKLIST.md still
describe the root MANIFEST.sha256 as a stale Round 10 inventory awaiting a
Round 11 freeze, while the current working tree already modifies that manifest.
After the concurrent root manifest work is finalized, replace those historical
sentences with the actually verified manifest generation/hash/status.  Do not
guess the final hash while the tree is still changing.

Final disposition: **PASS**.  Preserve the present high-caution wording, retain
the integral-t and common-scaling qualifications, and do not convert an
accessible-sources non-hit into a novelty or priority claim.
