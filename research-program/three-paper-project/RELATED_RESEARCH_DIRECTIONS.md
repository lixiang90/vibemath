# 平方等差列、低次数域与椭圆曲线模式：可突破方向

日期：2026-09-01

## 结论与优先级

综合文献空白、问题边界的清晰程度、可计算性，以及与本项目现有平方类、
二下降和模筛代码的兼容性，建议优先顺序如下。

| 优先级 | 问题 | 第一阶段可交付结果 | 难度/风险 |
|---|---|---|---|
| 1 | 立方数密度 `P_N(3)` 与纯三次域 Kummer 版 `R_(3,1)(N)` | 把严格范围从 `N<20` 向前推进；建立首批纯三次域纪录 | 中；已有曲线消元模板，最适合短期突破 |
| 1 | 允许有限多个平方类的 Rudin 函数 `R_s(N)` | 首批 `s=1,2` 纪录表、极值构造和统一上界 | 中；很可能产生新计算纪录 |
| 2 | 七项平方列的平方类秩与最小域次数 | 判定 `R_2(7)=6` 还是 7；分类六项秩2证书 | 中高；`delta(6)=4` 已由显式例子解决 |
| 2 | 四个立方及一般高次幂等差列的最小域次数 | 确定 `delta_3(4)` 是 2 还是 3；计算 `C_(k,m)` 的低次闭点 | 中高；四立方曲线已是亏格 10 |
| 3 | 首个 Weierstrass `x` 坐标九项等差列 | 攻 Campbell 八项族的 genus-5 第九项条件，或构造其他分支 | 高；Bremner 主族已被严格排除 |
| 4 | 椭圆曲线点在长等差列中的稀疏密度 | 固定曲线/固定秩的实验纪录与局部筛猜想 | 高；理论突破依赖高度与 Mordell--Lang |
| 5 | Weierstrass 等差列参数空间的低次数点 | 二次、三次闭点纪录和最小定义域次数 | 中高；适合作为第 3 项的数域版本 |

不建议把“二次域或三次域中最长的全平方等差列”本身作为主要课题：这个
边界已经基本解决，二次域的最大长度是 5，三次域的最大长度是 4。

## 1. 经典平方密度问题

令

```text
Q(N;q,a) = #{0 <= i < N : a+q i 是有理平方},
Q(N)     = max_(a,q) Q(N;q,a),       q != 0.
```

已知：

- Fermat--Euler 的“四个平方不能成非平凡等差列”等价于 `Q(4)=3`；
- Szemeredi 给出 `Q(N)=o(N)`；
- Bombieri--Granville--Pintz 把它改进为 `N^(2/3+o(1))`；
- Bombieri--Zannier 的当前经典一般上界为

  ```text
  Q(N) = O(N^(3/5+o(1)));
  ```

- Rudin 猜想 `Q(N)=O(sqrt(N))`；强形式认为极值由 `24i+1` 给出，其
  平方位置是广义五边形数；
- Gonzalez-Jimenez--Xarles 严格确定了 `6 <= N <= 52`，并在所有跳点
  验证了上述唯一性。公开文献检索中没有发现把严格范围推进到 52 以上的
  后续工作。

`Q(N)` 本身仍值得计算，但“严格证明下一个区间”不能只做整数穷举。指定
平方位置集合 `I` 后，问题对应高亏格曲线 `C_I` 的有理点，通常需要局部
排除、2-cover descent、Chabauty 或 Mordell--Weil sieve。较现实的第一步是：

1. 复现 `N<=52` 的表，校准实现；
2. 用模素数位图和 SAT/回溯枚举可能超过 `24i+1` 的位置集合；
3. 把未被局部排除的极少数 `C_I` 交给严格的曲线方法；
4. 同时搜索新的下界纪录，而不把有界搜索误称为 `Q(N)` 的证明。

主要来源：

