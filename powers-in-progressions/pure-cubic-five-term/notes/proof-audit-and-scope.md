# 第六轮乙线：纯三次域 Kummer 版五项非零密度

日期：2026-09-03  
主结论：**定义不退化，并且严格证明**

\[
R^{\times}_{(3,1)}(5)=4.
\]

五项全命中的全部颜色轨道已经分类和排除。所有达到 4 的具体有理 AP 的完整点分类尚未
完成；本报告把这个额外要求明确隔离，不用有限搜索冒充分类。

## 1. 精确定义与边界

令

\[
A_i=a+id\quad(0\le i<5),\qquad a,d\in\mathbf Q,quad d\ne0.
\]

对非平凡立方类 `[D] in Q*/Q*3`，令 `K_D=Q(cuberoot(D))`。定义
`R^x_(3,1)(5)` 为：存在同一个 `D` 和同一个公共有理缩放 `lambda in Q*`，使
`lambda*A_i` 在 `K_D` 中为立方的 **非零** 项的最大数目。

边界处理如下。

- `A_i=0` 没有 Kummer 类，且不计数。若计零，`-2,-1,0,1,2` 会在
  `Q(cuberoot(2))` 中五项全命中，问题被零支配。
- `D=0` 不定义数域，排除。
- 若 `[D]=1`，则 `K_D=Q`，次数退化；问题变成普通有理立方密度，而
  `P_5(3)=3`，不能达到本题最大值 4。
- `-1=(-1)^3`，所以 `D` 和 `-D` 给同一实纯三次域。
- 每个有理 `D` 类可取正的无立方因子整数代表，各素数指数规范为 1 或 2。
- `D` 与 `D^2` 给同一数域。更一般地，两个非退化纯三次域相同当且仅当它们在
  `Q*/Q*3` 中生成同一条 F3 直线。
- AP 按公共有理缩放等价；反转为 `(a,d)->(a+4d,-d)`。

公共缩放意味着单个 primitive integer 证书的颜色首先是仿射形式 `g+c_i delta`，不能
一开始误写成固定经过 1 的线性子空间。全局允许再缩放时可令 `g=0`，但素数支持证明中
必须保留 `g`；代码和正文都按此处理。

## 2. Kummer kernel：非平凡，恰为一条 F3 直线

写 `alpha^3=D`，以及

\[
y=a+b\alpha+c\alpha^2.
\]

将 `y^3` 在基 `1,alpha,alpha^2` 下约化，两个非有理系数为

\[
3(a^2b+Da c^2+Db^2c),\qquad
3(a^2c+ab^2+Dbc^2).
\]

若 `a=0`，两式立即给 `bc=0`，所以 `y` 在 `Q alpha` 或 `Q alpha^2` 上。
若 `a!=0`，令 `B=b/a,C=c/a`。消去 `C`、`B` 的两个 resultant 分别为

\[
BD(B^3D-1)^2,\qquad C(C^3D^2-1)^2.
\]

非退化假设排除 `B^3D=1` 和 `C^3D^2=1`；于是 `B=C=0`。因此

\[
y^3\in\mathbf Q^*\Longrightarrow
y\in\mathbf Q^*\sqcup\mathbf Q^*\alpha\sqcup\mathbf Q^*\alpha^2.
\]

反向显然，故

\[
\ker\bigl(\mathbf Q^*/\mathbf Q^{*3}\to K_D^*/K_D^{*3}\bigr)
=\{1,[D],[D]^2\}.
\]

所以本题没有退化成普通 `P_5(3)`；纯三次域确实新增加两个有理立方类。

同一域判别也随之得到：若 `K_E=K_D`，则 `E` 在 `K_D` 中为立方，所以
`[E] in <[D]>`；两边次数均为 3 排除单位类，故 `[E]=[D]` 或 `[D]^2`。反向由
`alpha`、`alpha^2` 直接成立。

## 3. 五位置颜色轨道

五项全命中时，经公共缩放可写

\[
A_i=D^{c_i}x_i^3,\qquad c_i\in\mathbf F_3,quad x_i\in\mathbf Q^*.
\]

三个等价操作为

\[
c_i\mapsto c_i+k,qquad c_i\mapsto-c_i,qquad
(c_0,\ldots,c_4)\mapsto(c_4,\ldots,c_0).
\]

脚本穷尽 `3^5=243` 个词，得到 **25 个轨道**。

其中 9 个轨道在位置三项 AP

```text
(0,1,2), (1,2,3), (2,3,4), (0,2,4)
```

