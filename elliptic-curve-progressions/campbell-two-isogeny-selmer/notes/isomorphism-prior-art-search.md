# Isomorphism-class prior-art audit

Search date: 2026-09-03.

## Exact identification data

The audited global minimal model is

```text
[a1,a2,a3,a4,a6] = [1,-16441530,0,45166889779200,0]
Delta_min = 2926451742397178075653974744686961623040000
N = 301245307115205810
c4 = 2157171698920561
j = 10038160648206649953061393462836377818780518481
    /2926451742397178075653974744686961623040000.
```

The original Campbell-Jacobian model is explicitly Q-isomorphic through
`x_original=36*x_minimal`,
`y_original=216*y_minimal+108*x_minimal`.

## Queries

Exact web, publisher/full-text, arXiv-facing and accessible-database queries:

```text
"16441530" "45166889779200" elliptic
"301245307115205810" elliptic curve
"2157171698920561" elliptic curve
"10038160648206649953061393462836377818780518481"
site:arxiv.org "301245307115205810" elliptic
site:arxiv.org "16441530" "45166889779200"
site:cs.uwaterloo.ca/journals/JIS Campbell "301245307115205810"
"2926451742397178075653974744686961623040000" elliptic
"59" "71699" "339106321" "elliptic curve"
site:lmfdb.org/EllipticCurve/Q/ "301245307115205810"
```

No indexed mathematical match was returned.

The following sources were also checked directly:

- Garikai Campbell, *A Note on Arithmetic Progressions on Elliptic Curves*,
  JIS 6 (2003), Article 03.1.3:
  https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html
- the accessible full PDF of the same article:
  https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.pdf
- Campbell's 1999 Rutgers dissertation, *Finding Elliptic Curves and
  Families of Elliptic Curves over Q of Large Rank*:
  https://ctnt-summer.math.uconn.edu/wp-content/uploads/sites/1632/2020/06/Campbell-Finding-elliptic-curves-and-families-of-elliptic-curves-over-Q-of-large-rank.pdf
- LMFDB's official rational-elliptic-curve completeness statement:
  https://www.lmfdb.org/EllipticCurve/Q/Completeness
- the EuDML record and bibliography metadata for Campbell's article:
  https://eudml.org/doc/50342
- the surviving biographical/author-page mirror that links Campbell's former
  Swarthmore page and identifies the 1999 dissertation:
  https://www.math.buffalo.edu/mad/PEEPS/campbell_garikai.html

Campbell's Article 03.1.3 contains the family and the genus-one parameter
curve `D`; Proposition 2.6 computes the rank of `D`.  It does not display the
index-8 quartic `H`, its Jacobian above, or either of the two isogeny Selmer
groups in this project.  The 1999 dissertation search likewise returned no
occurrence of the original or minimal coefficients; it predates the 2003
article.

## Database boundary

The author-page mirror did not expose a publication list beyond the already
located article and dissertation.  The LMFDB page states completeness for all conductors below 500,000, all
7-smooth conductors, and prime conductors up to 300,000,000.  The conductor
here is composite, has prime factors `59`, `71699`, and `339106321`, and is
about `3.0e17`.  It lies outside each complete family.  Consequently no
LMFDB label is assigned and a missing row is not evidence of novelty.

## Permitted conclusion

The search supports only the statement that no indexed prior computation of
this **specific Q-isomorphism class and its two displayed isogeny Selmer
groups was found by the recorded searches as of the date above**.  It does
not prove priority.  The narrow finite theorem remains the only safe novelty
claim; human inspection of non-indexed notes and the complete citation graph
is still required before any “first” language could be considered.
