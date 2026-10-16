"""Independent exact eta/E2/Sturm proof of the level-60 parametrization.

No tabulated modular identity, CM value, or prior Sun90 verifier is imported.
Inputs are the displayed eta exponents and the two integer polynomials.
Standard eta-quotient modularity/cusp-order criteria, derivative covariance,
and Sturm's theorem turn the exact finite checks into identities.
Run: python sun90_modparam_verify.py
"""
from fractions import Fraction as F
from math import gcd, prod
from pathlib import Path
import hashlib
import json
import sympy as s

LEVEL=60
INDEX=LEVEL*F(3,2)*F(4,3)*F(6,5)
assert INDEX==144
BOUND4=4*int(INDEX)//12
BOUND8=8*int(INDEX)//12
assert (BOUND4,BOUND8)==(48,96)
N=BOUND8+1
DIVS=[d for d in range(1,LEVEL+1) if LEVEL%d==0]
AR={d:1 for d in (1,3,4,5,12,15,20,60)}
BR={d:2 for d in (2,6,10,30)}
CR={d:1 for d in (2,6,10,30)}
XR={d:AR.get(d,0)-BR.get(d,0) for d in DIVS}
ZR={d:CR.get(d,0)+2*BR.get(d,0)-2*AR.get(d,0) for d in DIVS}

def square_fraction(value):
    p,q=value.numerator,value.denominator
    return s.integer_nthroot(p,2)[1] and s.integer_nthroot(q,2)[1]

