"""Exact Sturm certificate for the X60 degree-seven modular equation.

A=eta_1 eta_3 eta_4 eta_5 eta_12 eta_15 eta_20 eta_60 and
B=eta_2^2 eta_6^2 eta_10^2 eta_30^2 are weight-four holomorphic
forms with trivial character on Gamma_0(60). Clearing the recovered
polynomial by B(tau)^8 B(7tau)^8 gives weight 64, level 420.
Index=1152, so Sturm bound=6144. Integer arithmetic only.
"""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import sympy as s

BOUND=6144
SHIFT=256  # A^i B^(8-i) A7^j B7^(8-j) starts at q^(256+i+7j)
N=BOUND-SHIFT+1
AR={d:1 for d in (1,3,4,5,12,15,20,60)}
BR={d:2 for d in (2,6,10,30)}

def eta_product_unit(rs):
    sig=[0]*N
    for d in range(1,N):
        for m in range(d,N,d):sig[m]+=d
    log=[0]*N
    for d,r in rs.items():
        for n in range(d,N,d):log[n]-=r*d*sig[n//d]
    out=[1]
    for n in range(1,N):
        total=sum(log[k]*out[n-k] for k in range(1,n+1))
        assert total%n==0
        out.append(total//n)
    return out

def conv(a,b,n=N):
    """Exact signed Kronecker convolution, with a proven coefficient bound."""
    a=a[:n];b=b[:n]
    bound=min(len(a),len(b),n)*max(map(abs,a),default=0)*max(map(abs,b),default=0)
    if not bound:return [0]*n
    word=(bound.bit_length()+2+7)//8
    bits=8*word
    half=1<<(bits-1)
    def pack(v):
        pos=b''.join(max(t,0).to_bytes(word,'little') for t in v)
        neg=b''.join(max(-t,0).to_bytes(word,'little') for t in v)
        return int.from_bytes(pos,'little')-int.from_bytes(neg,'little')
    mask=(1<<(bits*n))-1
    offset=int.from_bytes(half.to_bytes(word,'little')*n,'little')
    packed=((pack(a)*pack(b))+offset)&mask
    raw=packed.to_bytes(word*n,'little')
    return [int.from_bytes(raw[i*word:(i+1)*word],'little')-half for i in range(n)]

def checks(rs):
    weight=sum(rs.values())//2
    assert sum(rs.values())%2==0
    assert sum(d*r for d,r in rs.items())%24==0
    assert sum((60//d)*r for d,r in rs.items())%24==0
    value=s.prod(d**r for d,r in rs.items())
    assert s.integer_nthroot(value,2)[1]
    assert all(r>=0 for r in rs.values())
    return weight

if __name__=='__main__':
    start=perf_counter()
    assert checks(AR)==checks(BR)==4
    assert 420*s.prod(1+s.Rational(1,p) for p in (2,3,5,7))==1152
    assert 64*1152//12==BOUND
    # Direct independent check of signed packing and truncation.
    av=[4,-3,2,-7];bv=[-5,1,4]
    assert conv(av,bv,6)==[sum(av[i]*bv[k-i] for i in range(len(av)) if 0<=k-i<len(bv)) for k in range(6)]
    data=json.loads(Path('prize90_geometry_mod7_result.json').read_text())
    coeff=[[0]*9 for _ in range(9)]
    for (i,j),v in zip(data['pairs'],data['coefficients']):
        coeff[i][j]=v
        if i!=j:coeff[j][i]=v
    a,b=eta_product_unit(AR),eta_product_unit(BR)
    print('eta products computed',round(perf_counter()-start,2),flush=True)
    ap=[[1]+[0]*(N-1)];bp=[[1]+[0]*(N-1)]
    for i in range(1,9):
        ap.append(conv(ap[-1],a));bp.append(conv(bp[-1],b))
        print('powers',i,'elapsed',round(perf_counter()-start,2),flush=True)
    E=[conv(ap[i],bp[8-i]) for i in range(9)]
    result=[0]*N
    for i in range(9):
        group=[0]*N
        for j in range(9):
            v=coeff[i][j]
            if not v:continue
            for k in range((N-1)//7-j+1):group[7*(k+j)]+=v*E[j][k]
        term=conv(E[i],group)
        for k in range(i,N):result[k]+=term[k-i]
        print('assembled row',i,'elapsed',round(perf_counter()-start,2),flush=True)
    nonzero=[(i+SHIFT,v) for i,v in enumerate(result) if v]
    assert not nonzero,nonzero[:5]
    x,y=s.symbols('x y')
    f=s.sympify(data['polynomial'])
    x0=(5-s.sqrt(21))/4
    yp=-2*(s.diff(f,x,2)-s.diff(f,x,y))/s.diff(f,x)
    G=(1-x)*(1-4*x)*(1+4*x*x)*(1-x+4*x*x)
    lam=s.simplify((1+x*s.diff(G,x)/(2*G)-x*yp/2).subs({x:x0,y:x0}))
    assert s.simplify(lam-(s.Rational(3,2)-11*s.sqrt(21)/42))==0
    assert s.simplify(s.diff(f,x).subs({x:x0,y:x0}))!=0
    out={'status':'proved modular identity by exact Sturm bound',
         'level':420,'weight':64,'index':1152,'sturm_bound':BOUND,
         'common_q_shift':SHIFT,'coefficients_verified_zero_through':BOUND,
         'polynomial_sha256':hashlib.sha256(data['polynomial'].encode()).hexdigest(),
         'diagonal':data['diagonal_factorization'],
         'target_lambda_from_implicit_derivatives':str(lam),
         'target_second_implicit_derivative':str(s.simplify(yp.subs({x:x0,y:x0}))),
         'elapsed_seconds':perf_counter()-start,
         'cm_branch_certificate':'prize90_geometry_cm_verify.py: exact rational eta-product bounds and root isolation'}
    Path('prize90_geometry_mod7_sturm_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2),flush=True)
