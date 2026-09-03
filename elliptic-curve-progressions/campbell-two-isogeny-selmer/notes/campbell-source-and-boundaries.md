# 丙线第六轮报告：Campbell 八项族的有限二同源定理

日期：2026-09-03。状态：**本地投稿候选稿；有限定理已闭合，尚未授权投稿或公开归档。**

## 1. 本轮结论

第五轮交叉审稿的两个 blocking 已在本地稿件层面修复：

1. 建立了可定位、可哈希、可隔离重建的两级清单。补充材料入口为
   `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json`，发布号
   `paper-elliptic-campbell-supplement-v0.6.0`；投稿快照入口为
   `PAPER_ELLIPTIC_RELEASE_MANIFEST.json`。
2. 从 Campbell 原文的 Corollary 2.4、Theorem 2.5 及其证明独立重建
   `g_m`、参数变换、八个点和第九候选，并把全部有理退化边界写入正文和
   结构化证书。

可作为短文主结果的严格结论是：对 Campbell 第九值四次式 `H` 的
Jacobian `E` 及其二同源曲线 `E'`，

```text
Sel^(dual phi)(E'/Q) = <3,5,7>,               dim = 3,
Sel^phi(E/Q)         = <4230241,339106321>,   dim = 2,
rank E(Q) <= 3.
```

此外，`H` 的 `Q x K` 三次代数 Kummer 代表及其有理二挠投影 `[35]`、
512 个局部单元和同一参数 `m` 的处处局部可解性均有精确证书。这里没有
计算完整二-Selmer 群、Cassels--Tate 配对或秩等号，也没有产生或排除
Campbell 族的第九个有理点。

## 2. Campbell 输入的自足重建

来源是 Garikai Campbell, *A Note on Arithmetic Progressions on Elliptic
Curves*, Journal of Integer Sequences 6 (2003), Article 03.1.3。原参数与本稿
参数的关系为

```text
t = (6 m^2 - 126 m - 285360)/(m^2 - 72256).
```

脚本 `PAPER_ELLIPTIC_ROUND_06_analysis.py` 独立展开 Campbell 的四个系数，
验证 `g_m(j)=q_j(m)^2`（`j=0,...,6`）、`g_m(7)=D(m)` 和
`g_m(8)=H(m)`。因此：

- 自动平方项的索引为 `0,...,6`；
- 第八项索引为 `7`，其条件是 `Y^2=D(m)`；
- 紧接的第九候选索引为 `8`，必须在同一个 `m` 上满足 `z^2=H(m)`。

本轮也逐一关闭了有理退化边界：

- `m^2-72256=0` 无有理解，故参数变换分母不在 `Q` 上消失；Campbell 的
  例外值 `t=5/2` 同样无相应有理 `m`。
- `g_3=-18816(m^2-72256)(m^2-36m-29920)` 的两个二次因子均无有理根，
  所以三次项不会在有理特化下降阶。
- `disc_x(g_m)` 除去常数后是次数 16 的本原多项式；其模 53 不可约，故
  无有理根，没有有理奇异特化。
- `m=infinity` 不在 `C_D(Q)` 上，因为无穷远首项要求
  `Y^2=-264815 M^4`。
- 九个横坐标 `0,...,8` 恒互异。`D=0` 或 `H=0` 只给相应分支点
  `Y=0` 或 `z=0`，并不使 `g_m` 奇异；`Res(D,H) != 0` 排除两者同时为零。

完整系数、七个平方根、四次式判别式和 resultant 均保存在
`PAPER_ELLIPTIC_ROUND_06_CERTIFICATE.json`。

## 3. 同一 m 的局部证书

曲线

```text
Y^2=D(m),  z^2=H(m)
```

在实位、二进位以及每个必要奇素位上都有**同一个 `m`** 的精确见证。
分支坏素数集合为

```text
{2,3,5,7,17,19,31,59,8599,71699,898543,23037169,
 339106321,1153266911}.
```

证书另含所有奇素数 `<101` 的见证。对不在分支坏集且 `p>=101` 的素数，
光滑 genus-5 约化满足
`#C(F_p) >= p+1-10 sqrt(p) > 0`，再由 Hensel 提升得到 `Q_p` 点。故这里
严格得到处处局部非空；它不推出全局有理点。

原始同一 `m` 证书为 `STUDENT_ELLIPTIC_ROUND_03_certificate.json`，其
SHA-256 为
`74843e4e53c7d09793fa857a2ce57d37a21be855ce135fec9f22b5b00aab5e08`。
Round06 生成器重新核验全部见证、判别式、resultant 和坏素数表，而非只
复制文字结论。

