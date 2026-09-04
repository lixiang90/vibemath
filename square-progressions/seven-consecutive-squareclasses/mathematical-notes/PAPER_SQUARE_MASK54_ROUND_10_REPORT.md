# Round 10: the mask-54 integral-point gate

Date: 2026-09-04

## Result

Among the seven necessary patterns left by mask 90, mask 54 occurs exactly in
IDs `59, 214, 230`.  Its complete integral-point set is

```text
y^2=(t+1)(t+2)(t+4)(t+5),
(t,y)=(-5,0),(-4,0),(-3,-2),(-3,2),(-2,0),(-1,0).
```

Every parameter makes one of the original seven integers `t,...,t+6` zero.
Consequently the three patterns are excluded at the same normalized parameter,
and the necessary-pattern chain becomes

```text
651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7 -> 4.
```

The four surviving IDs and canonical partition words are

```text
12:  0012202
31:  0001202
134: 0012131
276: 0010203
```

These remain necessary candidates only.  This result does not realize or
exclude any one of them and does not decide `R_2(7)`.

## Exact translation to the proved mask-108 curve

Write `s=t-1`.  Factor by factor,

```text
(s+2,s+3,s+5,s+6)=(t+1,t+2,t+4,t+5).
```

Thus `(s,Y) -> (t,y)=(s+1,Y)` is a bijection between integral points of

```text
Y^2=(s+2)(s+3)(s+5)(s+6)
```

and the mask-54 curve, with inverse `(t,y) -> (s,Y)=(t-1,y)`.  Translating
the already proved mask-108 list gives exactly the six displayed mask-54
points.  The generator binds the exact mask-108 certificate by SHA-256 and
stores the forward map, inverse map, factor identity, source list and target
list.

## Independent complete proof

The conclusion does not depend solely on reusing the mask-108 result.  Put

```text
A=(t+1)(t+5),   B=(t+2)(t+4)=A+3.
```

For `t<=-6` or `t>=0`, both factors are positive and
`gcd(A,B)=gcd(A,3)`.  If `AB` is a square, their common positive squarefree
kernel is `d in {1,3}`, so `A=d U^2`, `B=d V^2` and

```text
d(V^2-U^2)=3.
```

- If `d=1`, then `(V-U)(V+U)=3`; positivity gives `(U,V)=(1,2)`,
  hence `A=1` and `(t+3)^2=A+4=5`, impossible modulo 8.
- If `d=3`, then `(V-U)(V+U)=1`, hence `U=0`, contradicting `A>0`.

At the five complementary integers `-5<=t<=-1`, the right sides are
`0,0,4,0,0`, yielding exactly the six points above.  Since an integer which
is a rational square is an integer square, this also closes the rational-`y`,
integral-`t` condition required by the character quotient.

## Occurrence and same-parameter audit

The input is the exact seven-row output of the mask-90 certificate.  Rebuilding
the Round-04 occurrence table gives 105 occurrences, 41 distinct masks and 22
distinct genus-one masks.  The remaining constant-pairable ranking is

```text
(mask, patterns hit, |constant|)
(54,3,3), (27,2,3), (45,2,6), (85,2,8).
```

The exact records are `P59:m54`, `P214:m54`, and `P230:m54`; all use
representative mask 27, class 2, and the recorded map `t=u-1`.  The conclusion
uses each row's mask-54 quotient at that row's original normalized parameter;
it never combines points from different quotients.

## Artifacts and boundary

- Generator: `code/PAPER_SQUARE_MASK54.py`.
- Certificate: `certificates/PAPER_SQUARE_MASK54_CERTIFICATE.json`.
- Tests: `reproducibility/tests/PAPER_SQUARE_MASK54_test.py`.

The tests independently check the seven authoritative input rows, all 105
occurrences, exact ranking and records, factorwise translation, point-list
bijection, independent pairing identity, exhaustive middle interval, both
squarefree branches, degeneracy, exact three-row impact and disk certificate.
No bounded search, heuristic rank or Mordell--Weil computation supports the
theorem.

Certificate SHA-256:
`90d33bed3609712cb985170b60b6fb06264577b76dca6b7578606b42e9f585b9`.

## Integration and verification

The proposition, exact `7 -> 4` step and four-row table are integrated in the
paper.  The flat supplement is version `paper-square-supplement-v0.9.0`; its
35-file manifest SHA-256 is
`e218f10e116ec7732c9d369384bc06156195ea4cc62165cd3107583b03546c6d`.
All 87 squareclasses tests passed in a fresh temporary flat layout.  The paper
rebuilt to 11 A4 pages; the final LaTeX log has no warning, undefined-reference,
overfull-box or underfull-box match.  Visual inspection of pages 7 and 8 found
the new proposition, summary theorem, four-row table and manifest hash legible,
unclipped and correctly separated.
