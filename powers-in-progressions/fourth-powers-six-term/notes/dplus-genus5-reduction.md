# 乙线第五轮报告：P6 稿件修订、D+ 椭圆投影与 genus-5 闸门

日期：2026-09-03  
状态：**代数修订通过；D+ 全局点仍 fail-closed；稿件仍 submission-blocked。**

## 1. 本轮结论

本轮修复了 `PAPER_CUBE_MANUSCRIPT_REVIEW_ELLIPTIC_04.md` 的全部公式／证明型
blocking 与 major 项，并把两页目录式 TeX 扩为五页自足工作稿。最重要的新严格结论是：

1. `D_+` 的三个椭圆投影均已有显式公式和双层平方 lift；
2. `D_+` 还可双向化为 genus-1 四次

   \[
   G:\quad 5V^2=p^4-8p^3+18p^2+8p+1
   \]

   上的平方条件

   \[
   q^2=\frac{V}{1+p^2}.
   \]

3. 这个二次覆盖有 8 个几何分支点，故 genus 为 5；所以当前并没有降成有限个
   genus <= 1 问题，不能伪称闭合；
4. `D_+` 的 `X=Z` 非零对称分支只给 primitive trivial 点，`X=-Z` 分支与
   `XZ=0` 分支均由 5-adic valuation 排除。这个有限对称子问题已完整闭合，但不足以
   决定整个 cover。

## 2. 审稿问题的逐项修复

### 2.1 quartic--Jacobian 例外纤维

对 `D_{a,b}:v^2=ax^4+b`，`c^2=a+b`，保留原主 chart，并补齐：

- Jacobian 逆式代回 quartic 后，分子模椭圆方程余式为零；六行全部机器复核。
- `(1,-c)` 的有限像从 quartic 负分支的二阶 Taylor 展开求出，不再手填目标点。
- `(1,c)` 的 `T` 分子常数项为 `2c`，因此 `u` 有二阶极点，严格给出 `O`。
- 在 infinity 以 `e=1/x` 做 Laurent 展开，得到
  `T=+/-sqrt(a)`、`w=+4a(T+c)`，恰为两个 quartic infinity。
- `T^2=a, w=-4a(T+c)` 的另两个几何点不是 infinity，而是有限 quartic 点；补入

  \[
  q=-\frac{2Tc^3-4a^2+6ac^2}{4ac(T+c)}
  \]

  并精确验证 quartic 落点及 round trip。

这修正了第四轮报告中过强的几何表述。六个 `a=-1,-4,5,-6,-6,10` 都不是 Q 中平方，
所以不影响 Q-点传递。

### 2.2 quotient、总 conic 与 Kani--Rosen

- 六行都记录了唯一变号坐标比 `q`，且 `q^2=v/scale`；其余比由 `x` 生成。因此固定域
  恰为商域，泛型次数恰为 2，deck transformation 恰为指定 involution。
- 总商光滑性测试改为三个对角梯度系数均非零；这真正推出共同零点只有非射影原点。
- TeX 改用 norm map
  `Phi:J(C)->product J(C/H_i)`。在 cotangent spaces 上，`Phi^*` 是三条曲线微分
  pullback 的直和。总商 genus 0 排除 trivial character，三个一维 `H_i`-invariant
  spaces 恰为三个不同非平凡 character spaces，故 `Phi^*` 满秩、kernel 有限，得到
  Q-isogeny。这样严格区分了曲线微分 pullback 与 abelian tangent/cotangent map。

### 2.3 C1 covering 完备性

TeX 现在写出 `p=5` 的完整论证：若 `5|X,Z`，左端 valuation 至少 4；若 `5` 不整除
`Y`，右端 valuation 恰为 1，矛盾，故 `5|Y`，与 primitive 性矛盾。之后正奇因子

\[
A=(Z-X)^2+X^2,\qquad B=(Z+X)^2+X^2
\]

满足 `gcd(A,B)=1`、`AB=5Y^4`，逐素数 valuation 恰给且只给 `D_+`,`D_-` 两成员。
代码的 classifier 不再只看 `mod 5` 标签，而会求并验证精确 integral fourth roots；若
纸面 valuation 引理与输入不一致就抛错。

### 2.4 LMFDB 边界与 C29 freeze

- 全文统一改为 “LMFDB-recorded rank, used only for heuristic route selection”；没有
  rank upper bound、finite index、generators 或 saturation 被提升为定理输入。
- C29 manifest 新增完整 `live_certificate`；测试逐字段比较实时生成的 equation、maps、
  denominators、exceptional fibres 与 manifest，而不只检查源文件 hash。

## 3. D+ 三个显式投影及 lift

令 `Y=RS`。三个 quartic 坐标为：

