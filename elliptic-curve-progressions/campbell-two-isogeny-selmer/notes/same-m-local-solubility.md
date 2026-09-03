# 研究生丙第三轮报告：Campbell 包审计化与有界搜索

日期：2026-09-01

本轮遵守限制：**没有向任何外部在线计算服务发送文件、系数或计算请求**。
当前机器仍无本地 Magma 可执行文件，因而本报告没有 fake 2-Selmer 输出；
只交付可在获许可的本地 Magma 上运行的审计包。

## 1. 结论分类

### 1.1 已证明

1. 对 Campbell 纤维积

   ```text
   C: Y^2=D(m), Z^2=H(m)
   ```

   Round 02 的同一 `m` 证书确实证明
   `C(R) != empty` 且对每个素数 `p` 都有 `C(Q_p) != empty`。本轮将这些
   证书逐行嵌入 Magma 脚本；不再用分别调用 `IsLocallySoluble(MD,p)` 与
   `IsLocallySoluble(MH,p)` 代替纤维积断言。

2. 两个 binary quartic 的经典不变量满足

   ```text
   I = 12ae-3bd+c^2,
   J = 72ace+9bcd-27ad^2-27b^2e-2c^3,
   Disc(f) = (4I^3-J^2)/27.
   ```

   对模型 `y^2=f(x)`，复核的 Jacobian 方程为

   ```text
   y^2=x^3-27Ix-27J.
   ```

   并逐整数验证其 Weierstrass 判别式等于
   `16*27^4*Disc(f)`。

3. 缩放后的较小整模型为

   ```text
   J_D: y^2=x^3-137904664808967867*x
                 -4890817235485401208238826,       u=32;

   J_H: y^2=x^3-58243635870855147*x
                 -3811211217040595260188186,       u=64.
   ```

   这里严格验证了原模型的 `A,B` 分别除以 `u^4,u^6` 以及判别式除以
   `u^12`。**没有**声称这两个整模型是全局最小模型，也没有把无已知基点的
   torsor `C_H` 与 `J_H` 认同。

### 1.2 待本地 Magma

尚待计算的是

```text
SelH, AtoSelH := TwoCoverDescent(CH);
```

Magma 官方手册把第一个返回值定义为 `C_H` 的 **fake 2-Selmer set**。
逻辑只有：

- 若无界调用完整、无警告地结束且 `#SelH=0`，则严格推出
  `C_H(Q)=empty`，从而 `C(Q)=empty`，Campbell 该族不能闭合九项；
- 若 `#SelH>0`，只说明这一下降障碍没有排除有理点，**不能**推出
  `C_H(Q)` 非空，更不能推出纤维积有点；
- 若程序超时、报错、含警告、使用条件性类群结果或没有出现完成标记，
  则不产生任何 Selmer 结论。

本轮脚本只调用一次不带 `Bound`、`PrimeBound`、`PrimeCutoff` 的
`TwoCoverDescent(CH)`。没有运行属 3 商的带界预筛。

### 1.3 有界证据

精确搜索所有约化分数

```text
m=a/b, b>0, gcd(|a|,b)=1, max(|a|,b)<=50000.
```

结果：

| 项目 | 数量 |
|---|---:|
| 经严格实根区间剪枝后的整数对 | 15,635,928 |
| 约化整数对 | 9,505,799 |
| 模 `11,13,17,19,23` 预筛幸存 | 441,241 |
| `H_h(a,b)` 为整数平方 | 0 |
| 同时位于完整纤维积 | 0 |

因此高度盒内没有 `C_H(Q)` 点。该结果只是**有界证据**，不能外推成
`C_H(Q)=empty`。

## 2. 同一 `m` 的局部证书

Magma 文件
`STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m` 逐项断言：

- 实位在同一个 `m=-400` 有 `D(m)>0,H(m)>0`；
- `Q_2` 在同一个 `m=1` 有两个奇单位都等于 `1 mod 8`；
- 每个奇素数证书行同时验证

  ```text
  D(m)=dy^2 mod p, H(m)=hz^2 mod p, dy*hz != 0 mod p.
  ```

  表覆盖所有奇素数 `p<101` 和全部大于 100 的分支模型坏素数；
- 判别式、resultant、互素性和 14 个分支模型坏素数也在 Magma 中重新
  计算。其余好素数 `p>=101` 使用属 5 Weil 界与光滑 Hensel 提升。

Magma 表来自本轮 JSON；联结方式不是未经检查的注释：

1. 审计包装先验证 JSON 的 SHA-256：
   `74843e4e53c7d09793fa857a2ce57d37a21be855ce135fec9f22b5b00aab5e08`；
