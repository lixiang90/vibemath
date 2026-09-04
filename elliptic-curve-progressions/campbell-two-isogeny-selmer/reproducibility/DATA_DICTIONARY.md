# Data dictionary for the Campbell finite two-isogeny supplement

Release-root version: `paper-elliptic-campbell-local-release-v0.6.3`  
Mathematical-supplement version: `paper-elliptic-campbell-supplement-v0.6.1`

This dictionary describes the machine-readable certificates and both manifest
levels. It is explanatory metadata, not an additional mathematical proof. The
JSON documents are authoritative for their stored values; the generators and
tests are authoritative for recomputation.

## Common JSON conventions

- JSON types are written below as `object`, `array`, `string`, `integer`,
  `boolean`, or `null`. All displayed mathematical integers are exact JSON
  integers; no floating-point field is used as mathematical evidence.
- A prime used as an object key is necessarily a JSON string (for example
  `"59"`), even when the same prime appears elsewhere as an integer.
- SHA-256 values are lowercase 64-character hexadecimal strings.
- `mathematical_evidence_eligible: true` means that the file may support only
  the proved claims within its own `claim_boundary`. It never promotes a
  heuristic, bounded search, unexecuted input, withdrawn formula, or local
  point to a stronger global conclusion.
- `YES` in a local cell means local solubility at that one displayed place;
  `NO` means the stored exact obstruction excludes that ambient class at that
  place. It does not mean that a rational point exists or does not exist unless
  a separately stated theorem supplies that implication.

## 1. Same-parameter fibre-product certificate

File: `STUDENT_ELLIPTIC_ROUND_03_certificate.json`  
Role in supplement manifest: `same_m_input_certificate`  
Evidence eligibility: yes, within its explicit local/bounded boundary.

| Field | Type | Meaning |
|---|---|---|
| `coefficients.D`, `coefficients.H` | arrays of integers | Coefficients of the two binary quartics used for `Y^2=D(m)` and `Z^2=H(m)`. |
| `same_m_local_certificates.real` | object | One common rational `m`, with exact `D_m` and `H_m`, witnessing real solubility. |
| `same_m_local_certificates.two_adic` | object | One common integer `m`; `D_mod_8=H_mod_8=1` gives the stored 2-adic witness. |
| `same_m_local_certificates.odd_format` | array of six strings | Column declaration `[p,m,D_mod_p,sqrt_D,H_mod_p,sqrt_H]`. |
| `same_m_local_certificates.odd` | array of six-integer arrays | For each listed odd prime, the same residue `m` makes both quartic values squares modulo `p`; the last four entries satisfy the two displayed square congruences. |
| `same_m_local_certificates.remaining_good_primes` | string | The Weil-bound and Hensel bridge used outside the finite bad/small-prime list. |
| `binary_quartic_audits` | object | Exact quartic invariant and Jacobian-model checks for `D` and `H`. |
| `bounded_CH_search` | object | Height convention, bound, sieve data and observed counts. This is bounded evidence only. |
| `global_status` | object of booleans | Fail-closed flags: no rational point or fake 2-Selmer computation is asserted. |
| `classification.proved` | array of strings | Claims certified as proved by this file. |
| `classification.bounded_evidence` | array of strings | Searches that must not be read as proofs of global emptiness. |
| `classification.awaiting_magma` | array of strings | Unperformed external computation, not evidence. |

The Round-06 certificate repeats the same local theorem in
`same_m_local_summary`, binds this source file by SHA-256, records 30 odd-prime
witness rows, the real and 2-adic witnesses, the two discriminants and the
nonzero resultant. “Same-m” is essential: the two square conditions use the
same parameter at each place. Everywhere local solubility is not a global
rational point.

## 2. The 64 by 8 local matrix (512 cells)

File: `PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json`  
Generator: `PAPER_ELLIPTIC_CAMPBELL_analysis.py`  
Schema: `PAPER_ELLIPTIC_CAMPBELL-local-matrix-v1`  
Evidence eligibility: yes for the exact local classification and torsor
projection stated in `claim_boundary`.

### Top-level fields

