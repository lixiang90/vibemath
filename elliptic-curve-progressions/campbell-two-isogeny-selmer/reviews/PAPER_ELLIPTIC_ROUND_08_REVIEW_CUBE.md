# Independent review of Round 08: minimal model and conductor

Date: 2026-09-03
Reviewer: cube/powers line
Decision: **PASS**

Scope: `NEXT_ELLIPTIC_ROUND_08_REPORT.md`,
`code/NEXT_ELLIPTIC_ISOMORPHISM_AUDIT.py`, its six-test regression file and
certificate, and the global-minimal-model proposition in `paper/main.tex`.
No author file was modified.

## 1. Independent coordinate check

Start with

```text
Y^2=X^3-591895071 X^2+58536289153843200 X.
```

Substitute `X=36x`, `Y=216y+108x` and divide by `216^2=46656`.
The left side becomes `y^2+xy+x^2/4`; on moving the last term to the
right, the two nonzero coefficients are

```text
-591895071/36-1/4 = -16441530,
58536289153843200/1296 = 45166889779200.
```

Thus the claimed integral equation and admissible parameters
`(u,r,s,t)=(6,0,3,0)` are correct:

```text
y^2+xy=x^3-16441530x^2+45166889779200x.
```

## 2. Independent invariant arithmetic

From `[a1,a2,a3,a4,a6]=[1,-16441530,0,45166889779200,0]` I independently
obtained

```text
b2 = -65766119
b4 = 90333779558400
b6 = 0
b8 = -2040047932326401424752640000
c4 = 2157171698920561
c6 = 70577985500751764077559
Delta = 2926451742397178075653974744686961623040000.
```

The identity `c4^3-c6^2=1728*Delta` holds.  Independent factorization gives

```text
Delta = 2^28 3^16 5^4 7^10 59 71699 339106321,
```

and all seven displayed bases are prime.  Also
`gcd(c4,Delta)=1`, so `v_p(c4)=0` at every listed prime.  The reduced
fraction `j=c4^3/Delta` is exactly

```text
10038160648206649953061393462836377818780518481
/
2926451742397178075653974744686961623040000.
```

These values agree with the manuscript and stored certificate.

## 3. Minimality, including p=2 and p=3

The manuscript's argument is valid in residue characteristics 2 and 3.
If an integral Weierstrass equation is nonminimal over `Q_p`, an integral
model of smaller discriminant is related to it by an admissible change with
positive `p`-adic valuation of `u`.  Since `c4=u^4 c4'` and `c4'` is
integral, nonminimality forces `v_p(c4)>=4`.  Thus `v_p(c4)=0` proves
minimality, without an odd-residue-characteristic assumption.

As an independent direct check, at both `p=2` and `p=3` the minimal equation
reduces to

```text
y^2+xy-x^3=0.
```

Its only affine singular point is `(0,0)`, and its tangent cone is
`y(y+x)`, whose two factors are distinct over both residue fields.  Hence
the reduction is split multiplicative at 2 and 3.  In particular the
Kodaira types are `I_28` and `I_16`, respectively, and the local conductor
exponent is one; there is no wild additive contribution.

At each remaining bad prime, `v_p(Delta)>0` and `v_p(c4)=0` likewise give
multiplicative type `I_vp(Delta)` and conductor exponent one.  At every
unlisted prime the displayed integral minimal discriminant is a unit, so
the reduction is good.  Therefore the bad-prime set is exactly

```text
{2,3,5,7,59,71699,339106321},
```

the curve is semistable, and the conductor is the squarefree support

```text
2*3*5*7*59*71699*339106321 = 301245307115205810.
```

## 4. Test and evidence audit

- The six new tests pass independently.
- The exact Round-08 command passes **50/50 tests**.
- The new test file correctly checks the coordinate transformation,
  invariant scaling, expected factorization, conductor, `j`, stored
  certificate equality, and manuscript tokens.
- The manuscript-token test is only a regression guard, not the proof; the
  arithmetic and local arguments above independently supply that proof.

## 5. Required fixes and residual comments

**No blocking or mathematical fix is required.**  The global minimality,
discriminant, bad-prime support, semistability, Kodaira symbols and conductor
theorem are correct as stated.

Optional strengthening only: the proof could mention the explicit tangent
cone `y(y+x)` at 2 and 3.  This is not needed for correctness because the
unit-`c4` criterion already applies there, but it makes the small-prime
audit completely transparent.
