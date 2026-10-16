"""Exact algebraic certificate for Sun's 90/pi series.

Requires Python >=3.9 and SymPy 1.14. Run in a flat certificate directory.
The only data dependency is prize_congruence_curve90_jet_certificate.json
beside this script. No web request, guessed coefficients, floating-point
calculation, or machine-specific path is used.

Campbell--Cooper--Ye, arXiv:2602.09352v1, supplied discovery candidates.
This component checks the differential-algebra bridge, the change of
variables, lambda, constants, and convergence majorant. The complete proof
establishes the general modular parametrization by the separate eta/Sturm
certificate and the weighted CM evaluation by the paper's Fricke argument.
This component does not itself verify that analytic argument or prize priority.
"""
import json
from math import comb
from pathlib import Path
import sympy as s
from sympy.functions.combinatorial.numbers import stirling
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

BASE = Path(__file__).resolve().parent
u, v, q, z, t, c, h, x, j, k = s.symbols('u v q z t c h X j k')

def check_zero(expr):
    assert s.cancel(expr) == 0

def derivative(op, axis):
    """Ordinary partial derivative composed on the left of an operator."""
    out = {}
    for jet, coeff in op.items():
        out[jet] = out.get(jet, 0) + s.diff(coeff, (u, v)[axis])
        shifted = list(jet)
        shifted[axis] += 1
        shifted = tuple(shifted)
        out[shifted] = out.get(shifted, 0) + coeff
    return {a: s.expand(b) for a, b in out.items() if b != 0}

def scale(op, factor):
    return {a: s.expand(b * factor) for a, b in op.items()}

def add(*operators):
    out = {}
    for op in operators:
        for a, b in op.items():
            out[a] = s.expand(out.get(a, 0) + b)
    return {a: b for a, b in out.items() if b != 0}

def euler(op, axis):
    return scale(derivative(op, axis), (u, v)[axis])

# 1. Coefficient proofs of two Horn PDEs for
# H(u,v)=sum C(2j+2k,j+k)(j+3k)!/(j! k!^3) u^j v^k.
ratio_j = 2*(2*j+2*k+1)*(j+3*k+1)/((j+k+1)*(j+1))
check_zero((j+1)*(j+k+1)*ratio_j -
           (4*j*(j-1)+16*j*k+12*k*(k-1)+10*j+22*k+2))
# The two terms of P3 use a_{j-1,k}/a_{j,k-1}; boundary terms
# vanish because their respective multipliers are k^3 and j.
ratio_cross = j*(j+3*k-2)*(j+3*k-1)/k**3
check_zero(k**3*ratio_cross-j*(j+3*k-2)*(j+3*k-1))
P1 = {(2,0):u*(1-4*u), (1,1):v*(1-16*u), (0,2):-12*v*v,
      (1,0):1-10*u, (0,1):-22*v, (0,0):s.Integer(-2)}
part = {(0,0):s.Integer(1)}
for r in (2,1):
    part = add(euler(part,0), scale(euler(part,1),3), scale(part,r))
part = scale(euler(part,0),-v)
other = {(0,0):s.Integer(1)}
for _ in range(3):
    other = euler(other,1)
P3 = add(part,scale(other,u))
print('PASS: coefficient identities for the Horn PDEs', flush=True)

