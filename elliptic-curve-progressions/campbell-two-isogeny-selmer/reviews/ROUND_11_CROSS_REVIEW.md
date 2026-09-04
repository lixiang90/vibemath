# Round 11 cross-review: two-isogeny Selmer audit

## Verdict

**PASS.** I found no blocking mathematical or reproducibility defect in the
Round 11 two-isogeny Selmer audit.  The certified conclusions are exactly

\[
\operatorname{Sel}^{(\widehat\phi)}(E'/\mathbf Q)
 =\langle 3,5,7\rangle,
 \qquad
\operatorname{Sel}^{(\phi)}(E/\mathbf Q)
 =\langle 59\cdot71699,339106321\rangle,
\]

of orders (8) and (4), respectively, and hence

\[
2^{\operatorname{rank}E(\mathbf Q)}
 \le \frac{8\cdot4}{2\cdot2}=8,
\qquad \operatorname{rank}E(\mathbf Q)\le3.
\]

This is an upper bound only.  The materials do not identify the exact rank,
the full (2)-Selmer group, a Cassels--Tate pairing, or a ninth rational
point.

## Evidence reviewed

I cross-checked `paper/main.tex`, the Round 9--11 reports, the Round 9--11
Python validators and tests, `certificates/local_matrix_512.json`, and
`certificates/round11_isogeny_selmer_audit.json`.  The Round 11 unit suite was
also rerun independently: all eight tests passed (`Ran 8 tests in 81.630s`,
`OK`).

## Support and the complete set of places

The support lemma is correct.  For a squarefree representative (d), if
(p\nmid b) and (v_p(d)=1), a primitive local solution of

\[
N^2=dU^4+aU^2V^2+(b/d)V^4
\]

cannot exist.  If (V) is a unit, the last term has the unique odd valuation
(-1); if (p\mid V), primitivity forces (U) to be a unit and the first
term has the unique odd valuation (1).  Either case contradicts the parity
of the valuation of a square.  This valuation argument also covers (p=2).

The coefficient identities and factorizations were checked:

\[
\begin{aligned}
a&=-591895071, & b&=2^{18}3^{12}5^2 7^5,\\
a'&=-2a, & b'&=a^2-4b=3^4\cdot59\cdot71699\cdot339106321,\\
(a')^2-4b'&=16b.
\end{aligned}
\]

Consequently the union of the finite support on the two isogenous curves is
exactly

\[
S_f=\{2,3,5,7,59,71699,339106321\},
\]

and the complete set of places to check is (S=S_f\cup\{\infty\}).  No bad
prime is omitted.

For (p\notin S_f), the quartic discriminant identity

\[
\operatorname{disc}_T(dT^4+aT^2+b/d)=16b(a^2-4b)^2
\]

shows good reduction.  The proper smooth geometrically connected genus-one
model has an (\mathbf F_p)-point by the Hasse bound (all such primes here are
at least (11)); smooth lifting then gives a (\mathbf Q_p)-point.  Thus the
finite local work at the displayed seven primes is exhaustive.

## Exact local conditions and witnesses

On the (E)-side, the real condition removes all negative squareclasses and
the exact (\mathbf Q_{59}) condition removes the remaining positive
even-supported classes, leaving precisely

\[
\{1,3,5,7,15,21,35,105\}=\langle3,5,7\rangle.
\]

On the (E')-side, the exact conditions used in the certificate are

\[
d\equiv1\pmod8,
\qquad v_3(d)=0,
\qquad d\equiv1\pmod3,
\]

and their intersection leaves precisely

\[
\{1,4230241,339106321,1434501462453361\}
 =\langle4230241,339106321\rangle,
\]

where (4230241=59\cdot71699).  These are exact local classifications, not
bounded searches for small witnesses.

For each of the twelve survivor rows, all seven finite positive cells were
revalidated, giving (12\cdot7=84) checks.  In every cell the stored status is
`YES`, the stored pair ((U,V)) is primitive at the relevant prime, the
quartic right-hand side recomputes exactly, and its (\mathbf Q_2) or odd
(\mathbf Q_p) square criterion holds.  The twelve rows mean only the eight
(E)-side rows plus the four (E')-side rows; they are not a twelve-element
Selmer set.

Both displayed survivor sets contain the identity and are closed under
squareclass multiplication.  Their orders (8) and (4) therefore give
dimensions (3) and (2) over (\mathbf F_2).

## Isogeny direction and rank bound

The direction conventions are consistent.  For

\[
E:y^2=x^3+ax^2+bx,
\]

the degree-two map to (E') is

\[
\phi(x,y)=\left(\frac{y^2}{x^2},
 \frac{y(b-x^2)}{x^2}\right),
\]

and the dual map back to (E) is

\[
\widehat\phi(X,Y)=\left(\frac{Y^2}{4X^2},
 \frac{Y((a^2-4b)-X^2)}{8X^2}\right).
\]

Substitution verifies both target equations and that the composition has the
doubling (x)-coordinate.  The quartic cover attached to the (E)-side maps
to (E) and represents (\operatorname{Sel}^{(\widehat\phi)}(E'/\mathbf Q));
the (E')-side cover represents (\operatorname{Sel}^{(\phi)}(E/\mathbf Q)).

The exact-sequence identity used for the rank is

\[
2^r=
\frac{|E'(\mathbf Q)/\phi E(\mathbf Q)|\,
      |E(\mathbf Q)/\widehat\phi E'(\mathbf Q)|}
     {|E[\phi](\mathbf Q)|\,|E'[\widehat\phi](\mathbf Q)|}.
\]

Each rational kernel is (\{O,(0,0)\}), so both denominator factors are
exactly (2).  The two Mordell--Weil quotients inject into the corresponding
isogeny Selmer groups of orders (8) and (4).  This proves (r\le3), with
no converse assertion and no claim that either Selmer upper bound is attained
by the Mordell--Weil quotient.

## Nonblocking observations

The good-prime statement in the paper uses the weaker threshold (p\ge5);
outside the actual support the first possible prime is (11), so this causes
no gap.  The audit certificate records the kernel orders numerically, while
their value is also independently visible from the standard degree-two
isogenies and the rational points ((0,0)) on the two models.
