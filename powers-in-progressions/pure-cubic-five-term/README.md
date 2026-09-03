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
open colour/position models, the `0001` branch described below is now proved
to have positive rank; the other 30 remain open.  The prior-art search is
evidence of a careful search, not a proof of novelty.
`NEXT_CUBE_MATH_NOVELTY_AUDIT.md` gives the claim-by-claim correctness and
prior-art audit of the exact maximum.

Draft journal-facing prose is collected in `submission/`; author identity,
funding, conflicts, venue approval, and an immutable release locator remain
human-supplied gates.

## Four-hit extension

One of the original 31 four-hit models, positions `(0,1,3,4)` with colours
`0001`, is now proved to have positive rank.  The smooth diagonal cubic
`2X^3-3Y^3+Z^3=0` therefore supplies infinitely many inequivalent four-hit
progressions.  The smallest displayed new example is
`(64,1,-62,-125,-188)` over `Q(cuberoot(188))`.  See
`PAPER_CUBE_FOURHIT_0001_ROUND_07.md`; the other 30 models remain open.

Complete mathematical check (16 tests):

```powershell
python -m unittest discover -s code -p "*_test.py" -v
```
