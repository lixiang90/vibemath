# Campbell two-isogeny package: mathematical and novelty audit

Date: 2026-09-04
Scope: mathematics and priority only; no journal-format review.

## Decision

**The finite mathematical theorem survives the audit.**  The two displayed
2-isogeny Selmer groups are exact, not merely bounded-search survivor sets;
their dimensions give the stated bound `rank E(Q) <= 3`.  The `Q x K`
calculation and the rational projection `[35]` are exact integer identities.
The withdrawn cross-side Cassels--Tate expression is not used in any of these
positive deductions.  A later closed local argument also shows directly that,
on the `E` side, either of the places `Q_59` and `Q_71699` cuts the 32 signed
support classes to the same 16 classes, and adjoining the real condition cuts
them to exactly eight.

The safe novelty claim is much narrower than “new progress on the nine-term
problem”: this package gives a reproducible exact two-isogeny descent and
cubic-algebra calculation for **the one index-8 binary quartic obtained from
Campbell's Theorem 2.5**, together with an everywhere-local-solubility result
for its same-parameter genus-5 fibre product.  The searches below found no
published computation of these particular groups, but that is a not-found
report, not a proof of priority.

## 1. Exact two-isogeny descent

The audited curves are

```text
E : y^2 = X^3 - 591895071 X^2 + 58536289153843200 X,
E': y^2 = X^3 +1183790142 X^2 +116194618458722241 X.
```

Independent exact arithmetic gives

```text
B  = 2^18 3^12 5^2 7^5,
B' = A^2-4B = 3^4 59 71699 339106321,
(A')^2-4B' = 16B.
```

Thus the standard support lemma for
`y^2=x^3+a*x^2+b*x` leaves exactly the 32 signed squareclasses supported
on the primes of `b`, on each side.  The union of places at which a supported
cover can have bad reduction is exactly

```text
S = {infinity,2,3,5,7,59,71699,339106321}.
```

For `p` outside `S`, the covering

```text
C_d: N^2=d U^4+a U^2 V^2+(b/d)V^4
```

has quartic discriminant `16*b*(a^2-4*b)^2`, hence smooth genus-one
reduction.  Hasse plus Hensel supplies a local point.  This closes the
good-prime gap; no unlisted prime is being silently treated as a heuristic.

At the eight listed places, `certificates/local_matrix_512.json` contains all
`64*8=512` cells.  The audit re-executed all of the following:

- every finite `YES` cell supplies an integer pair `(U,V)` whose nonzero
  right side satisfies the exact `Q_p` square criterion (even valuation and
  square residue for odd `p`; even valuation and unit `1 mod 8` for `p=2`);
- every modular `NO` cell exhausts the two charts of
  `P^1(Z/p^k)` and all square residues modulo the recorded `p^k`;
- the remaining `NO` cells at `59` or `71699` use
  `4dF_d=(2dU^2+aV^2)^2-(a^2-4b)V^4`, with
  `v_p(a^2-4b)=1` and `(d/p)=-1`; its three primitive cases give either a
  nonsquare unit or odd valuation;
- the real `NO` cells are exactly the negative `d` classes on the `E` side,
  where all three terms of the quartic are nonpositive and no nontrivial
  projective point exists.

The `E`-side part now also has a short proof independent of the 512-cell
enumeration.  Put `delta=a^2-4b`.  At either `p=59` or `p=71699`,
`v_p(delta)=1`, `p` does not divide `2db`, and

```text
4dF_d=(2dU^2+aV^2)^2-delta*V^4.
```

For `(d/p)=1`, `(U:V)=(1:0)` gives a local point.  For `(d/p)=-1`, the
three exhaustive primitive cases `p|V`, `V(2dU^2+aV^2)` a unit, and
`p|(2dU^2+aV^2)` give respectively a nonsquare unit, a nonsquare unit, and
odd valuation.  Thus at either prime the locally soluble classes are exactly

```text
{-210,-70,-42,-30,-14,-10,-6,-2,1,3,5,7,15,21,35,105}.
```

The real locus is nonempty exactly for positive `d`; intersecting gives
`{1,3,5,7,15,21,35,105}`.  This is a complete local theorem, not a bounded
search, and it provides an independent structural check of the `E`-side
survivor set.

Consequently the locally soluble sets are exactly

```text
Sel^(dual phi)(E'/Q) = {1,3,5,7,15,21,35,105} = <3,5,7>, dimension 3,
Sel^phi(E/Q)         = {1,4230241,339106321,1434501462453361}
                     = <4230241,339106321>, dimension 2.
```

The standard exact sequence for `phi` and its dual gives

```text
2^rank = |E'(Q)/phi E(Q)| |E(Q)/dualphi E'(Q)|
         / (|E(Q)[phi]| |E'(Q)[dualphi]|).
```

Both kernel groups have order two and both Mordell--Weil quotients inject
into the computed Selmer groups.  Hence `rank E(Q) <= 3+2-2=3`.  No rank
equality, Mordell--Weil basis, or nonzero Sha class follows.

