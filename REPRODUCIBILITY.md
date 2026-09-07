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
