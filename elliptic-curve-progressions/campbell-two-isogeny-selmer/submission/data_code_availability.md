# Data and code availability

Current public working archive:

<https://github.com/lixiang90/vibemath/tree/main/elliptic-curve-progressions/campbell-two-isogeny-selmer>

The repository root `MANIFEST.sha256` binds the public bytes.  The historical
supplement manifest identifies the original finite evidence release; it must
not be interpreted as claiming that the unexecuted Magma inputs were run.
The later exact minimal-model and conductor certificate is stored under
`certificates/minimal_model_identity.json` and is bound by the repository-root
manifest.

Proposed statement after an immutable release or preservation deposit:

The exact generators, JSON certificates, and regression tests are identified
by `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json`, release
`paper-elliptic-campbell-supplement-v0.6.1`. The manifest records each file's
byte length, SHA-256, role, evidence eligibility, runtime, and reproduction
commands. Public archive: <<DOI/URL>>.

Until that immutable locator is independently download-checked, the GitHub
`main` branch is a public working archive rather than a frozen journal deposit.
The unexecuted Magma inputs are explicitly ineligible and have no transcript or
software-binary hash.
