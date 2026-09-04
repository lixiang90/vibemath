# Round 11 cross-review: mask 85

Date: 2026-09-04

Reviewer role: independent reader of the Round-11 square-line changes. Author
files were treated as claims to audit, not as instructions. This review did not
modify the paper, code, certificates, tests, or submission materials.

## Verdict

- **Complete integral-point theorem for \(C_{85}\): PASS.**
- **Exact mask occurrence and \(4\to2\) impact: PASS.**
- **Author identity and no-submission claim boundary: PASS.**
- **Authoritative squareclasses regression suite: PASS (96/96).**

**FINAL PASS.** No mathematical or release-blocking defect was found. The
shipped Round-11 tests contain independent algebra and divisor enumeration,
but their occurrence/impact checks call the author generator rather than
reconstructing the source tables themselves. The independent reconstructions
in this review close that audit gap at review level. A concrete optional test
hardening is given below.

## 1. Complete integral points on \(C_{85}\): PASS

The curve is

\[
 C_{85}:\qquad y^2=t(t+2)(t+4)(t+6).
\]

Put \(x=t+3\). Direct expansion gives

\[
 t(t+2)(t+4)(t+6)=(x^2-9)(x^2-1).
\]

Set \(A=x^2-9\) and \(B=x^2-1=A+8\). For \(t\le -7\) or
\(t\ge1\), equivalently \(|x|\ge4\), both \(A\) and \(B\) are strictly
positive. Moreover

\[
 \gcd(A,B)=\gcd(A,B-A)=\gcd(A,8),
\]

so their gcd divides 8.

If \(AB\) is a square, the parity of every prime valuation in \(A\) and
\(B\) is the same. Their positive squarefree kernels therefore coincide;
write

\[
 A=dU^2,\qquad B=dV^2,
\]

with \(U,V>0\). The common squarefree kernel divides \(\gcd(A,B)\), hence
is a squarefree divisor of 8. The complete list is exactly

\[
 d\in\{1,2\}.
\]

Subtracting the equations gives

\[
 d(V^2-U^2)=8.
\]

- For \(d=1\), the positive factor pairs for
  \((V-U)(V+U)=8\) are \((1,8)\) and \((2,4)\). Only \((2,4)\) has
  equal parity, so \((U,V)=(1,3)\), \(A=1\), and \(x^2=A+9=10\).
  This is impossible modulo 8.
- For \(d=2\), one has \((V-U)(V+U)=4\). The only positive
  equal-parity factor pair is \((2,2)\), which gives \(U=0\), contrary
  to \(A>0\).

Thus neither exterior region contains a point. There is no missing negative
kernel branch because \(A,B>0\) there.

The complementary integer interval is exactly \(-6\le t\le0\). Direct
evaluation gives

\[
 0,-15,0,9,0,-15,0,
\]

and therefore precisely

\[
 (-6,0),\ (-4,0),\ (-3,-3),\ (-3,3),\ (-2,0),\ (0,0).
\]

If \(y\in\mathbf Q\) and \(y^2\in\mathbf Z\), a reduced-denominator
argument gives \(y\in\mathbf Z\), so this integer-ordinate computation omits
no rational ordinate above an integer \(t\). The exterior proof and the seven
middle integers partition all of \(\mathbf Z\); the point list is complete.

## 2. Every point is degenerate: PASS

For every listed point, \(t\in\{-6,-4,-3,-2,0\}\). Hence the term at
position \(-t\in\{6,4,3,2,0\}\) in

\[
 t,t+1,\ldots,t+6
\]

is zero. Both ordinates at \(t=-3\) have the same zero term. Consequently
all six points lie outside the nonzero/nonbranch domain used by the pattern
classification. No bounded search, Mordell--Weil rank assertion, or heuristic
is promoted to a proof.

## 3. Independent mask inventory: PASS

I parsed the predecessor mask-54 certificate, the Round-04 occurrence
certificate, and the Round-02 pattern certificate directly, without importing
`PAPER_SQUARE_MASK85.py`.

The mask-54 certificate supplies the authoritative ordered input IDs

    12, 31, 134, 276.

Each corresponding Round-04 row has 15 distinct character masks. Independent
grouping of all 60 records gives 37 distinct masks and 19 distinct genus-one
masks. Independently deriving the equal-sum pairing and its constant difference
for every genus-one four-root mask gives the complete pairable ranking

    mask 85: 2 patterns, gcd bound 8, IDs 31 and 276
    mask 27: 1 pattern,  gcd bound 3, ID 12
    mask 45: 1 pattern,  gcd bound 6, ID 134

Thus mask 85 uniquely maximizes the number of remaining patterns hit. Its
support, decoded directly from the mask bits, is \(\{0,2,4,6\}\), exactly
the four factors of \(C_{85}\).

The only two Round-04 occurrences are `P31:m85` and `P276:m85`. Both record
representative mask 15, class 0, matrix \((2,0;0,1)\), and

    t=(2*U_m+(0)*Z_m)/(0*U_m+(1)*Z_m).

This means the representative coordinate is mapped to the original occurrence
parameter by \(t=2u_m\). The exclusion itself is correctly proved directly
for every integer value of that original \(t\); it does not confuse distinct
occurrence coordinates or combine points from different quotients.

