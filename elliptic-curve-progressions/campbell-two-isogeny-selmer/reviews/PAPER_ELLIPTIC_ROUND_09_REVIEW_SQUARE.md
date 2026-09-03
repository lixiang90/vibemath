# Independent review of `NEXT_ELLIPTIC_ROUND_09`

Date: 2026-09-04
Reviewer: square-progressions line
Decision: **PASS; no mandatory mathematical repair.**

This review is deliberately narrow.  It checks the stated two-place local
theorem for the (E)-side quartics.  It does not certify a complete Selmer
calculation, a rational point on the original Campbell curve, or an
independent second-CAS computation.

## Itemized verdict

| Item | Verdict | Independent check |
|---|---|---|
| Identity (4dF_d=(2dU^2+aV^2)^2-\Delta V^4) | **PASS** | Expanding gives coefficients (4d^2,4da,a^2-\Delta); since \(\Delta=a^2-4b\), these are exactly (4d(d,a,b/d)). |
| Discriminant valuation | **PASS** | Recomputed \(\Delta=3^4\cdot59\cdot71699\cdot339106321\); both tested primes are prime and have \(v_p(\Delta)=1\). |
| Three valuation branches when \((d/p)=-1\) | **PASS** | After primitive weighted-projective normalization, either (p\mid V), or (V) is a unit.  In the latter case (S=2dU^2+aV^2) is either a unit or divisible by (p).  Thus the three cases are exhaustive.  They give respectively a nonsquare unit, squareclass (d), or odd valuation (v_p(F_d)=1), each incompatible with (F_d=N^2). |
| Converse when \((d/p)=1\) | **PASS** | The point ((U:V:N)=(1:0:\sqrt d)) exists over \(\mathbf Q_p\). |
| Soluble squareclasses at (p=59,71699) | **PASS** | Independently recomputed the generator symbols at both primes as \((-1,2,3,5,7)=(-1,-1,+1,+1,+1)).  Both places therefore give exactly the same sixteen classes listed below. |
| Real place and two-place intersection | **PASS** | For (d>0), the same point at (V=0) works.  For (d<0), all three coefficients (d,a,b/d) are negative, so (F_d<0) off the forbidden origin.  Intersecting with the two finite-place set leaves exactly eight classes. |
| Consistency with the archived 512-row local matrix | **PASS** | Parsed the 32 (E)-side rows in `local_matrix_512.json`; its YES sets at 59 and 71699 are exactly the independently recomputed sixteen-class set, and its real intersection is exactly the eight-class set. |
| Claim boundary | **PASS** | The report, certificate and manuscript state only a necessary (E)-side support-class filter.  They do not identify the original (C_H) with a complete (E)-torsor, nor claim a global obstruction or rational point. |
| Independent-CAS wording | **PASS** | The report explicitly records that no Sage/Magma/GP/PARI executable was available and that Python/SymPy is not a second elliptic-curve CAS.  No second-CAS reproduction is claimed. |

The independently reproduced common sixteen-class set is

```text
-210, -70, -42, -30, -14, -10, -6, -2,
1, 3, 5, 7, 15, 21, 35, 105
```

and the real-place intersection is

```text
1, 3, 5, 7, 15, 21, 35, 105.
```

## Artifact and test checks

The reported SHA-256 values of the Round-09 script, certificate and PDF agree
with the bytes on disk.  The project test checks the identity, factorization,
prime/valuation facts, the local criterion, both exact lists, the old-matrix
comparison, provenance, and disk hash closure.  After the root runner was
updated to include this module and the cube Round-09 module, the complete root
suite passed **218 tests**.

## Non-blocking observations

1. The review found the typographical string `-1,qquad`; it was subsequently
   corrected to `-1,\qquad` and regression-tested.  It never changed the
   proposition or proof.
2. The three-case valuation argument is proved in the manuscript, while the
   machine certificate mainly stores the resulting Legendre-symbol criterion.
   Encoding the three cases as structured certificate fields would improve
   auditability, but is not needed for validity because the written proof is
   complete.

## Scope conclusion

The verified result is an exact local theorem for these (E)-side covers and
an eight-class necessary filter after two finite places and the real place.
It is not a complete isogeny-Selmer computation, does not settle compatibility
with the original Campbell fibre, and does not close the global problem.
