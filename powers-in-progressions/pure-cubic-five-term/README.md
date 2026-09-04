# Five-term progressions and pure cubic fields

## Main theorem

For nonzero terms of a rational five-term arithmetic progression, after a
single common rational scaling, the maximum number that can be cubes in one
common nontrivial pure cubic field is exactly four:

`R^times_(3,1)(5) = 4`.

The upper bound uses the Kummer kernel, 25 colour orbits, and finite-field
obstructions for all 60 local models.  The lower bound is witnessed by
`(-3,-1,1,3,5)` over `Q(cuberoot(3))` with the normalization stated in the
paper.

The result does not classify all four-hit progressions.  Of the original 31
open colour/position models, six branches described below are now proved to
have positive rank; the other 25 remain open.  The prior-art search is
evidence of a careful search, not a proof of novelty.
`NEXT_CUBE_MATH_NOVELTY_AUDIT.md` gives the claim-by-claim correctness and
prior-art audit of the exact maximum.

Draft journal-facing prose is collected in `submission/`; author identity,
funding, conflicts, venue approval, and an immutable release locator remain
human-supplied gates.

## Four-hit extension

Six of the original 31 four-hit models are now proved to have positive rank.
The first four are
`((0,1,3,4),0001)`, `((0,1,2,3),0010)`, `((0,1,2,3),0100)`, and
`((0,1,2,4),0111)`.  All arise from the smooth diagonal cubic
`2X^3-3Y^3+Z^3=0`, which supplies infinitely many inequivalent four-hit
progressions in each model.  The earlier displayed AP
`(64,1,-62,-125,-188)` realizes them over `Q(cuberoot(188))` and
`Q(cuberoot(62))` for the first two.  The reversed pair
`(-125,-62,1,64,127)` and `(127,64,1,-62,-125)` realizes the latter two over
`Q(cuberoot(62))` and `Q(cuberoot(127))`.  See
`PAPER_CUBE_FOURHIT_0001_ROUND_07.md` and
`PAPER_CUBE_FOURHIT_0010_ROUND_08.md`, together with the Round09 report; the
second positive-rank cubic `3X^3-4Y^3+Z^3=0` supplies the two further models
`((0,1,2,4),0010)` and `((0,1,3,4),0010)`.  Its first AP is
`(125,8,-109,-226,-343)`, over `Q(cuberoot(109))` and
`Q(cuberoot(226))`, respectively.  See
`PAPER_CUBE_FOURHIT_3PLUS1_ROUND_10.md`; the other 25 models remain open.

Complete mathematical check (36 tests):

```powershell
python -m unittest discover -s code -p "*_test.py" -v
```
