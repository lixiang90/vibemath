# Certificate data dictionary

The file `PAPER_CUBE_KUMMER5_CERTIFICATE.json` uses schema
`paper-cube-pure-cubic-kummer-n5-v2`.

## Top-level fields

- `definition`: theorem conventions (nonzero hits, common rational scaling,
  nonconstant rational AP).
- `kernel_certificate`: symbolic coefficients and two resultants used in the
  pure-cubic Kummer-kernel lemma.
- `D_normalization`: degree-three, sign and same-field conventions.
- `orbit_counts`: the `9+1+15=25` partition of five-color orbits.
- `monochromatic_representatives`, `four_same_representative`,
  `local_representatives`: canonical orbit representatives.
- `local_obstructions`: exactly 60 records, one per pair of one of 15 words and
  one of the four supported direction representatives `D=2,3,6,18`.
- `lower_witness`: the explicit AP, counted positions, radicand and cube roots.
- `five_hit_status`: exhaustive status of the five-hit problem.
- `four_hit_classification_gate`: fail-closed status of the distinct maximizer
  classification problem.

## One `local_obstructions` record

- `word`, `D`, `prime`: complete model identifier and obstruction prime.
- `equations`: the three exact diagonal-cubic equations in projective `P^4`.
- `good_prime_condition`: human-readable condition `p` prime and `gcd(p,3D)=1`.
- `finite_field_count.parameter_pairs_scanned`: exactly `p^2-1`, corresponding
  to all `(a,d) != (0,0)` in `F_p^2`.
- `excluded_zero_pair`: the sole pair omitted from the scan.
- `pairs_with_at_least_one_zero_term`: diagnostic count; such pairs are still
  tested, so projective boundary coordinates are not silently removed.
- `cube_image_size_including_zero` and `allowed_value_counts_by_position`:
  sizes of the finite-field weighted cube sets.
- `first_failure_counts_by_position`: disjoint histogram assigning every
  rejected `(a,d)` to its first failed position.
- `compatible_parameter_pairs`: zero for a certified obstruction.
- `count_identity_verified`: asserts that the failure histogram plus compatible
  count is exactly `p^2-1`.
- `good_prime_conditions`: machine booleans and the condition text.

All integers are exact; no floating-point values occur.
