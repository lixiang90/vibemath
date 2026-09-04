# Three-paper Goal completion audit

Audit date: 2026-09-04
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
| Repository-level reproduction | PASS: 87 tests | PASS: 36 tests | PASS: 65 tests |
| Code, structured certificates, tests, schema/data dictionary | PASS | PASS | PASS |
| LaTeX source and readable PDF | PASS: 11 pages | PASS: 8 pages | PASS: 11 pages |
| Exact comparison with accessible primary literature | PASS with residual priority risk | PASS with residual priority risk | PASS with medium residual priority risk |
| MathSciNet/zbMATH and equation-isomorphism priority audit | OPEN: human/database follow-up | OPEN: human/database follow-up | PARTIAL: exact minimal model/conductor searched; human database/citation-graph follow-up remains |
| External independent reproduction outside this workspace | OPEN | OPEN | OPEN |
| Internal clean-clone reproduction of a committed tree | PASS at commit `ccc4c4be6562` | PASS at the same commit | PASS at the same commit |
| Public source location and repository integrity manifest | PASS: GitHub `main` plus root `MANIFEST.sha256` | PASS | PASS |
| Human author identity, affiliation, contributions, funding and conflicts | OPEN: author-supplied facts required | OPEN: author-supplied facts required | OPEN: author-supplied facts required |
| Final journal choice and submission authorization | OPEN | OPEN | OPEN |

The public all-project command is `python tools/run_all_checks.py`; on the
Round10 working tree and the later clean clone it ran 243 tests with zero
failures in groups `87,33,36,14,8,65`.  The repository-wide SHA-256 index
is `MANIFEST.sha256`.  These facts establish internal reproducibility of the
asserted symbolic identities and finite certificates, not external peer
review, priority, or the unresolved long-term problems.

The clean-clone runner independently checked the committed rather than working
tree in an operating-system temporary directory.  Its eighth-round successful run
used the clean commit `4a8dae3dbc04712991783053e97b14b2d073964a`: all 198 tests
passed, the three papers rebuilt to 10, 7 and 9 pages, every final-log warning
list was empty, and the extracted-text SHA-256 of every rebuilt PDF equalled its
committed counterpart.  The exact record is
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_4a8dae3dbc04.json`,
with complete stdout/stderr in the adjacent `.log`.  The earlier commit
`559e89364b6e5c5e38e60d7b55b43ebb56e40409` and its 183-test run remain as a
historical seventh-round baseline.  This closes an internal environment-
isolation gap but is explicitly not external human reproduction.

The same protocol then passed on the clean Round09 commit
`85eb55b49f9f80e05a7d890fec7cc289083b802b`: source clean, all 218 tests
in groups `78,33,29,14,8,56`, PDF page counts 10, 7 and 10, identical
committed/rebuilt `pdftotext` SHA-256 values for each paper, and empty final-log
warning lists.  The exact records are
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.json`
and `research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.log`; the combined log SHA-256 is
`6bf7915a75983763fa8a98d096e8fbd2f6a7ee258a57575f0864912b56be0c00`.
This remains internal clean-clone evidence, not external human reproduction.

The same protocol then passed on the clean Round10 commit
`ccc4c4be6562534f25b18817c6c4773bb0cf0cc4`: source clean, all 243 tests in
groups `87,33,36,14,8,65`, PDF page counts 11, 8 and 11, identical
committed/rebuilt `pdftotext` SHA-256 values for each paper, and empty final-log
warning lists.  The text hashes are, respectively,
`97b9dc6242ebecc2e3a0a987c0265cd97eaf7a69f5620b7f9e64590d7892992e`,
`5619e94f4f937b31f7a778f18862e1aa2024adf4a2ccebb10658c6c858250bb1`, and
`18a684b57169564f314ffeedaffb4da15ad9be3344a8be792f7da54a6502aa8d`.
The exact records are
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_ccc4c4be6562.json`
and the adjacent `.log`; the combined log SHA-256 is
`72486507e0ebfafe8ba4b4a2415bcb19056a4e23d392d223548629bab6e59645`.
This remains internal clean-clone evidence, not external human reproduction.

## Current mathematical status

### Squareclasses

The defensible theorem is for an integer `t` with the seven entries
`t,...,t+6` nonzero.  If their rational squareclasses have affine rank at most
two, their equality partition is one of 4 displayed necessary patterns.  The
paper does not decide `R_2(7)`, does not prove that a remaining pattern is
realizable, and does not solve the three-by-three magic square of squares.

### Pure cubic fields

For nonzero entries of a nonconstant rational five-term progression, one
common rational scale, and one nontrivial pure cubic field, the exact maximum
number of cubes is four.  The proof exhausts all five-hit color classes.  It
does not classify all four-hit progressions.  One of the 31 arithmetic-point
models is now proved to have positive rank and supplies infinitely many
inequivalent maximizers; five further distinct orbits now have the same
property, so six models are settled and the other 25 models remain open.

### Campbell descent

The exact finite result concerns the index-8 quartic attached to Campbell's
family: its two rational 2-isogeny Selmer groups, `rank E(Q) <= 3`, the
`Q x K` cubic-algebra invariant and `[35]` projection, and an everywhere-local
same-parameter fiber product.  Round09 additionally proves that the real place
together with either `p=59` or `p=71699` leaves exactly eight `E`-side support
classes.  Round10 proves on the `E'` side that `Q_2` solubility is equivalent
to `d=1 mod 8`, while `Q_3` solubility is equivalent to `v_3(d)=0` and
`d=1 mod 3`; their intersection is exactly four classes.  These are local
necessary conditions.  They neither supply the ninth point nor decide
the rational points on `C_H`.  The former opposite-side Cassels--Tate formula
is rejected negative evidence and is not used by a positive theorem.

## Next gates

1. Attempt a complete mask-85 integral-point gate: on the 4 survivors it is
   the only constant-pairable genus-one mask hitting two rows (IDs 31 and 276).
   Stop fail-closed at the first genuinely global curve.
2. Use the two proved positive-rank diagonal cubics as templates to triage the
   remaining 25 pure-cubic models; require an exact map or local obstruction.
3. Analyze same-parameter compatibility for the four `E'`-side local survivor
   classes.  Independently reproduce the global minimal model and conductor in
   Sage/Magma/PARI when available, and finish the human citation-graph/database
   check before making any absolute priority claim.
4. Freeze the final payload as an immutable GitHub release or preservation DOI;
   the ordinary public `main` branch is already linked but is not immutable.
   Human identity and disclosure placeholders must remain until supplied and
   approved by the authors.

The Goal therefore remains `ACTIVE`: the three manuscripts have internally
accepted mathematical cores, but the original completion standard also asks
for database-level priority checks, external reproduction, and human-supplied
submission metadata that are not yet evidenced.
