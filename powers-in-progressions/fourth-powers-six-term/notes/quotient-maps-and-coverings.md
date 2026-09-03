# P6 第四轮：六个椭圆商、Jacobian 分解与 C1 有限覆盖

日期：2026-09-03。本文只把符号恒等式与初等算术标为证明；LMFDB 数据仅用于选线，有限域
trace 仅用于回归。完整有理点集、任何 Mordell--Weil 生成元的有限指数/饱和性均仍保持
fail-closed。

## 0. C29 冻结补丁

记

\[
D=r^3-3r^2+1,\quad Q=r^2-r+1,\quad
H=r^3-6r^2+3r+1.
\]

原始 C29 方程和正规化平面曲线分别为

\[
s^2(s+3)D^3=4Q^3H,\qquad
F(r,k):=kD-(1+4k^3)r(r-1)=0.
\]

### 引理 0.1（原始参数双向复合）

在主开集

\[
D(r)(s+2)(1+4k^3)\ne0
\]

上，两向映射为

\[
k={3r(r-1)\over(s+2)D(r)},\qquad
s={1-8k^3\over1+4k^3},
\]

且互逆。

证明：精确恒等式

\[
D^3-Q^3H=27r^3(r-1)^3
\]

把原方程化为

\[
s^2(s+3)+108h^3=4,\qquad h={r(r-1)\over D}.
\]

该奇异三次的正规化是

\[
s={1-8k^3\over1+4k^3},\qquad h={k\over1+4k^3},
\qquad k={3h\over s+2}.
\]

后两组复合分别模三次方程及模 (F) 化为零；代码不是数值抽样，而是对分子做精确多项式
余式。证毕。

完整边界审计如下。

- (D=0)：因为 \(\gcd(D,Q)=\gcd(D,H)=1\)，原始仿射曲线上无点。正规化方程中它与
  (1+4k^3=0) 形成 (3\times3=9) 个几何边界对，不能倒回原仿射模型。
- (s=-2)：这是 ((s,h)=(-2,0)) 的 cusp，正规化参数为 (k=\infty)。仿射原模型给
  (r=0,1)，紧化后另有 (r=\infty) 分支。
- (1+4k^3=0)：对应奇异三次的三个几何无穷远点；(-1/4) 不是有理立方，故无有理
  (k)。
- (h=0)：有 (s=1) 和重根 (s=-2)，而 (r=0,1,\infty)，恰给先前已经逐局部参数
  核验的六个正规化分支。

冻结文件为 `PAPER_CUBE_C29_FREEZE.json`；它绑定
`PAPER_CUBE_C29_model.py` 的 SHA256
`D0D0562D788874E09AB6333CAE49E29BB36A5073738120F0460CBB3C78413D23`。

## 1. 原曲线到六个四次商：全局态射

\[
C_1:4X^4+Z^4=5Y^4,\qquad
C_2:3X^4+2Z^4=5Y^4.
\]

把四次商写在加权射影空间 \(\mathbf P(1,1,2)\) 中，坐标为
\([x:t:v]\)，方程 (v^2=ax^4+bt^4)。下表给的是齐次态射，所以不仅是某个仿射
chart 上的公式。

| 曲线 / involution | \([x:t:v]\) | \((a,b,c)\), (c^2=a+b) | Jacobian |
|---|---|---|---|
| (C_1/\langle X\mapsto-X\rangle) | \([Z:Y:2X^2]\) | \((-1,5,2)\) | (w^2=u^3+20u\) |
| (C_1/\langle Z\mapsto-Z\rangle) | \([X:Y:Z^2]\) | \((-4,5,1)\) | (w^2=u^3+80u\) |
| (C_1/\langle Y\mapsto-Y\rangle) | \([Z:X:5Y^2]\) | \((5,20,5)\) | (w^2=u^3-400u\) |
| (C_2/\langle X\mapsto-X\rangle) | \([Z:Y:3X^2]\) | \((-6,15,3)\) | (w^2=u^3+360u\) |
| (C_2/\langle Z\mapsto-Z\rangle) | \([X:Y:2Z^2]\) | \((-6,10,2)\) | (w^2=u^3+240u\) |
| (C_2/\langle Y\mapsto-Y\rangle) | \([Z:X:5Y^2]\) | \((10,15,5)\) | (w^2=u^3-600u\) |

三元组不可能同时为零，故每行确为全局态射。每个非平凡变号 involution 恰有四个几何
不动点；Riemann--Hurwitz 给商 genus 1。

### 引理 1.1（四次商到 Jacobian 的统一显式映射）

对

\[
D_{a,b}:v^2=ax^4+b,qquad c^2=a+b,
\]

