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
| Repository-level reproduction | PASS local worktree: 96 tests; PENDING frozen cold clone | PASS local worktree: 42 tests; PENDING frozen cold clone | PASS local worktree: 73 tests; PENDING frozen cold clone |
| Code, structured certificates, tests, schema/data dictionary | PASS | PASS | PASS |
| LaTeX source and readable PDF | PASS working-tree render: 11 pages | PASS working-tree render: 9 pages | PASS working-tree render: 11 pages |
| Exact comparison with accessible primary literature | PASS with residual priority risk | PASS with residual priority risk | PASS with medium residual priority risk |
| MathSciNet/zbMATH and equation-isomorphism priority audit | OPEN: human/database follow-up | OPEN: human/database follow-up | PARTIAL: exact minimal model/conductor searched; human database/citation-graph follow-up remains |
| External independent reproduction outside this workspace | OPEN | OPEN | OPEN |
| Internal clean-clone reproduction of a committed tree | PASS at commit `ccc4c4be6562` | PASS at the same commit | PASS at the same commit |
| Public source location and repository integrity manifest | PARTIAL: GitHub `main`; root `MANIFEST.sha256` still records Round10 bytes and awaits the Round11 freeze | PARTIAL: same | PARTIAL: same |
| Author identity and nonfabrication boundary | PASS: sole named author `Codex (GPT-5.6-sol)`; no other identity fields invented | PASS: same | PASS: same |
| Actual journal submission, venue and transmission authorization | OUT OF SCOPE: submission-ready research is sufficient | OUT OF SCOPE | OUT OF SCOPE |

The public all-project command is `python tools/run_all_checks.py`. After the
Round11 square supplement manifest was synchronized, the current working tree
passed groups `96,33,42,14,8,73`, totaling **266/266** checks. This audit
still does **not** record a Round11 commit hash or Round11 cold reproduction.
The latest completed frozen baseline remains the Round10 clean clone with 243 tests and groups
`87,33,36,14,8,65`. The repository-wide `MANIFEST.sha256` still describes
that Round10 snapshot and is not a hash index for the current Round11 bytes.
These facts establish internal reproducibility only for the frozen baseline;
they do not establish external peer review, priority, or the unresolved
long-term problems.

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
`t,...,t+6` nonzero. If their rational squareclasses have affine rank at most
two, their equality partition is one of 2 displayed necessary patterns. The
Round11 mask-85 theorem proves the complete integral-point set on
`y^2=t(t+2)(t+4)(t+6)` and excludes exactly IDs `31,276`; every point is
degenerate. The paper does not decide `R_2(7)`, does not prove that either
remaining pattern is realizable or impossible, and does not solve the
three-by-three magic square of squares.

### Pure cubic fields

For nonzero entries of a nonconstant rational five-term progression, one
common rational scale, and one nontrivial pure cubic field, the exact maximum
number of cubes is four. The proof exhausts all five-hit color classes. It
does not classify all four-hit progressions. Six of the 31 arithmetic-point
models are proved to supply positive-rank infinite families. Round11 closes a
seventh model, `((0,1,2,4),0102)`, for existence via the nondegenerate AP
`(64,36,8,-20,-48)` over `Q(cuberoot(6))`; its elliptic quotient has positive
rank, but this does not prove infinitely many rational lifts to the genus-four
source. The other 24 models remain open.

### Campbell descent

The exact finite result concerns the index-8 quartic attached to Campbell's
family: its two rational 2-isogeny Selmer groups, `rank E(Q) <= 3`, the
`Q x K` cubic-algebra invariant and `[35]` projection, and an everywhere-local
same-parameter fiber product.  Round09 additionally proves that the real place
together with either `p=59` or `p=71699` leaves exactly eight `E`-side support
classes. Round10 proves on the `E'` side that `Q_2` solubility is equivalent
to `d=1 mod 8`, while `Q_3` solubility is equivalent to `v_3(d)=0` and
`d=1 mod 3`; their intersection is exactly four classes. Round11 combines
the complete local exclusions, the support lemma and all surviving positive
witnesses to determine the exact isogeny Selmer groups of orders 8 and 4 and
deduce `rank E(Q)<=3`. This is not an exact rank, full 2-Selmer or
Cassels--Tate computation. It neither supplies nor excludes the ninth point.
The former opposite-side Cassels--Tate formula remains rejected negative
evidence and is not used by a positive theorem.

## Next gates

1. Attack the two final square patterns separately: mask 27 hits ID 12 and
   mask 45 hits ID 134. Require a complete point theorem, a strict local
   obstruction, or a valid same-parameter exclusion; search non-hits are not
   proofs.
2. Triage the remaining 24 pure-cubic models by exact geometry, local
   obstructions and explicit low-height points. A legal AP closes existence;
   an infinite-family claim requires infinitely many source-curve points, not
   merely a positive-rank quotient.
3. Independently reproduce the Campbell minimal model, conductor and
   two-isogeny descent in Sage/Magma/PARI, then seek certified lower-rank or
   full-2-Selmer information. Do not upgrade `rank<=3` to equality or infer a
   ninth point without a global argument.
4. The Round11 manifests are synchronized and all 266 registered checks pass
   locally. Next freeze an exact source commit and run the internal clean-clone
   protocol before declaring Round11 reproducible. Continue human
   database/citation-graph priority checks without turning a not-found report
   into an absolute claim.

The Goal therefore remains `ACTIVE`: all three Round11 mathematical increments
have passed cross-review, but the Round11 tree is not yet frozen and cold
reproduced. The current completion standard is submission-ready research only;
no actual journal submission, human author substitute, affiliation, contact,
ORCID, venue, DOI or transmission authorization is required. The sole named
author is `Codex (GPT-5.6-sol)`, and no missing identity field may be invented.