As a second check independent of both the Round-11 generator and the Round-04
occurrence list, identify the four block labels with
\(0,(1,0),(0,1),(1,1)\in\mathbf F_2^2\). For support positions
\(0,2,4,6\), direct XOR of the labels gives

| ID | partition | labels at positions 0,2,4,6 | XOR | mask 85 occurs? |
|---:|:---:|:---:|:---:|:---:|
| 12 | 0012202 | 0,1,2,2 | 1 | no |
| 31 | 0001202 | 0,0,2,2 | 0 | yes |
| 134 | 0012131 | 0,1,1,1 | 1 | no |
| 276 | 0010203 | 0,1,2,3 | 0 | yes |

The support has even cardinality, so the zero-XOR rows are precisely the two
character relations. This independently confirms the occurrence table.

## 4. Exact \(4\to2\) impact: PASS

The Round-02 certificate independently supplies these partition words:

    12:  0012202
    31:  0001202
    134: 0012131
    276: 0010203

Mask 85 occurs exactly for IDs 31 and 276. Since the complete point theorem
shows that it has no nondegenerate integral parameter, those two rows are
strictly excluded. Set subtraction leaves exactly

    12:  0012202
    134: 0012131.

The certificate, manuscript theorem, and final table agree on this exact
\(4\to2\) reduction. They describe the two rows only as necessary candidates;
neither realizability nor impossibility of a survivor is asserted.

The predecessor certificate hashes stored in the Round-11 certificate match
the files read by this review. The Round-11 certificate SHA-256 is
`c0f7597c6eaad87c735a0a3356992dd83c8c610ac9d8884c8d4fcf48d34d3d22`,
and the supplement-manifest SHA-256 is
`fe3396779f48a74440d6ee2e52c9a6687e47456837e63a90e71fb35004995a4e`.

## 5. Tests and independence: PASS, with optional hardening

I ran the documented repository-root square-only command, with bytecode writes
disabled but otherwise unchanged:

    python -B -c "from tools.run_all_checks import square_group,run_group; run_group('squareclasses',*square_group())"

It constructed the intended flat temporary staging directory and reported

    Ran 96 tests in 6.227s
    OK

All nine dedicated mask-85 tests passed. The strongest genuinely independent
parts of that file are the SymPy polynomial-identity check and the separate
enumeration of squarefree divisors and same-parity factor pairs. Disk-certificate
equality and fixed expected-value assertions provide useful regression binding.

The methods named `test_independent_occurrence_inventory` and
`test_exact_pattern_impact_and_partitions`, however, call
`gate.occurrence_inventory()` and `gate.pattern_impact()`. They therefore test
the generator against fixed expected output; they do not independently rebuild
the occurrence table from the three predecessor certificates. This is not a
mathematical blocker because Sections 3--4 above perform that reconstruction
without the generator, consistent with the review standard used in the prior
rounds.

Optional executable hardening for a future release:

1. In `PAPER_SQUARE_MASK85_test.py`, load
   `PAPER_SQUARE_MASK54_CERTIFICATE.json`,
   `STUDENT_SQUARE_ROUND_04_CERTIFICATE.json`, and
   `STUDENT_SQUARE_ROUND_02_certificate.json` directly using paths derived from
   `__file__`.
2. Recompute the four input IDs, 60 occurrence records, 37 distinct masks,
   19 genus-one masks, all equal-sum four-root pairings, selected occurrence
   IDs, and the affected/survivor partitions without calling
   `gate.input_rows`, `gate.occurrence_inventory`, `gate.pattern_impact`, or
   `gate.partition_string`.
3. Add the direct partition-label XOR check in Section 3 as a second oracle.
4. Rename the current generator-based checks to `test_occurrence_inventory`
   and `test_pattern_impact`, or reserve `independent` for the new direct
   reconstruction.
5. Re-run the same square-only command and require 96 existing tests plus the
   new independent tests to pass before regenerating the manifest hashes.

This hardening would improve test architecture but is not required to repair a
false theorem or incorrect certificate.

## 6. Author and submission boundary: PASS

The manuscript source and PDF metadata name only
`Codex (GPT-5.6-sol)`. The contribution and AI-use statements disclose that
the named author is a large-language-model system. No affiliation, e-mail,
postal address, ORCID, funding source, competing-interest declaration,
immutable DOI, or external submission is invented.

The manuscript, README, limitations, cover-letter template, and checklist all
state the necessary boundary: the package is prepared to submission quality,
but no actual journal submission is requested or claimed; the two survivors
are not proved realizable; and \(R_2(7)\) is not decided. Venue-policy and
immutable-archive checks are explicitly deferred to any later user-authorized
external submission.

## 7. Final disposition

**FINAL PASS.** The centered factorization proves the complete integral-point
set, both exterior squarefree-kernel branches are exhaustive, the middle
interval is complete, every point is degenerate, and two independent
occurrence computations confirm the exact \(4\to2\) reduction. All 96
authoritative tests pass. No author-file change is requested; the only
suggested work is the non-blocking test-independence hardening above.