# 2. A_c(t)=(1-ct)^(-1) 2F1(1/3,2/3;1;27t/(1-ct)^3).
# This follows by writing n=j+k and summing (j+3k)! c^j t^(j+k)/(j! k!^3)
# first over j, by the binomial theorem. Verify its pulled-back Gauss ODE.
w = 27*t/(1-c*t)**3
wp = s.diff(w,t)
gauss_p = s.factor((1-2*w)*wp/(w*(1-w))-s.diff(wp,t)/wp)
gauss_Q = s.factor(-s.Rational(2,9)*wp**2/(w*(1-w)))
D = t*(2*c*t+1)*(c**3*t**3-3*c**2*t**2+3*c*t+27*t-1)
Np = 6*c**4*t**4-8*c**3*t**3-3*c**2*t**2+54*c*t**2+6*c*t+54*t-1
Nq = (c*t-1)*(2*c**3*t**2+2*c**2*t-c-6)
check_zero((gauss_p-2*c/(1-c*t))*D-Np)
check_zero((gauss_Q-c*gauss_p/(1-c*t))*D-Nq)
A = s.Poly((D/t)*h*(h-1)+Np*h+t*Nq,t)
As = [s.factor(A.nth(i)) for i in range(5)]
Ms = [s.cancel(4**i*As[i]*s.rf(h+s.Rational(1,2),i)*
       s.prod(h+i-r for r in range(3))/s.rf(h+1,i)) for i in range(5)]
Ls = [h**3*(h-1),
      -2*h*((11*c+54)*h**3+(-c+81)*h*h+(7*c+39)*h+c+6),
      12*c*(2*h+1)*((7*c+45)*h**3+7*c*h*h+(6*c-5)*h+2*c),
      -8*c**3*(2*h+1)*(2*h+3)*(17*h*h+24*h+12),
      80*c**4*(h+1)*(2*h+1)*(2*h+3)*(2*h+5)]
M = s.Poly(sum(z**i*Ms[i] for i in range(5)),h)
L = s.Poly(sum(z**i*Ls[i] for i in range(5)),h)
q1 = -(1+8*c*z)/(1-10*c*z)
q0 = 2*(1+2*c*z)/(1-10*c*z)
for i in range(6):
    check_zero(M.nth(i)-q1*(z*s.diff(L.nth(i),z)+
               (L.nth(i-1) if i else 0))-q0*L.nth(i))
f = [1,2*c+12,6*c*c+144*c+540]
check_zero(sum(Ls[i].subs(h,2-i)*f[2-i] for i in range(3)))
# Therefore L F_c=0: Q(LF_c)=0 and LF_c=C z^2(1+8cz)^(-3/2),
# whose coefficient of z^2 was just proved zero.
check_zero(L.nth(4)-(1-10*c*z)*((1-4*c*z)**3-108*z))
print('PASS: generic fourth-order period equation and Ore factorization', flush=True)

# Convert that already proved radial equation into an ordinary u,v PDE.
radial = s.Poly(sum(v**i*Ls[i].subs(c,u/v) for i in range(5)),h)
P4 = {}
for d in range(5):
    factor = sum(radial.nth(r)*stirling(r,d,kind=2) for r in range(d,5))
    for a in range(d+1):
        P4[(a,d-a)] = s.expand(factor*comb(d,a)*u**a*v**(d-a))

# 3. Restrict to the extra-section curve. Build the same derivative jets
# independently, then verify the supplied rational-function multipliers.
upath = -2*q*(1+6*q)/(1+8*q)
vpath = 16*q**4/(1+8*q)
Rs = [-h**3,
      -2*(22*h**3+15*h*h+9*h+2),
      -4*(181*h**3+219*h*h+142*h+32),
      -32*(169*h**3+270*h*h+181*h+45),
      -64*(244*h**3+384*h*h+149*h-18),
      512*(h+1)*(20*h*h+148*h+159),
      49152*(h+1)*(h+2)*(2*h+3)]
R = s.Poly(sum(q**i*Rs[i] for i in range(7)),h)

def path_theta(jets):
    out = {}
    for jet, coeff in jets.items():
        out[jet] = out.get(jet,0)+q*s.diff(coeff,q)
        for axis, path in enumerate((upath,vpath)):
            shifted = list(jet)
            shifted[axis] += 1
            shifted = tuple(shifted)
            out[shifted] = out.get(shifted,0)+q*s.diff(path,q)*coeff
    return {a:s.factor(b) for a,b in out.items()}

J = [{(0,0):s.Integer(1)}]
for _ in range(3):
    J.append(path_theta(J[-1]))
