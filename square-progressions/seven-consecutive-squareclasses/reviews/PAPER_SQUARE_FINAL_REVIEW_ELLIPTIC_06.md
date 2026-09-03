# 甲线第六轮冻结稿终审（丙组）

日期：2026-09-03  
审阅范围：`PAPER_SQUARE_ROUND_06_REPORT.md`、两级 manifest/生成器/测试、
`PAPER_SQUARE_TEX/main.tex`、`references.bib`、`main.pdf` 以及
`PAPER_SQUARE_SUBMISSION/`。本审稿未修改任何甲线文件。

## 决定

**ACCEPT，附两项 minor revision；无 mathematical blocking 或 major。**

本地冻结稿已经足以支持 Theorem 12 的有限必要分类：对非退化整数参数，七个
连续数的平方类若 affine rank 至多二，则其等值划分（模重标号与反射）属于表中
23 个候选。所有箭头

```text
651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23
```

均是必要条件筛。稿件没有声称任一候选可实现，也没有决定 `R_2(7)` 或一般有理
首项/公差的问题。

实际投稿仍须作者信息、期刊选择、人工原创性/引文复核、AI 声明以及公开归档
DOI/URL；这些是稿件已明示的外部步骤，不是本轮数学审稿的新 blocking。

## Minor revisions

### m1. Cover letter 应同步 651 的入口限定

正文摘要和 submission abstract 已正确写成：**先排除 affine rank 至多一，才有
651 个三/四块未标号划分**。但 `PAPER_SQUARE_SUBMISSION/cover_letter.md:12`
仍写 “reduces 651 initial patterns”，没有这个前置限定。它不会改变定理，但正是
上一轮 M2 所要避免的歧义。建议改成：

> After affine rank at most one is excluded, the theorem reduces the 651
> three- or four-block patterns to 23 explicitly listed necessary candidates.

### m2. 可选的 root-verifier 防御性加固

当前 `verify_manifest` 严格检查 schema、semantic version、release ID、空 archive
URL、13 行 payload 的顺序/角色/版本/字节/哈希、nested manifest 元数据、PDF
policy 和 submission 目录闭包；当前 JSON 的 claim boundary 也完全正确。
不过 verifier 没有逐字段固定 `release_status`、`author_metadata_status`、
`manifest_trust_anchor` 和 `claim_boundary`。最终外部 archive 对 root manifest 本身
做哈希锚定后，这些字段的篡改自然会改变 root hash，所以这不是当前闭包反例。
若希望 verifier 在尚无外部锚时也对这些语义字段 fail-closed，可在下一小修中加入
常量比较与负向 fixture。

## 核验一：`R_s(N)` 的零项与量词修复

正文现在明确量化

```text
a,q in Q, q != 0;
V <= Q*/Q*2, dim_F2(V)=s;
a+qi != 0 for every 0<=i<N.
```

因此 `[a+qi]` 始终有定义，进展非恒定，且 `V` 是**恰好** `s` 维。正文还明确
区分 common rational scaling 与 affine rank。Common-scaling 命题的 Kummer
kernel 论证覆盖次数 1、2、4；备注保留了未缩放公共类可能令所需域升到八次的
边界。

Lemma 1 的使用也正确：若七项 affine rank 为 0 或 1，公共缩放后任一六项窗口
落入某个一维平方类子空间，和 `R_1(6)=5` 矛盾。因此后续只枚举真正 rank-two
的三/四块标签，不把零项或 rank-one 模式偷偷计入。

## 核验二：651 的准确入口与摘要边界

正文及 submission abstract 都明确采用以下顺序：

1. 先由 `R_1(6)=5` 排除 affine rank 0/1；
2. rank two 至多使用四个标签且至少使用三个标签；
3. `S(7,3)+S(7,4)=301+350=651`；
4. 反射固定 35 个，Burnside 得 `(651+35)/2=343`；
5. 已知六项/四平方筛排除 59 个反射轨道，留下 284。

所以 651 不是“未经任何预筛的所有 affine-rank-at-most-two 配置”。正文摘要、
Proposition 4 和 submission abstract 已修正；唯一残留是上列 cover-letter 简写。

