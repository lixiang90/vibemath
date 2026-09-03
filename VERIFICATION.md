# Verification snapshot

Date: 2026-09-03

The allowlisted source tree was checked before the first Git commit.

- 108 tests passed for the three internally accepted paper evidence chains.
- 55 tests passed for the number-field magic-square, six-term fourth-power,
  and C29 long-term projects.
- Total: 163 passing tests, 0 failures.
- The public tree contained no LaTeX auxiliaries, caches, temporary build
  directories, archive ZIPs, or duplicate build-output directories.
- A targeted scan found no environment files, private-key files, GitHub tokens,
  AWS access-key identifiers, or obvious password/API-key assignments.

The tests establish consistency of the symbolic identities, finite
enumerations, and stored certificates that they assert.  They do not turn a
bounded search into a proof, establish novelty by themselves, or promote the
explicitly withdrawn Cassels--Tate expression.

The exact commands used were:

```powershell
python -m unittest -v STUDENT_SQUARE_ROUND_02_test_patterns.py STUDENT_SQUARE_ROUND_03_test.py STUDENT_SQUARE_ROUND_04_test.py PAPER_SQUARE_SAFE_test.py PAPER_SQUARE_MASK77_test.py PAPER_SQUARE_NEXT_GATE_test.py PAPER_SQUARE_MASK108_test.py PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py PAPER_CUBE_KUMMER5_test.py PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST_test.py

python -m unittest -v test_magic_square_search.py test_quadratic_elliptic_search.py test_number_field_magic.py test_bremner_j1728.py test_campbell_j1728.py test_spearman_kummer.py test_spearman_parameters.py test_bst_number_field.py PAPER_CUBE_P6_test_gate.py PAPER_CUBE_P6_test_maps.py PAPER_CUBE_C29_test_model.py
```

They were run from the parent research workspace, where the historical flat
file topology expected by the programs is preserved.  The public copies are
byte-for-byte copies indexed by `MANIFEST.sha256`.