restricted = {}
for r in range(4):
    for jet, coeff in J[r].items():
        restricted[jet] = s.factor(restricted.get(jet,0)+R.nth(r)*coeff)
W = {(0,0):4*q*(2*q+1), (1,0):(8*q*q+12*q+1)*upath,
     (0,1):(24*q*q+8*q-1)*vpath}
DW = path_theta(W)
cert = json.loads((BASE/'prize_congruence_curve90_jet_certificate.json').read_text(encoding='utf-8'))
assert cert['proved'] is True and cert['last_multiplier_means_W'] is True
jets = [tuple(a) for a in cert['jets']]
assert jets == [(a,d-a) for d in range(6) for a in range(d+1)]
operators = []
for name,a,b in cert['consequences']:
    op = {'P1':P1,'P3':P3,'P4':P4}[name]
    for axis in [0]*a+[1]*b:
        op = derivative(op,axis)
    operators.append(op)
substitution = {u:upath,v:vpath}
rows = [[s.cancel(s.sympify(op.get(jet,0)).subs(substitution)) for op in operators]
        +[s.cancel(W.get(jet,0))] for jet in jets]
field = QQ.frac_field(q)
mat = DomainMatrix.from_Matrix(s.Matrix(rows)).convert_to(field)
for target, key in [(DW,'gradient_first_order_multipliers'),
                    (restricted,'thirdorder_multipliers')]:
    vals = [s.sympify(a,locals={'q':q}) for a in cert[key]]
    assert len(vals) == len(operators)+1
    sol = DomainMatrix.from_Matrix(s.Matrix(vals)).convert_to(field)
    rhs = DomainMatrix.from_Matrix(s.Matrix([s.cancel(target.get(jet,0)) for jet in jets])).convert_to(field)
    assert (mat.matmul(sol)-rhs).is_zero_matrix
check_zero(s.sympify(cert['gradient_first_order_multipliers'][-1],locals={'q':q})-4*q/(1+8*q))
assert s.sympify(cert['thirdorder_multipliers'][-1]) == 0
# This proves theta W=4q/(1+8q) W. All coefficients of W are regular
# at q=0 and W(0)=0, so W=C sqrt(1+8q)=0. It also proves R B=0.
assert all(s.limit(coeff,q,0)==0 for coeff in W.values())
assert R.nth(0).subs(q,0)==0 and R.as_expr().subs(q,0)==-h**3
print('PASS: exact jet certificates for the curve equation and gradient identity', flush=True)

# 4. Reduce the prize expression to 3(35 theta_q+18) B at q=1/12.
qstar = s.Rational(1,12)
check_zero(upath.subs(q,qstar)+s.Rational(3,20))
check_zero(vpath.subs(q,qstar)-s.Rational(1,2160))
ru = s.cancel(q*s.diff(upath,q)/upath)
rv = s.cancel(q*s.diff(vpath,q)/vpath)
check_zero((357-105*ru).subs(q,qstar)-126*(8*q*q+12*q+1).subs(q,qstar))
check_zero((357-105*rv).subs(q,qstar)-126*(24*q*q+8*q-1).subs(q,qstar))
check_zero(s.Integer(49)-126*(4*q*(2*q+1)).subs(q,qstar))

# 5. Exact operator substitution B(phi(X))=K(X) Z_60(X).
phi = x/(2*(1-2*x)**2)
rho = s.factor(phi/s.diff(phi,x))
klog = -4/(1-2*x)+4*x/(1+4*x*x)
T = [{0:s.Integer(1)}]
for _ in range(3):
    out = {}
    for d, coeff in T[-1].items():
        out[d] = out.get(d,0)+rho*(s.diff(coeff,x)+klog*coeff)
        out[d+1] = out.get(d+1,0)+rho*coeff
    T.append({a:s.factor(b) for a,b in out.items()})
transformed = {}
for r in range(4):
    for d, coeff in T[r].items():
        transformed[d] = s.factor(transformed.get(d,0)+R.nth(r).subs(q,phi)*coeff)