def eta_modularity(rs,weight):
    assert sum(rs.values())==2*weight
    assert sum(d*r for d,r in rs.items())%24==0
    assert sum((LEVEL//d)*r for d,r in rs.items())%24==0
    character=prod((F(d)**r for d,r in rs.items()),start=F(1))
    assert square_fraction(character) and weight%2==0
    return character

assert eta_modularity(AR,4)==12960000
assert eta_modularity(BR,4)==12960000
assert eta_modularity(CR,2)==3600
assert eta_modularity(XR,0)==1
assert eta_modularity(ZR,2)==3600

def cusp_order(rs,den):
    return F(LEVEL,24*gcd(den*den,LEVEL))*sum(
        (F(gcd(den,d)**2,d)*r for d,r in rs.items()),start=F(0))

cusp=[]
for den in DIVS:
    ax,bx,cx,x,z=[cusp_order(rs,den) for rs in (AR,BR,CR,XR,ZR)]
    assert ax>=0 and bx>=0 and cx>=0 and z>=0
    if den in (2,6,10,30):
        assert (x,z)==(-2,6)
    else:
        assert (x,z)==(1,0)
    # G has degree 6 and nonzero constant; J has degree 6 and order 1.
    g_order=6*x if x<0 else F(0)
    j_order=6*x if x<0 else x
    assert g_order+2*z>=0 and j_order+4*z>=0
    cusp.append({'denominator':den,'X_order':str(x),'Z_order':str(z),
                 'G_X_Z_squared_order':str(g_order+2*z),
                 'J_X_Z_fourth_order':str(j_order+4*z)})
print('PASS: eta modularity, trivial characters, and all cusp orders',flush=True)

sigma=[0]*N
for d in range(1,N):
    for m in range(d,N,d):sigma[m]+=d

def eta_series(rs):
    lead=F(sum(d*r for d,r in rs.items()),24)
    assert lead.denominator==1 and lead>=0
    shift=int(lead)
    ld=[0]*N
    for d,r in rs.items():
        for m in range(d,N,d):ld[m]-=r*d*sigma[m//d]
    unit=[1]
    for n in range(1,N):
        value=sum(ld[k]*unit[n-k] for k in range(1,n+1))
        assert value%n==0
        unit.append(value//n)
    return [0]*shift+unit[:N-shift],ld,shift

def conv(a,b):
    return [sum(a[k]*b[n-k] for k in range(n+1)) for n in range(N)]

def D(a):return [n*a[n] for n in range(N)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,c):return [x*c for x in a]
def power(a,n):
    out=[1]+[0]*(N-1)
    for _ in range(n):out=conv(out,a)
    return out

X,L_tail,Xlead=eta_series(XR)
Z,_,Zlead=eta_series(ZR)
assert Xlead==1 and Zlead==0 and X[1]==1 and Z[0]==1
# D log X = (1/24) sum_d r_d d E2(d tau).
# Constant = sum d r_d/24=1; nonconstant coefficients are L_tail.
L=[Xlead]+L_tail[1:]
E2=[1]+[-24*sigma[n] for n in range(1,N)]
L24=[0]*N
for d,r in XR.items():
    L24[0]+=r*d
    for n in range(1,(N-1)//d+1):L24[d*n]+=r*d*E2[n]
assert all(a==24*b for a,b in zip(L24,L))
# Also check the formal logarithmic derivative without division.
assert D(X)==conv(X,L)

x=s.symbols('x')
Gexpr=(1-x)*(1-4*x)*(1+4*x*x)*(1-x+4*x*x)
Jexpr=4*x*(1-8*x+40*x*x-83*x**3+160*x**4-144*x**5)
G=[int(s.expand(Gexpr).coeff(x,i)) for i in range(7)]
J=[int(s.expand(Jexpr).coeff(x,i)) for i in range(7)]
assert G==[1,-6,17,-48,68,-96,64]
assert J==[0,4,-32,160,-332,640,-576]
Xp=[power(X,i) for i in range(7)]
def evaluate(coeffs):
    return [sum(coeffs[i]*Xp[i][n] for i in range(7)) for n in range(N)]
GX,JX=evaluate(G),evaluate(J)
Z2,Z4=power(Z,2),power(Z,4)
identity4=sub(power(L,2),conv(GX,Z2))
F8=sub(scale(conv(Z,D(D(Z))),2),scale(power(D(Z),2),3))
identity8=sub(F8,conv(JX,Z4))
assert not any(identity4[:BOUND4+1])
assert not any(identity8[:BOUND8+1])
# Extra exact coefficients have been computed; they also vanish.
assert not any(identity4) and not any(identity8)
print('PASS: weight-4 identity through Sturm bound 48',flush=True)
print('PASS: weight-8 identity through Sturm bound 96',flush=True)

# Algebraic covariance proof: for f of weight 2, a=c/(2*pi*i), j=c*tau+d,
# (Df)(gamma tau)=j^4 Df+2 a j^3 f, and
# (D^2f)(gamma tau)=j^6 D^2f+6 a j^5 Df+6 a^2 j^4 f.
jj,a,f,f1,f2=s.symbols('j a f f1 f2')
fg=jj**2*f
f1g=jj**4*f1+2*a*jj**3*f
f2g=jj**6*f2+6*a*jj**5*f1+6*a*a*jj**4*f
assert s.expand(2*fg*f2g-3*f1g*f1g-jj**8*(2*f*f2-3*f1*f1))==0
# This covariance, applied to a cusp expansion of f, proves holomorphy
# at every cusp as well as modularity. It supplies the weight-8 hypothesis.

# Derive the linear third-order equation independently from the two identities.
g,g1,g2,jv,j1,f3=s.symbols('G G1 G2 J J1 f3')
nonlinear=2*g*f*f2-g*f1*f1+g1*f*f1-jv*f*f
replacement={g:g1,g1:g2,jv:j1,f:f1,f1:f2,f2:f3}
derivative=sum(s.diff(nonlinear,symbol)*value for symbol,value in replacement.items())
linear=2*g*f3+3*g1*f2+(g2-2*jv)*f1-j1*f
assert s.expand(derivative-f*linear)==0
print('PASS: derivative covariance and the implied third-order equation',flush=True)

# At the already isolated CM nome 0<Q<59/500, a simple rational bound
# proves the positive sign of L/Z, independently of a square-root convention.
h=F(59,500)
L_lower=F(1)-sum((F(d)*h**d/(1-h**d)**3 for d in AR),start=F(0))
assert L_lower>0
# Z is a positive eta quotient for real 0<Q<1. Hence L=+sqrt(G(X))*Z
# at the CM point, and initially at the cusp X=Q+O(Q^2), Z=1+O(Q).

result={'status':'independently proved level-60 eta parametrization',
 'literature_table_data_used_as_theorems':False,
 'standard_theorems':['eta-quotient modularity and cusp-order criterion',
                      'E2 logarithmic derivative of eta',
                      'derivative covariance / Rankin-Cohen bracket',
                      'Sturm bound theorem'],
 'level':LEVEL,'index':int(INDEX),
 'weight4_sturm_bound':BOUND4,'weight8_sturm_bound':BOUND8,
 'coefficients_exactly_checked_through':N-1,
 'identity4':'(D log X)^2 = G(X) Z^2',
 'identity8':'2 Z D^2 Z - 3 (D Z)^2 = Z^4 J(X)',
 'linear_ode':'G delta^3 Z + (3/2) delta(G) delta^2 Z + ((1/2)delta^2(G)-J)delta Z -(1/2)delta(J) Z = 0',
 'G_coefficients':G,'J_coefficients':J,
 'cusp_orders':cusp,
 'positive_sign_at_CM_nome_bound':'0<Q<59/500',
 'L_lower_exact':str(L_lower),
 'X_series_sha256':hashlib.sha256(','.join(map(str,X)).encode()).hexdigest(),
 'Z_series_sha256':hashlib.sha256(','.join(map(str,Z)).encode()).hexdigest()}
Path(__file__).with_name('sun90_modparam_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','level','index','weight4_sturm_bound','weight8_sturm_bound','coefficients_exactly_checked_through']},indent=2))
