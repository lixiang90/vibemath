# Round 12 novelty audit: seven consecutive squareclasses

Search date: 2026-09-04.

This report audits the theorem that an integer block `t,t+1,...,t+6` of
nonzero terms with affine squareclass rank at most two has, up to relabelling
and reversal, one of the two necessary equality patterns `0012202` and
`0012131`. It also audits the complete integer-point reduction from four
candidates to those two patterns. This is a record of sources inspected, not
proof of priority. In the material inspected, we did not locate an equivalent
theorem.

## 1. Normalized formulations that were searched

1. Relabelling squareclasses does not change the equality partition.
2. Reversal sends `t` to `-t-6` and multiplies the reversed block by `-1`.
   Common multiplication preserves affine rank and equality blocks.
3. Multiplication by a rational square preserves every squareclass. Common
   multiplication by any nonzero rational translates all seven squareclasses
   and therefore preserves affine rank.
4. Affine rank at most two is equivalent to a common rational factor `lambda`
   for which all `lambda(t+i)` are squares in a multiquadratic field of degree
   at most four. Exact rank two permits a biquadratic field. Without common
   scaling, one additional square root can raise the degree to eight.
5. A rational AP `a+di` normalizes to `t+i`, `t=a/d`, after common division by
   `d`. The theorem assumes integer `t`, so it does not classify arbitrary
   rational progressions.
6. Translation, rational dilation and reversal of AP indices identify position
   subsets in the Rudin literature. They do not preserve the fixed integer
   parameter or the requirement that all fifteen character equations hold at
   the same parameter.
7. A fractional-linear change can identify an individual genus-one quartic,
   but generally does not preserve integral `t` or simultaneous compatibility.
   Multiplying a quartic right-hand side by a rational square is a `y`-rescaling;
   multiplying it by a nonsquare is a quadratic twist.

Item 4 is the principal collision channel: the theorem can be restated as a
necessary-pattern theorem for a commonly scaled seven-term progression of
squares in a degree-at-most-four multiquadratic field.

## 2. Primary sources and exact distinctions