之一上同色。缩放后这给三个非恒定有理立方组成 AP，违反 Darmon--Merel 定理。
另有唯一代表 `00100`：位置 `0,1,3,4` 四项同色，违反 Hajdu--Tengely 的
`P_5(3)=3`。

这里从有理表述调用整数表述没有隐藏假设：对有关位置的有限个有理立方根，以及 AP 的
首项、公差，取整数 `L` 清除全部分母；整条 AP 乘以共同立方 `L^3` 后成为整数 AP，
同时这些立方根乘以 `L` 后为整数。因此立方位置与非恒定性均保持，Darmon--Merel 与
Hajdu--Tengely 的整数结论均可严格应用。

剩余恰 15 个：

```text
00101 00102 00110 00112 00120 00121 00122
01001 01002 01012 01021 01102 01120 01201 01210
```

每个轨道的 12 个至多变换均由代码显式生成，所有 orbit 的并集重新覆盖 243 个词。

## 4. 素数支持引理

把 AP 化为 primitive integer progression。对 `i!=j`，

\[
\gcd(A_i,A_j)\mid |i-j|,
\]

因为该 gcd 同时整除 `(j-i)d`，而 `gcd(A_i,d)=gcd(a,d)=1`。所以 `p>3` 至多整除
五项中的一项。

对某个 `p>3`，五个 valuation residues 必须为

\[
e_i=g_p+c_i\delta_p\in\mathbf F_3.
\]

若唯一被 `p` 整除的项具有非零 residue，`(e_i)` 就是 singleton-support vector。
但上述 15 个词只有以下 block sizes：

```text
3+2, 3+1+1, 2+2+1.
```

- 两色 `3+2`：两个色块大小均至少 2，仿射函数不能只在一个位置非零；
- 三色情形：仿射函数在另外两个颜色上为零便恒为零。

故 singleton support 不可能。所有 `p>3` 在每项中的指数都为 `0 mod 3`。于是 offset
`g` 与 direction `delta` 都只支撑在 `{2,3}`。去掉 offset 后，`F3^2` 中只有四条方向，
可取代表

```text
D = 2, 3, 6, 18.
```

注意 `18` 与其逆类 `12` 定义同一纯三次域；这里只把 `18` 固定为曲线证书的方向代表。

## 5. 60 条具体曲线与完整局部排除

对词 `c=(c_0,...,c_4)` 和固定 `D`，五项 AP 条件成为 `P^4` 中三条三次方程：

\[
D^{c_i}x_i^3-2D^{c_{i+1}}x_{i+1}^3+D^{c_{i+2}}x_{i+2}^3=0,
\quad i=0,1,2.
\]

这给 `15*4=60` 条完全明确的 projective curve models。以下每格是在对应模型上无非零
`F_p` 点的好素数；列顺序为 `D=2,3,6,18`：

| word | 2 | 3 | 6 | 18 |
|---|---:|---:|---:|---:|
| 00101 | 7 | 7 | 31 | 7 |
| 00102 | 7 | 7 | 13 | 7 |
| 00110 | 7 | 7 | 13 | 7 |
| 00112 | 7 | 7 | 13 | 7 |
| 00120 | 7 | 13 | 13 | 31 |
| 00121 | 7 | 19 | 61 | 31 |
| 00122 | 13 | 13 | 13 | 43 |
| 01001 | 7 | 7 | 13 | 7 |
| 01002 | 7 | 7 | 61 | 7 |
| 01012 | 13 | 7 | 13 | 7 |
| 01021 | 7 | 13 | 13 | 31 |
| 01102 | 13 | 7 | 13 | 7 |
| 01120 | 7 | 7 | 61 | 7 |
| 01201 | 7 | 7 | 13 | 7 |
| 01210 | 7 | 13 | 31 | 31 |

每个 `p` 都满足 `gcd(p,3D)=1`。程序不是只检查 affine nonzero roots，而是枚举

\[
(a,d)\in\mathbf F_p^2\setminus\{(0,0)\}
\]

并检验每个 `a+id` 是否在 `D^{c_i} F_p^3`；这与枚举 projective curve 的全部点等价，
允许个别 `x_i=0`。模 `p` 无射影点立即排除 Q 点，不需要 Hensel 假设。

## 6. 主定理

上面 25 轨道的分割为

```text
9 monochromatic index-3AP
+ 1 four-same-color pattern
+ 15 local-obstruction patterns
= 25.
```

所以五项全命中不可能，`R^x_(3,1)(5)<=4`。

下界由全非零 AP

\[
-3,-1,1,3,5
\]

给出。在 `K=Q(alpha), alpha^3=3` 中，前四项分别是
`(-alpha)^3,(-1)^3,1^3,alpha^3`。因此

