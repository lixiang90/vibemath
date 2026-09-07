# Four-tree orchard construction

## Proved

For every integer `n >= 28`, the four-supporting-line construction in
`paper/main.tex` produces `n` points with rational coordinates and

`floor((n^2 + 12) / 28)`

distinct lines containing exactly four selected points. A common dilation
turns all coordinates into integers, so this is a lower bound for OEIS
[A172992](https://oeis.org/A172992).

The parameter

`v = ceil((s - d - 1) / 2)`

is essential. Replacing `d` by `c` makes the general claim false; for example,
the mistyped construction gives 29 rather than 30 guaranteed lines at `n=29`.

The construction gives 124 lines for `n=59` and 129 lines for `n=60`. At the
time of the source check (2026-09-06), the OEIS page listed 123 and 126. Thus
the rigorous claims are `A172992(59) >= 124` and `A172992(60) >= 129`, not
optimality or equality with the unknown maxima.

## Files

- `paper/main.tex` and `paper/main.pdf`: two-page English note.
- `paper/main-zh.tex` and `paper/main-zh.pdf`: two-page Chinese version.
- `code/verify_construction.py`: exact integer/rational implementation.
- `tests/test_verify_construction.py`: regression checks for the count,
  special cases, typo diagnostic, collinearity, and integer dilation.

## Reproduce

From this directory, run:

```powershell
python -m unittest -v tests/test_verify_construction.py
xelatex -interaction=nonstopmode -halt-on-error -output-directory=paper paper/main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=paper paper/main-zh.tex
```

The residue-class reduction in the paper is the proof of the closed count.
The executable checks are independent regression evidence and are not
presented as a replacement for that proof.
