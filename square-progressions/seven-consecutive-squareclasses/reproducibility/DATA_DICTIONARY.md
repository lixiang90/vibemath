# Data dictionary for certificates and manifests

Release described: `paper-square-submission-v0.6.4` with nested mathematical
supplement `paper-square-supplement-v0.5.0`.  This dictionary documents every
JSON file in the archive candidate.  It explains representation and claim
eligibility; it does not enlarge any theorem or turn diagnostic data into
proof.

## Common representations and units

- JSON integers are dimensionless exact integers unless a field below assigns
  a unit.  Counts have the stated combinatorial unit (patterns, orbits,
  characters, classes, occurrences, branches, points or tests).
- A `mask` is a nonnegative seven-bit integer.  Bit `i` represents the factor
  `t+i`, for `0 <= i <= 6`; its support is a list of those position indices.
- A `pattern` or restricted-growth word is a seven-character equality
  partition.  Equal digits mean equal square classes; digit names themselves
  carry no arithmetic value.  Pattern IDs are zero-based indices in the
  documented ranked list.
- `t`, `x`, `y`, `X`, `Y`, `R`, `S`, `U`, and `V` are exact integers or exact
  rational-coordinate strings as specified by the containing record.  There
  is no floating-point numerical evidence in a proof field.
- A modulus is a positive integer; residues are exact congruence classes
  modulo that modulus.  Prime lists contain rational primes.
- Ranks and dimensions are dimensions over the finite field explicitly named
  by the record, normally `F_2`.
- Polynomial coefficient arrays are ordered exactly as stated in their local
  record; equation and factorization fields are human-readable exact symbolic
  identities, not executable code.
- SHA-256 values are 64 lowercase hexadecimal characters computed from raw
  file bytes.  Byte counts are nonnegative integers measured in bytes.
- `mathematical_evidence_eligible=true` in the nested manifest means that the
  exact frozen bytes may support only the claim boundary recorded by that
  manifest.  It never means that every field is itself a proof: fields named
  `warning`, `scope`, `simulation`, `bounded_search`, `candidate`, or
  `diagnostic` retain their explicit non-proof status.

## `STUDENT_SQUARE_ROUND_02_certificate.json`

Structural schema: Round-02 pattern certificate (no explicit `schema` key;
identified by filename and the bound SHA in the supplement manifest).

- `problem` and `definitions` (`string`, `object`) define the normalized
  seven-term problem, labels, masks and character quotients.
- `counts` (`object`) gives exact counts in units of partitions/reversal
  orbits/survivors.
- `strict_excluded_patterns` (`array`, 59 reversal-orbit records) and
  `strict_exclusion_reason_counts_before_reflection` (`object`) record exact
  finite screens; `strict_local_obstruction_note` states their logical scope.
- `unique_character_quotients` (`array`, 63 records) stores the distinct
  nonzero seven-bit masks and curve-degree/genus metadata.
- `unresolved_genus_strata` (`array`) groups survivors by quotient genus;
  `unresolved_patterns_ranked` (`array`, 284 pattern records) is the canonical
  downstream universe.
- `zero_term_cases` (`array`, 7 records) separates the forbidden parameters
  `t=-i` from nondegenerate arithmetic.

Claim eligibility: exact evidence for the 651-to-343-to-284 enumeration and
the 63 character supports.  It is not evidence that any survivor is realizable
or globally pointless.

Supersession: later certificates add isomorphisms and exclusions but do not
replace this source enumeration.  Its frozen bytes remain authoritative under
supplement v0.5.0.

## `STUDENT_SQUARE_ROUND_03_CERTIFICATE.json`

Structural schema/version: `version="round03-v1.1"`; no separate `schema` key.

- `theorem_correction` (`object`) records the corrected affine formula and
  exact equal-block condition.
- `counts` (`object`) counts quartic/sextic masks, isomorphism classes and
  pattern compatibility rows.
- `quartic_masks` (`array`, 35 masks) and `sextic_masks` (`array`, 7 masks)
  store curve supports and invariants.
