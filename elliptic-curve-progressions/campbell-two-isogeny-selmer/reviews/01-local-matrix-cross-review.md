# Campbell 第三轮交叉审稿（研究生甲）

日期：2026-09-03  
审查对象：`PAPER_ELLIPTIC_CAMPBELL_REPORT.md`、`PAPER_ELLIPTIC_CAMPBELL_analysis.py`、`PAPER_ELLIPTIC_CAMPBELL_test.py`、`PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json`。  
结论：**未发现阻断性数学错误；当前报告没有把有理 2-挠投影误当成完整 torsor，也没有由 ambient 类推出 (C_H(\mathbf Q)) 的结论。** 下列两个非阻断审计缺口应在正式稿前补齐：完整二次数域分量的机器结构化核验，以及“只查坏位即可”的好素数引理/引用。

## 1. 独立复跑

执行

```text
python -m unittest -v PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_NEXT_test.py
```

结果为 **18/18 通过**。磁盘 JSON 与实时重算一致，两个源脚本 SHA-256 一致；64 行的 `(side,d)` 无重复，每行恰有 8 个位置，共 512 格且没有 `UNRESOLVED`。

## 2. 局部矩阵核验

### 2.1 (p=3) 的 24 个 `YES`

旧未决格中恰有 24 个位于 E 侧 (p=3)。我逐格重算了证书中的整数右端。若 (3\mid d)，取 ((U,V)=(3,1))，每格均有

\[
v_3(F_d)=4,\qquad 3^{-4}F_d\equiv1\pmod3;
\]

若 (3\nmid d)，取 ((U,V)=(9,1))，每格均有

\[
v_3(F_d)=6,\qquad 3^{-6}F_d\equiv1\pmod3.
\]

这里 (F_d\ne0)。对奇素数，非零 (q\in\mathbf Q_p) 为平方当且仅当 (v_p(q)) 为偶数且单位剩余类为平方。因此这些是实际 (mathbf Q_3) 点，而不是有限精度近似。报告中的“奇素数域”宜写成“奇素数 (p) 的局部域 (mathbf Q_p)”，但不影响论证。

### 2.2 (p=59,71699) 的 32 个 `NO`

恒等式可直接展开验证：

\[
4dF_d(U,V)=(2dU^2+aV^2)^2-(a^2-4b)V^4.
\]

对两素数的 16 个旧未决类，脚本逐格断言

\[
v_p(\delta)=1,\qquad v_p(2db)=0,\qquad \left(\frac d p\right)=-1.
\]

令 (A=2dU^2+aV^2)，把任意 (mathbf Q_p) 点按权重缩放为本原 (U,V\in\mathbf Z_p)。三种情况确实穷尽：

1. (p\mid V)：本原性给 (U\in\mathbf Z_p^\times)，且 (F_d\equiv dU^4\pmod p) 为非平方；
2. (V,A\in\mathbf Z_p^\times)：上式给 (4dF_d\equiv A^2\pmod p)，故 (F_d) 的 Legendre 符号等于 (d) 的符号，为 (-1)；
3. (V\in\mathbf Z_p^\times,p\mid A)：(A^2) 的赋值至少 2，而 (delta V^4) 的赋值恰为 1，故 (v_p(F_d)=1)。

三者都不可能令 (F_d) 为平方，所以每个 `NO` 是完整的 (mathbf Q_p) 阻碍。没有使用“找不到小见证”的反推。

### 2.3 512 格、模 (p^k) 否定与 `8+4`

两侧各由 4 个有限素数再加符号生成 (2^5=32) 个平方类，故为 64 行；位置为实位和 7 个坏素数，故为 512 格。旧的模 (2^8,3^6,5^5,7^4) 程序枚举

```text
(U:1), U mod p^k;
(1:V), V mod p^k with p|V,
```

这正是一套 (\mathbf P^1(\mathbf Z/p^k\mathbf Z)) 代表。若存在 (mathbf Q_p) 点，把 (U,V) 同时缩放到至少一个为单位；四次齐次性使 (N) 按二次权缩放。此时 (F_d(U,V)\in\mathbf Z_p)，所以 (N\in\mathbf Z_p)，其模 (p^k) 必出现在枚举中。因此“无模 (p^k) 解推出无 (mathbf Q_p) 解”在这里有效。

独立重算最终处处通过已检查位置的 ambient 类为

```text
E:      1,3,5,7,15,21,35,105
E_dual: 1,4230241,339106321,1434501462453361.
```

所以 `16+4 -> 8+4` 及其正见证成立。这里仍只是 Jacobian 两侧的局部 ambient 集，不是已算出的 isogeny Selmer 群。

## 3. (H)、二进四次类与 (d=35)

### 3.1 原方程与不变量

Campbell 定理 2.5 的四个 (g_i(m)) 系数与原文逐项一致；直接展开验证

\[
g_3(m)8^3+g_2(m)8^2+g_1(m)8+g_0(m)=H(m).
\]

因此 (z^2=H(m)) 确为补 (x=8) 所要求的必要平方条件。原文可核对于 [Campbell 2003](https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.pdf)。

由原始五个系数独立重算得到

\[
I=36191335541877218738176,
\]

\[
J=9700164465385312324077552400334848.
\]

四次判别式非零。三次预解式精确分解为

\[
(\phi-269378023424)
(\phi^2+269378023424\phi-36009487121810563530752).
\]

