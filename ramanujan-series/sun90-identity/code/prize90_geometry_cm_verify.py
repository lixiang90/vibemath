"""Self-contained arithmetic checks for the X60 CM branch and lambda.

Run prize90_geometry_mod7_sturm.py first for the modular-polynomial theorem.
No floating-point computation or guessed CM value is used in this verifier.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import sympy as s

def atan_bounds(x, even_terms):
    assert 0<x<1 and even_terms%2==0
    lower=sum((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(even_terms))
    upper=lower+x**(2*even_terms+1)/F(2*even_terms+1)
    return lower,upper

def exp_bounds(x, terms=20):
    assert 0<x<terms+2
    lower=sum(x**k/F(factorial(k)) for k in range(terms+1))
    tail=x**(terms+1)/F(factorial(terms+1))/(1-x/F(terms+2))
    return lower,lower+tail

if __name__=='__main__':
    data=json.loads(Path('prize90_geometry_mod7_result.json').read_text())
    sturm=json.loads(Path('prize90_geometry_mod7_sturm_result.json').read_text())
    assert sturm['polynomial_sha256']==sha256(data['polynomial'].encode()).hexdigest()
    assert sturm['coefficients_verified_zero_through']==sturm['sturm_bound']==6144
    # Machin's identity, checked through rational tangent addition.
    a=F(1,5)
    tan2=2*a/(1-a*a)
    tan4=2*tan2/(1-tan2*tan2)
    assert (tan4-F(1,239))/(1+tan4/F(239))==1
    al,au=atan_bounds(F(1,5),8)
    bl,bu=atan_bounds(F(1,239),2)
    pi_lo,pi_hi=16*al-4*bu,16*au-4*bl
    assert F(6283,2000)<pi_lo<pi_hi<F(22,7)
    root_lo,root_hi=F(683,2000),F(427,1250)
    assert root_lo**2<F(7,60)<root_hi**2
    exp_lo,_=exp_bounds(2*F(6283,2000)*root_lo)
    _,exp_hi=exp_bounds(2*F(22,7)*root_hi)
    qlo,qhi=F(29,250),F(59,500)
    assert exp_hi<1/qlo and exp_lo>1/qhi
    # Thus qlo < exp(-2*pi*sqrt(7/60)) < qhi.
    AD=(1,3,4,5,12,15,20,60)
    BD=(2,6,10,30)
    numerator_sum=sum(qhi**d/(1-qhi**d) for d in AD)
    denominator_sum=2*sum(qhi**d/(1-qhi**d) for d in BD)
    assert 0<numerator_sum<1 and 0<denominator_sum<1
    Xlo=qlo*(1-numerator_sum)
    Xhi=qhi*(1-qlo)/(1-denominator_sum)
    assert F(1,10)<Xlo<Xhi<F(11,100)
    # A/B is Fricke-invariant: its exponent list is invariant under d -> 60/d
    # and the product of d^r is one, eliminating the multiplier.
    exponents={d:1 for d in AD}
    exponents.update({d:-2 for d in BD})
    assert all(exponents.get(60//d)==v for d,v in exponents.items())
    assert s.prod(s.Rational(d)**v for d,v in exponents.items())==1
    x,y=s.symbols('x y')
    phi=s.sympify(data['polynomial'])
    diag=s.factor(phi.subs(y,x))
    assert s.Poly(diag,x).count_roots(s.Rational(1,10),s.Rational(11,100))==1
    x0=(5-s.sqrt(21))/4
    assert s.simplify(phi.subs({x:x0,y:x0}))==0
    assert s.Rational(1,10)<x0<s.Rational(11,100)
    fx=s.diff(phi,x)
    assert s.simplify(fx.subs({x:x0,y:x0}))!=0
    second=-2*(s.diff(phi,x,2)-s.diff(phi,x,y))/fx
    G=(1-x)*(1-4*x)*(1+4*x*x)*(1-x+4*x*x)
    lam=s.simplify((1+x*s.diff(G,x)/(2*G)-x*second/2).subs({x:x0,y:x0}))
    assert s.simplify(lam-(s.Rational(3,2)-11*s.sqrt(21)/42))==0
    out={'status':'exact rational CM branch and implicit derivative checks passed',
        'modular_polynomial_proof_dependency':'prize90_geometry_mod7_sturm.py',
        'cm_tau':'i*sqrt(7/60)', 'q_lower':str(qlo),'q_upper':str(qhi),
        'X_lower_exact':str(Xlo),'X_upper_exact':str(Xhi),
        'X_interval':'(1/10,11/100)', 'diagonal_roots_in_interval':1,
        'proved_X60_CM_value':str(x0),'proved_lambda60_CM_value':str(lam),
        'lambda_formula':'1 + x*Gprime/(2*G) - x*Ysecond/2',
        'scope':'exact arithmetic checks of the CM branch and implicit derivatives',
        'general_modular_parametrization_certificate':'sun90_modparam_verify.py',
        'weighted_CM_evaluation_proof':'paper: independent Fricke differentiation',
        'Fricke_argument_verified_by_this_program':False,
        'particular_literature_table_values_assumed':False,
        'priority_or_prize_eligibility_verified':False}
    Path('prize90_geometry_cm_verify_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if 'exact' not in k},indent=2))