G = (1-x)*(1-4*x)*(1+4*x*x)*(1-x+4*x*x)
H = 4*x*(1-8*x+40*x*x-83*x**3+160*x**4-144*x**5)
th = lambda a: x*s.diff(a,x)
Z = s.Poly(G*h**3+s.Rational(3,2)*th(G)*h*h+(th(th(G))/2-H)*h-th(H)/2,h)
ZD = {d:s.factor(sum(Z.nth(r)*stirling(r,d,kind=2)*x**d for r in range(d,4))) for d in range(4)}
multiplier = (1+4*x*x)**2/((2*x-1)**9*(2*x+1))
for d in range(4):
    check_zero(transformed[d]-multiplier*ZD[d])
assert Z.as_expr().subs(x,0)==h**3
# Both equations have a unique analytic solution with constant 1 at 0:
# their indicial equations are +/-theta^3, and K(0)=1, phi(0)=0.
print('PASS: pullback to the published level-60 modular equation', flush=True)

# 6. Apply the externally supplied CM special value and check all constants.
xstar = (5-s.sqrt(21))/4
K = (1-2*x)**2*s.sqrt(1+4*x*x)
check_zero(s.diff(K,x)/K-klog)
assert K.subs(x,0)==1 and phi.subs(x,0)==0
assert s.diff(phi,x).subs(x,0)==s.Rational(1,2)
lam = s.Rational(3,2)-11*s.sqrt(21)/42
check_zero(s.simplify(phi.subs(x,xstar)-qstar))
check_zero(rho-x*(1-2*x)/(1+2*x))
lam_algebraic = (35*rho*klog+18)/(35*(1-2*x)/(1+2*x))
assert s.simplify(lam_algebraic.subs(x,xstar)-lam)==0
# Weighted CM evaluation supplied by the paper's independent Fricke argument:
#                      (theta_X+lam)Z_60(Xstar)
#                      = sqrt(60/7)/(2*pi*sqrt(G(Xstar))).
positive_factor = 35*K*(1-2*x)/(1+2*x)*s.sqrt(s.Rational(60,7))/(2*s.sqrt(G))
assert s.simplify((positive_factor**2).subs(x,xstar)-900)==0
# Exact sign: 4<sqrt(21)<5 gives 0<Xstar<1/4. Hence every
# factor in positive_factor is positive, and the factor equals 30.
assert 4**2 < 21 < 5**2

# 7. Absolute convergence at the prize point, including all previous
# re-summations and derivatives, from a positive majorant at R=1/2088.
Rbound = s.Rational(1,2088)
b = 1-1296*Rbound
wbound = 108*Rbound/b**3
assert b == s.Rational(11,29) and wbound == s.Rational(2523,2662)
assert 0 < wbound < 1
assert 1/(b*(1-wbound)) == s.Rational(7018,139)
assert s.Rational(1,2160)/Rbound == s.Rational(29,30)
# |u(q)|,v(q) increase on 0<=q<=1/12, so the endpoint majorant
# also covers analytic continuation along that real path.
check_zero(s.diff(-upath,q)-2*(48*q*q+12*q+1)/(8*q+1)**2)
check_zero(s.diff(vpath,q)-64*q**3*(6*q+1)/(8*q+1)**2)
print('PASS: constants, sign, and absolute convergence', flush=True)
result = {'all_exact_checks_passed':True,
          'scope':'exact differential-algebra bridge, constants, and convergence majorant',
          'value':'90/pi',
          'discovery_reference':'arXiv:2602.09352v1, Tables 2-4 and 50',
          'particular_literature_table_values_assumed':False,
          'general_modular_parametrization_certificate':'sun90_modparam_verify.py',
          'weighted_CM_evaluation_proof':'paper: independent Fricke differentiation',
          'Fricke_argument_verified_by_this_program':False,
          'prize_priority_or_payment_confirmed':False}
(BASE/'verify_sun90_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