选 (P_+=(1,c)) 为原点。在 (x\ne1) 上令

\[
T={v+c+(2a/c)(x-1)\over(x-1)^2}.
\]

则到 (E_{a,b}:w^2=u^3-4abu) 的映射是

\[
u=2(cT+a),\qquad
w=2c(T^2-a)(x-1)-4a(T+c).                 \tag{1}
\]

逆映射的主 chart 是

\[
T={u/2-a\over c},\quad
q={w+4a(T+c)\over2c(T^2-a)},\quad
x=1+q,\quad v=Tq^2-c-{2a\over c}q.       \tag{2}
\]

代入后两侧复合恒等于恒等映射；(1) 的椭圆方程误差被
(v^2-ax^4-b) 整除。这给六行所需的显式双有理映射。由于源、靶的光滑射影模型都是
proper curves，该非恒定有理映射唯一延拓为态射。

公式主 chart 的例外也已审计：(P_+\mapsto O)，而 (P_-=(1,-c)) 的有限像依次是

\[
(5,15),(80,720),(-16,-48),(40,280),(60,480),(-24,-24).
\]

逆式的 `(T^2=a)` 上共有四个几何点，而不全是无穷远点：`w=+4a(T+c)` 的两点来自
四次模型的两个无穷远点；`w=-4a(T+c)` 的两点是主逆式的 `0/0`，对应有限四次点，并由

\[
q=-{2Tc^3-4a^2+6ac^2\over4ac(T+c)}
\]

恢复。该式代回四次与椭圆方程及双向复合均已作精确测试。六个 `a` 均非有理平方，故
`T^2=a` 不含 Q-有理椭圆点；所有六个四次商的有理点仍可由主 chart、`O` 与 `(1,-c)`
传递。

## 2. 总商与 Kani--Rosen 的 \(\mathbf Q\)-同源

平方坐标

\[
[A:B:C]=[X^2:Y^2:Z^2]
\]

给整个 (V_4) 的总商：

\[
4A^2+C^2=5B^2\quad(C_1),\qquad
3A^2+2C^2=5B^2\quad(C_2).
\]

两者均光滑且含 ([1:1:1])，故 genus 0。这里的光滑性不是“偏导多项式非零”这一弱检查：
三个对角梯度系数全非零，所以共同消失只可能发生在非射影点 `(0,0,0)`。令三个阶二子群
为 (H_i)，上述三个 genus-1 商为 (E_i=C/H_i)。取三个 norm 映射的乘积

\[
\Phi:J(C)\longrightarrow E_1\times E_2\times E_3.
\]

曲线商映射可分且非常值，故微分 pullback
`H^0(E_i,Omega^1)->H^0(C,Omega^1)` 单射，其像是 \(H_i\) 的一维不变空间。因为总商
genus 0，没有 (V_4)-不变微分；三条直线恰是三个不同的非平凡特征空间，其直和为三维。
在 abelian variety 的 cotangent spaces 上，`Phi^*` 正是这三个曲线微分 pullback 的直和，
故为同构。于是 `(dPhi)` 是同构，\(\ker\Phi\) 有限；源靶同为三维，因此

\[
J(C_1)\sim_{\mathbf Q}E_{20}\times E_{80}\times E_{-400},\qquad
J(C_2)\sim_{\mathbf Q}E_{360}\times E_{240}\times E_{-600}.
\]

