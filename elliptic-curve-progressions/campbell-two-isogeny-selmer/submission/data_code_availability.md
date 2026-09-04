# Data and code availability

Current public working archive:

<https://github.com/lixiang90/vibemath/tree/main/elliptic-curve-progressions/campbell-two-isogeny-selmer>

The historical `reproducibility/supplement-manifest-v0.6.1.json` identifies
the original finite evidence release and must not be interpreted as claiming
that the bundled Magma inputs were run. The repository-root manifest still
records Round10 bytes and is not a current Round11 inventory; it must be
regenerated only when the final Round11 payload is frozen.

Round 11 adds:

- `code/NEXT_ELLIPTIC_ROUND_11.py`;
- `code/NEXT_ELLIPTIC_ROUND_11_test.py`;
- `certificates/round11_isogeny_selmer_audit.json`;
- `NEXT_ELLIPTIC_ROUND_11_REPORT.md`.

These artifacts verify the isogeny and covering conventions, the exhaustive
support and place set, all 84 finite positive primitive witnesses, both exact
isogeny Selmer groups, and the rank upper bound. They do not prove an exact
rank, a full 2-Selmer group, a Cassels--Tate value, or a ninth rational point.

The complete current regression command, run from `code/`, is:

```powershell
python -W error -m unittest -q PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py test_same_m_local.py NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py NEXT_ELLIPTIC_ROUND_09_test.py NEXT_ELLIPTIC_ROUND_10_test.py NEXT_ELLIPTIC_ROUND_11_test.py
```

It passes 73 tests. The unexecuted Magma inputs remain explicitly ineligible
and have no transcript or software-binary hash. No independent second
elliptic-curve CAS is claimed. The GitHub `main` branch is a public working
archive, not a frozen journal deposit; no DOI or immutable preservation
identifier is asserted because no actual submission is requested.