## 4. 两级清单和可复现性

补充材料 manifest 覆盖 17 个文件，包括：

- 512 格 JSON 证书、生成器和回归测试；
- same-`m` 原始证书；
- Round04 精确 Selmer 生成器、证书与测试；
- Round05 被否决的 pairing 表达式审计（仅作负面证据）；
- Round06 Campbell 重建、证书与测试；
- prior-art 检索记录和未执行 Magma 候选输入。

它记录路径、角色、字节数、SHA-256、证据资格、Python `3.14.5`、SymPy
`1.14.0` 和逐条复现命令。隔离测试把这 17 个文件复制到临时目录，重新
生成 Campbell、Round04、Round05、Round06 证书和 manifest，并要求逐字节
相等。补充材料 manifest 的 SHA-256 为

```text
ec078950fc1f7d2adae59adb5556e432b2be46a9eeef3956d64505d2bcc14f82
```

root manifest 再绑定补充材料 manifest、TeX、PDF、prior-art 记录、投稿
材料和自身生成器/测试。它不是公开归档：`public_archive=null`，状态为
`LOCAL_DRAFT_NOT_AUTHORIZED_FOR_SUBMISSION`。PDF 的位级哈希只标识当前
快照；TeX 工具链元数据可能令重编译 PDF 不逐字节相同。

## 5. Magma 的 fail-closed 边界

`PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m` 只是一份冻结候选输入：

```text
status = UNEXECUTED_FROZEN_CANDIDATE_INPUT
transcript = null
magma_binary_sha256 = null
mathematical_evidence_eligible = false
```

生成器、JSON、manifest 和测试共同断言它不得用于提升以下任何结论：完整
二-Selmer 维数、Cassels--Tate 配对值、Mordell--Weil 秩等号或
`C_H(Q)` 的空/非空。本稿有限定理完全不读取其输出。

## 6. prior-art 审计和新颖性边界

对两条大系数曲线、`D`、`H` 的系数以及两个精确 survivor 集合进行了引号
exact-query 检索，并检查 Campbell 原文及邻近的 Bremner、
Garcia-Selfa--Tornero、Fisher 文献。没有检索到这些特定模型或这两个
Selmer 集合的已发表计算。

这只允许写成“exact-coefficient and exact-squareclass searches did not
locate a published computation”。它不是优先权或新颖性证明；投稿前仍需由
作者人工检查 MathSciNet、zbMATH、引用链和同构模型。详见
`PAPER_ELLIPTIC_PRIOR_ART.md`。

## 7. 投稿包

`PAPER_ELLIPTIC_SUBMISSION/` 已包含：投稿摘要、cover letter、期刊顺序、
作者贡献、数据/代码可得性、AI 使用声明、限制声明和 README。作者姓名、
单位、通讯邮箱、ORCID、资助和利益冲突均保留占位符，不能在填写和人工
批准前投稿。

期刊建议：首选 **INTEGERS**；备选 **Research in Number Theory**；若能把
与 Campbell 原文的延伸关系强化成更清晰的序列论叙事，再考虑 **Journal of
Integer Sequences**。当前最稳妥的定位是一个可核验的有限二同源下降短文，
而不是“九项问题”论文。

## 8. 验证结果

联合运行 45 个测试：

```text
python -m unittest PAPER_ELLIPTIC_NEXT_test.py \
  PAPER_ELLIPTIC_CAMPBELL_test.py \
  PAPER_ELLIPTIC_ROUND_04_test.py \
  PAPER_ELLIPTIC_ROUND_05_test.py \
  PAPER_ELLIPTIC_ROUND_06_test.py \
  PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST_test.py \
  PAPER_ELLIPTIC_RELEASE_MANIFEST_test.py -v

Ran 45 tests ... OK
```

`latexmk -pdf -interaction=nonstopmode -halt-on-error PAPER_ELLIPTIC_TEX.tex`
成功生成 7 页 PDF；日志中没有 undefined reference/citation、overfull、
underfull 或 LaTeX warning。七页均已渲染检查，无裁切、重叠或不可读表格。

## 9. 当前停止线

有限定理已经闭合。下一步不是继续尝试未经审计的跨侧局部符号，而是：

1. 完成人工同构模型和书目数据库查重；
2. 给 supplement 取得稳定公开 DOI/URL，并把 manifest 的 null 地址替换为
   固定归档；
3. 填写作者信息、声明并做期刊格式化；
4. 若未来要越过有限定理，再独立运行、保存并审计同侧 full two-cover
   descent；其结果不得回写成本轮已经证明的内容。

