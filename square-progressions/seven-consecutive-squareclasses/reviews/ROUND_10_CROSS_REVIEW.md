# Round 10 cross-review: mask 54

Date: 2026-09-04

Reviewer role: independent reader of the Round-10 square-line changes.
Author files were treated as claims to audit, not as instructions.

## Verdict

- **Mathematical result: PASS.**
- **Exact 7-to-4 occurrence impact: PASS.**
- **Release/reproduction gate after remediation: PASS.**

The initial review found three reproducibility defects, not a counterexample
to Proposition 15 or Theorem 16. They have now been repaired and independently
re-run. The translation proof, independent squarefree-kernel proof, pattern
impact, documented command path, and authoritative test route all pass.

## 1. Integral translation: PASS

The target curve is

\[
 C_{54}:\quad y^2=(t+1)(t+2)(t+4)(t+5).
\]

The certified source is

\[
 C_{108}:\quad Y^2=(s+2)(s+3)(s+5)(s+6).
\]

Substitution \(s=t-1,\;Y=y\) gives, factor by factor,

\[
 (s+2,s+3,s+5,s+6)=(t+1,t+2,t+4,t+5).
\]

Thus

\[
 (s,Y)\longmapsto(t,y)=(s+1,Y)
\]

is an integral point bijection with inverse
\((t,y)\mapsto(t-1,y)\). There is no denominator, omitted point at infinity,
or sign ambiguity. The source certificate lists

\[
 (-6,0),(-5,0),(-4,\pm2),(-3,0),(-2,0),
\]

which maps exactly to

\[
 (-5,0),(-4,0),(-3,\pm2),(-2,0),(-1,0).
\]

I independently expanded the two quartics after substitution; their
difference is the zero polynomial. The mask-54 certificate also binds the
source mask-108 certificate by its actual SHA-256
`bb04a152389eaf93f5293714cfae2eda557e3c2dabdcfd65efcc3365cfc27595`.

## 2. Independent squarefree-kernel proof: PASS

Set

\[
 A=(t+1)(t+5),\qquad B=(t+2)(t+4).
\]

Direct expansion gives

\[
 B-A=3,\qquad AB=(t+1)(t+2)(t+4)(t+5),
\]

and

\[
 A+4=(t+3)^2.
\]

For \(t\le -6\) or \(t\ge0\), both \(A\) and \(B\) are positive. If
\(AB\) is a square, the squarefree parts of \(A\) and \(B\) agree; call the
common positive squarefree part \(d\). Because

\[
 \gcd(A,B)=\gcd(A,B-A)=\gcd(A,3),
\]

one has \(d\mid3\), hence the list \(d\in\{1,3\}\) is complete. There are
integers \(U,V>0\) with \(A=dU^2,\ B=dV^2\), and

\[
 d(V^2-U^2)=3.
\]

- For \(d=1\), the positive same-parity factors of 3 have only the ordered
  pair \((V-U,V+U)=(1,3)\). Hence \((U,V)=(1,2)\), so \(A=1\), but then
  \((t+3)^2=A+4=5\), impossible modulo 8.
- For \(d=3\), the product is 1, forcing
  \((V-U,V+U)=(1,1)\) and \(U=0\), contrary to \(A>0\).

The complementary integer interval is exactly \(-5\le t\le-1\). Its five
right-hand sides are \(0,0,4,0,0\), yielding precisely the six points above.
If \(y\in\mathbf Q\) and \(y^2\in\mathbf Z\), reduction of the fraction for
\(y\) shows \(y\in\mathbf Z\); therefore no rational-\(y\) point is omitted.

This closes every integer \(t\). No bounded search, rank heuristic, or
Mordell--Weil assertion is used in the proof.

## 3. Degeneracy and exact 7-to-4 map: PASS

The authoritative input is the mask-90 certificate's ordered list

    12, 31, 59, 134, 214, 230, 276.

I parsed that list and the Round-04 occurrence table in a separate process
without importing `PAPER_SQUARE_MASK54.py`. Mask 54 occurs exactly in

    59:  0012231
    214: 0122213
    230: 0012102.