| Source | Normalized overlap | Difference | Risk |
| --- | --- | --- | --- |
| Balasubramanian--Luca--Thangadurai, [exact degree theorem](https://doi.org/10.1090/S0002-9939-10-10331-1), Proc. AMS 138 (2010), 2283-2288; [author PDF](https://www.hri.res.in/~thanga/papers/pamsfinal.pdf) | Exact general relation between square-product subsets and multiquadratic degree. | No consecutive block, equality partition, or integral-point reduction. | Medium overlap; high citation risk if omitted. |
| Xarles, [Squares in arithmetic progression over number fields](https://doi.org/10.1016/j.jnt.2011.07.010), JNT 132 (2012), 379-389, MR2875345; [arXiv](https://arxiv.org/abs/0909.1642) | Uniform degree-`d` bound and quadratic value `S(2)=6`. | No explicit degree-four seven-term pattern theorem. | Medium-high. |
| Gonzalez-Jimenez--Xarles, [Five squares in arithmetic progression over quadratic fields](https://doi.org/10.4171/RMI/754), RMI 29 (2013), 1211-1238, MR3148601; [arXiv](https://arxiv.org/abs/0909.1663) | Classifies five-square progressions over quadratic fields, including the `Q(sqrt(409))` example. | Degree-two/rank-at-most-one, not biquadratic rank two. | Medium-low. |
| Gonzalez-Jimenez--Xarles, [Rudin conjecture](https://doi.org/10.1112/S1461157013000259), LMS J. Comput. Math. 17 (2014), 58-76, MR3230858; [arXiv](https://arxiv.org/html/1301.5122) and [data](https://verso.mat.uam.es/~enrique.gonzalez.jimenez/research/tables/rudin/rudin.html) | Proposition 5 gives the five exceptional four-subsets of `{0,...,6}`; Corollary 6 gives `Q(6)=Q(7)=4`. | Classifies rational-square positions, not all seven squareclass equality blocks. | High positioning risk. |
| Gonzalez-Jimenez--Tho, [Squares in arithmetic progression over certain non-primitive quartic number fields](https://doi.org/10.1016/j.jnt.2025.11.005), JNT 282 (2026), 13-30; [arXiv](https://arxiv.org/html/2602.01380v1) | Studies five and six squares over certain quartic extensions. The `D=409` example gives `(7^2,13^2,17^2,409,23^2,649)` over `Q(sqrt(409),sqrt(649))`. | Uses twist-rank and class-number hypotheses and concerns existence/proper definition, not a universal necessary pattern for integer `t`. | Medium-high; it precludes any broad no-six-squares claim. |
| Gonzalez-Jimenez, [Squares in arithmetic progression over quadratic extensions of number fields](https://doi.org/10.1142/S1793042126500612), IJNT 22 (2026), 1141-1158; [arXiv](https://arxiv.org/html/2602.03251v1) | Under field-specific conditions, classifies long square APs up to square scaling and reversal. | Conditional and field-specific; extensions can have degree eight, with no seven-term rational equality-pattern classification. | Medium-high. |
| Bremner--Siksek, [Squares in arithmetic progression over cubic fields](https://arxiv.org/abs/1505.06424), IJNT 12 (2016), 1409-1414 | Excludes five-square progressions over cubic fields. | Different extension degree and no squareclass-pattern conclusion. | Low. |
| Erdos--Turk, [Products of integers in short intervals](https://doi.org/10.4064/aa-44-2-147-174), Acta Arith. 44 (1984), 147-174, MR86d:11073, Zbl 0547.10036; Granville--Selfridge, [Product of integers in an interval, modulo squares](https://doi.org/10.37236/1549), EJC 8 (2001), R5, MR1814512, Zbl 1107.11042 | Direct conceptual predecessors for square-product relations in short intervals. | Do not impose affine rank two or classify all simultaneous relations in one seven-block. | Medium conceptual overlap. |
| Saradha, [Squares in products with terms in an arithmetic progression](https://doi.org/10.4064/aa-86-1-27-43), Acta Arith. 86 (1998), 27-43; Bennett--Bruin--Gyory--Hajdu, [Powers from products of consecutive terms in arithmetic progression](https://doi.org/10.1112/S0024611505015625), PLMS 92 (2006), 273-306 | Treat perfect-power products of AP terms or blocks. | One perfect-power relation is weaker than the simultaneous relations and exact partition here. | Low-medium. |
| Bui--Pratt--Zaharescu, [Erdos-Graham-Granville-Selfridge problem](https://doi.org/10.1017/S0305004123000488), MPCPS 176 (2024), 309-323 | Connects interval subproducts to integral points on curves of the same broad form. | Distributional/minimal-endpoint results, not the exact seven-block rank problem. | Low-medium. |

The individual elementary quartic calculations therefore should not be
positioned as independently distinctive. We determine the combined finite
necessary-pattern reduction, including same-parameter compatibility of all
character equations.

## 3. OEIS and adjacent records

- [A221671](https://oeis.org/A221671) records the maximum number of rational
  squares in a nonconstant length-`n` AP and gives `a(7)=4`.
- [A216870](https://oeis.org/A216870) records the maximal five-square example
  over `Q(sqrt(409))`.
- [A099501](https://oeis.org/A099501) concerns a subset between consecutive
  squares whose product is twice a square.
- [A380998](https://oeis.org/A380998) concerns equality of ordinary integer
  subset products, not equality modulo rational squares.

Exact searches for `0012202`, `0012131`, and combinations of “rank”, “square
classes”, and “consecutive integers” did not locate a matching OEIS entry.
That negative result is not evidence of priority.

## 4. Bibliographic coverage and residual gaps

Primary journal pages, arXiv versions and author pages were used where
available, including [Xarles's publications](https://mat.uab.cat/~xarles/articles.htm),
[Gonzalez-Jimenez's research page](https://verso.mat.uam.es/~enrique.gonzalez.jimenez/research/research.html),
[Thangadurai's page](https://www.hri.res.in/people/Mathematics/thanga), and
[Granville's publication page](https://dms.umontreal.ca/~andrew/Cominator.html).
The [zbMATH author record for Granville](https://zbmath.org/authors/granville.andrew-j)
lists “Squares in arithmetic progressions” as Zbl 0771.11034 and “Product of
integers in an interval, modulo squares” as Zbl 1107.11042.

Stable complete MathSciNet search-result pages were not accessible in this
environment. The MR identifiers above were recovered from primary
bibliographies or author/journal records, but a subscription-level
MathSciNet/zbMATH citation-chain search remains advisable.

A 2024 item attributed to Nguyen Xuan Tho, “Squares in arithmetic progressions
over quadratic extensions of Q(zeta_8)”, was visible only through
[a ResearchGate record](https://www.researchgate.net/publication/384056197_SQUARES_IN_ARITHMETIC_PROGRESSIONS_OVER_QUADRATIC_EXTENSIONS_OF_Qz_8).
No authoritative full text was available for theorem-level comparison. Its
title suggests degree eight rather than the degree-four setting here, but it
remains an unresolved bibliographic gap and is not used as authority.

## 5. Risk assessment and safe claim

| Risk | Level | Consequence |
| --- | --- | --- |
| Exact duplicate of the two-pattern theorem | Low, not zero | No equivalent statement was located, but negative search is not proof. |
| Equivalent commonly scaled seven-square AP over a biquadratic field | Medium-high | Use this formulation in further searches and referee-facing comparison. |
| Omission of foundational or recent work | High if uncited | Cite BLT 2010, Xarles 2012, Gonzalez-Jimenez--Xarles 2013/2014, and both 2026 papers. |
| OEIS collision | Low | Nearby sequences concern square positions or ordinary products. |
| Database/full-text coverage gap | Medium | Complete the subscription search and obtain the 2024 Tho item before any priority wording. |

Safe formulation:

> We determine an exact necessary equality-pattern classification for seven
> consecutive nonzero integers whose rational squareclasses have affine rank
> at most two, and use complete integer-point calculations with same-parameter
> checks to reduce the candidates to two. In the sources inspected, we did not
> locate an equivalent statement.

This wording does not assert realizability of either survivor, does not decide
`R_2(7)`, and does not claim a classification of arbitrary rational
progressions or of all square progressions over quartic fields.
