# Round 09: the mask-90 integral-point gate

Date: 2026-09-04

## Result

The priority mask 90 closes by a complete elementary argument.  No
Mordell--Weil, Thue--Mahler, or bounded-search conclusion is used.

Among the ten patterns certified after the mask-51 gate, mask 90 occurs in
exactly IDs

```text
43, 251, 281.
```

Its complete integral-point set is

```text
y^2=(t+1)(t+3)(t+4)(t+6),
(t,y)=(-6,0),(-4,0),(-3,0),(-1,0).
```

Every listed parameter makes one of `t,...,t+6` zero.  Therefore these three
patterns are strictly excluded, and the necessary-pattern chain becomes

```text
651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7.
```

The seven surviving IDs are

```text
12, 31, 59, 134, 214, 230, 276.
```

They remain necessary candidates only.  This result neither realizes nor
excludes any one of them and does not decide `R_2(7)`.

## Independent reconstruction from the frozen inputs

The generator reads the mask-51 survivor list and the Round-04 occurrence
table, checking their raw SHA-256 values.  It reconstructs ten rows, exactly
15 distinct character masks per row, hence 150 occurrences.  There are 49
distinct masks and 25 distinct genus-one masks.  The pairable genus-one masks
are independently recovered as

```text
(mask, patterns hit, |constant|)
(54, 3, 3), (45, 3, 6), (90, 3, 6), (27, 2, 3), (85, 2, 8).
```

Mask 90 was the specified Round-09 priority among the three masks tied at
three affected patterns.  Its support is `{1,3,4,6}`.  The exact occurrence
records are `P43:m90`, `P251:m90`, and `P281:m90`; each is class 5 with
representative mask 45 and the recorded affine parameter map `t=u-1`.

## Complete elementary proof

Put

```text
A=(t+1)(t+6),   B=(t+3)(t+4).
```

Then the quartic right side is `AB`, while

```text
B-A=6,  gcd(A,B)=gcd(A,6),  hence gcd(A,B) divides 6.
```

If `t<=-7` or `t>=0`, both `A` and `B` are positive.  If their product is a
square, their common positive squarefree kernel is a squarefree divisor of 6:

```text
A=d U^2, B=d V^2, d in {1,2,3,6}, d(V^2-U^2)=6.
```

All four branches terminate:

1. `d=1`: `V^2-U^2=6`, impossible modulo 4.
2. `d=2`: `(V-U)(V+U)=3`; positivity leaves `(1,3)`, hence
   `(U,V)=(1,2)` and `A=2`.  But
   `(2t+7)^2=4A+25=33`, impossible since `5^2<33<6^2`.
3. `d=3`: `V^2-U^2=2`, impossible modulo 4.
4. `d=6`: `(V-U)(V+U)=1` forces `U=0`, contradicting `A>0`.

The complementary interval consists of the six integers `-6<=t<=-1`.  The
right sides are respectively

```text
0, -8, 0, 0, -8, 0,
```

which gives exactly the four displayed branch points.  Because an integer
which is a rational square is automatically an integer square, this also
closes the rational-`y`, integral-`t` condition needed by every character
quotient.

## Pattern impact

The three excluded partitions are

```text
43:  0100021
251: 0102221
281: 0102003
```

The exact survivors are

```text
12:  0012202
31:  0001202
59:  0012231
134: 0012131
214: 0122213
230: 0012102
276: 0010203
```

Since the mask-90 curve has no nondegenerate integral parameter at all, the
exclusion is a same-parameter argument and never combines points from
different character quotients.

## Artifacts and independent-review recipe

- Generator: `code/PAPER_SQUARE_MASK90.py`.
- Certificate: `certificates/PAPER_SQUARE_MASK90_CERTIFICATE.json`.
- Tests: `reproducibility/tests/PAPER_SQUARE_MASK90_test.py`.
- Certificate SHA-256:
  `2d07dcf9c1b237001e7e25cf2af0e6e3baa7f3b7fee3662fb6568e5caffa5c28`.

From the repository root, an independent reviewer can run:

```powershell
python square-progressions/seven-consecutive-squareclasses/code/PAPER_SQUARE_MASK90.py
python -c "import sys,unittest; sys.path.insert(0,r'square-progressions/seven-consecutive-squareclasses/code'); s=unittest.defaultTestLoader.discover(r'square-progressions/seven-consecutive-squareclasses/reproducibility/tests',pattern='PAPER_SQUARE_MASK90_test.py'); r=unittest.TextTestRunner(verbosity=2).run(s); raise SystemExit(not r.wasSuccessful())"
```

The eight dedicated tests independently check the ten-row input, all 150
occurrences, the exact pairing, all four squarefree branches, the complete
middle interval, the three affected IDs, the seven survivors and disk
certificate regeneration.

## Next gate

The remaining inventory shows mask 54 and mask 45 also hit three current
patterns.  Mask 54 is an integer translate of the already proved mask-108
quartic and is therefore the first low-risk target for a separately certified
next round.  That observation is not used here to claim any further exclusion.
## Integration and final verification

The proved proposition, exact `10 -> 7` chain and seven-row table are integrated
in `paper/main.tex`; `paper/main.pdf` was rebuilt to 10 pages.  Its final LaTeX
log contains no undefined citation/reference, overfull/underfull box, or package
warning match.  The versioned flat supplement is now
`paper-square-supplement-v0.8.0`; its manifest SHA-256 is
`29ee9fe4a34a01f4066c017912130f3c02dcd55a031fb9f19dc7046d8854eb54`.
The mask-90 generator, certificate and eight tests are included in its exact
32-file allowlist.

The full repository command `python tools/run_all_checks.py` passed: 78/78
squareclasses tests and 206/206 tests across all six groups.  This regression
does not add any claim beyond the elementary proof above.
