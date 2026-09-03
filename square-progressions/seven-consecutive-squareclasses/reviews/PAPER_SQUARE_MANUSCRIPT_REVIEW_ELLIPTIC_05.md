# 甲线第五轮稿件交叉审稿（丙组）

日期：2026-09-03  
审稿范围：`PAPER_SQUARE_ROUND_05_REPORT.md`、mask-108 脚本/证书/测试、
`PAPER_SQUARE_SUPPLEMENT_MANIFEST.*`、`PAPER_SQUARE_TEX/main.tex` 与
`main.pdf`、`PAPER_SQUARE_SUBMISSION/`。本审稿没有修改任何甲线文件。

## 总结判断

我没有发现阻断 Theorem 12（23 个必要模式分类）的数学错误。mask 108 的整数点
论证完整，`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23` 可独立复得；`R_1(6)=5`
的使用方向正确；Common scaling 命题中的 Kummer kernel 在零、二次及双二次三种
次数下均正确。57 项测试在原目录和只含 manifest 23 个文件的隔离目录中各通过一次。

稿件尚不能实际投稿，阻断项是外部/编辑性而非当前主定理：作者身份仍为
`Working draft`，公开归档 DOI/URL 为空，也尚无人工确认的原创性与 AI 使用声明。
此外，当前 manifest 严格闭合的是**数学补充材料的 23 文件 payload**，不是整个
TeX/PDF/投稿文件夹；投稿材料应避免把这两种“闭包”混称。

## Blocking

### B1（投稿阻断，非数学阻断）：公开归档及作者元数据尚未完成

`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json` 明确记录
`LOCAL_RELEASE_CANDIDATE_NOT_PUBLICLY_ARCHIVED`、`archival_url=null`；PDF 作者仍为
`Working draft`，cover letter、author contributions 和 data/code statement 都保留
占位符。因此当前可以称为“数学上可送独立复核的候选稿”，不能称为可实际提交包。
甲线报告和 submission README 已正确承认这一点。

### B2（仅在声称“整个投稿包哈希闭包”时阻断）：没有 submission root manifest

补充材料 manifest 不包含 `main.tex`、`references.bib`、`main.pdf` 或
`PAPER_SQUARE_SUBMISSION/` 的九个文件。submission README 虽列出了四个主要哈希，
但 README 自身及其余投稿文案没有被根哈希绑定，也没有测试在文案漂移时 fail-closed。
因此目前已证明的是“23 个 supplement 文件的依赖闭包”，不是“投稿包的哈希闭包”。
若论文只作前一较窄陈述，此项不影响数学结论；若准备冻结投稿包，则需新增独立的
release manifest（并避免把自引用根文件放进自己的 payload）。

## Major

### M1：`R_s(N)` 的定义应把零项和量词写得完全形式化

正文写

`R_s(N)=max_{a,q,V} #{0<=i<N : [a+qi] in V}`

但 `[0]` 在 `Q*/Q*2` 中无定义，而随后的“the nonzero terms form a rational arithmetic
progression”可能让读者误以为允许某一项为零再忽略。建议明确要求
`a+qi != 0` 对所有 `0<=i<N`，并明确 `a,q in Q, q != 0`、`dim V=s`；或者定义计数
集合时同时加入 `a+qi !=0`。这不影响本文应用（`t=-6,...,0` 已排除），但应在发表前
消除定义域歧义。

### M2：把 651 的入口条件在摘要/命题前再说一句

651 不是“仿射秩至多 2 的全部模式”原始数，而是先由 Lemma 1 排除 1、2 块情形后，
剩余 3、4 块未标号划分的总数。正文证明能够恢复这个逻辑，Theorem 12 也明确排除了
rank 0/1，因此定理成立；但摘要的“651 initial ... patterns”容易被误读为未经预筛的
全集。建议改成“after excluding affine rank at most one, the 651 three- or four-block
patterns ...”。

### M3：新颖性审计对主张足够谨慎，但尚不足以支持更强措辞

