# Submission materials — Campbell two-isogeny theorem

Status: research/referee-readiness package, not an actual submission.  The sibling directories
hold the paper, exact programs, certificates, audits and reproducibility data;
this directory contains only editable submission prose.

The current public working copy is
<https://github.com/lixiang90/vibemath/tree/main/elliptic-curve-progressions/campbell-two-isogeny-selmer>.
The root `MANIFEST.sha256` may predate the current Round-11 working bytes and
is not the current byte inventory. A new manifest and frozen release remain
research-package tasks; no preservation DOI is asserted.

The paper proves only the finite results stated in
`../NEXT_ELLIPTIC_MATH_NOVELTY_AUDIT.md`.  It does not solve Campbell's ninth
point problem and contains no Cassels--Tate value.  The unexecuted candidate
inputs are ineligible evidence.  In particular, the new Round-09 theorem is a
complete local statement: either `Q_59` or `Q_71699` cuts the 32 E-side signed
support classes to the same 16, and the real condition leaves eight.  It does
not provide a global point or obstruction.  The audited host had no
independent second elliptic-curve CAS, and database non-matches are not
novelty evidence.
The Round-10 theorem gives independent valuation/residue/Hensel proofs that
the E'-side `Q_2` and `Q_3` conditions intersect in exactly the four Selmer
classes. Round 11 combines both uniform gates with the support and good-prime
lemmas and revalidates every positive bad-place witness, proving the exact
isogeny Selmer groups of dimensions 3 and 2 and the rank upper bound 3. It
does not decide a rational ninth point or the exact rank.

Current synchronized artifact status: 11-page `../paper/main.pdf`, 73 passing
regression tests, and PDF SHA-256
`9296C024822D7CD3670E1D04CCCFB328DA26EA4198DD2AAC8E0F0E99E9024E1F`.
The historical v0.6.1 supplement manifest predates the Round-10 files; a new
manifest/release freeze remains necessary before submission.

Contents: `abstract.txt`, `cover_letter.md`, `journal_shortlist.md`,
`author_contributions.md`, `data_code_availability.md`, `ai_disclosure.md`,
`limitations.md`, and `si_caption.md`.

The sole named author is Codex (GPT-5.6-sol). No affiliation, email, postal
address, ORCID, or external endorsement is asserted. Venue-policy adaptation
and actual transmission are deliberately outside scope.
