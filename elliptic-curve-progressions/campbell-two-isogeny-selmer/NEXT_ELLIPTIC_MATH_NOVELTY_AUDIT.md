# Campbell two-isogeny package: mathematical and novelty audit

Date: 2026-09-03  
Scope: mathematics and priority only; no journal-format review.

## Decision

**The finite mathematical theorem survives the audit.**  The two displayed
2-isogeny Selmer groups are exact, not merely bounded-search survivor sets;
their dimensions give the stated bound `rank E(Q) <= 3`.  The `Q x K`
calculation and the rational projection `[35]` are exact integer identities.
The withdrawn cross-side Cassels--Tate expression is not used in any of these
positive deductions.

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
Campbell curve”, or “Cassels--Tate obstruction”.  Priority risk remains
**medium** until a minimal global model and conductor are computed with an
independent audited system and searched by isomorphism class, and Campbell's
citation graph/dissertation are checked beyond exact-string indexing.

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
python -m unittest -v PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py test_same_m_local.py
```

passes **44/44 tests**.  No Magma, Sage, PARI/GP, remote CAS, or claimed
descent transcript is used.