## 核验三：两级 manifest 闭包

### Supplement root

`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json`：

- schema `paper-square-supplement-manifest-v1`；
- release `paper-square-supplement-v0.5.0`；
- 恰含 23 个脚本、证书和测试；
- 每行均有路径、字节数、SHA-256、角色和证据资格；
- runtime 为 Python 3.14.5 / SymPy 1.14.0；
- `archival_url=null`，没有伪造公开归档状态；
- SHA-256 为
  `6004afc5334bbea62969640079cad80764d2938d73b6fd62a85abc2249794588`。

我另建空目录，只复制这 23 个文件，依次重跑 SAFE、mask 77、NEXT_GATE、
mask 108 和 supplement manifest 生成器。重建后 23/23 文件的字节长度与 SHA
全部相同，manifest hash 仍为上述值；随后隔离运行 **57/57 tests, OK**。

### Submission root

`PAPER_SQUARE_SUBMISSION_MANIFEST.json` 恰含 13 行：

- `main.tex`、`references.bib`、冻结的 `main.pdf`；
- nested supplement manifest；
- submission 目录的全部九个普通文件。

磁盘 submission 目录也恰有这九项，没有未绑定文件。root manifest 故意不把
自身放入 payload，避免自哈希循环；当前外部定位 SHA-256 为
`60a152f318c22d79377bf8cd9269604056c336ae32d63fe4975da747dfb13f6e`。
测试逐一篡改 13 个 payload、删除/增加 submission 文件、修改 schema/role/version
和插入自引用，均能 fail-closed。manifest 还正确区分“冻结参考 PDF 受哈希绑定”
与“因元数据时间戳，独立重编译无需 bitwise 相同”。

## 核验四：63 项联合测试与数学边界

在原目录独立运行报告给出的完整命令，结果为：

```text
Ran 63 tests in 6.087s
OK
```

其中 57 项是 nested mathematical/supplement suite，另 6 项是 submission-root
closure suite。测试覆盖：

- `651 -> 343 -> 284` 的 RGS/反射/筛计数；
- 每个 284 模式的 15 个字符，共 `284*15=4260`；
- `284 -> 98 -> 54 -> 35 -> 23` 及最终 23 个 ID/partition；
- mask 77、89 的 same-parameter 条件；
- mask 77、102、108 的完整整数点证明数据；
- 两级 manifest 的磁盘一致性和 tamper rejection。

主稿、两个 manifest、submission abstract、limitations、reproducibility 和 README
均维持以下 claim boundary：23 个模式只是必要候选；不证明可实现性或全部不可能；
不决定 `R_2(7)`；不把整数归一化结论外推为一般有理进展；不把 bounded search 或
未审计 CAS 输出当证明；“未检索到”不等于新颖性证明。

## 核验五：PDF 重编译与目检

为避免修改甲线冻结文件，我只把 `main.tex` 和 `references.bib` 复制到隔离临时目录，
运行：

```text
D:\texlive\2022\bin\win32\latexmk.exe -pdf \
  -interaction=nonstopmode -halt-on-error main.tex
```

结果为 7 页、267512 bytes；最终 LaTeX 日志没有 undefined citation/reference、
LaTeX/Package warning、overfull 或 underfull。重建 PDF 与冻结 PDF 的 SHA 因时间戳
不同，但 `pdftotext -layout` 输出逐字节相同，正好符合 manifest 的 PDF policy。

我逐页渲染检查了标题、`R_s(N)` 长公式、Kummer 命题、18 分支表、mask 102/108
论证、最终 23 模式表、manifest 长文件名和参考文献。未见裁切、重叠、黑块、坏字形、
不可读表格或页码问题。

## 最终可接受表述

> 对 `t in Z \ {-6,...,0}`，若 `[t],...,[t+6]` 的 affine rank 至多二，
> 则真实平方类等值划分（模重标号与反射）属于显式列出的 23 个必要候选；
> 证明由完全有限枚举、四连续因子恒等式和三个初等四次曲线整数点门组成。

在修正 cover letter 的一行并由作者完成外部投稿清单后，我建议冻结数学内容，
不再为终审引入新的 mask 或更强全局主张。