| Field | Type | Meaning |
|---|---|---|
| `equations.E`, `equations.E_dual` | objects | Integral two-isogeny quartic data for the two curve sides. |
| `checked_places` | array | The eight places checked for each ambient squareclass: infinity, 2, 3, 5, 7, 59, 71699 and 339106321. |
| `rows` | array of 64 objects | Thirty-two signed squareclasses on each of `E` and `E_dual`. Each row has `side`, integer `d`, and a `places` object. |
| `summary.cells` | integer | Exactly 512 = 64 rows times 8 places. |
| `summary.status_counts` | object of integers | Final totals: 384 `YES`, 128 `NO`, 0 `UNRESOLVED`. |
| `summary.surviving_ambient_classes` | object of integer arrays | Classes with `YES` at all eight displayed places: 8 on `E`, 4 on `E_dual`. At this certificate stage they are ambient local survivors. |
| `initial_stage_survivors_16_plus_4` | object | Historical first-stage survivors, retained for traceability rather than final classification. |
| `initial_stage_unresolved_cells` | integer | Historical value 56. The final rows resolve all of them. |
| `torsor_projection` | object | Binary-quartic invariants, rational 2-torsion scaling, `Q x K` resolvent data, and the projection of the Campbell `C_H` class to the `E`-side squareclass `d=35`. This is a cohomological component, not an isomorphism with the displayed quartic `C_d`. |
| `source_sha256` | object | Hashes of the scripts on which this certificate depends. |
| `claim_boundary` | object | Exact proved/not-proved boundary. |

### One local cell

Each `rows[i].places[p]` is an object with:

- `status` (`"YES"` or `"NO"`): final exact classification at the place;
- `method` (string): real sign analysis, exact p-adic squareclass witness, or
  exhaustive weighted-projective search modulo a prime power;
- `depth` (string or object): either an exact local method label or
  `{prime, exponent, modulus}` for finite modular exclusion;
- `previous_status` (optional string): audit trail from the earlier bounded
  stage, not the final result;
- `witness` (optional object): exact integers such as `U`, `V`, `rhs`, chart,
  valuation and residue-unit data supporting `YES`;
- `proof` (optional string): a symbolic valuation argument used instead of a
  bounded witness.

The matrix alone calls the 8+4 sets local ambient survivors. Round 04 upgrades
exactly those sets to the two isogeny Selmer groups only after adding the
support lemma and the good-prime Hasse--Hensel argument.

## 3. Clean Round-04 certificate: positive exact descent data

File: `PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json`  
Generator: `PAPER_ELLIPTIC_ROUND_04_analysis.py`  
Schema/version: `paper-elliptic-campbell-round-04-clean-v2`, `2.0.0`  
Evidence eligibility: yes, subject to `claim_boundary` and `supersession`.

| Field | Type | Meaning |
|---|---|---|
| `quadratic_field_and_z` | object | Exact definition of `K=Q(sqrt(1434501462453361))`, its `Q`-basis arithmetic, the `Q x K` resolvent factor, both components of `z(H)`, norms and square scalings. |
| `scaling` | object | Translation and Weierstrass scaling between the large Jacobian model and the small rational-2-torsion model. |
| `isogeny_descent.curves_and_isogeny` | object | Coefficients of `E`, `E_prime` and the kernels of the 2-isogeny and dual isogeny. |
| `isogeny_descent.support_lemma` | object | Complete squareclass support sets and the valuation argument, including the case where the quartic variable `N` need not be p-integral. |
| `isogeny_descent.good_prime_lemma` | object | Finite place set `S`, smoothness support and Hasse--Hensel bridge outside `S`. |
| `isogeny_descent.exact_selmer_groups` | object | The exact 8- and 4-element isogeny Selmer sets, F2 dimensions 3 and 2, chosen generators, naming convention, and rank upper bound 3. These are isogeny Selmer groups, not the full 2-Selmer group. |
| `known_mordell_weil_images` | object | Kummer images of only the proved points `O` and `(0,0)`, plus unexplained cosets explicitly marked as not-yet-Sha. |
| `source_sha256` | object | Hashes of the exact generators used. |
| `supersession` | object | Forbids the withdrawn Cassels--Tate setup fields and points to the Round-05 negative audit. |
| `claim_boundary` | object | Positive statements and the excluded rank/full-Selmer/Sha/Cassels--Tate/global-point conclusions. |

