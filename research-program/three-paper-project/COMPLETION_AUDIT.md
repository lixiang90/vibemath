# Three-paper Goal completion audit

Audit date: 2026-09-03
Rule: absence of a detected error is not proof that a completion condition is
met.  `PASS` below means that an artifact in this repository directly supports
the requirement; `OPEN` means that stronger evidence or human input remains.

## Requirement matrix

| Requirement | Squareclasses | Pure cubic | Campbell descent |
|---|---|---|---|
| A closed theorem rather than a bounded experiment | PASS: integer seven-term necessary-pattern theorem | PASS: exact maximum `R^times_(3,1)(5)=4` | PASS: exact two-isogeny Selmer groups and rank upper bound |
| Claim boundary states what is not proved | PASS | PASS | PASS |
| Proof and finite computation checked adversarially | PASS: `NEXT_SQUARE_MATH_NOVELTY_AUDIT.md` | PASS: `NEXT_CUBE_MATH_NOVELTY_AUDIT.md` | PASS: `NEXT_ELLIPTIC_MATH_NOVELTY_AUDIT.md` |
| Cross-review by another project member | PASS: `reviews/` | PASS: `reviews/` | PASS: `reviews/` |
| Repository-level reproduction | PASS: 63 tests | PASS: 16 tests | PASS: 49 tests |
| Code, structured certificates, tests, schema/data dictionary | PASS | PASS | PASS |
| LaTeX source and readable PDF | PASS: 9 pages | PASS: 4 pages | PASS: 8 pages |
| Exact comparison with accessible primary literature | PASS with residual priority risk | PASS with residual priority risk | PASS with medium residual priority risk |
| MathSciNet/zbMATH and equation-isomorphism priority audit | OPEN: human/database follow-up | OPEN: human/database follow-up | PARTIAL: exact minimal model/conductor searched; human database/citation-graph follow-up remains |
| External independent reproduction outside this workspace | OPEN | OPEN | OPEN |
| Public source location and repository integrity manifest | PASS: GitHub `main` plus root `MANIFEST.sha256` | PASS | PASS |
| Human author identity, affiliation, contributions, funding and conflicts | OPEN: author-supplied facts required | OPEN: author-supplied facts required | OPEN: author-supplied facts required |
| Final journal choice and submission authorization | OPEN | OPEN | OPEN |

The public all-project command is `python tools/run_all_checks.py`; after the
seventh-round extensions it ran 183 tests with zero failures.  The repository-wide SHA-256 index
is `MANIFEST.sha256`.  These facts establish internal reproducibility of the
asserted symbolic identities and finite certificates, not external peer
review, priority, or the unresolved long-term problems.

## Current mathematical status

### Squareclasses

The defensible theorem is for an integer `t` with the seven entries
`t,...,t+6` nonzero.  If their rational squareclasses have affine rank at most
two, their equality partition is one of 15 displayed necessary patterns.  The
paper does not decide `R_2(7)`, does not prove that a remaining pattern is
realizable, and does not solve the three-by-three magic square of squares.

### Pure cubic fields

For nonzero entries of a nonconstant rational five-term progression, one
common rational scale, and one nontrivial pure cubic field, the exact maximum
number of cubes is four.  The proof exhausts all five-hit color classes.  It
does not classify all four-hit progressions.  One of the 31 arithmetic-point
models is now proved to have positive rank and supplies infinitely many
inequivalent maximizers; the other 30 models remain open.

### Campbell descent

The exact finite result concerns the index-8 quartic attached to Campbell's
family: its two rational 2-isogeny Selmer groups, `rank E(Q) <= 3`, the
`Q x K` cubic-algebra invariant and `[35]` projection, and an everywhere-local
same-parameter fiber product.  It neither supplies the ninth point nor decides
the rational points on `C_H`.  The former opposite-side Cassels--Tate formula
is rejected negative evidence and is not used by a positive theorem.

## Next gates

1. Attempt a further exact exclusion among the 15 squareclass patterns using a
   new character mask; stop fail-closed at the first genuinely global curve.
2. Use the positive-rank `0001` four-hit branch as a template to triage the
   remaining 30 pure-cubic models; require an exact map or local obstruction.
3. Independently reproduce the now-explicit Campbell global minimal model and
   conductor in Sage/Magma/PARI when available, and finish the human citation-
   graph/database check before making any absolute priority claim.
4. After the mathematics stabilizes, replace public-archive placeholders with
   the verified GitHub commit URL.  Human identity and disclosure placeholders
   must remain until supplied and approved by the authors.

The Goal therefore remains `ACTIVE`: the three manuscripts have internally
accepted mathematical cores, but the original completion standard also asks
for database-level priority checks, external reproduction, and human-supplied
submission metadata that are not yet evidenced.
