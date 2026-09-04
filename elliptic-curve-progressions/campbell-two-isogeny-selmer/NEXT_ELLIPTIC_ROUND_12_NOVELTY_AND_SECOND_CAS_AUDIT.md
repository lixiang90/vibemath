# Round 12: novelty and independent-CAS audit

Audit date: 2026-09-04. This is a coverage-limited audit, not a proof of
priority. No Sage, Magma, PARI/GP, or remote CAS was run in this round.

## Result and contribution boundary

Campbell's 2003 article constructs the cubic Weierstrass family with eight
prescribed square values. It gives the parameter curve `D` and reports that
`D` has rank 2; it does not compute the Jacobian of the later index-8
ninth-value quartic `H`, either rational 2-isogeny Selmer group, or the rank
of that Jacobian.

Campbell's 1999 Rutgers dissertation is a decisive method-priority source.
For `y^2=x^3+a*x^2+b*x` it records the standard rational 2-isogeny, dual
curve, coverings `z^2=d*u^4+a*u^2*v^2+(b/d)*v^4`, the two Selmer groups,
rank formula, and GP local-test routines. The method is therefore not claimed
as new. The defensible contribution is the exact, certificate-backed target
computation

```text
Sel^(hat(phi))(E'/Q) = {1,3,5,7,15,21,35,105},
Sel^phi(E/Q) = {1,4230241,339106321,1434501462453361},
rank E(Q) <= 3.
```

This is only a rank upper bound. Campbell's rank-2 parameter curve is distinct
from this Jacobian.

## Sources and searches

- Campbell article: *Journal of Integer Sequences* 6 (2003), 03.1.3,
  <https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html>.
- Campbell dissertation: *Finding Elliptic Curves and Families of Elliptic
  Curves over Q of Large Rank*, Rutgers University, 1999,
  <https://ctnt-summer.math.uconn.edu/wp-content/uploads/sites/1632/2020/06/Campbell-Finding-elliptic-curves-and-families-of-elliptic-curves-over-Q-of-large-rank.pdf>.
- Free MathSciNet MR Lookup identifies MR1971433, reviewer Joe P. Buhler,
  MSC 11G05 (11D25). The complete subscription citation graph was unavailable.
- zbMATH Open identifies Zbl 1022.11026 / document 1919531. Its review and
  structured reverse-review results contain no target computation. Old
  reference metadata are incomplete, so this is not exhaustive.
- Exact invariant and coefficient searches found no indexed target
  computation. They can miss alternate presentations and unpublished code.
- LMFDB's published complete ranges are conductor below 500,000, 7-smooth
  conductor, and prime conductor through 300,000,000. Cremona ecdata stops at
  500,000. The target conductor `301245307115205810` is outside those
  ranges, so database absence is expected and is not novelty evidence.

General fixed-j rank bounds, simultaneous progressions, and Bremner-type
uniformity results do not compute these target groups or rank.

## Risk and safe language

Method novelty is not claimed. Target-specific computational novelty has
moderate confidence, with medium residual risk from the inaccessible complete
MathSciNet graph, incomplete old zbMATH metadata, database coverage limits,
non-indexed work, and isomorphic or twisted presentations.

Safe language is: "For the index-8 binary quartic attached to Campbell's
Theorem 2.5, we compute and certify the two displayed rational 2-isogeny
Selmer groups and deduce `rank E(Q) <= 3`." Do not use "first", "new
descent", "exact rank", or "solution of the ninth-point problem".

## Independent-CAS status

The host has no usable Sage, Magma, or PARI/GP; PowerShell `gp` is a shell
alias. The executable free Sage protocol is in
`notes/independent-second-cas-plan.md`. It enumerates all signed squarefree
divisors and applies exact Sage `test_els` tests on both isogenous models,
then checks orders in proof mode. PARI/GP offers a weaker rank-interval check;
locally licensed Magma would be an optional third implementation. None was
executed.

## Package verification

The unchanged elliptic regression command passes 73/73 tests. The revised
manuscript compiles to 11 pages with SHA-256
`1b27cc0331736af6b2078d4b0ddb21d2e21e3dc97403eb8235a2ae1f9a2a40f3`.
All 11 pages were rendered and visually inspected; no clipping, overlap,
broken reference, or unreadable table was found. The final LaTeX log contains
no undefined citation/reference, overfull/underfull box, or package warning.