This is the only clean positive certificate for the exact isogeny Selmer
groups. It deliberately contains none of `d35_cassels_tate_setup`,
`pairing_bits_to_compute`, or `decisive_outcome`.

## 4. Round-05 negative-evidence certificate

File: `PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json`  
Generator: `PAPER_ELLIPTIC_ROUND_05_analysis.py`  
Schema: `paper-elliptic-campbell-round-05-correction-v1`  
Evidence eligibility: **negative audit only**.

| Field | Type | Meaning |
|---|---|---|
| `conic_and_tangent` | object | Exact auxiliary conic point, residual and tangent coefficients. These are candidate local-function ingredients, not a pairing. |
| `rejected_opposite_side_formula_audit` | object | Local branch data at the checked places. `well_definedness_test` is `FAIL_BRANCH_INDEPENDENCE`; possible products are both `-1` and `1`. |
| `exact_isogeny_selmer_groups_reused` | object | A copied consistency summary of the Round-04 groups; Round 04 remains the positive authority. |
| `required_next_objects` | object | Precise same-side or full-2-Selmer objects required before a genuine pairing computation can be defined. |
| `claim_boundary.proved` | array | Only the conic/tangent identities and failure of the old branch-dependent expression, plus reuse of Round-04 facts. |
| `claim_boundary.withdrawn` | array | Statements that must never be revived: the opposite-side expression is not a defined Cassels--Tate pairing and cannot prove `C_H(Q)` empty. |
| `claim_boundary.not_proved` | array | Full 2-Selmer, any relevant pairing, and rational-point existence/nonexistence remain open here. |

Within `local_data[p]`, `U`, `V`, `rhs` and `precision_exponent` describe the
chosen p-adic input; each `branches` entry stores modular `N` and `L`, the
valuation/unit and the value of the rejected Hilbert expression. These numbers
certify branch dependence only. They are not Cassels--Tate values.

The file `PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m` is frozen but unexecuted.
The supplement manifest marks it `mathematical_evidence_eligible: false`; there
is no transcript or trusted Magma binary hash.

## 5. Round-06 source and provenance certificate

File: `PAPER_ELLIPTIC_ROUND_06_CERTIFICATE.json`  
Generator: `PAPER_ELLIPTIC_ROUND_06_analysis.py`  
Schema/version: `paper-elliptic-campbell-round-06-v1`, `1.0.0`  
Evidence eligibility: yes within its exact source/provenance boundary.

| Field | Type | Meaning |
|---|---|---|
| `campbell_source_reconstruction` | object | Campbell citation/location, parameter change, cubic coefficients, seven square-root identities, `D`/`H` coefficients, indices 0 through 8, and every recorded rational degeneration boundary. |
| `same_m_local_summary` | object | Hash-bound summary of the earlier common-parameter local certificate, including discriminants, resultant, 30 odd witnesses and the real/2-adic witnesses. |
| `prior_art` | object | Dated exact-query audit. `exact_query_result` and `novelty_boundary` are search metadata, not a proof of novelty. |
| `provenance.python_exact_pipeline` | object | Executed/tested evidence flag. |
| `provenance.magma_full_descent` | object | `UNEXECUTED_FROZEN_CANDIDATE_INPUT`, null transcript/hash and explicit forbidden promotions. Its eligibility is false. |
| `claim_boundary` | object | Separates source/local/finite facts from ninth-point, full-descent and Cassels--Tate claims. |

## 6. Two-level manifests and archive records

### Mathematical supplement manifest

File/schema: `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json`,
`paper-elliptic-supplement-manifest-v1`; version `0.6.1`.

- `release_status` is the fail-closed string
  `LOCAL_RELEASE_CANDIDATE_NOT_PUBLICLY_ARCHIVED`; `archival_url` is null.
- `runtime` stores Python and SymPy version strings.
- `files` is an array of objects with `path` (string), `bytes` (integer),
  `sha256` (string), `role` (string) and
  `mathematical_evidence_eligible` (boolean).
