# Data and code availability

Current public working archive:

<https://github.com/lixiang90/vibemath/tree/main/elliptic-curve-progressions/campbell-two-isogeny-selmer>

The repository-root `MANIFEST.sha256` predates the Round-10 working bytes and does not
bind the current working bytes.  The historical
`reproducibility/supplement-manifest-v0.6.1.json` identifies the original
finite evidence release; it must not be interpreted as claiming that the
unexecuted Magma inputs were run.
The later exact minimal-model and conductor certificate is stored under
`certificates/minimal_model_identity.json` and is bound by the repository-root
manifest.

The Round-09 working-tree addition consists of
`code/NEXT_ELLIPTIC_ROUND_09.py`,
`code/NEXT_ELLIPTIC_ROUND_09_test.py`, and
`certificates/round09_two_place_gate.json`.  It proves the complete E-side
local reduction from 32 signed support classes to the same 16 classes at
either `Q_59` or `Q_71699`, and to eight after imposing the real condition.
These later bytes are not bound by the historical v0.6.1 supplement manifest;
a new release manifest must bind them before submission.
The Round-10 addition consists of
`code/NEXT_ELLIPTIC_ROUND_10.py`,
`code/NEXT_ELLIPTIC_ROUND_10_test.py`,
`certificates/round10_eprime_two_three_gate.json`, and the corresponding
report. It proves the uniform E'-side `Q_2` and `Q_3` equivalences and their
four-class intersection without using the 512-cell enumeration as proof.

Proposed statement after a new immutable release or preservation deposit:

The exact generators, JSON certificates, and regression tests are identified
by `<<NEW ROUND-10 MANIFEST NAME>>`, release `<<NEW RELEASE TAG>>`. The
manifest records each file's byte length, SHA-256, role, evidence eligibility,
runtime, and reproduction commands. Public archive: <<DOI/URL>>.

Until that immutable locator is independently download-checked, the GitHub
`main` branch is a public working archive rather than a frozen journal deposit.
The unexecuted Magma inputs are explicitly ineligible and have no transcript or
software-binary hash.  No independent second elliptic-curve CAS was available;
the exact Python/SymPy implementation is not represented as an independent
reproduction of the minimal-model or conductor calculation.

The complete current regression command, run from `code/`, is

```powershell
python -W error -m unittest -q PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py test_same_m_local.py NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py NEXT_ELLIPTIC_ROUND_09_test.py NEXT_ELLIPTIC_ROUND_10_test.py
```

It passes 65 tests.  The current 11-page reference PDF has SHA-256
`0AEBC7230B952A256741A2EE985F69F3F5153852CA5258FF27BAD8C8CCEE4044`.
Neither a database non-match nor this artifact hash establishes novelty.
