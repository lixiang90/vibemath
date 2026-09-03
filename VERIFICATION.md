# Verification snapshot

Date: 2026-09-03

The organized public source tree was checked again after the mathematical and
novelty audit.

- 63 tests passed for the seven-consecutive-squareclass project, including the
  exact mask-99 integral-point gate.
- 33 tests passed for the number-field magic-square project.
- 16 tests passed for the pure-cubic five-term project, including the
  positive-rank four-hit branch.
- 14 tests passed for the six-term fourth-power project.
- 8 tests passed for the C29 simultaneous-torsion project.
- 49 tests passed for the Campbell two-isogeny Selmer project, including the
  exact minimal-model and conductor audit.
- Total: 183 passing tests, 0 failures.
- The public tree contained no LaTeX auxiliaries, caches, temporary build
  directories, archive ZIPs, or duplicate build-output directories.
- A targeted scan found no environment files, private-key files, GitHub tokens,
  AWS access-key identifiers, or obvious password/API-key assignments.

The tests establish consistency of the symbolic identities, finite
enumerations, and stored certificates that they assert.  They do not turn a
bounded search into a proof, establish novelty by themselves, or promote the
explicitly withdrawn Cassels--Tate expression.

The exact repository-level command used was:

```powershell
python tools/run_all_checks.py
```

The entry point uses temporary directories for historical flat-layout programs
and runs the Campbell checks directly against their organized public paths.
It creates no build product in the repository.
