# Round 10: the second 3+1 cluster has positive rank

Date: 2026-09-04. Status: **the two models attached to
3X^3-4Y^3+Z^3=0 are proved to contain infinitely many inequivalent
four-hit progressions.**

No bounded search or heuristic rank enters the proof. A small signed search
was used only to discover the point (5:2:-7); every assertion below is
instead certified by exact identities, the group law, and Nagell--Lutz.

## 1. The two models and their common curve

The Round-09 reconstruction has exactly two models in the cluster

    3+1 | canonical coefficient key (1,-4,3):
      ((0,1,2,4),0010)
      ((0,1,3,4),0010).

In both models, positions 0,1,4 have the repeated color. Write

\[
 A_0=X^3,\qquad A_1=Y^3,\qquad A_4=Z^3.
\]

The five-term AP relation \(A_4=4A_1-3A_0\) is precisely

\[
 C:\qquad 3X^3-4Y^3+Z^3=0.                       \tag{1}
\]

Conversely a point of (1) gives

\[
 (A_0,\ldots,A_4)=
 (X^3,Y^3,2Y^3-X^3,3Y^3-2X^3,Z^3).              \tag{2}
\]

Thus the reduction loses no information. The partial derivatives of (1)
are \(9X^2,-12Y^2,3Z^2\), with no common projective zero, so \(C\) is a
smooth genus-one curve. We use \(O=(1:1:1)\) as origin.

## 2. Exact diagonal-cubic map

Put

\[
\begin{aligned}
N&=12X^3Y^3+4Y^3Z^3-3Z^3X^3,\\
T&=(3X^3+4Y^3)(-4Y^3-Z^3)(Z^3-3X^3).
\end{aligned}
\]

On \(XYZ\ne0\), define

\[
 \phi(X:Y:Z)=
 \left(\frac{N}{X^2Y^2Z^2},
       -\frac{T}{2X^3Y^3Z^3}\right)=(u,v).       \tag{3}
\]

Exact multivariate division in the certificate script proves

\[
 T^2-4N^3+3888X^6Y^6Z^6
 =(3X^3-4Y^3+Z^3)H(X,Y,Z),                       \tag{4}
\]

with zero remainder. Hence (3) lands on

\[
 E:\qquad v^2=u^3-972.                            \tag{5}
\]

There are no rational points of \(C\) with \(XYZ=0\): the three cases would
make one of \(4,-3,4/3\) a rational cube. In any case, (3), as a rational
map from a smooth projective curve to the proper curve \(E\), extends through
its finitely many apparent exceptional points.

Now take

\[
 P=(5:2:-7)\in C(\mathbf Q),\qquad Q=(13,35)\in E(\mathbf Q).
\]

Exact substitution gives

\[
 \phi(O)=(13,-35)=-Q,
\]

and the tangent formula at \(Q\), whose slope is \(507/70\), gives

\[
 \phi(P)=
 \left(\frac{129649}{4900},
       -\frac{45441143}{343000}\right)=2Q.        \tag{6}
\]

The discriminant of the displayed integral equation (5) is

\[
 \Delta=-16\cdot27\cdot972^2=-2^8 3^{13}.
\]

Since \(Q\) is integral, has nonzero second coordinate, and
\(35^2=1225\nmid\Delta\), Nagell--Lutz proves that \(Q\) has infinite
order. Translate \(\phi\) by \(-\phi(O)\). It is nonconstant by (6), sends
origins to origins, and therefore is an isogeny of genus-one curves. It
sends \(P-O\) to \(2Q-(-Q)=3Q\), which is non-torsion. Thus \(P-O\) is
non-torsion and \(C(\mathbf Q)\) has positive rank.

The certificate also implements the exact chord law on (1). Its tangent at
\(O\) has third intersection \(P\), and the first seven multiples of \(P-O\)
are verified to be distinct points of \(C(\mathbf Q)\). This finite check is
a regression test, not the proof of infinite order; Nagell--Lutz is the
proof.

