# Campbell two-isogeny Selmer computation

Author: **Codex (GPT-5.6-sol)**. This is a research-complete manuscript
project, not an actual journal submission; no affiliation, email, ORCID,
funding source, or external institutional endorsement is asserted.

## Proved

For the Campbell Jacobian and two-isogeny models defined in the paper,

- `Sel^(dual phi)(E'/Q) = <3,5,7>` has dimension 3;
- `Sel^phi(E/Q) = <4230241,339106321>` has dimension 2;
- the Mordell--Weil rank is at most 3;
- an explicit global minimal model is
  `y^2+x*y=x^3-16441530*x^2+45166889779200*x`, with conductor
  `301245307115205810` and multiplicative reduction at every bad prime;
- the stated `Q x K` invariant and the `[35]` projection identities hold;
- on the `E'` side, `Q_2` solubility is equivalent to `d=1 mod 8`,
  `Q_3` solubility is equivalent to `v_3(d)=0` and `d=1 mod 3`, and their
  intersection is exactly `{1,4230241,339106321,1434501462453361}`;
- the same-parameter local-solubility and 512-cell local matrix statements hold
  with the precise boundaries recorded in the paper.

## Not proved and corrected

No ninth rational point or impossibility result, full 2-Selmer group,
Cassels--Tate value, or rank equality is claimed.  The earlier cross-isogeny
Hilbert-symbol expression was invalid.  Its rejection is preserved in
`notes/ct-pairing-correction.md` and `certificates/ct_formula_rejection.json`;
those files are negative evidence, not a pairing computation.
No independent second elliptic-curve CAS is available; the exact standard-
library proof and its compatibility test are not described as independent
external reproduction.

Three unexecuted Magma/audit input texts are retained under
`notes/candidate-input/` solely so that the fail-closed provenance tests are
reproducible.  They are `INELIGIBLE` as mathematical evidence: no Magma output,
execution transcript, or claimed CAS conclusion is present.

`NEXT_ELLIPTIC_MATH_NOVELTY_AUDIT.md` gives the current claim-by-claim
correctness, contamination, and prior-art audit.

Journal-facing research-readiness prose is collected in `submission/`. The author identity
is fixed above. An immutable release locator and any venue-specific approval
remain deliberately absent because no actual submission is requested.