- [Gonzalez-Jimenez--Xarles, *On a conjecture of Rudin on squares in
  arithmetic progressions*](https://arxiv.org/abs/1301.5122)
- [Xarles, *Squares in arithmetic progression over number fields*](https://arxiv.org/abs/0909.1642)
- [Bombieri--Zannier, *A note on squares in arithmetic progressions II*](https://www.bdim.eu/item?id=RLIN_2002_9_13_2_69_0)

## 2. 最值得新定义的函数：有限平方类版本 `R_s(N)`

经典 `Q(N)` 只允许平方类 `1`。令 `V` 是 `Q*/Q*2` 中维数为 `s` 的
`F_2` 子空间，定义

```text
R_s(N) = max #{0 <= i < N : [a+qi] in V},
```

最大值同时对非平凡有理等差列和所有这样的 `V` 取；若某一项为零，把它
作为平方单独计数并在平方类分组中只分配一次。于是：

- `R_0(N)=Q(N)`；
- `R_1(N)` 正是“某个二次域中，有理值等差列的多少项成为平方”的统一
  版本；
- `R_2(N)` 对应双二次四次域中的有理值平方；
- 更一般地，它记录一条有理等差列在一个多二次低次数域中的平方密度。

这里有一个立即成立而且有用的上界：

```text
R_s(N) <= 2^s Q(N) = O_s(N^(3/5+o(1))).
```

证明是把 `V` 的每个平方类分别除掉一个代表元；每一类中的位置本身是
另一个有理等差列中的平方位置，因此至多有 `Q(N)` 个。

数域解释也很精确。对数域 `K`，令

```text
V_K = {[r] in Q*/Q*2 : r 在 K 中是平方}.
```

若 `dim V_K=s`，则由这些平方根生成的 `2^s` 次多二次域包含于 `K`，所以
`2^s | [K:Q]`。特别地：

- 二次域至多允许两个有理平方类；
- 奇数次域没有新的有理平方类，所以有理值三次域问题严格退化为普通
  `Q(N)`；
- 非双二次的四次域至多只有一个二次子域，而双二次域可允许四个平方类。

建议提出平方类版 Rudin 猜想：

```text
对固定 s，R_s(N)=O_s(sqrt(N)).
```

这是本列表中最可能较快取得新结果的问题。可先计算 `s=1,2`、`N<=100`
或 `N<=200` 的极值下界和候选极值结构；程序只需在现有平方类线性代数、
模平方筛和 AP 哈希上增加一个 `F_2` 秩约束。

## 3. 全平方长列的最小定义域次数

定义

```text
delta(k) = 包含非平凡 k 项平方等差列的数域的最小次数。
```

目前六项的最小次数已经可严格确定：

```text
delta(3)=1,
delta(4)=2,
delta(5)=2,
delta(6)=4.
```

下界来自：二次域不存在六项平方等差列；Bremner--Siksek 证明任何三次域
都不存在五项，因此更不可能有六项。四次上界有非常小的显式证书：

```text
1, 25, 49, 73, 97, 121
```

公差为 24，并且在双二次域

```text
Q(sqrt(73), sqrt(97))
```

中依次是 `1,5,7,sqrt(73),sqrt(97),11` 的平方。`73,97` 是独立平方类，
所以该域次数确为 4；所有平方根都是互异代数整数。

因此原先“搜索四次域六项列”的任务已经完成。新的最集中问题是：

> 七项有理 AP 能否只使用四个平方类？等价地，`R_2(7)=7` 是否成立？

已严格得到

```text
R_1(5)=5, R_1(6)=5, R_2(6)=6,
```

于是下一步是判定 `R_2(7)` 为 6 还是 7，并分类六项秩2证书。允许对整条
AP 作公共有理缩放时，应使用平方类向量的**仿射** `F_2` 维数；固定 AP、
固定数域并要求原值直接成为平方时，则使用线性子空间 `V_K`。两种表述在
全局极值中可经公共缩放互换，但在单个证书和有界搜索中不能混用。

对七项有理值层可搜索

```text
affine-rank_F2([a], [a+q], ..., [a+6q]) <= 2.
```

当前原型在规范本原 AP 的有界盒 `H<=1000` 中检查了 1,216,767 个七项
候选，尚无仿射秩不超过2的命中；这只是有界证据，不是全局不存在证明。

### 3.1 更长平方列的低次数点层

五项平方列由一个 genus-5 曲线 `C` 参数化；六项与七项条件是在其上继续
加平方条件。完成有理值平方类分支后，再研究这些曲线的次数 4 闭点、
对称幂、椭圆商和 Mordell--Weil sieve，目标转为 `delta(7)` 及更长列，
而不是重复求 `delta(6)`。

主要来源：

- [Xarles, *Squares in arithmetic progression over number fields*](https://arxiv.org/abs/0909.1642)
- [Gonzalez-Jimenez--Xarles, *Five squares in arithmetic progression over
  quadratic fields*](https://arxiv.org/abs/0909.1663)
- [Bremner--Siksek, *Squares in arithmetic progression over cubic fields*](https://arxiv.org/abs/1505.06424)
- [Gonzalez-Jimenez, *Squares in arithmetic progression over quadratic
  extensions of number fields*](https://arxiv.org/abs/2602.03251)
- [Gonzalez-Jimenez--Tho, *Squares in arithmetic progression over certain
  non-primitive quartic number fields*](https://arxiv.org/abs/2602.01380)

## 4. Weierstrass 椭圆曲线上的九项 `x`-等差列

对椭圆曲线而言必须区分模型：

- 两个 Weierstrass 方程的 `x` 坐标只相差仿射变换，因而 `x`-等差性质
  是模型不变量；
- Edwards、Huff 或四次模型到 Weierstrass 模型通常使用非线性有理函数，
  所以这些模型上的纪录不能直接算作 Weierstrass `x` 纪录。

已定位的文献边界是：

- Bremner 构造了无限多个 Weierstrass 椭圆曲线，每条含八项有理
  `x`-等差列；
- Moody 在 Edwards 坐标中构造了无限长度 9；
- 四次椭圆模型有无限长度 12 和个别长度 14；
- 这些更长纪录都是模型相关的。本次检索尚未定位到 Weierstrass
  `x` 坐标长度 9 的已发表构造。在宣布“首例”前仍应做一次 MathSciNet/
  zbMATH 级别的书目核验。

这个问题有一个非常具体的代数模型。经仿射标准化令目标横坐标为
`0,1,...,k-1`。存在三次多项式 `f` 使 `(i,y_i)` 位于
`y^2=f(x)` 上，当且仅当平方序列的四阶有限差分为零：

```text
y_(i+4)^2 - 4 y_(i+3)^2 + 6 y_(i+2)^2 - 4 y_(i+1)^2 + y_i^2 = 0
```

对所有 `0<=i<=k-5` 成立，并且插值得到的三次式判别式非零。对于 `k=9`，
这是 `P^8` 中五个对角二次方程的交。建议路线：

1. 整理并区分所有已知八项族与其等价关系；
2. 不再尝试扩展 Bremner 1999 的主八项族：Gonzalez-Jimenez 已在 2015 年
   证明其第九项条件对应的 genus-5 曲线只有退化有理点；
3. 改攻 Campbell 的另一秩2八项族。第九项条件可写成
   `Y^2=D(m), Z^2=H(m)` 的 genus-5 双二次覆盖，并有 genus `1,1,3` 的
   三个自然商；
4. 三个商严格说是 genus `1,1,3`；其中 `Z^2=H(m)` 尚无已知有理点，
   只能先视为 genus-1 torsor。先检查实位、2-adic、坏素数和无穷远，
   再做 2-cover descent；有理点存在后才转成椭圆曲线并讨论秩与
   Mordell--Weil sieve，最后处理 genus-3 商；
5. 并行研究其他八项分支和完整三维九项空间，但每个数值命中必须回代
   精确验证；
6. 若有理点稀少，再搜索次数 2、3 的闭点，建立最小定义域纪录。

主要来源：

- [Bremner, *On arithmetic progressions on elliptic curves*](https://doi.org/10.1080/10586458.1999.10504629)
- [Gonzalez-Jimenez, *Covering techniques and rational points on some genus
  5 curves*](https://arxiv.org/abs/1311.5759)
- [Campbell, *A note on arithmetic progressions on elliptic curves*](https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.pdf)
- [Moody, *Arithmetic progressions on Edwards curves*](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=907596)
- [Ulas, *A note on arithmetic progressions on quartic elliptic curves*](https://cs.uwaterloo.ca/journals/JIS/VOL8/Ulas/ulas7.pdf)

## 5. 椭圆曲线点在长等差列中的密度

对固定数域和 Weierstrass 椭圆曲线可定义

```text
M_(E,K)(N) = max_(a,q) #{0<=i<N : a+qi in x(E(K))}.
```

完整长度问题只是 `M_(E,K)(N)=N` 的极端情形。现有理论说明：

- 固定 `j` 的曲线族中，长的完整 `x`-等差列迫使 Mordell--Weil 秩增长；
- 2026 年的 pattern theorem 对有限秩子群在 AP、GP、平移和 Mobius 轨道
  中的模式给出秩相关统一界；
- Choi 对固定曲线证明广义 AP 中的正密度占据最终不可能，并在 Lang 高度
  猜想下得到更统一、有效的秩指数界。

仍然有价值的具体问题是：

1. 对固定 `E/Q`，能否无条件证明 `M_E(N) <<_E N^(1-epsilon)`，甚至
   `N^(1/2+o(1))`？
2. 能否让指数或常数只依赖 `rank E(K)`、`[K:Q]` 和 `h(j)`？
3. 对小秩曲线建立实验性的 `M_E(N)` 纪录表，并测量局部素数筛后的存活
   密度，寻找比“秩大”更准确的构造指标。

这一方向理论意义很强，但短期突破概率低于 `R_s(N)` 和 `R_2(7)`，因为
有效统一结论很快碰到 Lang 高度下界、秩一致有界或 Uniform Mordell--Lang。

主要来源：

- [Garcia-Fritz--Pasten, *Elliptic curves with long arithmetic progressions
  have large rank*](https://arxiv.org/abs/1910.14485)
- [Choi, *Additive Rigidity for x-coordinates of rational points on elliptic
  curves*](https://arxiv.org/abs/2510.03828)
- [Garcia-Fritz--Pasten, *Patterns on elliptic curves beyond Bremner's
  conjecture*](https://arxiv.org/abs/2605.14962)

## 6. 建议的实际执行顺序

### 第一阶段：两周量级的计算课题

1. 复现 `P_N(3)` 在 `N<20` 的严格位置模式表，并枚举 `20<=N<=27`
   中需要证明的剩余曲线；
2. 实现 `F_3` 立方类版本 `R_(3,1)(N)`，给出纯三次域的第一批纪录；
3. 实现 `R_s(N)` 的平方类秩搜索器，先做 `s=0,1,2`；
4. 用 `s=0,N<=52` 复现平方已知表；
5. 给出 `R_1(N),R_2(N)` 的第一批下界纪录及极值 AP；
6. 专门搜索六项 AP 的平方类秩是否能降到 2。

### 第二阶段：代数几何课题

1. 把六项 genus-5/双覆盖模型接到 Magma 的低次数点和 Mordell--Weil
   sieve；
2. 对 Campbell 八项族的新 genus-5 第九项条件做 2-cover descent；
3. 对所得曲线先算完整局部可解性、亏格、Jacobian 分解和已知点生成子群；
4. 只在结构显示有希望时扩大高度搜索。

### 成功判据

以下任一项都构成清楚的新结果：

- 把立方精确极值 `P_N(3)` 的严格范围从 `N<20` 向前推进；
- 第一张 `R_(3,1)(N)` 纪录表，或一个纯三次域中四个立方的有理值 AP；
- 第一个非平凡的 `R_1(N)` 或 `R_2(N)` 严格纪录表；
- 判定 `R_2(7)=6` 还是 7，或分类六项平方类秩2证书；
- 对该分支的严格不存在证明；
- 一个 Weierstrass 椭圆曲线上的九项有理 `x`-等差列；
- 一个九项参数空间上的次数 2 或 3 闭点最小纪录；
- 对固定秩/固定 `j` 的 `M_E(N)` 新的无条件定量界。

## 7. 固定指数的立方数与高次幂密度

对整数等差列定义

```text
P_(a,b;N)(k) = #{0 <= i < N : ai+b 是整数 k 次幂},
P_N(k)       = max_(a>0,b in Z) P_(a,b;N)(k).
```

若改用有理等差列和有理 `k` 次幂，在固定 `N` 下可同时清除分母，所以
得到的是同一个极值问题。这里必须区分三种量词：

1. `a,b` 固定而 `N -> infinity`；
2. 每个 `N` 都允许重新选择 `a,b`，即真正的 `P_N(k)`；
3. 对公差 `a` 的大小或除数个数附加限制。

### 7.1 已知精确结果

Hajdu--Tengely 完全确定了固定等差列的渐近常数。对奇数 `k`，渐近最优
的是公差 1 的整数列；对偶数 `k`，最优列由模素数的 `k` 次幂剩余类
决定，`k=4` 时恰有 `5i+1` 与 `80i+1` 两种最优类型。

他们进一步提出高次幂版 Rudin 问题：

```text
P_N(k) = O_k(N^(1/k)) ?
```

对奇数 `k`，允许负项时更精确的候选极值列是以 0 为中心、尽量对称的
连续整数区间。令

```text
b_x = floor(((N-1)/2)^(1/k))^k,
```

猜测最优列为 `i-b_x`。对立方 `k=3`，他们已经严格证明 `N<20`；此时

```text
P_N(3) = 3,  3 <= N <= 9,
         4, 10 <= N <= 16,
         5, 17 <= N <= 19.
```

证明不是公差有界穷举。指定立方所在的位置 `n_i` 后，每个三元组给出

```text
(n_j-n_i)X^3 + (n_i-n_k)Y^3 + (n_k-n_j)Z^3 = 0,
```

即 genus-1 三元三次曲线；多个条件的交再取对称商，得到 genus-2 曲线，
最后用有理点计算、Chabauty 和局部排除逐一消元。这正是把严格范围推进到
`N>=20` 时应复用的模板。

### 7.2 一般上界的新边界

Bourgain--Demeter 对公差 `q` 证明了

```text
P_(q,b;N)(k) <<_k d(q)^(k-1) N^(1/k),
```

其中 `d(q)` 是除数函数。因此公差只有有界多个因子时，猜想指数已经达到。
Novakovic 在 2026 年进一步指出：若 `q << N^r`，其中 `r` 固定，则对每个
`epsilon>0` 有

```text
P_(q,b;N)(k) <<_(k,epsilon,r) N^(1/k+epsilon).
```

所以全局 `P_N(k)` 的真正未知区域被压缩为：公差随 `N` 超多项式增长，或
至少其除数结构异常复杂。另一方面，Hajdu--Papp 证明对每条固定 AP，且
指数 `k` 足够大时，其首 `N` 项中的 `k` 次幂至多
`(1+epsilon)N^(1/k)`；但其起始阈值依赖该 AP，不能直接交换最大值与极限。

这给出三个清楚的新课题：

1. **立方精确纪录**：严格确定 `P_N(3)` 的下一个区间，第一目标是
   `20 <= N <= 27`，并公开所有未被局部筛排除的位置模式；
2. **大公差结构定理**：证明极值 AP 可归一化为 `q <= N^C`，便可立即结合
   2026 年结果得到 `N^(1/k+epsilon)`；若做不到，则刻画必须出现的高次幂
   因子和除数结构；
3. **偶数高次幂精确问题**：先把 `P_N(4)` 的已证范围从 `N<=5` 推进，
   再研究 `k=6,8` 的渐近最优模数是否也在有限 `N` 后成为精确极值。

主要来源：

- [Hajdu--Tengely, *Powers in arithmetic progressions*](https://doi.org/10.1007/s11139-020-00331-5)
- [Bourgain--Demeter, *On the number of k-th powers inside arithmetic
  progressions*](https://arxiv.org/abs/1811.11919)
- [Hajdu--Papp, *Uniform bounds for the number of powers in arithmetic
  progressions*](https://doi.org/10.1007/s13398-022-01313-6)
- [Novakovic, *A comment on the number of k-th powers inside arithmetic
  progressions*](https://arxiv.org/abs/2607.15895)

## 8. Kummer 类版本：低次数域中“至少若干项为立方”

平方类函数 `R_s(N)` 有一个自然的素指数推广。对素数 `ell`，令 `V` 是
`Q*/Q*ell` 中维数为 `s` 的 `F_ell` 子空间，定义

```text
R_(ell,s)(N) = max #{0 <= i < N : [a+qi] in V}.
```

这是固定尺度的线性版本。若允许把整条 AP 乘以任意有理数，则应把“落在
子空间 `V`”替换为“落在某个仿射陪集”；计算时锚定一个非零项并取类向量
差。全局对所有 AP 取最大时两种版本经公共缩放等价，但单个证书与有界盒
搜索必须注明使用哪一种。

把 `V` 的 `ell^s` 个幂类分别除以代表元，立即得到

```text
R_(ell,s)(N) <= ell^s P_N(ell).
```

因此合理的 Kummer--Rudin 猜想是

```text
R_(ell,s)(N) = O_(ell,s,epsilon)(N^(1/ell+epsilon)),
```

强版本则去掉 `epsilon` 并寻找精确极值族。

数域解释对立方尤其干净。若素数 `ell` 不整除 `[K:Q]`，一个有理非
`ell` 次幂不可能在 `K` 中突然成为 `ell` 次幂；否则 `K` 会包含次数为
`ell` 的子域 `Q(root_ell(r))`。所以：

- 二次数域不会增加任何有理数的立方类，故“有理值 AP 中多少项在二次域
  成为立方”严格等于普通 `P_N(3)`；
- 非纯三次数域同样不会增加有理立方类；
- 对纯三次域 `K=Q(root_3(D))`，新出现的有理立方类恰为
  `1,D,D^2`，即一个一维 `F_3` 子空间；相应的统一极值正是
  `R_(3,1)(N)`。

首轮计算已经严格得到（零单独计作立方）

```text
R_(3,1)(4)=4,
R_(3,1)(5)=5.
```

因此后续建议做：

1. 继续严格验证 `R_(3,1)(N)` 的小 `N` 表，并另列“全部非零”版本；
2. 寻找长度至少6、全部落在三个立方类 `1,D,D^2` 中的有理 AP；
3. 对候选位置模式建立三次剩余模筛，再计算对应三元三次曲线；
4. 比较 `R_(3,1)(N)` 与平凡上界 `3P_N(3)` 的差距，猜测正确常数；
5. 再推广到 `R_(ell,1)`，它对应纯 `ell` 次域中的有理值 AP。

这里与平方情形有一个重要反差：奇数次域不增加有理平方类，但三次域恰好
是第一个能增加有理立方类的次数。因此平方与立方的两套计算可以共用
“幂类秩 + 局部筛”框架，却应使用 `F_2` 与 `F_3` 两套线性代数。

## 9. 连续三项、四项高次幂与最小定义域次数

令 `C_(k,m)` 参数化 `m` 个 `k` 次幂组成的非恒定等差列：

```text
X_i^k - 2X_(i+1)^k + X_(i+2)^k = 0,
0 <= i <= m-3.
```

它是 `P^(m-1)` 中 `m-2` 个次数 `k` 的完全交曲线；在特征 0 的光滑情形，

```text
g(C_(k,m)) = 1 + k^(m-2) ((m-2)k-m)/2.
```

这一个公式解释了难度为何突然上升：

```text
C_(2,4): genus 1,
C_(2,5): genus 5,
C_(3,3): genus 1,
C_(3,4): genus 10.
```

Darmon--Merel 证明，对所有 `k>=3`，有理数域上没有非初等的连续三项
`k` 次幂；其方程就是 `X^k+Z^k=2Y^k`。立方 `k=3` 是唯一仍为椭圆曲线
的高次幂情形。Gonzalez-Jimenez 给出精确对应

```text
C_(3,3)  <->  E: y^2=x^3-27,
```

并证明 `Q(sqrt(D))` 中存在非初等三立方 AP，当且仅当 `X_0(36)` 的
`D`-二次扭曲具有正秩。特别地，若 `D=+/-p`、`p>3` 且
`p == 3 (mod 4)`，正秩无条件成立；所以最小定义域次数已经确定为

```text
delta_3(3)=2
```

（排除恒定列和 `-1,0,1` 型初等列）。清除分母后还可把根同时变成代数
整数，故这个结论也适用于“代数整数的立方”版本。

下一条真正开放而集中的纪录是

```text
delta_3(4) = 包含四个互异非零立方 AP 的数域最小次数.
```

公开检索没有发现二次域四立方 AP 的构造或不存在定理。纯三次域已经有
极小的显式证书：

```text
-3, -1, 1, 3
```

在 `Q(root_3(3))` 中依次是 `-root_3(3),-1,1,root_3(3)` 的立方，故

```text
2 <= delta_3(4) <= 3.
```

下界来自任取连续三项并应用 Darmon--Merel；上界中的根互异且都是代数
整数。现在只剩一个二选一问题：是否存在真正二次坐标的四立方 AP？若排除
二次点便得到 `delta_3(4)=3`，若找到便得到 `delta_3(4)=2`。

有理值 Kummer 子问题也已有精确小值。令 `D` 取无立方因子代表并允许零
单独计作立方，则

```text
R_(3,1)(4)=4,   证书 -3,-1,1,3 in Q(root_3(3)),
R_(3,1)(5)=5,   证书 -2,-1,0,1,2 in Q(root_3(2)).
```

第二个等号依赖“允许零项”的约定；若要求所有项非零，则必须另立版本。

建议攻击顺序：

1. 先查 `C_(3,4)` 的二次点，即 `C_(3,4)^(2)(Q)`；利用坐标置换、反转
   和乘三次单位根的自同构寻找低亏格商；
2. 有理值 Kummer 搜索不能排除二次点：二次数域不会把有理非立方变成立方，
   所以潜在二次点必须具有真正二次的根或立方值；
3. 计算开放曲线 `C_(3,4)^(2)(Q)`，利用二次共轭对、两个三立方 genus-1
   投影的兼容条件、Jacobian 覆盖和 Mordell--Weil sieve；无需继续找三次
   点，因为显式纯三次点已经达到当前上界；
4. 对一般 `k>=4`，研究 `C_(k,3)` 的二次、三次点与
   `delta_k(3)`；朴素非零上界为 `delta_k(3)<=k^2`，来自 AP `1,2,3`；
5. 借鉴 Fermat 曲线低次数点、对称幂 Chabauty、Mordell--Weil sieve 和
   模方法，但注意 Fermat 曲线 `X^k+Y^k=Z^k` 与本曲线系数 2 并不相同。

三立方的二次域路线也明确回答了 Heegner 点问题：Heegner 点、二下降、
Waldspurger 系数都能用于证明扭曲正秩并构造点，但它们主要解决
`C_(3,3)`；到了四立方，核心对象是 genus-10 曲线，不能期待单独一条
椭圆曲线的 Heegner 点理论直接解决。

主要来源：

- [Darmon--Merel, *Winding quotient and some variants of Fermat's Last
  Theorem*](https://perso.imj-prg.fr/wp-content/uploads/merel-pub/winding.pdf)
- [Gonzalez-Jimenez, *Three cubes in arithmetic progression over quadratic
  fields*](https://arxiv.org/abs/0909.0227)
- [Xarles, *Squares in arithmetic progression over number fields*](https://arxiv.org/abs/0909.1642)
- [Gonzalez-Jimenez, *Quadratic points on the Fermat quartic over number
  fields*](https://arxiv.org/abs/2602.01398)（方法邻近，曲线不同）

## 10. 混合指数与“任意完全幂”方向

还应把“每项都是同一个 `k` 次幂”与“各项指数可以不同”彻底分开。对原始
整数 AP，Hajdu--Tengely 已得到若干尖锐长度界：

- 指数来自 `{2,p}`、`p` 为素数时，非恒定本原列长度至多 6；
- 指数来自 `{2,5}` 时长度至多 4；
- 指数来自 `{3,p}` 时长度至多 4；
- 固定指数上界 `L` 后，长度至少 4 的本原混合幂列只有有限多个。

Hajdu--Papp 又证明：对每条固定 AP，允许任意指数的完全幂个数渐近仍由
平方主导，至多

```text
(sqrt(8/3)+epsilon) sqrt(N).
```

2026 年关于“几乎完全的非齐次幂”的工作把系数允许为固定有限素数集上的
`S`-单位，并在若干结论中使用 `abc` 猜想；这说明混合指数路线仍活跃，
但条件与定义稍改就会产生任意长例子。

因此这个方向只建议研究有明确规范化的版本：

1. 固定 `gcd(a,b)=1`、指数集合和允许的 Kummer 类，建立小长度完整表；
2. 把 `{2,3}`、`{2,5}` 的已知整数结果推广到指定二次或三次数域；
3. 研究混合幂类密度 `R_(2,s_2;3,s_3)(N)`，但先固定类空间维数，防止
   问题因任意系数而退化；
4. 将 `abc` 条件结论与可无条件计算的 `k=3,4` 小指数情况分开记录。

这一路线的突破概率低于 `P_N(3)`、`R_(3,1)` 和 `delta_3(4)`，但适合在
主搜索中顺带保存“某项是平方或立方”的命中数据，形成独立纪录表。

主要来源：

- [Hajdu--Tengely, *Arithmetic progressions of squares, cubes and n-th
  powers*](https://arxiv.org/abs/0707.0593)
- [Hajdu--Papp, *Uniform bounds for the number of powers in arithmetic
  progressions*](https://doi.org/10.1007/s13398-022-01313-6)
- [Novakovic, *Almost perfect inhomogeneous powers in arithmetic
  progression*](https://arxiv.org/abs/2606.14340)
