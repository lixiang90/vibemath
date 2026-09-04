# Seven consecutive squareclasses: mathematical and novelty audit

Audit date: 2026-09-04
Audited tree: `vibemath/square-progressions/seven-consecutive-squareclasses/`

## Round-11 status addendum

The claim trace below originally stopped at 23 patterns. Five later elementary
gates are now proved and certificate-bound: mask 99 gives `23 -> 15`, mask
51 gives `15 -> 10`, mask 90 gives `10 -> 7`, mask 54 gives `7 -> 4`, and
mask 85 gives `4 -> 2`.
The current headline theorem
is therefore the necessary
classification

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7 -> 4 -> 2`.

For mask 51, all 15 input packets were re-read from the mask-99 certificate:
225 occurrences contain 53 distinct masks and 26 genus-one four-factor masks.
Among masks already covered by a proved integral translate, mask 51 uniquely
maximizes impact (five patterns). Its curve is the integral translate `s=t-1`
of mask 102 and also has an independent `gcd(A,B)|4`, `d in {1,2}` proof.
All its integral points are degenerate. See `PAPER_SQUARE_MASK51_REPORT.md` and
`PAPER_SQUARE_MASK51_CERTIFICATE.json`.

For mask 90, the exact pairing `A=(t+1)(t+6)`, `B=(t+3)(t+4)` gives
`B-A=6` and `gcd(A,B)|6`. The four squarefree kernels
`d in {1,2,3,6}` and the six complementary integers give only degenerate
branch points, so IDs `43,251,281` are excluded. The remaining IDs are
`12,31,59,134,214,230,276`. The same novelty boundary remains in force:
this is a necessary finite classification and does not decide `R_2(7)` or
realize any survivor.

For mask 54, `s=t-1` gives a point-by-point integral bijection with the already
proved mask-108 curve. Independently, `A=(t+1)(t+5)` and
`B=(t+2)(t+4)=A+3` reduce the positive regions to the two squarefree kernels
`d in {1,3}`; the five complementary integers give the same six points. Every
point has a zero in the original seven-term block. The exact occurrence audit
therefore excludes IDs `59,214,230`, leaving `12,31,134,276`.

For mask 85, the centered variable `x=t+3` gives
`t(t+2)(t+4)(t+6)=(x^2-9)(x^2-1)`.  In the positive regions the two factors
differ by 8, so their common positive squarefree kernel is `d in {1,2}`.
The only same-parity factor pairs force `x^2=10` or `U=0`; the seven
complementary integers give six degenerate points.  The exact occurrence
audit excludes IDs `31,276`, leaving `12,134`.

## Verdict

I found no blocking mathematical error in the stated theorem.  The defensible
publishable unit is deliberately narrow:

> For an integer `t` with none of `t,...,t+6` zero, if their rational
> squareclasses have affine rank at most two, then, up to relabelling and
> reversal, their equality partition belongs to the explicitly listed two
> patterns; the exact necessary-pattern reduction is
> `651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7 -> 4 -> 2`.

This is a necessary-pattern classification, not a realization theorem and not
a decision of `R_2(7)`.  Its strongest apparent novelty lies in combining an
affine Kummer-label enumeration with all fifteen character equations at one
common parameter.  The individual subset-product curves and the elliptic model
`Y^2=X^3-36X` are not safe novelty claims.

I did find three repairable precision defects and fixed them in the paper:

1. Xarles is now cited to Section 4 for the six-term quadratic-field
   obstruction, avoiding the convention-sensitive phrase “Theorem 1,
   `S(2)=6`”.
2. The symmetric four-block screen now explicitly enumerates the primitive gap
   pairs `(1,1),(1,2),(1,3),(1,4),(2,1)` and connects them to the five sets of
   González-Jiménez--Xarles Proposition 5.
3. The mask-77 prose now says accurately that the JSON records equations and
   moduli while the generator and regression test exhaust the residue triples;
   the JSON alone does not contain a full residue truth table.

The prior-art section and bibliography were also widened to cover the closest
subset-product literature.  These changes were made both in the working source
and in the audited `vibemath/.../paper` source.

## Claim-by-claim trace

| Claim | Proof/data dependency | Adversarial check | Result |
|---|---|---|---|
| Rank-zero or rank-one cannot occur | `main.tex`, Lemma `R_1(6)=5`; Xarles Section 4; explicit AP `49,169,289,409,529,649` | The first five selected terms really have one squareclass over `Q(sqrt(409))`, and every endpoint six-window would otherwise become six squares after common scaling | Sound; no computation used |
| Common-scaling/Kummer equivalence | `main.tex`, Proposition “Common scaling” | Checked both directions in `Q*/Q*2`; multiplying by the common class kills the affine offset.  Equality of labels follows from injectivity when the difference rank is two.  Zero terms are explicitly excluded | Sound.  It does **not** claim the unscaled terms lie in one biquadratic field |
| `651 -> 343 -> 284` | `code/STUDENT_SQUARE_ROUND_02_patterns.py`; `certificates/STUDENT_SQUARE_ROUND_02_certificate.json`; its test | Independently checked `S(7,3)+S(7,4)=651`, 35 reversal-fixed words, 109 screened words/59 orbits, 542 survivors/26 fixed words.  Burnside gives 343 and 284 | Exact finite enumeration |
| The finite screen is mathematically justified | Lemma `R_1(6)=5`; González-Jiménez--Xarles Proposition 5 and Corollary 6 | A four-set with equal outside gaps has gaps `(a,b,a)`, `2a+b<=6`; after gcd normalization precisely the five cited exceptional types occur.  A block of size at least five contradicts `Q(7)=4` | Sound after the explicit-gap repair |
| Every packet has exactly 15 character quotients | `main.tex`, “Fifteen characters”; Round-02 relation basis; `code/PAPER_SQUARE_SAFE_inventory.py`; Round-04 occurrence table | The affine map `T:F_2^7 -> F_2 + F_2^2` has rank 3, hence a four-dimensional kernel with 15 nonzero characters.  Machine totals recompute `284*15=4260`; variable/lookup tests cover all occurrences | Sound and self-contained |
| `284 -> 98` | Four-consecutive-factor lemma; SAFE code/certificate/test | The factorization `(n+1-y)(n+1+y)=1` is complete over integers.  All four consecutive masks are checked against each kernel, not just one representative | Exact; depends essentially on integral `t` |
| Integral points on mask 77 and `98 -> 54` | `code/PAPER_SQUARE_MASK77_analysis.py`; mask-77 certificate/test | `gcd(A,B)|72` gives 18 squarefree-kernel/sign/factor branches.  Fifteen are excluded by complete finite residue enumeration; the remaining three have verified factor-size contradictions, leaving only branch points and `(6,+/-72)`.  For every affected pattern the code tests the same candidate `t` against all 15 characters; it does not infer compatibility from separate quotient points | Sound.  The bounded search field is marked conjectural and is not used in completeness |
| `54 -> 35` via mask 102 | `code/PAPER_SQUARE_NEXT_GATE.py`; certificate/test | `A=(t+1)(t+6)`, `B=(t+2)(t+5)`, `B-A=4`, `gcd(A,B)|4`; the two positive squarefree kernels and six middle integers exhaust all integer cases | Sound elementary integral-point theorem |
| `35 -> 23` via mask 108 | `code/PAPER_SQUARE_MASK108.py`; certificate/test | `A=(t+2)(t+6)`, `B=(t+3)(t+5)=A+3`, `gcd(A,B)|3`; kernels 1 and 3 plus middle integers exhaust all cases.  Exactly 12 occurrence rows are removed | Sound elementary integral-point theorem |
| `23 -> 15` via mask 99 | `code/PAPER_SQUARE_MASK99.py`; certificate/test | Complete squarefree-kernel branches give the stated integral points and remove exactly eight occurrence rows | Sound elementary integral-point theorem |
| `15 -> 10` via mask 51 | `code/PAPER_SQUARE_MASK51.py`; certificate/test | The integer translate to mask 102 and an independent `gcd(A,B)|4` proof agree; exactly five patterns are removed | Sound elementary integral-point theorem |
| `10 -> 7` via mask 90 | `code/PAPER_SQUARE_MASK90.py`; certificate/test | `B-A=6`, `gcd(A,B)|6`; the kernels `1,2,3,6` plus the six middle integers leave only four degenerate branch points. Exactly IDs `43,251,281` are removed | Sound elementary integral-point theorem |
| `7 -> 4` via mask 54 | `code/PAPER_SQUARE_MASK54.py`; certificate/test | The integer point bijection `s=t-1` with mask 108 and an independent `B-A=3`, `gcd(A,B)|3` proof agree; exactly IDs `59,214,230` are removed at the same parameter | Sound elementary integral-point theorem |
| `4 -> 2` via mask 85 | `code/PAPER_SQUARE_MASK85.py`; certificate/test | The centered factors differ by 8; the two squarefree kernels and seven middle integers exhaust all cases. Exactly IDs `31,276` are removed at the same parameter | Sound elementary integral-point theorem |
| Final 2-row table | Mask-85 `remaining_pattern_ids` and the upstream ranked rows | Independently checked IDs and partition words `12:0012202`, `134:0012131` | Exact. IDs are ordering-dependent; partition words carry the mathematical content |

## Search-to-proof boundary and synthetic-data audit

No theorem above is obtained from a height-bounded search.  The only bounded
search in the mask-77 artifact is labelled `conjectural_only`; its output is
not read by the branch-completeness proof.

`STUDENT_SQUARE_ROUND_04_pipeline.py` can generate synthetic rank/point CSV
fixtures, and its certificate contains a warning about them.  This is a real
audit hazard because a casual reader could conflate the parser demonstration
with arithmetic evidence.  However, the present theorem chain reads only the
exact `pattern_occurrences`, character masks, transforms and invariant fields
constructed before those fixtures.  The eight gate programs read the Round-04
occurrence table and their predecessor exact certificates; none reads
`STUDENT_SQUARE_ROUND_04_SIMULATED_*`, Round-05 synthetic output, a claimed
Mordell--Weil rank, or an unexecuted CAS transcript.  Thus no current theorem
depends on simulated arithmetic.

Two nonblocking reproducibility cautions remain:

- several generator invariants are Python `assert` statements, so the official
  reproduction command must not use `python -O`;
- the mask-77 JSON is a compact certificate, not a stand-alone list of every
  residue triple.  Its finite proof is the triple “branch equations + generator
  + regression test”, which the revised prose now says explicitly.

## Prior-art search and collision risk

The following are the closest primary or publisher/DOI sources located.  An
absence-of-hit search is not proof of novelty.

### Squares in arithmetic progressions and low-degree fields

- González-Jiménez--Xarles, [On a conjecture of Rudin on squares in arithmetic progressions](https://doi.org/10.1112/S1461157013000259), especially Proposition 5 and Corollary 6; [author manuscript](https://arxiv.org/html/1301.5122v1).  It already develops curves attached to subsets of an AP and proves the five exceptional four-subsets.  The present paper must not claim invention of that curve method.
- Xarles, [Squares in arithmetic progression over number fields](https://doi.org/10.1016/j.jnt.2011.07.010); [author manuscript](https://arxiv.org/abs/0909.1642).  Section 4 excludes six nonconstant squares over quadratic fields.
- Bremner--Siksek, [Squares in arithmetic progression over cubic fields](https://arxiv.org/abs/1505.06424), IJNT 12 (2016), 1409--1414.  This is about actual squares in cubic fields, not affine rational squareclass partitions.
- González-Jiménez, [Squares in arithmetic progression over quadratic extensions of number fields](https://doi.org/10.1142/S1793042126500612), IJNT 22 (2026), 1141--1158.
- González-Jiménez--Tho, [Squares in arithmetic progression over certain non-primitive quartic number fields](https://doi.org/10.1016/j.jnt.2025.11.005), JNT 282 (2026), 13--30.

The two 2026 papers make any broad “quadratic/quartic-field square progression”
claim high risk.  Their published descriptions concern actual square
progressions under extra field/rank/class-number hypotheses.  I found no
statement in the accessible versions that gives this seven-term affine
squareclass equality classification, but the paper should continue to state
only “we did not locate”.

### The directly relevant subset-product literature

- Saradha, [Squares in products with terms in an arithmetic progression](https://doi.org/10.4064/aa-86-1-27-43), Acta Arith. 86 (1998), 27--43; [EuDML record](https://eudml.org/doc/207179).
- Granville--Selfridge, [Product of integers in an interval, modulo squares](https://doi.org/10.37236/1549), Electronic J. Combin. 8 (2001), R5; [journal page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v8i1r5).
- Bui--Pratt--Zaharescu, [A problem of Erdős--Graham--Granville--Selfridge on integral points on hyperelliptic curves](https://doi.org/10.1017/S0305004123000488), MPCPS 176 (2024), 309--323; [author manuscript](https://arxiv.org/abs/2211.12467).

These are conceptually closer than the number-field papers: they study square
products of selected interval/AP terms and curves of the form
`y^2=x product(x+j_i)`.  Exact searches for the three masks 77, 102 and 108 and
their expanded quartics did not locate the same stated integral-point lists,
but those lists are elementary and should not be marketed as independently
novel.  Their role is to make the combined finite classification explicit.

### Elliptic/Pell neighbours

- Pethő--Zimmer--Gebel--Herrmann, [Computing all S-integral points on elliptic curves](https://doi.org/10.1017/S0305004199003916).
- Masser--Rickert, [Simultaneous Pell Equations](https://doi.org/10.1006/jnth.1996.0137).
- Bremner--Silverman--Tzanakis, [Integral points in arithmetic progression on y²=x(x²-n²)](https://doi.org/10.1006/jnth.1999.2430).
- [LMFDB 576.c3](https://www.lmfdb.org/EllipticCurve/Q/576/c/3) identifies the mask-77 elliptic model.

These sources confirm that neither the congruent-number model nor the general
S-integral/Pell strategy is novel.  They do not appear to contain the present
integer-parameter branch certificates or the two-pattern conclusion.

## Claims to retain, narrow, or remove

### Retain as the headline theorem

The summary classification for **integer** `t`, **nonzero** seven-term block,
**affine** rational squareclass rank at most two, modulo **relabelling and
reversal**, with the two partition words printed in the theorem and exact
certificate.  Describe it as an exact necessary-pattern reduction.

### Retain as supporting lemmas, not novelty headlines

- the common-scaling/Kummer kernel equivalence;
- the exact finite counts and fifteen-character construction;
- the complete integral-point gates for masks 77/89, 102, 108, 99, 51, 90, 54 and 85;
- the same-parameter compatibility checks.

### Must remain downgraded or explicitly disclaimed

- “first”, “new”, “previously unknown”, or “complete prior-art search”;
- novelty of subset-product/Kummer curves or of `Y^2=X^3-36X`;
- a classification of all rational `t` or arbitrary common difference;
- existence of either remaining pattern;
- nonexistence of rank-two seven-term progressions or a decision of `R_2(7)`;
- a claim that the unscaled seven terms are squares in one biquadratic field;
- any result inferred from simulated rank/point fixtures or unexecuted CAS
  candidates;
- “651 initial patterns” without the qualifier that affine rank at most one
  has already been excluded and exactly three/four equality blocks are being
  enumerated.

## Verification performed

- Ran the thirteen squareclasses regression modules: **96 tests, all passed**.
- Recomputed all headline counts and `284*15=4260` occurrences from source.
- Recomputed the final two IDs and checked every partition word printed in
  the table.
- Checked the mask-77 branch split: 18 total, 15 finite congruence
  obstructions, 3 factor-size closures, 0 unresolved.
- Rechecked the mask-99, mask-51, mask-90, mask-54 and mask-85 pattern impacts and complete
  squarefree-kernel branches.
- Verified that supplement v0.10.1 and SHA-256
  `deb3eade7c9f25c6e0c8da019f21f7a0943bdd50fcf263f7add6ed8b3ed0309e`
  match the mathematical supplement manifest used by the working tree.
- Rebuilt the revised paper with the full BibTeX/LaTeX chain; the final log has
  no undefined citation/reference, overfull/underfull box, or LaTeX warning.

## Recommendation

The mathematics is suitable for circulation as a short, computer-assisted
finite-classification paper, provided the claim boundary above is used.  The
largest remaining scholarly risk is not a proof gap but novelty positioning:
the subset-product literature is extensive, so the contribution should be the
specific affine-rank-two seven-term classification and auditable simultaneous
compatibility reduction, not the general curve construction or the individual
quartics.