\[
\boxed{R^{\times}_{(3,1)}(5)=4}.
\]

这是严格结果，不依赖 Magma/Sage、秩猜测或高度搜索。

## 7. “所有极值类”的精确完成边界

本轮已完成的是：**所有假想五命中颜色／位置极值类的完整分类与排除**。

若“所有极值类”要求列出每一个实际达到最大值 4 的 rational AP，则这是额外的有理点分类，
本轮不能诚实声称完成。四个被计位置的组合连同颜色，在 affine color、`D<->D^2`、反转下
有 **38** 个组合轨道：

- 3 个单色轨道由普通 `P_5(3)=3` 排除；
- 4 个含同色三项子 AP 的轨道由 Darmon--Merel 排除；
- 仍有 31 个 weighted complete-intersection models 需要分类 Q 点。

小盒搜索已经发现多个不同四命中模式，因此没有理由把所有 maximizer 压成
`-3,-1,1,3,5` 一个类。证书将这一状态写成
`FINITE_MODELS_DEFINED_BUT_RATIONAL_POINTS_NOT_CLASSIFIED`。这正是下一轮的 fail-closed
边界；不能用有界搜索替代 31 个模型的有理点证明。

建议论文最小单元先以精确最大值定理、Kummer kernel、25 轨道和 60 个局部证书投稿；
“所有四命中 AP”作为增强定理，优先研究含三个同色位置的 genus-1 子族，而不是同时攻击
31 个模型。

## 8. 文件与复现

- `PAPER_CUBE_KUMMER5.py`：kernel、轨道、曲线方程与局部证书生成器；
- `PAPER_CUBE_KUMMER5_CERTIFICATE.json`：固定的 60 模型 prime table 与证据边界；
- `PAPER_CUBE_KUMMER5_test.py`：独立重新枚举 243 词、60 个模障碍、stored/live 一致性；
- `PAPER_CUBE_KUMMER5_TEX.tex`：可编译最小稿。

复现命令：

```text
python -m unittest -v PAPER_CUBE_KUMMER5_test.py
python PAPER_CUBE_KUMMER5.py
pdflatex -interaction=nonstopmode -halt-on-error PAPER_CUBE_KUMMER5_TEX.tex
pdflatex -interaction=nonstopmode -halt-on-error PAPER_CUBE_KUMMER5_TEX.tex
```

## 9. 文献边界

- Darmon--Merel, [Winding quotient and some variants of Fermat's Last Theorem](https://perso.imj-prg.fr/wp-content/uploads/merel-pub/winding.pdf), J. Reine Angew. Math. 490 (1997), 81--100：使用三项同指数立方 AP 的非平凡解不存在。
- Hajdu--Tengely, [Powers in arithmetic progressions](https://doi.org/10.1007/s11139-020-00331-5), Ramanujan J. 55 (2021), 965--986：使用 `P_5(3)=3`。

本轮未作“文献中首次”的绝对主张；新颖性仍需对精确 Kummer 定义与 60 条模型做最终
MathSciNet/zbMATH 查重。

## 10. 最终验证

- `python -m unittest -v PAPER_CUBE_KUMMER5_test.py`：**7 tests OK**；
- TeX 连续编译两次成功，最终 log 无 warning、overfull 或 underfull；
- PDF 为 3 页，逐页 PNG 渲染目检无裁切、重叠、坏字形或裸露链接框；
- 投稿包冻结 PDF SHA-256：`8E43AA32992D744FECDB3A9037790BB00BE9EDAA8276630E082A78FE21C599AB`。

## 11. P6 长期线冻结待办（不混入本定理）

甲组复核确认 P6 的手工归约，但指出第五轮证书仍有三项真实审计缺口；本轮不为此打断
Kummer5 已闭合主定理：

1. `check_dplus_reduction()` 中 `5*V^2-F` 的现有断言是恒真式，须改为从
   `5q^4=F/(1+p^2)^2` 与 `V=q^2(1+p^2)` 精确核验两向复合，并机器计算
   `V/(1+p^2)` 在四个零、四个极和两个 infinity 的 divisor orders；
2. P6 正文须补“有理 AP -> primitive integral AP”的共同四次幂清分母桥，才能无缝调用
   Hajdu--Tengely 的整数表述；
3. 须补 `D_+` 的加权射影紧化边界以及统一 quartic--Jacobian 模型使用条件。

这些均记录为 P6 恢复时的 blocking audit items；在修复前不得把相应 Python 断言或正文
称为完整双向／边界证书。它们不影响本报告的 Kummer kernel、25 轨道、素数支持引理与
60 个独立模障碍。