2. 包装再验证 Magma 文件的 SHA-256：
   `ae6a61f417f82e29d6e496229399a05ce88a0f085d5e6f29869e9c03acdf00e8`；
3. Python 回归测试逐行确认 JSON 的六元组在 Magma 文件中原样出现，
   并独立复算同一 `m` 的两平方根等式。

## 3. 无界 Magma 审计包装

文件：

- `STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m`；
- `STUDENT_ELLIPTIC_ROUND_03_run_magma_audit.ps1`。

在装有本地 Magma 的机器上运行：

```powershell
& .\STUDENT_ELLIPTIC_ROUND_03_run_magma_audit.ps1 `
  -MagmaPath 'C:\path\to\magma.exe' `
  -TranscriptDirectory '.'
```

包装执行下列审计：

1. 验证 JSON 与 Magma 脚本哈希，防止证书和输入漂移；
2. 先运行 `magma --version`，将版本写入 transcript；Magma 脚本内再输出
   `GetVersion()`；
3. 用 `-b -n` 禁用启动文件，避免用户启动代码改变计算；
4. 完整保存标准输出和标准错误至带时间戳的
   `STUDENT_ELLIPTIC_ROUND_03_magma_transcript_*.txt`；
5. 非零退出码立即失败；
6. transcript 若含 warning、runtime/internal/user/syntax error、GRH、
   conditional、not proven、terminated、abort 或 exception，立即失败并保留
   transcript；
7. 只有同时出现同一 `m` 局部证书、descent 完成、Selmer 基数和总审计
   完成四个标记，包装才返回成功。

因此，只有包装报告 clean transcript 后，才允许把 `#SelH` 写入“已证明”
部分。本轮没有生成 transcript，也没有 Selmer 基数。

## 4. 高度搜索的完备性

`H` 有四个互异实根。Sturm 隔离所得有理区间为

```text
(-7898/19, -32839/79),
(-4971/53, -2251/24),
(11789/82, 1869/13),
(53583/152, 8813/25).
```

它们分别严格包含于

```text
(-416,-415), (-94,-93), (143,144), (352,353).
```

四个粗区间端点的 `H` 值都为负，首项系数也为负，故 `H(m)>=0` 只可能在

```text
-416 < m < -93  或  143 < m < 353.
```

搜索只删去这个已证明不可能为平方的实区间外部分。模素数筛把 `0` 也视为
平方，故不会删去分支点；最终对齐次四次式

```text
H_h(a,b)=b^4 H(a/b)
```

使用整数 `isqrt` 验证。由于 `b^4` 本身为平方，
`H(a/b)` 为有理平方当且仅当 `H_h(a,b)` 为整数平方。于是给定高度盒内的
负结果是完备的。

## 5. 文件与验证

- `STUDENT_ELLIPTIC_ROUND_03_local.py`：同一 `m` 证书、不变量复核、Sturm
  区间与精确高度搜索；
- `STUDENT_ELLIPTIC_ROUND_03_certificate.json`：机器可读、分类后的结果；
- `STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m`：决定性无界下降；
- `STUDENT_ELLIPTIC_ROUND_03_run_magma_audit.ps1`：版本、哈希、transcript
  与 warning 失败即停；
- `STUDENT_ELLIPTIC_ROUND_03_test.py`：五项回归测试。

验证结果：

```text
python -m unittest -v STUDENT_ELLIPTIC_ROUND_03_test.py
Ran 5 tests -- OK

PowerShell parser: OK
Magma executable: unavailable
```

## 6. 下一步与停止条件

唯一优先动作是在有许可的**本地** Magma 上运行审计包装。

- clean transcript 且 `#SelH=0`：立即结题，不再计算属 3 商；
- clean transcript 且 `#SelH>0`：保存 fake Selmer 元素及映射，再逐覆盖做
  有理点/Mordell--Weil sieve；非空本身不是点；
- 任何 warning、条件性、错误或未完成：保持“待 Magma”，不得根据部分
  输出作结论；
- 若完整 `C_H` 路线不能闭合，再考虑属 3 商，不先投入该高成本分支。

## 7. 参考

- Magma V2.29 Handbook, [Two-Selmer Set of a
  Curve](https://magma.maths.usyd.edu.au/magma/handbook/text/1619)。该页明确
  `TwoCoverDescent` 返回 fake 2-Selmer set，空集推出无有理点；也明确
  `PrimeBound`/`PrimeCutoff` 会产生可能更大的集合。
- Magma V2.29 Handbook, [Command Line
  Options](https://magma.maths.usyd.edu.au/magma/handbook/text/47)。该页记录
  `--version`、`-b`、`-n` 的含义。