| factor | `(x,v)` | D+ extra lift | reverse reconstruction |
|---|---|---|---|
| `E_20` | `(Z/(RS),2X^2/(R^2S^2))` | `alpha^2=v/2`, `eta^2=(x-alpha)^2+alpha^2` | `(X,Z,R,S)=(alpha eta,x eta,eta,1)` |
| `E_80` | `(X/(RS),Z^2/(R^2S^2))` | `beta^2=v`, `eta^2=(beta-x)^2+x^2` | `(x eta,beta eta,eta,1)` |
| `E_-400` | `(Z/X,5R^2S^2/X^2)` | `gamma^2=v/5`, `eta^2=(x-1)^2+1` | `(1/eta,x/eta,1,gamma/eta)` |

再与统一 `quartic_to_jacobian` 公式复合，即得三个 `D_+ -> E_A` 的显式 `(u,w)`；代码证书
保存其完全展开式，并验证目标椭圆方程。三个 reverse reconstruction 也逐恒等式核验：
第二个 `D_+` 方程分别约化为原 quartic 方程。

## 4. 同时降维及为何本轮不能闭合

`R!=0`。令

\[
x_0=X/R^2,\quad z_0=Z/R^2,\quad q=S/R.
\]

第一方程成为 `(z_0-x_0)^2+x_0^2=1`，参数化为

\[
x_0=\frac{2p}{1+p^2},\qquad
z_0=\frac{1+2p-p^2}{1+p^2},\qquad
p=\frac{x_0}{1+z_0-x_0}.
\]

`p=infinity` 对应 `X=0`，已由 valuation 排除。第二方程化为本报告开头的 `(G,q)`。
精确计算给

\[
\operatorname{disc}(F)=2^{17},\qquad
\operatorname{Res}(F,1+p^2)=2^9.
\]

因此零、极支集不相交。`V/(1+p^2)` 在四个 `F` 根处各有奇阶零，在 `p=+/-i` 上的
四个点各有奇阶极；两个 infinity 的阶为 0。Riemann--Hurwitz 给 `g(D_+)=5`。

结论是明确的 stop-rule：仅靠手工椭圆投影，本轮不能把全局点问题降到有限 genus <= 1；
继续宣称即将手证闭合不可信。

## 5. 最小经审计 CAS 需求

本机没有 Magma、Sage、mwrank、PARI/GP；PowerShell 的 `gp` 是别名而非 PARI。
任何未来 promotion 至少必须保存二进制 hash、版本、输入 hash、完整 stdout/stderr、退出码及
唯一成功 marker，并产生以下数学对象：

1. 对 `G:5V^2=F(p)` 给严格 `RankBounds`、生成元和 finite-index/saturation 证明；
2. 计算 `G(Q)` 上函数 `V/(1+p^2)` 取平方的所有点／cosets，逐一处理四个零、四个极及
   两个 infinity；
3. 若走三个因子路线，对 `E_20,E_80,E_-400` 分别给同样的 rank upper bound、饱和基与
   两层 lift cosets；
4. 对余下 genus-5 covers 给可核验的 descent + Mordell--Weil sieve／Chabauty 完备证书。

缺任一 finite-index 或 saturation 环节都不能提升为“无非平凡点”。

## 6. 低垂备选与投稿判据

已经闭合的低垂备选单元是 **D+ 对称与零坐标 strata 的完整分类**：
`X=Z` 只给 primitive trivial 点，`X=-Z` 与 `XZ=0` 无非零 Q 点。它同时清除了三个投影
主 chart 的相关边界，可作为正文引理；但它不是独立可发表主定理。

继续 P6 的条件：取得 `G(Q)` 的严格 MW basis + saturation，并使 square-value sieve
成为有限问题。退出／转题条件：无法获得上述审计对象，或 genus-5 cover 的 Jacobian rank
门不打开。当前投稿状态仍是 **blocked**，因为 `D_+(Q)`、`C_1(Q)`、`P_6(4)` 均未闭合。

## 7. 复现与 QA

执行：

```text
python -m unittest -v PAPER_CUBE_C29_test_model.py PAPER_CUBE_P6_test_gate.py PAPER_CUBE_P6_test_maps.py
pdflatex -interaction=nonstopmode -halt-on-error PAPER_CUBE_TEX.tex
pdflatex -interaction=nonstopmode -halt-on-error PAPER_CUBE_TEX.tex
```

结果：**22 tests OK**；PDF 5 页，最终 log 无 LaTeX warning、overfull/underfull box；5 页均经
PNG 渲染目检，无裁切、重叠或坏字形。最终 PDF SHA-256：
`8AD9C3673B653241F4DF8D4646CB0A2C500DAA4FB3386725D86B39EBB43DCD21`。

## 8. 外部来源边界

- [Hajdu--Tengely, Powers in arithmetic progressions, Ramanujan J. 55 (2021), 965--986](https://doi.org/10.1007/s11139-020-00331-5)：使用 Theorem 3 及 pp. 983--986 的 N=6 讨论。
- [Kani--Rosen, Idempotent relations and factors of Jacobians, Math. Ann. 284 (1989), 307--327](https://doi.org/10.1007/BF01443582)：只作同源分解背景；本文给本例微分证明。
- [LMFDB](https://www.lmfdb.org/)：只作 2026-09-03 的选线记录，不作证明输入。
