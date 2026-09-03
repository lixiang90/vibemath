# 丙线第三轮：Campbell 64 格局部矩阵与具体 torsor 投影

日期：2026-09-03  
状态：NEXT 的证明缺口已修；64 行、512 格实位/坏素数矩阵全部严格判定；
`C_H` 的完整二进四次 2-cover 类已写入三次 étale 代数，并确定其有理 2-挠分量为
E 侧 `d=35`。没有计算 Selmer 群，也没有判定 `C_H(Q)`。

## 1. NEXT 修订

### 1.1 `y`-slice 的逆式与四个边界

对

```text
eta^2=rho^4-6rho^2+1,
U=(eta+1)/rho^2,
X=2U-6,
Y=2rho(U^2-1),
```

映到

```text
Y^2=X(X+4)(X+8),
```

公共仿射开集上的逆式已加入代码与测试：

```text
rho=2Y/[(X+4)(X+8)],
eta=(X^2-32)/[(X+4)(X+8)].
```

光滑射影模型上四个被仿射公式删去的点为

```text
(rho,eta)=(0,+1) -> O,
(rho,eta)=(0,-1) -> (0,0),
infinity_+        -> (-4,0),
infinity_-        -> (-8,0),
```

其中两个无穷远点按 `eta/rho^2 -> +/-1` 区分。非退化门也已补齐：切片变量
`p=1-rho^2` 若为零，则四次式给 `eta^2=-4`；而 `rho!=0,Y=0` 会令
`U=+/-1`，分别给 `4rho^2=0` 或 `8rho^2=0`。故任何非边界有理点确实有
`p!=0` 且 `Y!=0`。

### 1.2 “4 不是 congruent number”的可定位来源

