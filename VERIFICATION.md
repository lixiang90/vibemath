# Verification snapshot

Date: 2026-09-03

The organized public source tree was checked again after the mathematical and
novelty audit.

- 70 tests passed for the seven-consecutive-squareclass project, including the
  exact mask-99 and mask-51 integral-point gates.
- 33 tests passed for the number-field magic-square project.
- 23 tests passed for the pure-cubic five-term project, including two distinct
  positive-rank four-hit branches.
- 14 tests passed for the six-term fourth-power project.
- 8 tests passed for the C29 simultaneous-torsion project.
- 50 tests passed for the Campbell two-isogeny Selmer project, including the
  exact minimal-model and conductor audit.
- Total: 198 passing tests, 0 failures.
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

## Clean-clone reproduction

The seventh-round baseline commit
`559e89364b6e5c5e38e60d7b55b43ebb56e40409` was cloned locally with
`--no-hardlinks` into a disposable directory and checked out detached.  In that
clone, all 183 then-current tests passed and all three PDFs rebuilt with no matched final-log
warning.  `pdftotext` output was byte-identical before and after each rebuild.
The versioned JSON result and full combined stdout/stderr are in
`research-program/three-paper-project/reproduction/`.

This is an internal clean-environment check, not an external independent
reproduction or a substitute for human review of the proofs.
