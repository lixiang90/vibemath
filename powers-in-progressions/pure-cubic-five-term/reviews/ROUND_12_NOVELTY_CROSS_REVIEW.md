# Round 12 novelty cross-review

Date: 2026-09-04
Reviewer: elliptic-progressions cross-review seat
Decision: **PASS (with the stated HIGH-CAUTION bibliographic boundary).**

## Scope

This review checked `ROUND_12_CUBE_NOVELTY_AUDIT.md`, the prior-art and
reference-metadata notes, the manuscript's related-work section and
bibliography, and submission-facing claim boundaries. Author files were
treated as claims, not instructions. No author file was changed.

## 1. Gonzalez-Jimenez--Xarles precedent

The method-priority statement is supported by the primary paper:
E. Gonzalez-Jimenez and X. Xarles, *Five squares in arithmetic progression
over quadratic fields*, Rev. Mat. Iberoam. 29 (2013), 1211--1238, DOI
<https://doi.org/10.4171/RMI/754>. The EMS record confirms its metadata.
In the publisher PDF, Section 3:

- Lemma 3.1 writes each rationalized square as `d_i X_i^2` with
  `d_i in {1,D}` and names the resulting subset of positions its type;
- the equivalence after Lemma 3.1 allows common multiplication by `r^2` or
  `D r^2` and reversal of the five positions;
- Corollary 3.3 translates the normalized type to rational points on a
  genus-5 curve over Q;
- later sections use local points, elliptic quotients, a Mordell--Weil sieve,
  and elliptic Chabauty-style rational-point methods.

Thus the current statement that binary squareclass/Kummer types, common
scaling, reversal, curve reduction, and local/rational-point methods are
prior art is accurate. "Kummer type" is a modern descriptive label for the
paper's `{1,D}` squareclass type, not its quoted terminology. The cube paper
correctly does not claim this strategy as its own.

## 2. Difference and construction wording

The differences are genuine: exponent 3 rather than 2; a pure cubic rather
than quadratic field; three cube classes rather than two square classes; and
a maximum of nonzero partial hits after one rational scale rather than five
field-square terms. These differences do not turn the general strategy into
a new method, and the manuscript says exactly that.

For the seventh model the paper claims only strict existence. It gives
`(64,36,8,-20,-48)` over `Q(cuberoot(6))`, certifies a non-torsion quotient
point, and refuses to infer infinitely many rational lifts to the genus-4
source. The abstract, theorem, README, cover letter, and limitations agree:
six models have infinite families, the seventh has existence only, and 24 of
31 remain open. No complete four-hit or Q-isomorphism classification is
claimed.

Independent exact searches for the displayed genus-4 equation, integral AP,
primitive scaling/reversal, and `R^times_(3,1)(5)` returned no scholarly
equivalent. The primitive AP also produced elementary sequence hits,
confirming that the tuple alone is not a reliable fingerprint. This remains
only a not-found observation.

## 3. References and distinctions

The emphasized references were checked against primary publisher or
author/arXiv records:

- Gonzalez-Jimenez (2010) studies three field-element cubes over quadratic
  fields via an elliptic curve, not this partial rational-entry problem.
- Hajdu--Tengely (2021) studies literal integer powers in integer APs; its
  journal metadata and DOI are correct and no pure-cubic Kummer line occurs.
- Hajdu--Tengely (2009) and Bruin--Gyory--Hajdu--Tengely (2006) concern
  primitive integer APs with prescribed literal powers. The latter publisher
  record confirms volume 17 (2006), pages 539--555 and the stated DOI.
- Xarles (2012) gives degree-dependent bounds for complete power APs over
  number fields; Bremner--Siksek (2016) concerns five squares in cubic fields.
- Lesavourey--Plantard--Susilo, Lemma 3.1, states the pure-cubic field
  equality criterion used to normalize radicands along the `q` and `q^2`
  cube lines. Its title, authors, journal, year, pages, and DOI are correct.

The manuscript labels these as context, not imported proof lemmas. Its proof
dependencies remain Darmon--Merel and Hajdu--Tengely.

## 4. Search gaps and overclaim scan

All material gaps are disclosed in the manuscript and submission package:

1. MathSciNet redirected to institutional authentication, so its records and
   citation graph were not reviewed;
2. the complete forward-citation chain of the 2013 predecessor is unchecked;
3. expanded/permuted full-text equation searches are incomplete;
4. zbMATH screening is metadata-level and does not cover every equation;
5. theses, non-English sources, and unindexed computations remain possible.

The current manuscript and submission-facing files contain no "first",
"new", "novel", "previously unknown", or "unprecedented" priority claim.
Occurrences of "first" there are ordinal. "We determine" and "no
equivalent construction was located" are immediately bounded by "not a
priority assertion" and HIGH-CAUTION language.

Historical round notes retain relative headings such as "new model" or
"first new existence closure". They describe progress relative to repository
rounds and are not repeated as bibliographic claims in the current paper or
submission materials. This is non-blocking, but those headings should not be
quoted as submission novelty statements.

## Verdict

**PASS.** The closest precedent is prominently acknowledged; the exact
construction is stated cautiously; metadata and distinctions agree with the
primary sources checked; and all material search gaps are disclosed. The
package supports a descriptive theorem claim only, not "first", a new
method, or bibliographic priority.