Assessment: **proved by a finite exact computation plus standard descent
lemmas**.  The local tests are sufficient for exactness.

## 2. `Q x K`, norm, and `[35]`

The cubic resolvent splits as `Q x K`, where

```text
K=Q(w),  w^2=D,
D=1434501462453361=59*71699*339106321.
```

The quadratic factor has discriminant `12288^2 D` and roots
`-134689011712 +/- 6144w`.  Direct evaluation of Fisher's cubic invariant

```text
z(g)=(4a*phi+3b^2-8ac)/3
```

gives

```text
z_Q = 9250179026780160 = 35*16257024^2,
z_K = 467235380575281152-6963847168w
    = 64^2(114071137835762-1700158w),
N(z_K/64^2)=35*15915620907648^2.
```

The full etale norm is a square.  Scaling by `64` and translating
`X=x_small+197298357` sends the rational resolvent factor to the visible
2-torsion Kummer coordinate; therefore the rational projection of `[H]` is
`[35]`.  This identifies one cohomological projection only: it does **not**
identify `C_H` with the even quartic `C_35`.

Assessment: **proved exact identities and a valid rational-factor
projection**.

## 3. Cassels--Tate contamination audit

The old expression written as `<35,4230241>_CT` is undefined in the claimed
formalism: the two entries live in opposite isogeny Selmer groups.  Its
tangent/Hilbert-symbol evaluation is branch-dependent at both `59` and
`71699`.  It is therefore retained only as a negative well-definedness
certificate.

No positive theorem depends on it:

- `PAPER_ELLIPTIC_ROUND_04_analysis.py` derives Selmer groups, rank bound,
  and `Q x K/[35]` before and independently of the Round-05 audit;
- `certificates/selmer_clean_v2.json` contains no proposed pairing value or
  rational-point conclusion and now points only to
  `ct_formula_rejection.json` as the negative audit;
- the manuscript explicitly says that no full 2-Selmer group,
  Cassels--Tate value, rank equality, or decision on `C_H(Q)` is known;
- all three bundled Magma/PowerShell files are marked
  `BUNDLED_UNEXECUTED_NOT_EVIDENCE`, with path and SHA-256 but no transcript
  or execution claim.

One historical note did still present the withdrawn cross-side gate without
an up-front warning.  This audit added a supersession banner to
`notes/clean-two-isogeny-descent.md`.  The actual conic point and tangent
remain valid identities, but only as data in the rejected-formula audit.

Assessment: **no contamination of the positive theorem after this repair**.

## 4. Prior art and novelty boundary

### Located primary sources

1. Campbell's original article constructs the relevant eight-term family
   and is the source of Theorem 2.5; its abstract also distinguishes the
   non-Weierstrass length-9 construction:
   https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html
2. Bremner's 1999 article is the earlier length-8 Weierstrass-family source:
   https://doi.org/10.1080/10586458.1999.10504629
3. Garcia-Selfa--Tornero study simultaneous arithmetic progressions, not
   this numerical descent:
   https://doi.org/10.1017/S0004972700038429
4. Garcia-Fritz--Pasten prove a general rank-growth theorem for long
   progressions in fixed-j families, not the rank or Selmer groups of this
   curve:
   https://doi.org/10.1093/imrn/rnaa061
5. Fisher gives the binary-quartic Selmer description and the exact cubic
   invariant used here:
   https://doi.org/10.1007/s40993-022-00376-z
6. Fisher's rational-2-torsion paper is the relevant higher-descent context:
   https://arxiv.org/abs/1509.03234

### Exact-model search

Web, publisher, arXiv-facing, and exact-string searches through 2026-09-03
for the pairs

```text
"-591895071" "58536289153843200"
"1183790142" "116194618458722241"
"1434501462453361" Selmer
"4230241" "339106321" elliptic
"850079" "11210976" "138714149248"
"269378023424" elliptic
```

returned no match to a prior rank/Selmer computation.  Campbell's paper was
the only located source of the underlying family.  This search is not
isomorphism-invariant: a minimal model may have wholly different
coefficients.  LMFDB also cannot serve as a completeness proof here; its
official coverage is all conductors below 500,000, all 7-smooth conductors,
and prime conductors up to 300,000,000, not all rational elliptic curves:
https://www.lmfdb.org/EllipticCurve/Q/Completeness

### Safe claim and remaining risk

Use only:

> For the index-8 binary quartic attached to Campbell's Theorem 2.5, we give
> an exact, reproducible local certificate for its two rational 2-isogeny
> Selmer groups, the resulting rank upper bound, its explicit cubic-algebra
> invariant and `[35]` projection, and the everywhere-local solubility of the
> same-parameter genus-5 fibre product.

Do not use “first”, “new solution of the nine-term problem”, “rank of the
Campbell curve”, or “Cassels--Tate obstruction”.  The minimal-model and
isomorphism-class part of this earlier risk assessment is discharged in
Section 6 below.  The remaining priority risk is the incomplete human audit
of Campbell's full citation graph and non-indexed literature.

## 5. Repairs and reproducibility result

