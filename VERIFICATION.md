# Verification snapshot

Date: 2026-09-04

The organized public source tree was checked again after the mathematical and
novelty audit.

- 96 tests passed for the seven-consecutive-squareclass project, including the
  exact mask-99, mask-51, mask-90, mask-54, and Round11 mask-85
  integral-point gates.
- 33 tests passed for the number-field magic-square project.
- 42 tests passed for the pure-cubic five-term project, including the exact
  Round09 clustering, six distinct positive-rank four-hit models, and the
  Round11 strict-existence certificate for a seventh model.
- 14 tests passed for the six-term fourth-power project.
- 8 tests passed for the C29 simultaneous-torsion project.
- 73 tests passed for the Campbell two-isogeny Selmer project, including the
  exact minimal-model/conductor audit, the Round09 `E`-side two-place local
  gate, the Round10 `E'`-side `Q_2`/`Q_3` gate, and the Round11 support/place
  bridge proving both exact isogeny Selmer groups and only `rank <= 3`.
- Total: 266 passing tests, 0 failures.
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

These working-tree checks extend the completed Round11 clean-clone reproduction
of source commit `20bb94753801907b46d41db611ab18c4cd9f9a10`.  At the Round11
evidence-recording freeze, the repository-root `MANIFEST.sha256` was
regenerated after adding the durable JSON/log evidence. Its 270 unique rows
were then re-read; every path existed, every SHA-256 matched, and the listed
path set equalled the frozen repository file set. The source commit, not the
later evidence-recording commit, is the tree tested by that cold clone.

The current Round12 working tree adds primary-source novelty audits and
cross-reviews for all three papers.  Each cross-review passes under its stated
claim boundary: database and citation-chain gaps remain disclosed, no search
non-hit is used as priority evidence, and the Campbell independent second-CAS
protocol remains unexecuted.  Round12 is not yet frozen or cold-reproduced;
the root manifest is therefore intentionally pending regeneration at the
Round12 freeze.

The current squareclasses, pure-cubic, and Campbell PDF files have respectively
12, 10, and 11 pages, with file SHA-256 values
`0312007e2125fe27b6ab358c0b4f81b15d0f689e05e62743de61b47b945b0ac1`,
`253f2403c26d13d62b7f758dc9188ce5577cfe82d54d425beffe26404684cb4f`, and
`1b27cc0331736af6b2078d4b0ddb21d2e21e3dc97403eb8235a2ae1f9a2a40f3`.
All three PDF metadata records name `Codex (GPT-5.6-sol)` as author.

## Clean-clone reproduction

The seventh-round baseline commit
`559e89364b6e5c5e38e60d7b55b43ebb56e40409` remains as a historical record.  It
was cloned locally with `--no-hardlinks` into a disposable detached checkout;
all 183 then-current tests passed and all three PDFs rebuilt with no matched
final-log warning or change in their extracted text.

The same protocol was then run successfully on the clean eighth-round source
commit `4a8dae3dbc04712991783053e97b14b2d073964a`.  The source worktree was clean,
all 198 tests passed, and the rebuilt squareclasses, pure-cubic and Campbell
papers had respectively 10, 7 and 9 pages.  Every final log had an empty
matched-warning list.  The committed/rebuilt `pdftotext` SHA-256 pairs were:

| paper | committed text SHA-256 | rebuilt text SHA-256 |
|---|---|---|
| squareclasses | `00ff150a899afd2c477f953c5e268d6b2a28429b405bc961bcbd5cbe12646b07` | `00ff150a899afd2c477f953c5e268d6b2a28429b405bc961bcbd5cbe12646b07` |
| pure cubic | `83f8f4bb14c275015e2d4e83d6ef42671abad7ae641bbe449fd6cb988907fbdc` | `83f8f4bb14c275015e2d4e83d6ef42671abad7ae641bbe449fd6cb988907fbdc` |
| Campbell Selmer | `35134ec00e087ea53929d95bf8c71c33fe4dea9e80c0df924fe57006979fd2b9` | `35134ec00e087ea53929d95bf8c71c33fe4dea9e80c0df924fe57006979fd2b9` |

