# Reproducibility

Python computations were last checked with Python 3.14.5 and SymPy 1.14.0.
Run tests from the paper directory specified in its `README.md`.  The layouts
separate code, certificates, and tests for reading; the project-specific
verification script stages an ephemeral flat copy when historical programs
expect their evidence files beside the source.

PDFs are reference renderings.  Rebuilding a PDF may require TeX Live and the
packages imported by its source.  Generated LaTeX auxiliary files must remain
untracked.

Certificate hashes in historical supplement manifests refer to the original
research workspace paths.  The repository-wide `MANIFEST.sha256` records the
actual public-tree bytes and is the current integrity index.