Xarles 的原论文摘要确实说二次数域上的最大长度为 5，和正文引用
“Theorem 1, `S(2)=6`”的推论一致；Gonzalez-Jimenez--Xarles 的原文 Corollary 6 明确有
`Q(6)=Q(7)=4`。当前网页/精确方程检索没有找到与 Theorems 7、8 相同的已发表陈述，
但这种负检索不能证明优先权。正文已经使用 “not found report, not proof of novelty”，
limitations 也禁止 `first/new/previously unknown`，所以现有措辞可接受。若投稿前想把
“新结果”写进摘要或 cover letter，必须先由人工作更强的 MathSciNet/zbMATH/引文链
检索；否则保持当前弱措辞。

原始来源核对：

- Xavier Xarles, *Squares in arithmetic progression over number fields*,
  arXiv:0909.1642；摘要陈述 quadratic-field bound 为 5：
  https://arxiv.org/abs/0909.1642
- Gonzalez-Jimenez--Xarles, *On a conjecture of Rudin on squares in arithmetic
  progressions*, arXiv:1301.5122；Corollary 6 为 `Q(6)=Q(7)=4`：
  https://arxiv.org/abs/1301.5122

## Minor

### m1：manifest 测试的“命令覆盖”断言偏弱

`test_commands_cover_all_paper_generators_and_tests` 只检查五个子串，不逐个证明所有
generator/test 都出现在 reproduction command。当前 23 文件隔离重建已实证成功，故
不是现状错误；为防下次增文件后静默遗漏，建议从 `ARTIFACTS` 的 role 自动生成或逐项
断言命令覆盖。

### m2：所有 manifest 条目都标 `mathematical_evidence_eligible=true`

测试文件和生成器源也被标成 evidence-eligible，语义较宽。建议改成明确的 role-based
说明：证书承载结果，生成器与测试承载可复核性；或者把布尔字段解释为“可进入审计
payload”，避免与“某文件单独构成数学证据”混淆。

### m3：PDF 重建哈希不稳定是预期现象，README 的限定必须保留

临时空目录从 `main.tex`/`references.bib` 重建成功，7 页、最终 log 无 undefined
reference/citation、Warning、Overfull、Underfull；全页目检无溢出、截断或表格破版。
新 PDF 字节数同为 255867，但 SHA-256 因 PDF 元数据时间而不同。submission
`reproducibility.md` 已准确说 PDF hash 只是 reference artifact，不承诺 bit-for-bit
重建；该限定不可删。

## 独立数学核验

### 1. mask 108 完整性

令

`A=(t+2)(t+6)=(t+4)^2-4`，`B=(t+3)(t+5)=(t+4)^2-1=A+3`。

当 `t<=-7` 或 `t>=-1` 时 `A,B>0`。若 `AB` 是平方，把二者写成共同正平方自由核
`A=dU^2, B=dV^2`；因 `gcd(A,B)|3`，只有 `d=1,3`。

- `d=1`：`(V-U)(V+U)=3`，正同奇偶因子对只有 `(1,3)`，故 `(U,V)=(1,2)`；
  `A=1` 等价于 `(t+4)^2=5`，模 8 不可能。
- `d=3`：`(V-U)(V+U)=1`，故 `U=0`，与外区间 `A>0` 矛盾。
- 唯一未覆盖整数 `t=-6,-5,-4,-3,-2` 逐项给 RHS `0,0,4,0,0`。

所以整数点恰为
`(-6,0),(-5,0),(-4,+/-2),(-3,0),(-2,0)`；全部使七个原项之一为零。
论证没有高度界或漏掉负平方自由核的问题，因为外区间的 `A,B` 都严格为正。

### 2. 651 -> 343 -> 284 -> 98 的独立枚举

我另写一次性、未 import 甲线模块的 RGS/反射/关系核重算，得到：