- `affine_classes` and `pgl2_Q_classes` (`array`, 16 class records each) store
  representative masks, members and exact rational transformations.
- `padic_witnesses` (`array`) stores finite local formulas and prime/modulus
  data; `pattern_compatibility` (`array`, 284 rows) retains the single common
  parameter `t` across the fifteen quotients.
- `magma_scope` is a claim-boundary string, not a Magma result.
- `sha256_without_this_field` authenticates the canonical JSON body with that
  one field omitted.

Claim eligibility: exact evidence for the stated finite isomorphism partition,
maps and compatibility bookkeeping.  It is not a simultaneous rational-point
solution and contains no trusted external CAS conclusion.

Supersession: Round 04 refines parser and occurrence metadata; it does not
invalidate the Round-03 transformations.

## `STUDENT_SQUARE_ROUND_04_CERTIFICATE.json`

Structural schema/version: `version="round04-v1.0"`; no separate `schema` key.

- `j_invariant_proof` and `quartic_j_invariants` store exact rational invariant
  formulas/values for the twelve genus-one classes.
- `pgl2_Q_classes`, `affine_and_pgl_member_partitions_equal`,
  `nonaffine_transform_count`, and `nonaffine_transforms` record the exact
  16-class partition and eleven non-affine rational maps.
- `pattern_occurrences` (`array`, 284 records) maps every occurrence back to
  its source mask and common `t` constraints.
- `parser_schema` describes accepted rank/point transcript columns and types.
- `simulation_warning` explicitly marks synthetic end-to-end data as test-only.
- `sha256_without_this_field` authenticates the canonical body.

Claim eligibility: exact evidence for invariants, finite transformations,
parser constraints and occurrence fan-out.  Synthetic fixtures and simulated
rank/torsion points are never mathematical evidence.

Supersession: paper-level certificates below supersede only later exclusion
lists, not these geometric or parser records.

## `PAPER_SQUARE_SAFE_CERTIFICATE.json`

Schema: `PAPER_SQUARE_SAFE-integral-pattern-inventory-v1`.

- `source_sha256` binds the generators/input certificates used here.
- `scope_warning` limits every conclusion to the stated integral normalized
  problem.
- `self_contained_enumeration` stores exact 651/343/284 and related pattern,
  rank and character counts.
- `representative_classes` (`array`, 16 records) gives minimal integral models,
  masks, degrees, genera, discriminant support and entry points.
- `window_rank_audit`, `theorem_2026_scope`,
  `consecutive_four_character_theorem`, and
  `mask_77_89_affine_reflection` store exact finite counts, hypotheses,
  equations and the integral reflection map.

Claim eligibility: exact evidence for the SAFE classification table,
186/98 screen and mask-77/89 incidence.  Conditional literature-hypothesis
fields do not assert that those hypotheses hold here.

Supersession: the mask-77 certificate supplies the complete point proof and
same-parameter exclusion; SAFE remains the authoritative input inventory.

## `PAPER_SQUARE_MASK77_CERTIFICATE.json`

Schema: `paper-square-mask77-v1`.

- `input_sha256` binds SAFE and Round-04 inputs.
- `mapping` stores exact forward/inverse birational formulas and boundary
  points for the quartic and elliptic models.
- `gcd_squarefree_lemma`, `branch_summary`, and `branches` encode the complete
  squarefree-kernel split: 18 branches, integer variables and exact moduli.
- `d1_branch`, `factor_size_proofs`, and
  `factor_size_structured_certificate` store symbolic terminal arguments for
  the non-congruence branches.
- `proved_integral_points` is the six-point integral set, with coordinates in
  integers.
- `same_t_pattern_audit` stores the 44 exact pattern exclusions and the 54
  survivors after all fifteen masks are checked at one parameter.
- `bounded_search` is diagnostic only; `scope_warning` and
  `global_completeness_status` state the proof boundary.

Claim eligibility: all finite residue exhaustions, symbolic factor proofs,
integral points and 44 same-parameter exclusions are eligible.  The bounded
search is not.

