# vibemath

Research sources, papers, certificates, and audit records for arithmetic
progressions of powers, magic squares of squares, and arithmetic progressions
on elliptic curves.

The repository is organized as `theme/paper`.  A directory may be a completed
paper or a clearly labelled long-term paper project.  Mathematical correctness,
claim boundaries, exact certificates, and independent checks take precedence
over journal-specific formatting.

## Research map

| Theme / paper | Status | Main result or current boundary |
|---|---|---|
| `square-progressions/seven-consecutive-squareclasses` | internally accepted | For integer `t`, the equality patterns of the nonzero block `t,...,t+6` with affine rational squareclass rank at most two are reduced through the exact chain `651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23`.  Realizability or impossibility of the final 23 patterns, and therefore `R_2(7)`, remain open. |
| `powers-in-progressions/pure-cubic-five-term` | internally accepted | `R^times_(3,1)(5)=4` for nonzero terms after one common rational scaling into cubes in a common nontrivial pure cubic field. |
| `elliptic-curve-progressions/campbell-two-isogeny-selmer` | internally accepted | Exact two-isogeny Selmer groups for the stated Campbell Jacobian and `rank <= 3`; no ninth rational point, full 2-Selmer group, Cassels--Tate value, or rank equality is claimed. |
| `square-progressions/magic-squares-over-number-fields` | active long-term project | Searches and reductions for order-three magic squares of squares over low-degree number fields; exploratory outputs are not promoted to theorems. |
| `powers-in-progressions/fourth-powers-six-term` | active long-term project | Exact reductions and quotient maps for the six-term fourth-power problem; `P_6(4)` remains open. |
| `powers-in-progressions/elliptic-simultaneous-torsion-c29` | active long-term project | Explicit genus-two model and birational-map audit; rank and complete rational-point set remain open. |

Each paper directory has its own `README.md`.  Final PDFs are deliberately
tracked; LaTeX auxiliaries, temporary builds, duplicate PDFs, simulated data,
and unexecuted CAS outputs are not.

The three internally accepted projects each contain a `NEXT_*_MATH_NOVELTY_AUDIT.md`
report.  A bibliographic “not found” result is treated as priority-risk
evidence, never as proof that a result is first.

No software or document license has yet been selected.  Until one is added,
ordinary copyright law applies.
