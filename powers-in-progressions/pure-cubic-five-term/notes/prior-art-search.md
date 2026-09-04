# Prior-art search record

Search dates: 2026-09-03 and 2026-09-04. Result status: **no equivalent
formulation or construction located in the accessible search results;
HIGH-CAUTION**. This is not a proof of priority. The Round-12 details,
including normalized searches for the explicit seventh-orbit witness, are in
../ROUND_12_CUBE_NOVELTY_AUDIT.md.

## Target formulation searched

For a nonconstant rational AP `A_i=a+id`, determine the maximum number of
nonzero positions for which one common `lambda in Q*` makes `lambda A_i` a cube
in a single nontrivial pure cubic field `Q(cuberoot(D))`. The exact five-term
equations searched were

```text
D^c0*x0^3 - 2*D^c1*x1^3 + D^c2*x2^3 = 0
D^c1*x1^3 - 2*D^c2*x2^3 + D^c3*x3^3 = 0
D^c2*x2^3 - 2*D^c3*x3^3 + D^c4*x4^3 = 0
```

modulo affine color change in `F_3`, radicand inversion and reversal.

## Exact queries

The web/arXiv-facing searches included:

```text
"R_(3,1)" arithmetic progression cube
"R^\\times_{(3,1)}"
"common rational scaling" cubes "pure cubic field"
"five-term arithmetic progression" cubes "number field"
"pure cubic field" cubes "arithmetic progression"
"cubes in a pure cubic field" arithmetic
"Kummer" "arithmetic progression" cubes number field
"Q(cuberoot" arithmetic progression cubes Kummer
"D^{c_i}" "x_i^3" arithmetic progression
"x0^3-2" "x1^3" "x2^3" pure cubic field
"A_i=a+id" "pure cubic" cube
"five-hit" cubes arithmetic progression
```

The notation-only query produced unrelated uses of `R_(3,1)`, illustrating why
the prose and equation queries are more informative. None of the accessible
results stated the target maximum or the 25-orbit/60-model theorem.

## Nearest relevant hits

- Gonzalez-Jimenez--Xarles, DOI <https://doi.org/10.4171/RMI/754>, is the
  closest methodological predecessor. Their five-squares problem over
  quadratic fields already uses Kummer types, common scaling, reversal,
  curves over Q, and local-solubility arguments. The present exponent,
  field, ternary colors, and partial-hit theorem differ, but the general
  type/scaling/reversal strategy must not be presented as originating here.
- Darmon--Merel, DOI <https://doi.org/10.1515/crll.1997.490.81>, proves the
  equal-exponent three-term obstruction actually used here.
- Hajdu--Tengely, DOI <https://doi.org/10.1007/s11139-020-00331-5>, studies the
  ordinary integer-power density function and proves the `N<20` cube values;
  it does not formulate the common-scale pure-cubic Kummer variant.
- Hajdu--Tengely, “Arithmetic progressions of squares, cubes and n-th powers,”
  arXiv:0707.0593, treats primitive integer progressions of prescribed unlike
  powers, not rational terms becoming cubes in one pure cubic field.
- Bruin--Győry--Hajdu--Tengely, “Arithmetic progressions consisting of unlike
  powers,” arXiv:math/0512419, proves finiteness/classification results for
  integer progressions with bounded assigned exponents, again a different
  condition.
- Gonzalez-Jimenez, DOI <https://doi.org/10.1007/s00013-010-0166-5>, studies
  three cubes in AP over quadratic fields, rather than four partial hits among
  five rational entries after a common scale in a pure cubic field.
- Xarles, DOI <https://doi.org/10.1016/j.jnt.2011.07.010>, gives
  degree-dependent bounds for complete progressions of powers over number
  fields, not the present exact partial-hit maximum.
- Bremner--Siksek, DOI <https://doi.org/10.1142/S179304211650086X>, exclude
  five squares in a cubic field; the exponent and power condition differ.
- “Arithmetic progressions in certain subsets of finite fields,” *Finite Fields
  and Their Applications* **91** (2023), 102264, DOI
  <https://doi.org/10.1016/j.ffa.2023.102264>, counts APs among finite-field
  squares/cubes. It is context for finite-field cube sets, not the number-field
  Kummer problem and is not used in the proof.

## Round-12 database status and required follow-up

zbMATH Open was searched at metadata level for exact titles and broader
cube/AP combinations. No equivalent record was located, but the interface is
not a full-text equation search. MathSciNet article, author, title, and
all-fields routes redirected to a LibLynx institutional-authentication page,
so its database records and citation graph were not reviewed.

Before any priority assertion, complete an authenticated MathSciNet search,
review the forward-citation chain of Gonzalez-Jimenez--Xarles (2013), search
full text for expanded/permuted forms of the source equation, inspect theses
and non-English sources, and ask a specialist in Diophantine equations or
arithmetic progressions of powers. The manuscript uses descriptive theorem
language only.


## Round-11 existence-result boundary

The exact model \(((0,1,2,4),0102)\), its curve
\((X^3+Y^3)(2Y^3-X^3)=2W^3\), and the progression
\((64,36,8,-20,-48)\) over \(\mathbf Q(\sqrt[3]{6})\) were searched together
with the source tuple, primitive scaled tuple, reversal, and the isomorphic
radicand line represented by 36. No equivalent construction was located in
the accessible sources. MathSciNet authentication, forward-citation review,
and a complete full-text formula search remain unresolved; the result is
therefore stated only as verified existence. The unreviewed rank-zero
quotient notes are not incorporated into the manuscript theorem or novelty
claim.
