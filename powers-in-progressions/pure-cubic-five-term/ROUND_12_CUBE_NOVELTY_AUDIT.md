# Round 12 cube novelty audit

Date: 2026-09-04

Decision: **HIGH-CAUTION.** No equivalent construction was located in the
sources accessible during this audit. This is a search result, not a proof of
priority. MathSciNet, the complete forward-citation chain, and full-text
formula searches remain incomplete.

## Target and equivalence normalization

The Round-11 witness is

    (64,36,8,-20,-48),  d=-28,  K=Q(alpha),  alpha^3=6.

The four hits are 64=4^3, 36=(alpha^2)^3, 8=2^3, and
-48=(-2 alpha)^3. The omitted term is not a cube: the rational classes dying
in K*/K*3 are 1,[6],[36], all with 5-adic valuation zero modulo 3, whereas
v_5(-20)=1. This proves strict existence in ((0,1,2,4),0102), not an
infinite family on its genus-four source.

Searches included the source tuple (8,9/2,1,-5/2,-6), the primitive tuple
(16,9,2,-5,-12), the reversal (-12,-5,2,9,16), scaled/reversed forms, and
(X^3+Y^3)(2Y^3-X^3)=2W^3 in factored, expanded, and elementary
variable-swapped forms. The reversed integer tuple alone has many elementary
AP search hits, none involving cubes in a number field; it is not a reliable
bibliographic fingerprint.

Lesavourey--Plantard--Susilo, "Short Principal Ideal Problem in multicubic
fields," J. Math. Cryptol. 14 (2020), 359--392, DOI
<https://doi.org/10.1515/jmc-2019-0028>, Lemma 3.1, states that for noncubes
p,q, Q(cuberoot(p))=Q(cuberoot(q)) exactly when p=q a^3 or p=q^2 a^3.
Thus the field search covered the radicand lines represented by 6 and 36.
Changing [6] to [36]=[6]^2 takes the raw hit colors 0201 to 0102.

Only common scaling and reversal are AP equivalences here. A general
coordinate or factor permutation need not preserve the ordered AP positions.
The Round-09 permutation clusters are reuse identifications, not a complete
classification of equivalent constructions over Q.

## Closest methodological predecessor

Gonzalez-Jimenez--Xarles, "Five squares in arithmetic progression over
quadratic fields," Rev. Mat. Iberoam. 29 (2013), 1211--1238, DOI
<https://doi.org/10.4171/RMI/754>, arXiv:0909.1663,
[publisher record](https://ems.press/journals/rmi/articles/12398),
[publisher PDF](https://ems.press/content/serial-article-files/38451),
[zbMATH Zbl 1362.11013](https://zbmath.org/6260624), is the strongest
methodological predecessor found.

That paper already encodes square classes by binary Kummer types, identifies
common rational-square or D-times-square scaling, quotients by reversal,
reduces the typed problem to curves over Q, and applies rational-point and
local-solubility methods. The present theorem differs in exponent 3, pure
cubic fields, ternary colors, and a partial-hit maximum rather than five
square terms. These are precise mathematical differences, but the general
type/color, scaling, reversal, curve, and local-obstruction strategy must not
be presented as originating in this manuscript.

## Other directly relevant primary literature

- Gonzalez-Jimenez, "Three cubes in arithmetic progression over quadratic
  fields," Arch. Math. 95 (2010), 233--241, DOI
  <https://doi.org/10.1007/s00013-010-0166-5>,
  [arXiv](https://arxiv.org/abs/0909.0227),
  [zbMATH](https://zbmath.org/5797321): three full cube terms with roots in a
  quadratic field, not four partial hits among five rational entries after a
  common scale in a pure cubic field.
- Hajdu--Tengely, "Powers in arithmetic progressions," Ramanujan J. 55
  (2021), 965--986, DOI
  <https://doi.org/10.1007/s11139-020-00331-5>,
  [zbMATH](https://zbmath.org/7383300): literal integer powers in integer APs;
  it supplies the ordinary-cube bound but has no number-field Kummer classes.
- Hajdu--Tengely, "Arithmetic progressions of squares, cubes and n-th
  powers," [arXiv](https://arxiv.org/abs/0707.0593),
  [zbMATH](https://zbmath.org/5654314), and Bruin--Gyory--Hajdu--Tengely,
  "Arithmetic progressions consisting of unlike powers,"
  [arXiv](https://arxiv.org/abs/math/0512419): primitive integer APs with
  literal prescribed powers, not partial Kummer hits.
- Xarles, "Squares in arithmetic progression over number fields," J. Number
  Theory 132 (2012), 379--389, DOI
  <https://doi.org/10.1016/j.jnt.2011.07.010>,
  [arXiv](https://arxiv.org/abs/0909.1642),
  [zbMATH](https://zbmath.org/6005605): degree-dependent bounds for complete
  power progressions, not this exact partial-hit maximum.
- Bremner--Siksek, "Squares in arithmetic progression over cubic fields,"
  Int. J. Number Theory 12 (2016), 1409--1414, DOI
  <https://doi.org/10.1142/S179304211650086X>,
  [arXiv](https://arxiv.org/abs/1505.06424),
  [zbMATH](https://zbmath.org/6589285): five squares in cubic fields; the
  exponent and field-power condition differ.
- Argaez-Garcia, "On perfect powers that are sums of cubes of a five term
  arithmetic progression," [arXiv](https://arxiv.org/abs/1901.05382),
  [zbMATH](https://zbmath.org/7055471): a power represented by a sum of
  cubes, not cube positions in a field.

## Coverage, gaps, and permitted wording

The search covered web-indexed scholarly pages, arXiv, publisher pages,
relevant author publication pages, and zbMATH Open metadata. A broad zbMATH
"arithmetic progressions cubes" query returned 48 records; focused
cubic-field and five-term queries returned only distinct problems such as
those above. Metadata non-hits do not search every equation in papers,
theses, books, non-English sources, or unindexed notes.

MathSciNet article, author, title, and all-fields URLs all redirected to a
LibLynx "Where Are You From" institutional-authentication page. Its records
and citation graph were therefore not reviewed. Search-engine-visible MR
identifiers do not replace that database search.

Before any priority assertion: (1) run authenticated MathSciNet searches;
(2) review the complete forward-citation chain of Gonzalez-Jimenez--Xarles
(2013); (3) search full text for expanded/permuted source equations and all
normalized AP tuples; and (4) inspect theses and non-English sources and
obtain a specialist bibliographic check.

Permitted description: the manuscript determines the stated exact maximum,
exhausts five-hit color classes through 25 orbits and 60 certified local
obstructions, proves six stated infinite branches, and exhibits strict
existence in the seventh stated model. It makes no priority claim. The exact
record is: **no equivalent construction located in accessible sources;
bibliographic clearance incomplete; HIGH-CAUTION.**
