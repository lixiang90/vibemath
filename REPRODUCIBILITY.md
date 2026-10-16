# Reproducibility

Python computations were last checked with Python 3.14.5 and SymPy 1.14.0.
The layouts separate code, certificates, and tests for reading.  Run the
self-contained verification entry point from the repository root:

```powershell
python tools/run_all_checks.py
```

It stages ephemeral flat copies when historical programs expect their evidence
files beside the source; the temporary directories are automatically removed.

PDFs are reference renderings.  Rebuilding a PDF may require TeX Live and the
packages imported by its source.  Generated LaTeX auxiliary files must remain
untracked.

The four-tree orchard note has a focused exact-arithmetic check at
`incidence-geometry/four-tree-orchard/tests/test_verify_construction.py`; it is
also included in `tools/run_all_checks.py`.  Its English and Chinese PDFs are
built from the corresponding sources in the project's `paper/` directory.

Certificate hashes in historical supplement manifests refer to the original
research workspace paths.  The repository-wide `MANIFEST.sha256` records the
actual public-tree bytes and is the current integrity index.

## Sun's ninety-dollar series for $1/\pi$

The `ramanujan-series/sun90-identity` project has a separate complete
verification entry point. Its computational dependencies are Python >= 3.9
and SymPy 1.14.0. From the repository root, run:

```powershell
python -m pip install sympy==1.14.0
python ramanujan-series/sun90-identity/verify.py
```

This runs the exact eta/Sturm parametrization, differential-algebra bridge,
degree-seven modular-equation Sturm certificate, and CM branch checks. The
combined record is
`ramanujan-series/sun90-identity/reproducibility/full_verification.json`.
The default command leaves tracked files unchanged. Add
`--report reproducibility/full_verification.json` to regenerate that record.
This project is also included in `python tools/run_all_checks.py`.
The paper explains the standard eta-quotient, Sturm, and Fricke theory and
the analytic arguments accompanying the computational identities.

The committed PDF is `ramanujan-series/sun90-identity/paper/main.pdf`.
To rebuild it, use XeLaTeX with the packages imported by `main.tex`,
including `ctex` and its Fandol fonts. For example, from the repository root:

```powershell
cd ramanujan-series/sun90-identity/paper
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The second pass resolves cross-references. Keep the generated `.aux`, `.log`,
and other LaTeX build files untracked. Compilation and the exact program
checks support reproducibility; external peer review, first-proof priority,
and the prize decision remain unconfirmed.
