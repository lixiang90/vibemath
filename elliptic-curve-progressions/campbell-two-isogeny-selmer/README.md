# Campbell two-isogeny Selmer computation

## Proved

For the Campbell Jacobian and two-isogeny models defined in the paper,

- `Sel^(dual phi)(E'/Q) = <3,5,7>` has dimension 3;
- `Sel^phi(E/Q) = <4230241,339106321>` has dimension 2;
- the Mordell--Weil rank is at most 3;
- the stated `Q x K` invariant and the `[35]` projection identities hold;
- the same-parameter local-solubility and 512-cell local matrix statements hold
  with the precise boundaries recorded in the paper.

## Not proved and corrected

No ninth rational point or impossibility result, full 2-Selmer group,
Cassels--Tate value, or rank equality is claimed.  The earlier cross-isogeny
Hilbert-symbol expression was invalid.  Its rejection is preserved in
`notes/ct-pairing-correction.md` and `certificates/ct_formula_rejection.json`;
those files are negative evidence, not a pairing computation.

Unexecuted Magma inputs are deliberately excluded from this repository.