## 3. Two infinite four-hit families

Let

\[
 P_n=O+n(P-O)=(X_n:Y_n:Z_n),\qquad n\in\mathbf Z.
\]

These points are pairwise distinct. For \(n\ne0\), (2) is nonconstant:
\(X_n^3=Y_n^3\) would force \(X_n=Y_n=Z_n\), hence \(P_n=O\).
The entries at positions \(0,1,4\) are nonzero by the preceding coordinate
argument. The two middle entries are also nonzero: their vanishing would
make \(2\) or \(3/2\) a rational cube.

Neither middle entry is a rational cube. Otherwise (2) would have four
rational cubes among five positions, contradicting the cited exact bound
\(P_5(3)=3\) of Hajdu--Tengely. Choose positive cube-free representatives
\(D_{2,n}\) and \(D_{3,n}\) of their respective rational cube classes.
The Kummer-kernel lemma already proved in the paper then shows:

- over \(\mathbf Q(\sqrt[3]{D_{2,n}})\), positions \(0,1,2,4\) have colors
  0010;
- over \(\mathbf Q(\sqrt[3]{D_{3,n}})\), positions \(0,1,3,4\) have colors
  0010.

Both fields are genuinely cubic because neither class is trivial. The
paper's main theorem \(R^\times_{(3,1)}(5)=4\) excludes the uncounted position
in either construction, so these are exactly four-hit progressions rather
than unverified partial patterns.

Distinct points of \(C(\mathbf Q)\) give distinct progressions up to common
rational scaling: comparing any one of positions \(0,1,4\) makes the scale a
rational cube, and injectivity of cubing over \(\mathbf Q\) recovers the same
projective point. Reversal has fibers of size at most two. Hence each of
the two models contains infinitely many equivalence classes.

At \(P=(5:2:-7)\), (2) is the integer AP

    (125, 8, -109, -226, -343), common difference -117.

If \(\alpha^3=109\), then positions \(0,1,2,4\) are the cubes of
\(5,2,-\alpha,-7\). If \(\beta^3=226\), then positions \(0,1,3,4\) are the
cubes of \(5,2,-\beta,-7\). Exact cube-class tests give

    D=109: [0,0,1,none,0]
    D=226: [0,0,none,1,0].

The valuations at 109 and 113 already distinguish the two omitted rational
classes in this example; the global four-hit theorem provides the uniform
exclusion for the entire Mordell--Weil family.

## 4. Claim boundary

This round closes exactly the two models in the second 3+1 cluster. With
the four earlier branches, six of the original 31 four-hit models are now
proved positive-rank, leaving 25 open. It does not determine the exact rank,
torsion subgroup, or generators of \(C(\mathbf Q)\), and it does not classify
any genus-four cluster. The Round-09 permutation keys remain reuse
certificates only; they are not asserted to be complete
\(\mathbf Q\)-isomorphism invariants.

The dated prior-art audit has not found this exact partial-hit formulation,
but database-level novelty screening remains pending. Consequently this
result is presented as a proved mathematical extension, not as a certified
priority claim.

## 5. Reproduction

Files:

- code/PAPER_CUBE_FOURHIT_3PLUS1_ROUND10.py: exact map, group law, cube
  classes, sample multiples, and certificate generator;
- code/PAPER_CUBE_FOURHIT_3PLUS1_ROUND10_test.py: seven independent tests;
- code/PAPER_CUBE_FOURHIT_3PLUS1_ROUND10_CERTIFICATE.json: frozen exact
  certificate, SHA-256
  1bdadc0c5afa58d69d1d8803a4e23149f0140af5fee1d52a1a1f028ff8963687.

Run from the code directory:

    python -m unittest -v PAPER_CUBE_FOURHIT_3PLUS1_ROUND10_test.py

The discovery search is deliberately absent from the proof certificate.