| 量 | 独立结果 |
|---|---:|
| `S(7,3)+S(7,4)` | 651 |
| 反射固定原始划分 | 35 |
| 筛前反射轨道 | 343 |
| 严格筛排除原始划分 / 轨道 | 109 / 59 |
| 幸存原始划分 / 反射固定 / 轨道 | 542 / 26 / 284 |
| 每一幸存模式非零 kernel 元素数 | 15 |
| 含 mask 15/30/60/120 的模式 | 186 |
| 第一轮积分排除后 | 98 |

Burnside 等式分别为 `(651+35)/2=343` 与 `(542+26)/2=284`。

### 3. 98 -> 54 -> 35 -> 23 与表 1

从 Round-04 的 284 行 occurrence 数据重新构造每行 15-mask 集，不读取后续 survivor
列表：连续四 mask 留 98；对 77 使用唯一非分支参数 `t=6`、对 89 使用 `t=-12`，并在
同一 `t` 检查全 15 个乘积，恰排 44 留 54；mask 102 排 19 留 35；mask 108 排 12
留 23。得到的 ID 和 restricted-growth words 与 Table 1 逐项一致：

`9,12,26,31,33,43,50,59,83,134,188,210,212,214,230,251,257,266,268,271,276,281,283`。

因此 651 到 23 的每一箭头都表示必要条件筛，不含“23 个可实现”的逆向断言。

### 4. `R_1(6)=5` 及其在汇总定理中的作用

若六项平方类全落在一维子空间 `V=<[D]>`，每一项在 `Q(sqrt(D))` 中都是平方。
Xarles 的二次数域结果排除六项非恒定平方列，故至多五项。反例下界来自公差 120 的
六项
`49,169,289,409,529,649`：前五项的平方类属于 `<[409]>`。所以 `R_1(6)=5`。
对任一七项 affine-rank 0/1 实现，公共缩放后任一六项端点窗口都落入一维线性子空间，
与该引理矛盾；故 Theorem 12 中实际 affine rank 必为 2。这正当化了只枚举 3/4 块，
也使标签到真实平方类的线性映射秩为 2、从而在 `F_2^2` 上单射。

### 5. Kummer kernel

对 `L=Q(sqrt(D1),sqrt(D2))`，若 `[r]` 在 `L*/L*2` 中消失且 `r` 非平方，则
`Q(sqrt(r))` 是 `L` 的二次子域。度 4 双二次情形恰有三个二次子域，对应
`[D1],[D2],[D1D2]`，所以 kernel 恰为 `<[D1],[D2]>`；度 2 时 kernel 是唯一相应的一维
子空间，度 1 时为零。正文还正确保留了公共类 `c`：未经缩放的七项可能需要再添
`sqrt(c)` 而升到八次域。未发现把 affine coset 错当成线性子空间的问题。

## 复跑与制品一致性

- 原目录完整命令：57/57 passed，5.124 s。
- 隔离目录：只复制 manifest 所列 23 文件，依次重跑四个数学生成器和 manifest；
  重生成的 23 文件全部与原件 SHA-256/字节长度一致，根 manifest 仍为
  `6004afc5334bbea62969640079cad80764d2938d73b6fd62a85abc2249794588`；随后
  57/57 passed，5.068 s。
- 当前磁盘上的 `main.tex`、`references.bib`、`main.pdf`、manifest、mask-108
  certificate 哈希与 submission README/round-05 report 所列值全部一致。
- 临时空目录 LaTeX/BibTeX/pdflatex 全链成功；最终 PDF 7 页。逐页目检标题、公式、
  18 分支表、最终 23 模式表和参考文献，无可见布局缺陷。

## 可接受的最小投稿结论

在完成 B1/B2 的行政冻结且处理 M1/M2 的措辞后，可以投稿的最小单元是：

> 对非退化整数 `t`，若七个连续整数的平方类 affine rank 至多 2，则其真实平方类
> 等值划分（模重标号与反射）属于显式列出的 23 个必要候选；证明由完整有限枚举、
> 一个四连续因子引理及三个初等 quartic 整数点门组成。

必须继续明确：不证明 23 个模式中任何一个可实现，不决定 `R_2(7)`，也不把本文的
整数归一化定理外推为任意有理首项/公差的分类。
