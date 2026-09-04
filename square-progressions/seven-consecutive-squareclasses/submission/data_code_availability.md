# Data and code availability

## Proposed statement

The exact generators, JSON certificates, and regression tests supporting the
finite classification are collected in supplement release
`paper-square-supplement-v0.10.1`.  Its root file is
`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json`, SHA-256
`deb3eade7c9f25c6e0c8da019f21f7a0943bdd50fcf263f7add6ed8b3ed0309e`.
The manifest lists 38 bound artifacts, their byte lengths and SHA-256 values,
the Python and SymPy versions, the reproduction commands, and the mathematical
claim boundary.

The repository-level `MANIFEST.sha256` predates the current Round11 manuscript,
supplement, audits, and submission prose.  It must not be cited as binding the
current working bytes until a final release freeze regenerates it.

The current public working archive is
<https://github.com/lixiang90/vibemath/tree/main/square-progressions/seven-consecutive-squareclasses>.
The repository root manifest currently binds only its older Round10 snapshot.
A regenerated manifest plus a versioned release or preservation-service DOI
is still required before journal submission if the selected journal requires
an immutable locator.

The historical supplement manifest still records its original local-release
state and must not be reinterpreted retroactively.  For a submission release,
freeze the current public payload, insert the immutable locator, and perform a
download-and-hash check.  If any artifact changes, create a new semantic
version and do not reuse the v0.10.1 supplement hash.

The supplement contains no confidential, personal, or third-party dataset.
