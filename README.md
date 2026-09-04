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
| `square-progressions/seven-consecutive-squareclasses` | internally accepted + Round12 novelty cross-review PASS | For integer `t`, the equality patterns of the nonzero block `t,...,t+6` with affine rational squareclass rank at most two are reduced through the exact chain `651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7 -> 4 -> 2`.  Realizability or impossibility of the final 2 patterns, and therefore `R_2(7)`, remain open. |
| `powers-in-progressions/pure-cubic-five-term` | internally accepted + Round12 novelty cross-review PASS/HIGH-CAUTION | `R^times_(3,1)(5)=4`; six of the initial 31 four-hit models yield infinite families, and a seventh has a rigorously verified nondegenerate point.  The Round09 reconstruction groups its 29-model input into 25 clusters under the explicitly stated permutation action.  Seven models are closed for existence and 24 remain open; no infinite family is claimed for the seventh genus-four source. |
| `elliptic-curve-progressions/campbell-two-isogeny-selmer` | internally accepted + Round12 novelty/second-CAS cross-review PASS | The two exact isogeny Selmer groups have dimensions 3 and 2, giving only `rank <= 3`; an explicit global minimal model has conductor `301245307115205810`.  The exact support/place bridge incorporates the Round09 `E`-side and Round10 `E'`-side local theorems and revalidates every surviving bad-place witness.  No ninth rational point, global obstruction, full 2-Selmer group, Cassels--Tate value, or rank equality is claimed; the independent second-CAS protocol remains unexecuted. |
| `square-progressions/magic-squares-over-number-fields` | active long-term project | Searches and reductions for order-three magic squares of squares over low-degree number fields; exploratory outputs are not promoted to theorems. |
| `powers-in-progressions/fourth-powers-six-term` | active long-term project | Exact reductions and quotient maps for the six-term fourth-power problem; `P_6(4)` remains open. |
| `powers-in-progressions/elliptic-simultaneous-torsion-c29` | active long-term project | Explicit genus-two model and birational-map audit; rank and complete rational-point set remain open. |

Each paper directory has its own `README.md`.  Final PDFs are deliberately
tracked; LaTeX auxiliaries, temporary builds, duplicate PDFs, simulated data,
and unexecuted CAS outputs are not.

The three internally accepted projects each contain a `NEXT_*_MATH_NOVELTY_AUDIT.md`
report.  A bibliographic “not found” result is treated as priority-risk
evidence, never as proof that a result is first.

The sole named author of the three research-ready manuscripts is
`Codex (GPT-5.6-sol)`.  No affiliation, contact address, ORCID, funding source,
venue selection, or actual journal submission is asserted.

The Round12 working tree incorporates three primary-source novelty audits and
their cross-reviews.  All three cross-reviews pass under explicit residual-risk
boundaries: no accessible-source non-hit is promoted to priority, authenticated
MathSciNet/citation-chain follow-up remains open, and the Campbell independent
second-CAS protocol has not been run.  The current squareclasses, pure-cubic,
and Campbell PDFs have 12, 10, and 11 pages, with SHA-256 values
`0312007e2125fe27b6ab358c0b4f81b15d0f689e05e62743de61b47b945b0ac1`,
`253f2403c26d13d62b7f758dc9188ce5577cfe82d54d425beffe26404684cb4f`,
and `1b27cc0331736af6b2078d4b0ddb21d2e21e3dc97403eb8235a2ae1f9a2a40f3`.
Round12 has not yet been frozen or cold-reproduced, and the root manifest is
intentionally left for regeneration after that freeze.

Round 11 source commit `20bb94753801907b46d41db611ab18c4cd9f9a10` passes the
recorded internal clean-clone protocol: all 266 tests pass in groups
`96,33,42,14,8,73`; the three PDFs rebuild to 11, 9 and 11 pages; their
committed/rebuilt text hashes match; and the final-log warning-pattern lists
are empty. Durable evidence is indexed under
`research-program/three-paper-project/reproduction/`. This is internal
reproduction, not external human review, and no push or journal submission is
claimed by the evidence-recording commit.

No software or document license has yet been selected.  Until one is added,
ordinary copyright law applies.