The eighth-round versioned result is
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_4a8dae3dbc04.json`;
its complete combined stdout/stderr is the adjacent `.log` file.

The same protocol then succeeded on the clean Round09 commit
`85eb55b49f9f80e05a7d890fec7cc289083b802b`.  The source was clean; all 218
tests passed in groups `78,33,29,14,8,56`; the three PDFs had 10, 7 and 10
pages; every final-log warning list was empty; and each committed/rebuilt
`pdftotext` SHA-256 pair was identical:

| paper | committed text SHA-256 | rebuilt text SHA-256 |
|---|---|---|
| squareclasses | `f945d398d6169e5e2ad1009d1b6f9ef0f9150f89c72a5fb67a4b37ea6bdfa7a4` | `f945d398d6169e5e2ad1009d1b6f9ef0f9150f89c72a5fb67a4b37ea6bdfa7a4` |
| pure cubic | `6ca420753b087ed24bbf675c8c5f8069a9dfc54428213b4b455503120fbfbbf4` | `6ca420753b087ed24bbf675c8c5f8069a9dfc54428213b4b455503120fbfbbf4` |
| Campbell Selmer | `b1413392f725f042a3809bb4d7c3f709453a11e7024a2ed0faaa23033b6fac98` | `b1413392f725f042a3809bb4d7c3f709453a11e7024a2ed0faaa23033b6fac98` |

The Round09 records are
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.json`
and `research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.log`; the combined log SHA-256 is
`6bf7915a75983763fa8a98d096e8fbd2f6a7ee258a57575f0864912b56be0c00`.

Finally, the protocol succeeded on the clean Round10 commit
`ccc4c4be6562534f25b18817c6c4773bb0cf0cc4`.  The source was clean; all 243
tests passed in groups `87,33,36,14,8,65`; the PDFs had 11, 8 and 11 pages;
every final-log warning list was empty; and each committed/rebuilt
`pdftotext` SHA-256 pair was identical:

| paper | committed text SHA-256 | rebuilt text SHA-256 |
|---|---|---|
| squareclasses | `97b9dc6242ebecc2e3a0a987c0265cd97eaf7a69f5620b7f9e64590d7892992e` | `97b9dc6242ebecc2e3a0a987c0265cd97eaf7a69f5620b7f9e64590d7892992e` |
| pure cubic | `5619e94f4f937b31f7a778f18862e1aa2024adf4a2ccebb10658c6c858250bb1` | `5619e94f4f937b31f7a778f18862e1aa2024adf4a2ccebb10658c6c858250bb1` |
| Campbell Selmer | `18a684b57169564f314ffeedaffb4da15ad9be3344a8be792f7da54a6502aa8d` | `18a684b57169564f314ffeedaffb4da15ad9be3344a8be792f7da54a6502aa8d` |

The Round10 records are
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_ccc4c4be6562.json`
and the adjacent `.log`; the combined log SHA-256 is
`72486507e0ebfafe8ba4b4a2415bcb19056a4e23d392d223548629bab6e59645`.

The protocol then succeeded on the clean Round11 source commit
`20bb94753801907b46d41db611ab18c4cd9f9a10`. The source was clean; all 266
tests passed in groups `96,33,42,14,8,73`; the PDFs had 11, 9 and 11 pages;
every final-log warning-pattern list was empty; and each committed/rebuilt
`pdftotext` SHA-256 pair was identical:

| paper | committed text SHA-256 | rebuilt text SHA-256 |
|---|---|---|
| squareclasses | `5aca3c9cc84f52121a501a3f08640d1aa806a0154e2bb1429cd0e977e6659f9d` | `5aca3c9cc84f52121a501a3f08640d1aa806a0154e2bb1429cd0e977e6659f9d` |
| pure cubic | `59cdb61632ddc7273a3733f562206a23e6bec2ddca0dbfd2ffc3e200effb9fbe` | `59cdb61632ddc7273a3733f562206a23e6bec2ddca0dbfd2ffc3e200effb9fbe` |
| Campbell Selmer | `7616879662139ea87f2fc1d992aa5e7fafff45ea7057dc79d6ad4181a9752b23` | `7616879662139ea87f2fc1d992aa5e7fafff45ea7057dc79d6ad4181a9752b23` |

The Round11 records are
`research-program/three-paper-project/reproduction/INTERNAL_COLD_REPRODUCTION_20bb94753801.json`
and the adjacent `.log`. The JSON SHA-256 is
`ab12184073c6c53d90d306caa701eb1476dbf1e02c944eb7c84bfa42fdf6c1c4`;
the combined log SHA-256 is
`584cb911399d45d666b8cc7a1123d30650f478feefe1fbd810bd13723e9dfe46`.

This is an internal clean-environment check, not an external independent
reproduction or a substitute for human review of the proofs.
