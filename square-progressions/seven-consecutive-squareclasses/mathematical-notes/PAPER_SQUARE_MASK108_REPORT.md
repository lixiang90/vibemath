# Mask 108 integral-point gate

The mask has support `{2,3,5,6}` and curve

\[
y^2=(t+2)(t+3)(t+5)(t+6).
\]

Set `A=(t+2)(t+6)` and `B=(t+3)(t+5)=A+3`.  For `t<=-7` or
`t>=-1`, both are positive and `gcd(A,B)|3`.  If `AB` is a square, their
common positive squarefree kernel is `d=1` or `3`.

- `d=1`: `V²-U²=3`, so the only positive same-parity factor pair is
  `(V-U,V+U)=(1,3)`.  Hence `(U,V)=(1,2)`, but `A=1` gives
  `(t+4)²=5`, impossible modulo 8.
- `d=3`: `V²-U²=1`, so the only nonnegative factor pair is `(1,1)`,
  forcing `U=0`, incompatible with `A>0`.
- At the five remaining integers `t=-6,...,-2`, direct evaluation gives
  the complete list below.

Therefore

\[
H_{108}(\mathbb Z)={(-6,0),(-5,0),(-4,-2),(-4,2),(-3,0),(-2,0)}.
\]

Every listed parameter makes one of the original seven consecutive integers
zero, so there is no nondegenerate parameter.  Mask 108 occurs in 12 of the 35
input patterns; those 12 are strictly excluded and 23 remain.  The exact IDs,
upstream hashes and five machine checks are in
`PAPER_SQUARE_MASK108_CERTIFICATE.json`.