二次因子的判别式为

\[
2^{24}3^2\cdot1434501462453361,
\]

所以其代数确为 (mathbf Q(\sqrt{1434501462453361}))。

### 3.2 (z(H)) 与范数

Cremona--Fisher 的约定给

\[
z(H)=\frac{4a\phi+3b^2-8ac}{3}
=\frac{943720940177342464-3400316\phi}{3}.
\]

精确 resultant 重算给出的范数为

\[
37093056870271943410974720^2.
\]

该平方根的负值正是六次半不变量

\[
b^3+8a^2d-4abc,
\]

故公式与范数检验相容。Cremona--Fisher §6 Theorem 13 确实把此 (z(H)) 类识别为二进四次 2-cover 在
(H^1(\mathbf Q,J_H[2])) 中的类，而不仅是具有相同 (I,J) 的数值标签；见
[Cremona--Fisher, *On the equivalence of binary quartics*](https://johncremona.github.io/papers/quartequiv.pdf)。

### 3.3 有理分量及缩放

在有理预解根处，

\[
z(H)_{\mathbf Q}=9250179026780160
=2^{24}3^8 5\,7^5,
\]

故其平方类为 (35)。大 Jacobian 的有理 2-挠根是

\[
x_{\rm big}=-3\phi=64^2(-197298357).
\]

用 (x_{\rm big}=64^2x_{\rm small}) 缩放，再令

\[
X=x_{\rm small}+197298357,
\]

直接展开得到

\[
y^2=X^3-591895071X^2+58536289153843200X.
\]

且

\[
x_{\rm big}+3\phi=64^2X.
\]

右端只差平方因子，所以 Cassels 映射的有理分量确实对应 E 侧 ([X]=35)，不是对偶侧，也没有遗漏一个 (64) 的非平方因子。

## 4. torsor 边界判定

本报告在此处措辞是合格的：

- `z(H)` 作为 ((\mathbf Q\times K)^*/(\mathbf Q\times K)^{*2}) 中的显式元素给出了完整 2-cover 类；
- `d=35` 只是在投影 ((\mathbf Q\times K)^*/\square\to\mathbf Q^*/\square) 下的一个分量；
- 单个分量既不确定 (K) 分量，也不说明 (C_H\cong C_{35})，更不能决定 (C_H(\mathbf Q))；
- 其余 ambient `d` 是 Jacobian 同源下降候选，不是 (C_H) 的其他“可能身份”。

主报告 §4.3、§5 以及 JSON 的 `claim_boundary` 都明确保留了这些区别。因此没有出现本轮要求重点防范的“有理 2-挠投影 = 完整 torsor”误判。

## 5. 非阻断问题与建议

1. **完整 (K) 分量尚未机器结构化。** JSON 把 `representative` 和代数写成人类字符串；现有测试严格验证 (I,J)、有理根、有理分量和范数，但没有把二次因子构造成 `Q[phi]/(...)` 后逐系数核验代表元，也没有测试二次因子判别式的平方自由部分。当前纸面计算正确，但正式可审计证书应把代表存成有理系数对、二次多项式和乘法表，而非仅存字符串。

2. **“处处局部”的好素数桥梁应显式写出。** 512 格只列实位和 7 个坏素数。由于 (d) 只支撑在相应 (2b) 上，其他素数处是非分歧的标准同源覆盖；也可由好约化和 Hasse--Hensel 论证得到局部点。正式稿应给一个精确引理或标准 2-isogeny descent 引用，否则 JSON 本身只证明“通过所列位置”，尚未自足证明“处处局部可解”。

3. **来源绑定属于证据工程缺口。** `H=g(8)` 测试只绑定转录进脚本的 (g_i)，没有绑定 Campbell PDF；本次人工逐项核对通过。正式归档可保存原文页码、系数摘录哈希或独立录入 fixture。

4. **既有 (C_H) 处处局部可解结论需交叉引用。** 本轮 Jacobian ambient 矩阵本身不证明原 torsor (C_H) 处处局部可解。主报告“与已证明处处局部可解相容”并未倒置推理，但论文版应明确指向此前同一-(m) 局部证书，避免读者误以为 `d=35` 留在 ambient 集就足以证明该命题。

这些都不推翻本轮 24/32、512 格、`8+4`、(z(H)) 或 (d=35) 的结论。

## 6. 下一轮最优任务

不应继续扩展小见证搜索。最小、决定性的任务是：

1. 先把 (z(H)) 的 (mathbf Q\times K) 两个分量做成结构化可重算证书，并验证其在所有坏位的完整局部类，而非只验证有理投影；
2. 在可信本地 Magma 可用时，对 (C_H) 实际运行无 cutoff 的 `TwoCoverDescent`，保存版本、完整 transcript、返回集合正文和输入哈希；
3. 若 fake 2-Selmer set 为空，即严格推出 (C_H(\mathbf Q)=\varnothing)；若非空，只把返回类与结构化 (z(H)) 比较，并继续 Cassels--Tate/更高覆盖，绝不由 `d=35` 或非空 fake set 推出有理点。

在没有可信下降输出前，可接受的最终状态仍是：局部 ambient 集为 `8+4`，完整二进四次类 (z(H)) 已显式给出，其有理 2-挠投影为 E 侧 (d=35)，而 (C_H(\mathbf Q)) 未判定。