Supersession: the Next-Gate input hash fixes the resulting 54 rows; no later
certificate changes the mask-77 point theorem.

## `PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json`

Schema: `paper-square-next-gate-v1`.

- `input_sha256` binds the 54-row mask-77 output and its generator.
- `selection_rule` explains the deterministic representative ranking.
- `constant_pairing_ranking` (`array`) records exact impact and pairing data.
- `mask102_integral_points` stores the integral equation, factor split,
  exceptional interval and complete point list.
- `pattern_impact` stores units of 54 input patterns, 19 excluded IDs and 35
  surviving IDs.

Claim eligibility: exact evidence for the mask-102 integral-point theorem and
54-to-35 exclusion.  Ranking scores select work; they are not arithmetic
existence probabilities.

Supersession: the mask-108 certificate binds the 35-row output and supplies the
next complete exclusion.

## `PAPER_SQUARE_MASK108_CERTIFICATE.json`

Schema/version: `paper-square-mask108-v1`, semantic version `1.0.0`.

- `input_sha256` binds the 35-row Next-Gate output and source.
- `integral_points` stores the exact equation, gcd/kernel alternatives,
  factorization proof, middle-interval check and six integral points.
- `pattern_impact` stores units of 35 input patterns, 12 excluded IDs and the
  final 23 necessary candidate IDs/partitions.

Claim eligibility: exact evidence for the mask-108 point theorem and the
35-to-23 exclusion.  It does not assert realizability of any final candidate
or decide `R_2(7)`.

Supersession: this is the terminal mathematical certificate in supplement
v0.5.0.  A later release must use a new semantic version and manifest hash.

## `PAPER_SQUARE_SUPPLEMENT_MANIFEST.json`

Schema/version: `paper-square-supplement-manifest-v1`, semantic version
`0.5.0`, release id `paper-square-supplement-v0.5.0`.

- `files` is the exact 23-row mathematical allowlist.  Each row has `path`
  (`string`), `bytes` (`integer`, bytes), `sha256` (`string`), `role` (`string`)
  and `mathematical_evidence_eligible` (`boolean`).
- `runtime` records Python and SymPy version strings;
  `reproduction_commands` is an ordered command array.
- `claim_boundary` separates proved and unproved statements.
- `release_status`, null `archival_url`, `source_control_commit`, and
  `source_control_note` prevent a local package from posing as a public archive.

Claim eligibility: only listed bytes with `mathematical_evidence_eligible=true`
may support the stated proved boundary, subject to every internal warning.

Supersession: v0.5.0 remains nested in submission root v0.6.4.  It is not
silently modified; any changed mathematical byte requires a new supplement
release.

## `PAPER_SQUARE_SUBMISSION_MANIFEST.json`

Schema/version: `paper-square-submission-manifest-v1`, semantic version
`0.6.4`, release id `paper-square-submission-v0.6.4`.

- `payload` is the exact root allowlist.  Each row has `path`, byte count,
  SHA-256, role and component version.
- `closure.exact_submission_files` fixes every regular file permitted in
  `PAPER_SQUARE_SUBMISSION/`; `root_manifest_excluded_to_avoid_self_reference`
  explains why this JSON does not hash itself.
- `nested_supplement` records the nested manifest identity/status.
- `pdf_policy` distinguishes the hash-bound reference PDF from legitimate
  timestamp differences in an independently rebuilt PDF.
- `release_status`, null `archival_url`, `author_metadata_status`,
  `manifest_trust_anchor`, and `claim_boundary` are fail-closed semantic fields.
- `verification_commands` is the ordered local audit recipe.

Claim eligibility: the manifest authenticates package identity and closure; it
does not itself prove mathematics.  The claim boundary delegates mathematical
evidence to the unchanged nested supplement.

Supersession: v0.6.4 supersedes v0.6.3 because manuscript structure and
submission prose changed.  The root JSON is non-self-referential, so the final
ZIP SHA-256 or future immutable repository record must externally pin its
bytes.  Any subsequent payload edit requires v0.6.5 or later, regenerated
hashes, tests, PDF and archive acceptance.
