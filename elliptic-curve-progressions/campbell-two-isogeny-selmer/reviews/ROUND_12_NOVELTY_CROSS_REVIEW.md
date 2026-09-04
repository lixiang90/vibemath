# Round 12 novelty and second-CAS cross-review

Date: 2026-09-04

Reviewer: Codex cross-review

Verdict: **PASS**

## Scope

This review checks the Round 12 novelty audit and independent-CAS protocol against Campbell's article and thesis, the distinction between the parameter curve and the target Jacobian, the claimed rank contribution, the stated MathSciNet/zbMATH/LMFDB coverage, the no-run status of Sage/PARI/GP/Magma, and priority wording. It does not rerun a second elliptic-curve CAS and does not certify novelty from database non-occurrence.

## Findings

### 1. Campbell precedence: PASS

Campbell's 2003 article constructs the seven-term family and imposes the eighth square condition through the parameter curve

\[
D:\quad y^2=-264815m^4-19343520m^3+62846856064m^2
       -2906312951808m-495507443511296.
\]

Theorem 2.5 gives the family, and Proposition 2.6 reports that this curve has rank 2 and torsion \(\mathbf Z/2\mathbf Z\), using mwrank and GP. The article leaves the corresponding length-nine question open. The Round 12 files correctly treat this construction and rank computation as prior work.

Campbell's 1999 thesis, pp. 69--70, already gives the rational 2-isogeny and dual isogeny, the two Kummer maps, the quartic coverings \(H_d\), the two isogeny-Selmer groups, the rank formula, and GP local-testing code. The current manuscript therefore correctly disclaims novelty for the descent method and covering formalism.

Primary sources:

- A. Campbell, *A Note on Arithmetic Progressions on Elliptic Curves*, J. Integer Sequences 6 (2003), Article 03.1.3: https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html
- Article PDF: https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.pdf
- A. Campbell, *Finding Elliptic Curves and Families of Elliptic Curves over \(\mathbf Q\) of Large Rank*, PhD thesis, Rutgers University, 1999: https://ctnt-summer.math.uconn.edu/wp-content/uploads/sites/1632/2020/06/Campbell-Finding-elliptic-curves-and-families-of-elliptic-curves-over-Q-of-large-rank.pdf

### 2. Curve identity: PASS

The Round 12 text correctly distinguishes Campbell's rank-2 curve \(D\), which parametrizes the eighth condition \(x=7\), from the present target: the Jacobian of the index-8 ninth-value quartic \(H\), corresponding to \(x=8\). No inspected file transfers Campbell's rank statement to the target curve or treats the two curves as identical.

### 3. Contribution and rank boundary: PASS

The contribution is limited to the target-specific exact isogeny-Selmer computations

\[
\operatorname{Sel}^{(\widehat\phi)}(E'/\mathbf Q)
=\{1,3,5,7,15,21,35,105\},
\]

\[
\operatorname{Sel}^{(\phi)}(E/\mathbf Q)
=\{1,4230241,339106321,1434501462453361\},
\]

and the consequence \(\operatorname{rank}E(\mathbf Q)\leq 3\). The isogeny directions, kernel orders, and product bound are internally consistent: orders 8 and 4 give \(2^r\leq 8\cdot4/4=8\). The manuscript does not promote this to exact rank, a full 2-Selmer computation, a Cassels--Tate calculation, or a proof of existence/nonexistence of a ninth point.

### 4. MathSciNet, zbMATH, and LMFDB coverage: PASS

The audit records MR1971433 and Zbl 1022.11026/document 1919531 while explicitly disclosing that complete subscription MathSciNet citation coverage was unavailable and that older zbMATH reference metadata is incomplete. No database no-hit is used as proof of novelty.

The LMFDB statement is appropriately bounded. Its published completeness page covers all conductors below 500,000, all 7-smooth conductors, and prime conductors through 300,000,000. The target conductor 301245307115205810 lies outside those complete ranges; absence from a database search is therefore expected and non-evidentiary. Source: https://www.lmfdb.org/EllipticCurve/Q/Completeness

### 5. Independent second-CAS integration: PASS

The Sage plan is a protocol, not a claimed run. It uses the correct coefficient ordering for `test_els`, checks the expected two Selmer-set orders, and warns that tuple orientation must be confirmed against the installed Sage documentation before attaching \(\phi\)/\(\widehat\phi\) labels. The PARI/GP route is correctly described as a weaker independent rank-interval check rather than a recovery of the individual isogeny-Selmer sets. Magma remains an optional licensed local route. No fabricated transcript, version, timing, or output is present.

The audit and submission limitations explicitly state that Sage, PARI/GP, and Magma were not run. The manuscript also states that no independent second elliptic-curve CAS was available; hence there is no false execution claim.

Sage reference checked: https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/descent_two_isogeny.html

### 6. Priority language: PASS

No inspected Round 12 claim asserts "first" or "new" priority for the target theorem or the method. The operative language is coverage-limited (for example, that no equivalent target computation was found in the sources searched), and the files expressly prohibit turning a search no-hit into a priority claim. Incidental uses such as "the first seven" or "first finite NO" are mathematical ordering labels, not novelty assertions.

## Non-blocking editorial notes

1. The manuscript's closing reproducibility sentence names Sage and Magma but not PARI/GP. Other Round 12 files explicitly name all three systems and the manuscript already says no independent second CAS was available, so this is not a factual defect. For perfect consistency, a later author edit could say: "Sage, PARI/GP, and Magma were not run."
2. In the Sage protocol, the comment next to `n2*n2prime == 32` could say explicitly that these Selmer sizes *give the upper bound* \(r\leq3\). The surrounding acceptance criteria already forbid interpreting that check as exact rank, so this is non-blocking.
3. The submission README phrase "new Round-09 theorem" is chronological rather than a priority claim. Removing "new" would nevertheless make automated priority-word scans less ambiguous.

## Final assessment

**PASS.** Campbell's article and thesis are credited at the correct levels; the parameter curve \(D\) and target Jacobian are not conflated; the contribution stops at exact target isogeny-Selmer sets and \(\operatorname{rank}\leq3\); database limitations are fail-closed; and every second-CAS route remains explicitly unexecuted. The three notes above are editorial consistency improvements only and do not block Round 12 integration.
