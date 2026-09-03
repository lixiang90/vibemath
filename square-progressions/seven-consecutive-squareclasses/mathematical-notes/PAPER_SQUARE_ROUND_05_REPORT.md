# Square line, round 5: manuscript repair and mask 108

Date: 2026-09-03

## Outcome

All mathematical blocking/major points in
`PAPER_SQUARE_MANUSCRIPT_REVIEW_CUBE_04.md` have been repaired in the source
and local supplement.  A new elementary integral-point theorem closes mask
108, so the strict chain is now

\[
651\to343\to284\to98\to54\to35\to23.
\]

This still does **not** decide `R_2(7)`: the final 23 patterns are necessary
candidates, not proved realizations.

## 1. Manuscript repairs

### Definition and use of `R_1(6)=5`

The paper now defines

\[
R_s(N)=\max_{a,q,V}\#\{0\le i<N:[a+qi]\in V\},
\]

with `q != 0` and `dim_F2(V)=s`.  Xarles's exact result is cited as Theorem 1,
`S(2)=6`: a nonconstant progression over a quadratic field cannot have six
square terms.  This gives the upper bound for `R_1(6)`.  The progression

`49,169,289,409,529,649`

has its first five terms square over `Q(sqrt(409))`, giving the lower bound.
The paper explicitly explains the common-scaling passage from affine rank at
most one to this linear-subspace formulation.

### Kummer kernel

The common-scaling proposition now proves

\[
\ker(\mathbb Q^*/\mathbb Q^{*2}\to L^*/L^{*2})
=\langle[D_1],[D_2]\rangle
\]

by observing that a killed rational class produces a quadratic subfield
`Q(sqrt(r))` of `L`, then using the three quadratic subfields of a
biquadratic extension.  Degree-one/two degeneracies are handled explicitly.

### Summary theorem and candidate table

The new summary theorem states exactly that any nondegenerate integral
seven-term affine-rank-at-most-two instance must have one of 23 canonical
equality partitions.  The proof explains why the actual rank is exactly two,
so the labels are the true squareclass blocks.  A table gives every final ID
and restricted-growth word and states the ordering convention.  It also says
that realizability and `R_2(7)` remain open.

### Bibliography

The Bremner--Siksek entry and prior-art note now read **cubic fields**,
International Journal of Number Theory 12 (2016), 1409--1414.  The Xarles
entry now includes DOI `10.1016/j.jnt.2011.07.010`, and the misleading
`MassPethoTzanakis` key was renamed `MasserRickert`.

## 2. New theorem: mask 108

For

\[
H_{108}:y^2=(t+2)(t+3)(t+5)(t+6),
\]

put

\[
A=(t+2)(t+6),\qquad B=(t+3)(t+5)=A+3.
\]

Outside `-6 <= t <= -2`, both factors are positive and `gcd(A,B)|3`.
Thus a square product has a common positive squarefree kernel `d=1` or `3`.

- `d=1`: `V^2-U^2=3`; the factor pair `(1,3)` gives `(U,V)=(1,2)`,
  but `A=1` means `(t+4)^2=5`, impossible modulo 8.
- `d=3`: `V^2-U^2=1`; the factor pair `(1,1)` forces `U=0`, contrary
  to positivity.
- Exact evaluation of the five middle integers completes the list.

Hence

\[
H_{108}(\mathbb Z)={(-6,0),(-5,0),(-4,\pm2),(-3,0),(-2,0)\}.
\]

All parameters are degenerate in the original seven terms.  Mask 108 occurs
in exactly 12 of the 35 input rows, excluding IDs

`32,70,71,84,193,195,197,229,237,248,256,264`.

The final 23 IDs are

`9,12,26,31,33,43,50,59,83,134,188,210,212,214,230,251,257,266,268,271,276,281,283`.

Files: `PAPER_SQUARE_MASK108.py`, `_test.py`, `_CERTIFICATE.json`, and
`_REPORT.md`.  Certificate SHA-256:
`BB04A152389EAF93F5293714CFAE2EDA557E3C2DABDCFD65EFCC3365CFC27595`.

## 3. Supplement manifest

`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json` is the locator for release
`paper-square-supplement-v0.5.0`.  It records 23 core generator, certificate
and test files with byte lengths, SHA-256 values, roles and
`mathematical_evidence_eligible`; it also records Python/SymPy versions,
commands, semantic version and claim boundary.

Manifest SHA-256:
`6004AFC5334BBEA62969640079CAD80764D2938D73B6FD62A85ABC2249794588`.
The paper cites both filename and hash.

The release is deliberately marked
`LOCAL_RELEASE_CANDIDATE_NOT_PUBLICLY_ARCHIVED`, with null archive URL and an
explicit note that this workspace is not a Git repository.  Thus the local
auditability blocker is removed, but public DOI/URL deposit remains a genuine
administrative submission blocker; the report does not pretend otherwise.

## 4. Verification and build

The complete dependency-closure command passed **57/57 tests**:

- Round02: 7;
- Round03: 7;
- Round04: 9;
- SAFE: 10;
- mask77: 10;
- mask102/next gate: 5;
- mask108: 5;
- supplement manifest: 4.

TeX Live 2022 `latexmk` completed the BibTeX/pdflatex chain.  The result is a
7-page PDF, 255867 bytes.  Final `main.log`/`build.log` has no match for
`undefined`, `Warning`, `Overfull`, or `Underfull`.

- `main.tex` SHA-256:
  `B8006375C8361AC212BEEAE1415E6EDF9F5123C668078E97D446B033D6E102CE`;
- `main.pdf` SHA-256:
  `8119310571D37943475E1BCA6417409C512679B146E7608D312B3966EA5586AD`;
- `build.log` SHA-256:
  `8DF1814172DF96096C340AC599932AB5E047DEC7226B65CF58FC6C240B75D6BB`.

## 5. Submission status

The mathematical and reproducibility issues identified by the cross-review
are fixed in the local manuscript.  Remaining blockers are external rather
than mathematical:

1. freeze the exact manifest payload in a public archival release and insert
   its DOI/URL;
2. replace “Working draft” author metadata with the actual authorship and
   target-journal format;
3. obtain a fresh independent proofread of the new summary theorem and mask
   108 gate.

Until the archive step is done, status is **mathematically submission-ready
candidate, not yet an externally reproducible submission package**.