这正是 Kani--Rosen 幂等关系在本例的直接微分证明；早先五个好素数的 trace 等式只保留作
符号/扭曲回归测试，完全不参与同源证明。一般背景见
[Kani--Rosen 原论文](https://doi.org/10.1007/BF01443582)。

## 3. LMFDB 只用于选线

2026-09-03 通过 LMFDB 官方 API 对精确 (a)-invariants 核对得到：

| 因子 | LMFDB 模型/标签 | 数据库 rank | torsion 阶 |
|---|---|---:|---:|
| (E_{20}) | [800.e2](https://www.lmfdb.org/EllipticCurve/Q/800/e/2) | 1 | 2 |
| (E_{80}\cong E_5) | [1600.m2](https://www.lmfdb.org/EllipticCurve/Q/1600/m/2) | 1 | 2 |
| (E_{-400}\cong E_{-25}) | [800.d3](https://www.lmfdb.org/EllipticCurve/Q/800/d/3) | 1 | 4 |
| (E_{360}) | [57600.bl2](https://www.lmfdb.org/EllipticCurve/Q/57600/bl/2) | 2 | 2 |
| (E_{240}\cong E_{15}) | [7200.bc2](https://www.lmfdb.org/EllipticCurve/Q/7200/bc/2) | 1 | 2 |
| (E_{-600}) | [57600.bt1](https://www.lmfdb.org/EllipticCurve/Q/57600/bt/1) | 2 | 2 |

这里 (E_A:y^2=x^3+Ax)，而 (A=80,-400,240) 分别除以 (2^4) 得数据库的
(5,-25,15) 模型。该表只说明 C1 的数据库总秩 3 低于 C2 的 5，因而选 C1；它不替代
本地 2-descent、有限指数和饱和证明。API 原始入口例如
[800.e2 JSON](https://www.lmfdb.org/api/ec_curvedata/?lmfdb_label=800.e2&_format=json)，
数据范围/可靠性边界见 [LMFDB reliability](https://www.lmfdb.org/EllipticCurve/Q/Reliability)。

## 4. C1 的有限第四幂覆盖集

对 primitive integral C1 点，2-adic 检查已知 (X,Y,Z) 全奇。先注意

\[
Z^4+4X^4=(Z^2-2XZ+2X^2)(Z^2+2XZ+2X^2). \tag{3}
\]

若素数 (p\mid X,Z)，则对 `p!=5`，C1 方程推出 (p\mid Y)。若 `p=5`，左端的
5-adic valuation 至少为 4；若 `5` 不整除 `Y`，右端 valuation 恰为 1，矛盾，故仍有
`5|Y`。两种情形都与 primitive 矛盾，所以 \(\gcd(X,Z)=1\)。记 (3) 的两因子为
(A,B)。它们均为正奇数。
若奇素数 (p\mid A,B)，则 (p\mid4XZ)；再代入 (A) 即推出 (p\mid X,Z)，矛盾。
所以 \(\gcd(A,B)=1\)。由

\[
AB=5Y^4
\]

逐素数比较 valuation，所有 primitive 点恰落入以下两张覆盖之一：

\[
\begin{array}{ll}
\mathcal D_+:&A=R^4,\quad B=5S^4,\quad Y=\pm RS,\\
\mathcal D_-:&A=5R^4,\quad B=S^4,\quad Y=\pm RS.
\end{array}                                      \tag{4}
\]

(Z\mapsto-Z) 交换两张覆盖，故算术上只需处理一张代表。状态表：

| cover | 局部状态 | 已知全局点 | 非平凡全局点 |
|---|---|---|---|
| \(\mathcal D_+\) | 处处局部可解（由 Q 点） | \((X,Z,R,S)=(1,1,1,1)\) | 未决 |
| \(\mathcal D_-\) | 处处局部可解（由 Q 点） | \((1,-1,1,1)\) | 未决 |

因此本轮已经得到**有限且完备**的两张第四幂提升 covering collection，但尚未证明其有理点
只有上述 trivial 点。这个边界很重要：椭圆因子的 rank 表也不能自行关闭 (4)。

## 5. 已证、未决和下一步最小任务

已证：六个全局 quotient 态射；统一四次到 Jacobian 的双向公式；总商 conic；
(J(C_i)) 的 Q-同源分解；C1 的两张完备 primitive covering collection；两张 cover
均处处局部可解。

未决：六个 Mordell--Weil 群的本地严格生成元与饱和证书；\(\mathcal D_+\) 的全部 Q 点；
故 (C_1(\mathbf Q)) 和 (P_6(4)) 尚未闭合。

下一轮最小任务是只处理 \(\mathcal D_+\)：把其投到 LMFDB-recorded rank-1（仅作选线）
因子 (E_{20},E_5,E_{-25})，
计算每一投影上的平方类条件，并用经审计的 2-descent + elliptic Chabauty/Mordell--Weil
sieve 关闭非平凡 lift。第五轮已证明这一 lift 等价于 genus-1 四次

\[
5V^2=p^4-8p^3+18p^2+8p+1
\]

上的平方条件 `q^2=V/(1+p^2)`；相应双覆盖有 8 个分支点，genus 为 5。因此没有进一步
下降或经审计的有限指数/饱和及筛证书时，稿件仍 submission-blocked，不能把现有代数入口
单独描述成可投稿单元。

## 6. 可复核命令

```text
python -m unittest PAPER_CUBE_C29_test_model PAPER_CUBE_P6_test_gate PAPER_CUBE_P6_test_maps -v
python PAPER_CUBE_C29_model.py
python PAPER_CUBE_P6_maps.py
```

核心代码：`PAPER_CUBE_P6_maps.py`；测试：`PAPER_CUBE_P6_test_maps.py`。脚本不访问网络，
不调用外部 CAS，也不会把 LMFDB 或 synthetic transcript 提升为数学证明。