`Y^2=X'^3-16X'` 有 `Y!=0` 有理点等价于 4 为 congruent number；该性质在
乘有理平方后不变，所以等价于 1 为 congruent number。所用 Fermat 无限下降的准确现代
出处为：R. Takloo-Bighash, *A Pythagorean Introduction to Number Theory*,
Springer UTM (2018), Chapter 4, Theorem 4.4，
[DOI 10.1007/978-3-030-02604-2](https://doi.org/10.1007/978-3-030-02604-2)。
该定理证明没有平方数是 congruent number，而不只是给出数值表。

### 1.3 整数措辞

旧报告的“保存一个整数 `U/V`”已更正为“保存本原整数对 `(U,V)`，即有理射影比
`U:V`”。在 `(1:V)` 图上仿射比是 `1/V`，原措辞确实过强。模素数幂否定所需的是
权射影缩放后存在本原整数对，而不是 `U/V` 为整数。

## 2. 64 行 JSON 证书

新文件 `PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json` 保存：

* 两侧 64 个 `d`；
* 每行 `infinity,2,3,5,7,59,71699,339106321` 共 8 格；
* 每格恰取 `YES/NO/UNRESOLVED` 之一；
* `YES` 的本原整数对、右端、赋值与单位；
* `NO` 的模数深度或 valuation-normalized 证明数据；
* 生成脚本与所依赖 NEXT 脚本的 SHA-256。

当前哈希为

```text
PAPER_ELLIPTIC_CAMPBELL_analysis.py
  6e22518a4ab2570059854c5401130dd8bdcae2424f2721f5e6a969c2419da489
PAPER_ELLIPTIC_NEXT_analysis.py
  eca5a1ba67d2178724555cd770ee832864b11bd850953c18444efb6300b1abdf
```

矩阵汇总：

| 项目 | 数量 |
|---|---:|
| 行 | 64 |
| 格 | 512 |
| `YES` | 384 |
| `NO` | 128 |
| `UNRESOLVED` | **0** |
| 旧 56 未决格变为 `YES` | 24 |
| 旧 56 未决格变为 `NO` | 32 |

原先的模数深度仍为 `2^8,3^6,5^5,7^4`。新闭合的格不是靠扩大“小见证”盒：
`p=3` 使用显式赋值规范化点；`p=59,71699` 使用对所有 `Q_p` 点成立的赋值分岔。

## 3. 56 个未决格的完整局部像

写

```text
E: y^2=X^3+aX^2+bX,
a=-591895071,
b=58536289153843200,
F_d(U,V)=dU^4+aU^2V^2+(b/d)V^4.
```

### 3.1 `p=3`：24 格全部 `YES`

这里 `v_3(a)=2,v_3(b)=12`。对旧未决 `d`：

* 若 `3|d`，取 `(U,V)=(3,1)`，精确得到 `v_3(F_d)=4` 且单位模 3 为 1；
* 若 `3∤d`，取 `(U,V)=(9,1)`，精确得到 `v_3(F_d)=6` 且单位模 3 为 1。

奇素数域中非零数为平方当且仅当赋值为偶且剩余单位为平方，所以这 24 个整数对都是完整
`Q_3` 点证书，不是模 3 的近似见证。

### 3.2 `p=59,71699`：各 16 格全部 `NO`

令

```text
delta=a^2-4b=3^4*59*71699*339106321,
A=2dU^2+aV^2.
```

有恒等式

```text
4d F_d(U,V)=A^2-delta V^4.                           (3.1)
```

在 `p=59` 或 `71699`，旧未决格恰满足

```text
v_p(delta)=1,  v_p(2db)=0,  (d/p)=-1.
```

对任一本原 `(U,V)`：

1. 若 `p|V`，则 `U` 是单位且 `F_d=dU^4 (mod p)` 为非平方；
2. 若 `V` 是单位且 `A` 是单位，由 (3.1) 得 `[F_d]=[d]` 模 `p`，仍为非平方；
3. 若 `V` 是单位且 `p|A`，则 (3.1) 右端赋值恰为 1，所以 `v_p(F_d)=1`，不可能是平方。

三种情况穷尽权射影点。因此 32 个 `NO` 是完整 `Q_p` 不可解证明；没有把无小见证当作
局部阻碍。

### 3.3 最终 ambient 幸存类

```text
E side:
  {1,3,5,7,15,21,35,105}

E' side:
  {1,4230241,339106321,1434501462453361}
```

所以第一阶段的 `16+4=20` 被严格压到 `8+4=12`。这些仍只是两个 2-同源下降的处处局部
可解 ambient classes；未执行全局像计算，不能称为两个 Selmer 群。

## 4. `C_H` 与 ambient `d` 的具体代数对应

这是本轮最重要的对象边界修复。20 个旧 ambient `d` 并不各自代表 `C_H`；它们是
`J_H` 与对偶曲线的可能 Kummer 像。要把 Campbell torsor 接入，必须计算二进四次本身在
`H^1(Q,J_H[2])` 的类，再投影到有理 2-挠分量。

### 4.1 从 Campbell 原方程重建 `H`

仓库中的 Campbell 定理 2.5 系数 `g3,g2,g1,g0` 已逐项重建，严格恒等式为

```text
g3(m)*8^3+g2(m)*8^2+g1(m)*8+g0(m)
=H(m)
=-850079m^4-11210976m^3+138714149248m^2
  -5501355374592m-1679721044504576.
```

所以 `C_H:z^2=H(m)` 正是给 Campbell 八项曲线补 `x=8` 的条件，并非只凭相同不变量选出的
任意 torsor。

### 4.2 完整三次 étale 代数类

对二进四次 `H=aX^4+bX^3Z+cX^2Z^2+dXZ^3+eZ^4`，使用
Cremona--Fisher 的约定

```text
I=12ae-3bd+c^2,
J=72ace+9bcd-27ad^2-27b^2e-2c^3,
f(phi)=phi^3-3I*phi+J,
z(H)=[(4a*phi+g4(1,0))/3],
g4(1,0)=3b^2-8ac.
```

精确分解为

```text
f(phi)=(phi-269378023424)
       *(phi^2+269378023424*phi-36009487121810563530752).
```

因此

```text
L=Q[phi]/(f)=Q x Q(sqrt(1434501462453361)),
z(H)=[(943720940177342464-3400316*phi)/3] in L*/L*^2.
```

其范数是精确平方

```text
1375894867981228621717488095403425365462140479078400
=37093056870271943410974720^2.
```

公式及其与 2-cover/Cassels 映射的相容性可定位于 J. E. Cremona--T. A. Fisher,
[*On the equivalence of binary quartics*](https://johncremona.github.io/papers/quartequiv.pdf)，
§2 的 `z(g)` 定义及 §6 Theorem 13。

### 4.3 有理分量恰为 E 侧 `d=35`

在有理根 `phi=269378023424` 上，`z(H)` 的分量为

```text
9250179026780160=2^24*3^8*5*7^5,
```

故平方类为 `35`。大 Jacobian 模型
`y^2=x^3-27Ix-27J` 到仓库小模型使用 `u=64` 的 Weierstrass 缩放；有理 2-挠横坐标满足

```text
-3phi=64^2*(-197298357).
```

再平移 `X=x_small+197298357` 后，Cassels 有理分量满足

```text
x_big+3phi=64^2*X.
```

`64^2` 是平方，所以该分量正是标准 E 侧同源下降的 `[X]=d=35`。它确实留在最终八个
E-side 局部类中；这也与 `C_H` 已证明处处局部可解相容。

必须严格区分：本结论识别的是 `C_H` 的完整 `H^1(Q,J_H[2])` 类在**有理 2-挠因子**上的
投影；不声称 `C_H` 与显示的偶四次 `C_35` 同构，也不以单个 `d=35` 取代完整
`TwoCoverDescent(C_H)`。其余 19 个旧 ambient 类只是 Jacobian 同源下降的候选，不是
Campbell torsor 的 19 种可能身份；新筛后其余 11 个也同理。

## 5. 严格结论与尚缺步骤

### 已证明

* NEXT 的 `y`-slice 逆式、四边界、`p!=0`、`rho!=0 => Y!=0`；
* 64 行、512 格全部 `YES/NO`，无 `UNRESOLVED`；
* 原 56 格严格分成 `24 YES + 32 NO`；
* ambient 局部集合压缩为 `8+4`；
* `H=g_m(8)`；
* `C_H` 的完整三次 étale 代数代表 `z(H)` 以及其 E 侧投影 `d=35`。

### 尚未证明

* `8+4` 是否分别等于真实 isogeny Selmer groups；
* `C_H(Q)` 是否为空；
* 仅凭 `d=35` 不能恢复完整 2-cover 类或决定全局点；
* 没有可信本地 Magma 的 fake 2-Selmer 输出。

下一步不再扩展局部见证。最低成本的严格任务是把已知
`z(H) in (Q x K)^*/square` 直接作为 `TwoCoverDescent(C_H)` 的独立输入/输出核验；若 fake
2-Selmer set 非空，再计算 `8+4` 的全局同源 Selmer 像与 Cassels--Tate 配对，检查含
`d=35` 的完整类是否被配对排除。

## 6. 文件与测试

* `PAPER_ELLIPTIC_NEXT_analysis.py`、`PAPER_ELLIPTIC_NEXT_test.py`：NEXT 修订；
* `PAPER_ELLIPTIC_CAMPBELL_analysis.py`：矩阵、valuation 证明、`H=g(8)` 与 Cassels 类；
* `PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json`：完整 512 格及 SHA；
* `PAPER_ELLIPTIC_CAMPBELL_test.py`：逐格、逐 witness、逐 NO 方法与 torsor 投影回归。

验证：

```text
python -m unittest -v PAPER_ELLIPTIC_NEXT_test.py
Ran 9 tests -- OK

python -m unittest -v PAPER_ELLIPTIC_CAMPBELL_test.py
Ran 9 tests -- OK
```

全部计算为本地精确整数/有理数运算；未调用外部在线 CAS，未把任何有界搜索失败升级为
不存在性结论。

主要原始来源：Garikai Campbell,
[*A Note on Arithmetic Progressions on Elliptic Curves*](https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.pdf),
J. Integer Sequences 6 (2003), Article 03.1.3；Cremona--Fisher 上引二进四次论文。

