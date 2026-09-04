# Executable independent-CAS plan

Status: protocol only, not executed. The theorem does not depend on this
file. A future run must archive the software version, complete output, script
SHA-256, and exit status.

## Primary route: SageMath

Run this as a `.sage` file in a clean Sage installation:

```python
from sage.all import EllipticCurve, QQ, ZZ, prod
from sage.schemes.elliptic_curves.descent_two_isogeny import (
    test_els, two_descent_by_two_isogeny,
)

A = ZZ(-591895071)
B = ZZ(58536289153843200)
Aprime = -2*A
Bprime = A*A - 4*B
assert Aprime == 1183790142
assert Bprime == 116194618458722241

def signed_squarefree_divisors(n):
    ps = ZZ(abs(n)).prime_divisors()
    for mask in range(1 << len(ps)):
        d = prod(ps[i] for i in range(len(ps)) if (mask >> i) & 1)
        yield ZZ(d)
        yield ZZ(-d)

def locally_soluble_classes(a, b):
    return sorted(
        d for d in signed_squarefree_divisors(b)
        if test_els(d, 0, a, 0, b // d)
    )

expected_E = sorted(ZZ(x) for x in [1,3,5,7,15,21,35,105])
expected_Eprime = sorted(ZZ(x) for x in
    [1,4230241,339106321,1434501462453361])

classes_E = locally_soluble_classes(A, B)
classes_Eprime = locally_soluble_classes(Aprime, Bprime)
print("E-side classes:", classes_E)
print("Eprime-side classes:", classes_Eprime)
assert classes_E == expected_E
assert classes_Eprime == expected_Eprime

E = EllipticCurve(QQ, [0, A, 0, B, 0])
assert E(0, 0).order() == 2
n1, n2, n1prime, n2prime = two_descent_by_two_isogeny(
    E, selmer_only=True, proof=True, verbosity=0
)
print("two-isogeny descent counts:", n1, n2, n1prime, n2prime)
assert n2 == 8
assert n2prime == 4
assert n2*n2prime == 32  # rank upper bound: log_2(8)+log_2(4)-2 = 3
```

The class lists are the primary check: they start only from the two models
and exhaust every signed supported squareclass. The final call checks the two
orders and yields the standard 2-isogeny rank upper bound 3; it does not
compute an exact rank. Confirm tuple orientation against the installed Sage documentation
before naming `phi` and `hat(phi)`; compare the sets before assigning
direction labels. Keeping verbosity zero avoids relying on diagnostic-output
format. Official documentation:
<https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/descent_two_isogeny.html>.

## Secondary route: PARI/GP

```gp
A = -591895071;
B = 58536289153843200;
E = ellinit([0,A,0,B,0]);
ellglobalred(E)
ellrank(E)
```

Archive the exact version and output. `ellrank` gives a full-2-descent rank
interval but not the two individual isogeny-Selmer squareclass sets required
here. Numerical `ellanalyticrank` is not a proof of algebraic rank.

## Optional third route: locally licensed Magma

Do not use a paid online service. With a local license, construct `E`, the
point `(0,0)`, `TwoIsogeny`, and `DualIsogeny`; verify the codomain is
isomorphic to

```text
y^2 = x^3 + 1183790142*x^2 + 116194618458722241*x.
```

Call `SelmerGroup` on both maps with `Bound := -1`, normalize inverse-map
representatives in `Q*/Q*^2`, and compare unordered sets before assigning
directions. Expected orders are 8 and 4. Then use the documented rank-bound
interface to check the upper bound 3. Documentation:
<https://magma.maths.usyd.edu.au/magma/handbook/text/1570>.

## Acceptance criteria

1. Archive software name, version, platform, script SHA-256, stdout/stderr,
   and exit status.
2. Record both normalized squareclass sets, not only dimensions.
3. Check isogeny directions from domain and codomain.
4. State only a rank upper bound unless separate lower-bound evidence exists.
