# Data and code availability

## Proposed statement

The exact generators, JSON certificates, and regression tests supporting the
finite classification are collected in supplement release
`paper-square-supplement-v0.9.0`.  Its root file is
`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json`, SHA-256
`e218f10e116ec7732c9d369384bc06156195ea4cc62165cd3107583b03546c6d`.
The manifest lists 35 bound artifacts, their byte lengths and SHA-256 values,
the Python and SymPy versions, the reproduction commands, and the mathematical
claim boundary.

The repository-level `MANIFEST.sha256` binds the manuscript, bibliography,
reference PDF, supplement files, audits and submission prose currently in the
public working tree.

The current public working archive is
<https://github.com/lixiang90/vibemath/tree/main/square-progressions/seven-consecutive-squareclasses>.
The repository root `MANIFEST.sha256` binds the public bytes.  A versioned
release or preservation-service DOI is still required before journal
submission if the selected journal requires an immutable locator.

The historical supplement manifest still records its original local-release
state and must not be reinterpreted retroactively.  For a submission release,
freeze the current public payload, insert the immutable locator, and perform a
download-and-hash check.  If any artifact changes, create a new semantic
version and do not reuse the v0.9.0 supplement hash.

The supplement contains no confidential, personal, or third-party dataset.
<<HUMAN AUTHOR TO CONFIRM THIS SENTENCE BEFORE SUBMISSION>>.
