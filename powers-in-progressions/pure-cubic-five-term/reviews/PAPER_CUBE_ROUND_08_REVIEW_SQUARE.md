# Round 08 independent review (square line)

## Decision

**PASS; no blocking mathematical correction found.**  The new colour type `0010` is genuinely inequivalent to the earlier `0001` type, the cubic-to-Mordell map checks identically, the displayed point gives a non-torsion class by Nagell--Lutz, and the pure cubic example and all stated boundary exclusions are valid.  The result closes a second one of the 31 unresolved four-hit colour orbits; it does not classify the other 29 or determine the exact Mordell--Weil rank.

## Item-by-item audit

| Item | Verdict | Independent check |
|---|---|---|
| Orbit `0010` versus `0001` | **PASS** | I independently generated the action of colour translation, multiplication by `1,2` in `F_3`, and reversal.  Each orbit has size 12 and their intersection is empty.  Canonical representatives are respectively `((0,1,2,3),(0,0,1,0))` and `((0,1,3,4),(0,0,0,1))`.  More simply, reversal sends the omitted endpoint 4 to endpoint 0, whereas the old type omits the fixed middle position 2. |
| Exhaustive orbit context | **PASS** | Independent enumeration of all `5*3^4=405` normalized four-hit data gives 38 orbits: 3 one-colour, 4 monochromatic-three-AP, and 31 previously unresolved.  Both representatives occur in the last set and are distinct. |
| Plane cubic and AP | **PASS** | Writing `A_0=X^3`, `A_1=Y^3`, the condition that `A_3=3A_1-2A_0=Z^3` is exactly `2X^3-3Y^3+Z^3=0`.  The five terms `(X^3,Y^3,2Y^3-X^3,Z^3,4Y^3-3X^3)` all have difference `Y^3-X^3`; conversely any nonconstant `0010` lift gives such a point. |
| Smooth genus-one model | **PASS** | The partial derivatives are `6X^2,-9Y^2,3Z^2`; they have no common projective zero in characteristic zero.  With `O=(1:1:1)`, the smooth plane cubic is an elliptic curve. |
| Map to `v^2=u^3-243` | **PASS** | With `a=X^3,b=Y^3,c=Z^3`, `N=6ab+3bc-2ca` and `T=(2a+3b)(-3b-c)(c-2a)`, direct expansion gives `T^2-4N^3+972a^2b^2c^2=0` after substituting `c=3b-2a`.  Hence `u=N/(X^2Y^2Z^2)`, `v=-T/(2XYZ)^3` satisfies `v^2=u^3-243` wherever written.  Since the source is smooth projective and the target is proper, the rational map extends. |
| Images of the two points | **PASS** | Direct substitution gives `phi(O)=(7,-10)=-Q` and `phi(4:1:-5)=(16009/400,-2021723/8000)=2Q` for `Q=(7,10)`.  Independent tangent arithmetic on `v^2=u^3-243` gives the same coordinates for `2Q`; translating by `Q` sends `P` to `3Q`. |
| Nagell--Lutz non-torsion argument | **PASS** | `Q` lies on the integral nonsingular model because `10^2=7^3-243`.  Its discriminant is `-2^4*3^13=-25509168`, not divisible by `10^2` (indeed it has no factor 5).  Nagell--Lutz therefore excludes torsion.  Thus the translated nonconstant origin-preserving map is an isogeny and `P` is non-torsion. |
| Explicit pure cubic example | **PASS** | At `P=(4:1:-5)`, the AP is `(64,1,-62,-125,-188)` with four equal differences `-63`.  If `beta^3=62`, its first four entries are `4^3,1^3,(-beta)^3,(-5)^3`.  Since 62 is not a rational cube, `x^3-62` is irreducible and this is a genuine pure cubic field. |
| Zero/degenerate boundaries | **PASS** | `X=0`, `Y=0`, `Z=0` would respectively make `3,-2,3/2` rational cubes.  `A_2=0` and `A_4=0` would make `2` and `4/3` rational cubes.  Difference zero forces `X=Y` and then `Z=X`, hence the origin; excluding `n=0` removes it.  These arguments also show all stated terms used as cube roots are nonzero. |
| General pure cubic lift | **PASS** | For each nonzero multiple, write the noncube class of `A_2` as `D w^3` with positive cube-free `D`; then the four indicated terms are cubes in `Q(cuberoot D)`.  If `A_2` were already a rational cube, clearing rational denominators by a common cube would contradict the cited `P_5(3)=3` theorem. |
| Fifth-term boundary | **PASS** | If `A_4` were a cube in the same `K_D`, all five terms would have cube classes in one cyclic subgroup.  This is ruled out by the already proved `R^times_(3,1)(5)=4`; the use is not circular with the present orbit construction. |
| Infinitely many inequivalent APs | **PASS** | Multiples of a non-torsion point are distinct.  If two resulting APs differ by a rational cube scale, comparison of `A_0=X^3` recovers the projective cubic point; reversal has fibres of size at most two.  Hence infinitely many points give infinitely many equivalence classes. |

## Reproduction record

- Ran `python -m unittest discover -s code -p "*_test.py" -v`: **23/23 tests passed**.
- Independently recomputed the two 12-element colour orbits and obtained intersection size zero.
- Independently recomputed the full `405 -> 38 = 3+4+31` orbit partition.
- Independently expanded and reduced the Mordell identity, recalculated `2Q`, and checked all four AP differences.
- SHA-256 of `code/PAPER_CUBE_FOURHIT_0010_CERTIFICATE.json`: `49CCAD32EEDBA997CAE5C7749087CE2C99A529DE8DF4954F0CCB23A4FF368BAA`, agreeing with the round report.

## Must-fix findings

None.

## Minor, nonblocking audit improvements

1. Several boundary facts in the new certificate (`A_2=0`, `A_4=0`, and the fifth-hit exclusion) are stored as explanatory strings rather than machine-recomputed assertions.  The paper proof is self-contained and correct, so this is a certificate-coverage issue only.  A future release could add explicit algebraic assertions for them.
2. The cleared Mordell identity is exercised by the inherited base test rather than duplicated in the new `0010` test file.  The combined 23-test command does run it; an explicit dependency/version pointer from the new certificate to that inherited check would make the audit trail more local.
3. The certificate field `translated_point_image = "3Q"` is textual.  It follows rigorously from the separately checked images `phi(O)=-Q` and `phi(P)=2Q`, but could also be encoded as exact rational coordinates.

## Claim boundary

The defensible new theorem is: the `0010` orbit is a second distinct four-hit colour orbit admitting infinitely many nondegenerate five-term rational APs that become cubes in suitable pure cubic fields, with an explicit example in `Q(cuberoot 62)`, while the fifth term is not a cube in the same field.  The manuscript correctly leaves 29 of the 31 nontrivial colour orbits unresolved and does not claim an exact rank computation or a rational parametrization of the cubic.
