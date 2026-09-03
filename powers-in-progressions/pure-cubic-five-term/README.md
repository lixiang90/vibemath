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

The result does not classify all four-hit progressions; 31 finite
colour/position models remain.  The prior-art search is evidence of a careful
search, not a proof of novelty.  `NEXT_CUBE_MATH_NOVELTY_AUDIT.md` gives the
current claim-by-claim correctness and prior-art audit.

Minimal check:

```powershell
Set-Location code
python -m unittest -v PAPER_CUBE_KUMMER5_test.py
```
