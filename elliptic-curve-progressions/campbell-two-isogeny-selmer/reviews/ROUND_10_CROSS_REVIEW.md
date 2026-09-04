# Cross-review of the Round-10 E-prime two-place gate

Date: 2026-09-04

## Verdict: PASS

I found no missing valuation branch, false Hensel implication, incorrect
survivor intersection, or overstatement of the certificate-relative
minimality claim.  The two local `iff` statements are complete for the 32
signed squarefree representatives supported on
`{3,59,71699,339106321}`.  This review does not elevate the stored-matrix
minimality audit to a theorem about all finite primes, and it does not address
the global ninth-point problem.

Audited bytes:

- `code/NEXT_ELLIPTIC_ROUND_10.py`, SHA-256
  `168daebd47bdbeebff9eee63543af421625d9c4acc6744a98cc2b019c27f2372`;
- `certificates/round10_eprime_two_three_gate.json`, SHA-256
  `9e1e4c0a0c0c56e63d47be039efebe203a29b1d664b5ab2740135ebd98a18fe0`;
- source matrix `certificates/local_matrix_512.json`, SHA-256
  `fff2f35f398c2d14227d9b032d205e24d5332a39346487c76180cdf805ba32c9`;
- the Round-10 report, regression test, README, and the proposition and proof
  in `paper/main.tex`.

## 1. Identity and normalization

For

```text
F'_d=d U^4+A' U^2 V^2+(B'/d)V^4,
A'=1183790142=2c,
B'=116194618458722241,
```

direct expansion verifies

```text
4dF'_d=(2dU^2+A'V^2)^2-((A')^2-4B')V^4.
```

The recorded constants also check exactly:

```text
c=591895071 = 7 mod 8,
(A')^2-4B'=2^22*223298222175,
v_3(A')=2,
A'/9=1 mod 3,
B'/3^4=1 mod 3.
```

After dividing the displayed identity by four and using `N^2=F'_d`, it
becomes

```text
d N^2=T^2-2^20*k*V^4,  T=dU^2+cV^2,
```

exactly as stated.  Every supported `d` is an odd 2-adic unit and has
3-adic valuation zero or one.

## 2. Complete Q_2 branch audit

Scale a putative point so that `U,V` are primitive in `Z_2`.  The primitive
assignments are exhausted as follows.

| parity of `(U,V)` | valuation of `T` | correction after division by `T^2` |
|---|---:|---:|
| odd, even | `0` | at least `24` |
| even, odd | `0` | at least `20` |
| odd, odd and `d=3 mod 8` | `1` | at least `18` |
| odd, odd and `d=5 mod 8` | `2` | at least `16` |
| odd, odd and `d=7 mod 8` | `1` | at least `18` |

There is no both-even case by primitivity.  In the all-odd rows,
`T=dU^2+cV^2=d+7 mod 8`, giving the displayed valuations exactly.  Thus for
every nonsquare odd class `d=3,5,7 mod 8`, the right side is

```text
T^2 * (1 + element of 2^16 Z_2),
```

a nonzero square in `Q_2`.  Hence `dN^2` is a square and so `d` is a square,
contradicting the odd-unit square criterion.  This proves necessity without
assuming `N` is a unit.

For sufficiency, if `d=1 mod 8`, then for `f(X)=X^2-d`,

```text
v_2(f(1)) >= 3 > 2 v_2(f'(1)) = 2.
```

The strengthened Hensel criterion therefore gives `sqrt(d)` in `Q_2`, and
`(U:V:N)=(1:0:sqrt(d))` is a valid cover point.  Both directions of

```text
C'_d(Q_2) nonempty iff d=1 mod 8
```

are proved.

## 3. Complete Q_3 branch audit

Normalize `U,V` to be primitive in `Z_3`.

### Case `v_3(d)=1`

- If `U` is a unit, the three term valuations are `1`, at least `2`, and at
  least `3`; the first term is uniquely lowest, so `v_3(F'_d)=1`.
- If `3` divides `U`, primitivity makes `V` a unit.  The term valuations are
  at least `5`, at least `4`, and exactly `3`; the last term is uniquely
  lowest, so `v_3(F'_d)=3`.

Both are impossible square valuations.  These are all assignments for this
case.

### Case `v_3(d)=0`

- If `U` is a unit, `F'_d=dU^4 mod 3`, so a square requires `d=1 mod 3`.
- If `U=3^r u` with `r=1`, then `u,V` are units.  Dividing by `3^4`, which is
  a square, gives unit residue `d+1+d^{-1}`.  For `d=-1 mod 3` this is `-1`.
- If `r>=2`, the same quotient has unit residue `d^{-1}`; for
  `d=-1 mod 3` this is again `-1`.

The split `r=0,1,>=2` is exhaustive, and no cancellation was ignored because
each forbidden quotient is already a nonzero nonsquare unit modulo three.
Conversely, for `d=1 mod 3`, the root `1` of `X^2-d mod 3` is simple since
the derivative is `2`, a 3-adic unit.  Ordinary Hensel lifting gives
`sqrt(d)` and the point `(1:0:sqrt(d))`.  Therefore

```text
C'_d(Q_3) nonempty iff v_3(d)=0 and d=1 mod 3.
```

## 4. Survivor sets and intersection

Using

```text
59=71699=3 mod 8,  q=339106321=1 mod 8,
59=71699=-1 mod 3, q=1 mod 3,
```

the two criteria give exactly

```text
Q_2: {1,q}*{1,3*59,3*71699,59*71699},
Q_3: {1,q}*{1,59*71699,-59,-71699}.
```

Their intersection is

```text
{1, 59*71699, q, 59*71699*q}
 = {1,4230241,339106321,1434501462453361}.
```

This agrees with both the generated certificate and a separate residue audit.
As a diagnostic cross-check, I enumerated every primitive residue pair for
all 32 representatives modulo `2^8` and modulo `3^6`; the classes admitting a
square right side were exactly the two eight-class lists above.  This finite
check corroborates but is not used as the proof of local sufficiency.

## 5. Scope of the minimality statement

The script reads the 32 stored `E_dual` rows and the seven finite columns

```text
2, 3, 5, 7, 59, 71699, 339106321.
```

It recomputes all one-column survivor counts; their minimum is eight.  It then
checks all 21 finite two-column combinations.  Exactly `{2,3}` and `{2,5}`
have survivor set equal to the displayed four classes.  Hence two columns are
minimal **within this stored finite-place matrix**, and `{2,5}` is the only
other minimal pair there.

This is a deterministic certificate conclusion, not a new local theorem for
every prime.  The manuscript correctly says “in the stored eight-place
matrix” and later explicitly identifies the comparison with its seven finite
place columns.  The Round-10 report likewise attributes the statement to an
audit of the existing certificate.  I found no wording that claims that no
unrecorded prime could by itself produce the same four-class set.

## 6. Reproduction and remaining boundaries

The author's nine Round-10 regression tests pass.  They check the constants,
coefficient identity, supported-class lists, all-odd 2-adic valuations,
two local classifications, intersection, matrix compatibility, minimal pairs,
disk certificate and manuscript boundary tokens.

The result is a complete local theorem for the stated 32 covers.  It does not
prove a rational ninth point, a global obstruction, a Cassels--Tate value,
rank equality, independent second-CAS reproduction, or novelty.  Those limits
are stated accurately in the report, certificate, README and manuscript.