Repairs made during this audit:

- updated all code/tests to the repository `code/` + `certificates/` layout;
- regenerated the matrix, clean Selmer, rejection, and provenance
  certificates from their current sources;
- recorded all three bundled candidate inputs by path and SHA-256 while
  keeping them ineligible;
- replaced the stale clean-certificate pointer and manuscript certificate
  hashes;
- added the historical-note supersession warning.

From `code/`, the exact command

```powershell
python -W error -m unittest -q PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py test_same_m_local.py NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py NEXT_ELLIPTIC_ROUND_09_test.py NEXT_ELLIPTIC_ROUND_10_test.py
```

passes **65/65 tests**.  No Magma, Sage, PARI/GP, remote CAS, or claimed
descent transcript is used.  The host audit found no independent
elliptic-curve CAS, so Python/SymPy is not presented as a second
implementation of the minimal-model, Kodaira-type, splitness, or conductor
calculation.

## 6. Isomorphism-invariant priority audit

The exact follow-up computation is stored in
`certificates/minimal_model_identity.json` and generated by
`code/NEXT_ELLIPTIC_ISOMORPHISM_AUDIT.py`.  It uses the admissible change

```text
x_original = 36*x_minimal,
y_original = 216*y_minimal + 108*x_minimal,
(u,r,s,t) = (6,0,3,0).
```

It sends the Campbell-Jacobian model to the integral equation

```text
E_min: y^2+x*y=x^3-16441530*x^2+45166889779200*x,
a-invariants [1,-16441530,0,45166889779200,0].
```

The exact invariants are

```text
c4 = 2157171698920561
   = 43*461*2789*5821*6703,
c6 = 70577985500751764077559,
Delta_min = 2926451742397178075653974744686961623040000
          = 2^28*3^16*5^4*7^10*59*71699*339106321,
j = 10038160648206649953061393462836377818780518481
    /2926451742397178075653974744686961623040000.
```

The original and new invariants satisfy
`c4_old=6^4*c4_min`, `c6_old=6^6*c6_min`, and
`Delta_old=6^12*Delta_min`.  Moreover `gcd(c4_min,Delta_min)=1`.
Therefore at every bad prime the displayed integral equation has
`v_p(c4)=0`: it is already `p`-minimal, has multiplicative reduction of
type `I_{v_p(Delta_min)}`, and has conductor exponent one.  At all other
primes it has good reduction.  This proves, without Tate-algorithm software,

```text
N_E = rad(Delta_min)
    = 2*3*5*7*59*71699*339106321
    = 301245307115205810.
```

This also gives a fail-closed reason not to assign an LMFDB label.  The
conductor is composite, not 7-smooth, and far above the LMFDB's complete
conductor range of 500,000; it is outside every completeness family listed
on the official page.  Exact searches by the minimal `a`-invariants,
conductor, `c4`, and the numerator of `j` returned no relevant mathematical
record.  The additional queries were

```text
"16441530" "45166889779200" elliptic
"301245307115205810" elliptic curve
"2157171698920561" elliptic curve
"10038160648206649953061393462836377818780518481"
```

No Sage, Magma, PARI/GP, or remote CAS was available or invoked; the six
new regression tests independently re-evaluate the coordinate change,
invariant scaling, minimality criterion, discriminant factorization,
conductor, `j`, and the manuscript formulas.

Priority assessment after the isomorphism-invariant search: **low-to-medium
risk for the narrowly worded finite theorem**, rather than the previous
medium risk.  The lack of an LMFDB row is expected from its published
coverage and is not novelty evidence.  A claim of absolute priority still
requires human inspection of Campbell's dissertation and a citation-graph
search, but neither the original model nor its global minimal isomorphism
class was located in indexed literature through 2026-09-03.

The query log and database-scope boundary are frozen separately in
`notes/isomorphism-prior-art-search.md`.  In particular, Campbell's
Proposition 2.6 computes the rank of the parameter curve `D`, not the
Jacobian of the later ninth-value quartic `H`; the two calculations must not
be conflated.

## 7. Round-09 and Round-10 artifacts and claim boundary

The closed two-place argument is generated by
`code/NEXT_ELLIPTIC_ROUND_09.py` and frozen in
`certificates/round09_two_place_gate.json`; its six dedicated tests are part
of the 65-test command above.  The complementary Round-10 `E'`-side theorem is
generated by `code/NEXT_ELLIPTIC_ROUND_10.py` and frozen in
`certificates/round10_eprime_two_three_gate.json`; its dedicated tests are also
part of the same command.  The current paper is 11 pages.  Its SHA-256 is

```text
0aebc7230b952a256741a2ee985f69f3f5153852ca5258ff27bad8c8ccee4044
```

This local theorem neither supplies nor obstructs a rational ninth point and
does not decide `C_H(Q)`.  The absence of a database hit remains only a dated,
coverage-limited search result and is not a proof of novelty.  The exact
minimal-model and conductor formulas have one auditable implementation and a
direct mathematical proof, but no independent second-CAS reproduction on the
audited host.