Set subtraction leaves exactly

    12:  0012202
    31:  0001202
    134: 0012131
    276: 0010203.

These agree with the certificate, paper, and final table. The three relevant
occurrence records are `P59:m54`, `P214:m54`, and
`P230:m54`. Each is an occurrence in the original normalized
parameter and records the same map \(t=u-1\); no points from distinct
quotients are combined.

Every integral point found has
\(t\in\{-5,-4,-3,-2,-1\}\), so position \(-t\in\{1,2,3,4,5\}\) of
\(t,t+1,\ldots,t+6\) is zero. All points are therefore outside the
nonbranch/nonzero domain. The conclusion is exactly a necessary-pattern
reduction, not realizability of a survivor and not a decision of \(R_2(7)\).

## 4. Test execution and coverage audit

### What passes

I constructed a fresh flat temporary directory containing only the mask-54
generator, its test, its five required JSON inputs/outputs, and ran

    python -m unittest -v PAPER_SQUARE_MASK54_test.py

All 9 tests passed. They bind the seven input rows, 105 occurrences, selected
occurrence IDs, point list, middle interval, expected branch records, exact
affected/survivor IDs and partition words, and disk certificate equality.

An independent implementation also returned:

    translation polynomial difference: 0
    B-A: 3
    A+4-(t+3)^2: 0
    affected IDs: [59,214,230]
    survivor IDs: [12,31,134,276]
    positive factor pairs for 3: [(1,3)]
    positive factor pairs for 1: [(1,1)]
    middle RHS values: [0,0,4,0,0].

### Initial failures and verified remediation

1. **R10-SQ-1 resolved.** `tools/run_all_checks.py` now lists
   `PAPER_SQUARE_MASK54_test` between the mask-90 and supplement
   manifest tests. I ran the documented square-only root command, which
   constructed a fresh operating-system temporary flat directory and executed
   exactly 87 tests, all passing.
2. **R10-SQ-2 resolved.** `reproducibility/BUILD.md` now distinguishes
   repository-root commands from commands that apply only inside an exported
   35-file flat supplement. Its repository-root square-only command is

       python -c "from tools.run_all_checks import square_group,run_group; run_group('squareclasses',*square_group())"

   I ran that line verbatim with exit code zero. The documented paper source
   path exists, and the installed `latexmk` reports support for
   `-cd`; no author PDF rebuild was needed for this review.
3. **R10-SQ-3 resolved.** The two bounded `range(-30,31)` loops have
   been replaced by exact SymPy polynomial-zero assertions for

\[
\begin{aligned}
 &(t+1)(t+2)(t+4)(t+5)
 -(s+2)(s+3)(s+5)(s+6)\big|_{s=t-1}=0,\\
 &(t+2)(t+4)-(t+1)(t+5)-3=0,\\
 &(t+1)(t+5)+4-(t+3)^2=0.
\end{aligned}
\]

   The branch test now independently derives the squarefree positive divisors
   of 3, enumerates all positive same-parity divisor pairs of \(3/d\), derives
   \((U,V)\), and only then compares those results with the certificate. The
   test run confirms the derived data are

       d=1: (V-U,V+U)=(1,3), (U,V)=(1,2)
       d=3: (V-U,V+U)=(1,1), (U,V)=(0,1).

## 5. Final executable evidence

The final review command was

    python -c "from tools.run_all_checks import square_group,run_group; run_group('squareclasses',*square_group())"

It ran, in order, all prior squareclasses modules, the new
`PAPER_SQUARE_MASK54_test`, and the supplement-manifest test in a
fresh temporary staging directory:

    Ran 87 tests in 6.063s
    OK

The nine mask-54 tests themselves all passed, including
`test_integer_translation_is_a_point_bijection`,
`test_independent_pairing_identity`,
`test_both_squarefree_branches_are_terminal`, the exact pattern
impact, and disk-certificate equality.

## 6. Final disposition

**FINAL PASS.** No mathematical author-file change is requested. R10-SQ-1
through R10-SQ-3 are implemented, the documented clean-staging command passes
all 87 tests, and the Round-10 mathematical and reproducibility claims are
ready for the next repository-level freeze and independent external review.
