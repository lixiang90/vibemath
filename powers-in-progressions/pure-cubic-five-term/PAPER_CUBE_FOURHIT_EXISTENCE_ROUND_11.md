# Round 11 continuation: one 0102 orbit closed for existence

Date: 2026-09-04. Author: Codex (GPT-5.6-sol). Status: **one further genus-four model has a proved
nonconstant, nonzero four-hit progression; its natural elliptic quotient has
positive rank**.

This is an existence closure, not a rational-point classification and not an
infinite-family theorem.

## 1. Exact model

For the model on positions (0,1,2,4) with canonical word 0102, positions
0 and 2 have the repeated color. Put \(A_0=X^3\), \(A_2=Y^3\). Then

\[
 A_1=(X^3+Y^3)/2,\qquad A_4=2Y^3-X^3.
\]

The two singleton terms lie in inverse Kummer classes precisely when

\[
 C:\quad (X^3+Y^3)(2Y^3-X^3)=2W^3.                 \tag{1}
\]

Equivalently,

\[
 -2X^6+2X^3Y^3+4Y^6-4W^3=0
\]

in \(\mathbf P(1,1,2)\). Its normalization is the smooth genus-four curve
already reconstructed in Round 09.

The exact point

\[
 (X:Y:W)=(2:1:-3)
\]

satisfies (1). It gives the rational AP

\[
 (8,9/2,1,-5/2,-6).
\]

Multiplication by the rational cube \(8\) preserves all pure-cubic hit
conditions and gives the integer AP

\[
 (64,36,8,-20,-48),\qquad d=-28.                 \tag{2}
\]

## 2. Four hits over a genuine cubic field

Let \(K=\mathbf Q(\alpha)\), \(\alpha^3=6\). The polynomial \(T^3-6\) is
Eisenstein at 2, so \([K:\mathbf Q]=3\). In (2),

\[
 64=4^3,\qquad 36=(\alpha^2)^3,\qquad
 8=2^3,\qquad -48=(-2\alpha)^3.
\]

Thus positions \(0,1,2,4\) are cubes in \(K\). Their raw classes modulo
\(\langle6\rangle\subset\mathbf Q^\times/\mathbf Q^{\times3}\) are
0201; the allowed color automorphism \(c\mapsto2c\) gives 0102.

The omitted term is not a cube in \(K\). By the paper's Kummer-kernel lemma,
a rational number whose cube root lies in \(K\) has class in
\(\{1,6,36\}\mathbf Q^{\times3}\). Every such class has 5-adic valuation
zero modulo 3, whereas \(v_5(-20)=1\). Hence \(-20\notin K^3\).

All five entries in (2) are nonzero and pairwise distinct, and the common
difference is nonzero. This proves a legal, nondegenerate four-hit AP for the
specified model.

## 3. Strict positive-rank quotient certificate

On \(Y\ne0\), put

\[
 u=-2W/Y^2,\qquad v=2(X/Y)^3-1.
\]

Equation (1) gives the exact identity

\[
 E:\quad v^2=u^3+9.                              \tag{3}
\]

The source point maps to \(P=(6,15)\). The integral equation (3) has
discriminant

\[
 \Delta=-16\cdot27\cdot9^2=-34992.
\]

Since \(15\ne0\) and \(15^2=225\nmid34992\), Nagell--Lutz proves that \(P\)
is non-torsion. Therefore the quotient has positive Mordell--Weil rank.

This does **not** imply infinitely many rational points on \(C\): a
positive-rank quotient of a genus-four curve need not have infinitely many
rational lifts. The result closes this orbit only in the explicitly stated
existence sense.

## 4. Reproduction and search boundary

- PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11.py recomputes the curve, progression,
  Kummer colors, omitted-term valuation obstruction, quotient identity, and
  Nagell--Lutz certificate.
- PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11_test.py independently expands the
  source and quotient identities, reconstructs the AP, checks the four cube
  witnesses, checks the valuation-vector obstruction and field degree, and
  rechecks the stored JSON.
- PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11_CERTIFICATE.json is the frozen exact
  certificate.

Low-height searches used to choose this orbit are discovery evidence only.
No search non-hit is used in the theorem.
