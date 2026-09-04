# Five-term progressions and pure cubic fields

## Main theorem

For nonzero terms of a rational five-term arithmetic progression, after a
single common rational scaling, the maximum number that can be cubes in one
common nontrivial pure cubic field is exactly four:

`R^times_(3,1)(5) = 4`.

The upper bound uses the Kummer kernel, 25 colour orbits, and finite-field
obstructions for all 60 local models. The lower bound is witnessed by
`(-3,-1,1,3,5)` over `Q(cuberoot(3))` with the normalization stated in the
paper.

The result does not classify all four-hit progressions. Of the original 31
open colour/position models, six have proved positive-rank infinite families
and one further model has a rigorously verified nondegenerate point. Thus
seven are closed for existence and 24 remain open. The unreviewed rank-zero
quotient notes from Round 11 are not included in this count or in the
manuscript's theorems.

The prior-art search is evidence of a careful search, not a proof of priority.
Its status is HIGH-CAUTION: no equivalent construction was located in the
accessible sources, while MathSciNet authentication, a forward-citation chain,
and full-text equation searches remain incomplete. Gonzalez-Jimenez--Xarles
(2013) is a direct methodological precedent for Kummer types, scaling,
reversal, curve reduction, and local solubility in the quadratic five-squares
setting. `NEXT_CUBE_MATH_NOVELTY_AUDIT.md` and
`ROUND_12_CUBE_NOVELTY_AUDIT.md` record the claim boundary. Draft
journal-facing prose is collected in `submission/`.
The requested author is Codex (GPT-5.6-sol); no affiliation, ORCID,
corresponding-author address, or actual submission is asserted.

## Four-hit extension

The first six closed models have infinite families. Four arise from
`2X^3-3Y^3+Z^3=0`:

- `((0,1,3,4),0001)`;
- `((0,1,2,3),0010)`;
- `((0,1,2,3),0100)`;
- `((0,1,2,4),0111)`.

The second positive-rank cubic `3X^3-4Y^3+Z^3=0` supplies

- `((0,1,2,4),0010)`;
- `((0,1,3,4),0010)`.

The seventh existence closure is `((0,1,2,4),0102)`. Its genus-four curve is

`(X^3+Y^3)(2Y^3-X^3)=2W^3`.

The point `(X:Y:W)=(2:1:-3)` yields the integer AP
`(64,36,8,-20,-48)` over `Q(cuberoot(6))`. The natural quotient
`v^2=u^3+9` contains the certified non-torsion image `(6,15)`. This proves
existence in the seventh model, not infinitely many rational points on the
genus-four source.

See `PAPER_CUBE_FOURHIT_EXISTENCE_ROUND_11.md` and the exact script,
certificate, and independent test in `code/`.

Complete mathematical check (42 tests):

```powershell
python -m unittest discover -s code -p "*_test.py" -v
```
