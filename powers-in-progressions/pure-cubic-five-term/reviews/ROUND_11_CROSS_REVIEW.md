# Round 11 cross-review: strict existence in the `0102` model

Date: 2026-09-04
Reviewer: elliptic-line cross-review
Verdict: **PASS (no blocking mathematical finding)**

I reviewed the Round-11 existence note, generator, frozen JSON certificate,
independent test module, and the theorem as propagated to `paper/main.tex`.
The explicit arithmetic progression, field degree, four cube witnesses,
omitted-term obstruction, colour normalization, quotient map, and
Nagell--Lutz argument are all correct.  The manuscript also keeps the
essential claim boundary: this closes one model for existence and does not
deduce an infinite family on the genus-four source curve.

## 1. Source point and arithmetic progression

The model uses repeated-colour positions 0 and 2, with

\[
 A_0=X^3,\qquad A_2=Y^3,
\]

so the full five-term progression is

\[
 A_k=\frac{(2-k)X^3+kY^3}{2}\quad(0\leq k\leq4).
\]

The inverse-class condition on positions 1 and 4 is represented by

\[
 C:\ (X^3+Y^3)(2Y^3-X^3)=2W^3
 \subset \mathbf P(1,1,2).
\]

At the asserted point `(X:Y:W)=(2:1:-3)`, both sides are `-54`:

\[
 (8+1)(2-8)=-54=2(-3)^3.
\]

The associated rational progression is

\[
 (8,9/2,1,-5/2,-6),
\]

whose common difference is `-7/2`.  Multiplication by the rational cube
`8=2^3` gives

\[
 (64,36,8,-20,-48).
\]

The four adjacent differences are independently

\[
 36-64=8-36=-20-8=-48-(-20)=-28.
\]

Thus the displayed integer tuple is an arithmetic progression.  Its five
entries are nonzero and pairwise distinct because the common difference is
nonzero.

The generator stores the expanded source equation multiplied by 2, with
coefficient vector `(-2,2,4,-4)`.  This is exactly twice the expanded
equation in the paper and defines the same curve; it is not a normalization
error.

## 2. The cubic field and exactly four cube positions

Let `K=Q(alpha)` with `alpha^3=6`.  The polynomial `T^3-6` is Eisenstein at
2: its non-leading coefficients are divisible by 2, while its constant term
is not divisible by 4.  Hence it is irreducible and `[K:Q]=3`; the field is
genuinely cubic.

The four claimed witnesses check exactly:

\[
 64=4^3,\qquad
 36=(\alpha^2)^3,\qquad
 8=2^3,\qquad
 -48=(-2\alpha)^3.
\]

I also rechecked the paper's Kummer-kernel lemma rather than treating it as
a computational assumption.  If
`y=a+b alpha+c alpha^2` has rational cube, vanishing of the two non-rational
coefficients gives the two equations displayed in the paper.  When `a=0`
they force `bc=0`.  When `a` is nonzero, the stated resultant
`B*D*(B^3*D-1)^2` forces `B=0`, because `D=6` is not a rational cube, and
then the first equation forces `C=0`.  Consequently

\[
 \ker\bigl(\mathbf Q^*/\mathbf Q^{*3}\to
 K^*/K^{*3}\bigr)=\langle[6]\rangle
 =\{[1],[6],[36]\}.
\]

Every representative of one of these three rational cube classes has
5-adic valuation congruent to 0 modulo 3.  In contrast,
`v_5(-20)=1`.  Therefore `-20` is not a cube in `K`.  Together with the four
explicit roots, this proves **exactly** four cube positions, not merely at
least four.

## 3. Colour word and model identification

Relative to the generator `[6]`, the cube-class exponents at positions
`(0,1,2,4)` are

\[
 (0,2,0,1).
\]

The permitted generator inversion is the colour automorphism
`c -> 2c=-c` in `F_3`; it sends this word to

\[
 (0,1,0,2),
\]

which is the specified canonical word `0102`.  The omitted entry is at
position 3, so the position set is exactly `0124`.  The common scaling by 8
is a rational cube and does not change any colour.

One purely terminological sentence in the manuscript says that the classes
“modulo `<[6]>` are `0201`.”  Literally, quotienting by `<[6]>` would erase
these distinctions.  The proof and code plainly mean “the exponents with
respect to the generator `[6]`,” which is mathematically what is used.
This wording does not affect the theorem or certificate verdict.

## 4. Elliptic quotient and Nagell--Lutz

On the chart `Y != 0`, put

\[
 u=-2W/Y^2,\qquad v=2(X/Y)^3-1.
\]

Writing `T=(X/Y)^3`, the source equation gives

\[
 (T+1)(2-T)=2W^3/Y^6.
\]

Therefore

\[
 u^3=-4(T+1)(2-T)=4T^2-4T-8,
\]

and hence

\[
 v^2=(2T-1)^2=u^3+9.
\]

This independently verifies the sign, the factor 2, and the target curve
`E: v^2=u^3+9`.  The source point maps to `(u,v)=(6,15)`, and
`15^2=6^3+9=225`.

The displayed integral short Weierstrass equation is nonsingular, with

\[
 \Delta=-16\cdot27\cdot9^2=-34992.
\]

For an integral torsion point with nonzero second coordinate, Nagell--Lutz
requires `v^2` to divide the discriminant.  Here `225` does not divide
`34992`.  Thus `(6,15)` is non-torsion, and `E(Q)` has positive
Mordell--Weil rank.  No exact-rank or torsion-subgroup claim is needed.

## 5. Claim boundary

The standalone note, generator docstring, JSON `claim_boundary`, theorem
proof, abstract, and final claim-boundary section are mutually consistent.
They assert:

- one nondegenerate four-hit progression in the model `((0,1,2,4),0102)`;
- positive rank of its elliptic quotient;
- closure of this one model for **existence**.

They do **not** infer that the genus-four source has infinitely many rational
points or infinitely many rational lifts of points on the quotient.  The
main manuscript explicitly distinguishes this seventh existence result from
the six previously proved infinite branches and leaves 24 models open.  This
is the correct logical boundary.

## 6. Tests and frozen certificate

The dedicated command

```text
python -W error -m unittest -v PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11_test.py
```

passes all six tests.  The suite independently checks the source identity,
AP and field witnesses, colour word, quotient identity and point,
Nagell--Lutz condition, and exact equality between regenerated certificate
data and the stored JSON.

The reviewed certificate
`code/PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11_CERTIFICATE.json` has SHA-256

```text
ae840c1ad7b332322da97bd4d59d20222411a26c506b4701bbbb40fddd41035c
```

and agrees with the current generator.  I found no mathematical or
reproducibility defect requiring an author-file change.