- `reproduction_commands` is an ordered string array.
- `claim_boundary` is an object with `proved` and `not_proved` strings.
- `ineligible_input_policy` names the unexecuted Magma input and why it is
  excluded.
- `supersession_policy` names Round 04 as clean positive evidence, lists its
  forbidden fields, names Round 05 as the negative audit, and forbids treating
  that audit as a pairing value.
- `test_accounting` records 39 isolated core tests, 3 supplement-manifest
  tests, 3 release-manifest tests, and total 45.

### Release-root manifest

File/schema: `PAPER_ELLIPTIC_RELEASE_MANIFEST.json`,
`paper-elliptic-release-root-v1`; version `0.6.3`.

- `release_id` and `status` identify a local draft not authorized for
  submission; `public_archive` is null.
- `files` is an array of `{path:string, bytes:integer, sha256:string}`. It
  binds the supplement manifest, manuscript TeX/PDF, submission metadata and
  this data dictionary.
- `commands` supplies mathematical rebuild, paper build and 45-test commands.
- `pdf_policy` explains why the frozen PDF hash is authoritative even when
  build metadata changes.
- `claim_boundary` repeats the deliberately narrow release claim.

### Deterministic archive allowlist and audit

- `PAPER_ELLIPTIC_ARCHIVE_CANDIDATE_ALLOWLIST.json` uses schema
  `paper-elliptic-deterministic-archive-v1`. Its `members` array stores path,
  exact byte length and SHA-256 for every member; `manifest_anchors` hashes
  both manifest levels; `archive` stores filename, length and hash. Timestamp,
  POSIX mode, compression and local-only status are explicit top-level fields.
- The ZIP member set is exactly the sorted union of the release manifest
  itself, every release-root row and every supplement row. No recursive
  directory traversal is used.
- `PAPER_ELLIPTIC_ARCHIVE_CANDIDATE_AUDIT.json` records empty-directory
  extraction, manifest validation, the 45-test transcript hash, forced TeX
  rebuild, page/text checks and machine-checkable RNT metadata. This is an
  execution record, not mathematical evidence beyond the tests it identifies.

## 7. Round-11 exact isogeny-Selmer audit

Certificate: ../certificates/round11_isogeny_selmer_audit.json
Generator: ../code/NEXT_ELLIPTIC_ROUND_11.py
Regression test: ../code/NEXT_ELLIPTIC_ROUND_11_test.py

This certificate checks the two isogeny maps and covering identity
symbolically, proves the union of required places, binds the Round-09 and
Round-10 uniform local gates by SHA-256, revalidates all 84 finite positive
primitive witnesses for the twelve surviving classes, checks both survivor
sets are squareclass subgroups, and records Selmer dimensions 3 and 2. Its
rank field stores only rank_upper_bound=3 and exact_rank_claimed=false. It is
not evidence for a full 2-Selmer group, exact rank, Cassels--Tate value, or
ninth point.

## 8. Eligibility and supersession quick reference

| Object | May support | Must not support |
|---|---|---|
| Same-m certificate / Round-06 summary | Everywhere local solubility of the smooth same-parameter fibre product | A global rational parameter |
| 512-cell certificate | Exact local matrix and the `d=35` rational-component projection | A full 2-Selmer group or rational point |
| Round-04 clean v2 | Exact two isogeny Selmer groups, `Q x K` invariant, visible MW images, rank at most 3 | Rank equality, Sha membership, pairing, `C_H(Q)` emptiness |
| Round-05 correction | Failure of the old opposite-side/branch-dependent formula | Any Cassels--Tate value or global conclusion |
| Round-06 certificate | Campbell-source identities, degeneration boundaries, provenance and hash-bound local summary | Novelty proof, full descent or ninth-point conclusion |
| Unexecuted Magma file | Human-readable candidate input only | Any theorem or computed invariant |
| Prior-art report | Dated “not found” search record | Proof of novelty |

Whenever summaries overlap, the clean Round-04 certificate controls positive
descent claims, the Round-05 certificate controls only the withdrawal/negative
audit, and the Round-06 certificate controls source reconstruction and
provenance. No field in a superseded or ineligible object may override those
boundaries.
