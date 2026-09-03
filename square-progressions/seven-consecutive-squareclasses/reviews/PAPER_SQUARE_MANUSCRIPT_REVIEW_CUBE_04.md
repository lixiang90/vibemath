# Square manuscript cross-review (cube line, round 4)

审稿日期：2026-09-03。审查对象为 `PAPER_SQUARE_TEX/main.tex`、`main.pdf`、
`build.log`、Round-04 报告、prior-art 说明，以及 SAFE / mask77 / next-gate
脚本与证书。本报告只审不改。

## 总评

**数学核心目前没有发现反例或错误计数；但稿件尚不宜投稿。** 阻断点是正文所依赖的
计算补充材料在稿内没有可定位、可下载的版本，因此读者无法从独立稿件复核
`651 -> 343 -> 284 -> 98 -> 54 -> 35`。补齐正式 supplement/data-availability 后，
稿件可进入一次 major revision；若不继续关闭 35 个模式，定位应是短篇计算/初等数论论文，
而不是对七项问题的最终解决。

## 独立复核通过的项目

### 1. mask 102 的完整整数点与 19/35 计数

令

\[
A=(t+1)(t+6),\qquad B=(t+2)(t+5)=A+4.
\]

在 `t<=-7` 或 `t>=0` 时二者为正，且 `gcd(A,B)|4`。若 `AB` 为平方，二者的
共同正 squarefree kernel 必为 `d=1` 或 `2`。

- `d=1` 给 `(V-U)(V+U)=4`。唯一同奇偶正因子对是 `(2,2)`，迫使 `U=0`，
  与外区间的 `A>0` 矛盾。
- `d=2` 给 `V^2-U^2=2`，模 4 不可能。
- `t=-6,...,-1` 的右端依次为 `0,0,12,12,0,0`。

所以

\[
H_{102}(\mathbf Z)=\{(-6,0),(-5,0),(-2,0),(-1,0)\}
\]

是完整列表，而不是有界搜索。独立从 Round-04 occurrence 表重算：mask 102 恰击中
54 行中的 19 行；证书给出的 19 个 ID 互异，并与 35 个 survivor 互补。35 个 survivor
清单与动态生成完全一致。

### 2. `651 -> 35` 数值链

独立复跑结果：

- `S(7,3)+S(7,4)=301+350=651`；反射不动 35 个，Burnside 得 343。
- 第一屏删除 109 个 raw words、59 个反射轨道；余 542 个，其中反射不动 26 个，
  得 `(542+26)/2=284`。
- 每行关系空间维数 4，恰有 15 个非零 character；总出现数 `284*15=4260`。
- consecutive-four mask 删除 186，余 98。
- mask 77/89 在 98 行中出现数为 26、25，交 7，并 44；same-`t` 检查全部失败，余 54。
- mask 102 再删 19，余 35。

测试命令

```text
python -m unittest -v PAPER_SQUARE_SAFE_test.py PAPER_SQUARE_MASK77_test.py PAPER_SQUARE_NEXT_GATE_test.py
```

实测 **25/25 通过**。SAFE、mask77、next-gate 三个 SHA256 也分别与报告中的
`6FB8...164C`、`A74F...25F8`、`B63F...A178` 一致。

### 3. mask 77 的 18 分支和 15 个模阻碍

从 `x=t+3` 得

\[
x^2-dU^2=9,\qquad x(x-1)=dV^2,qquad d\in\{1,2,3,6\}.
\]

对每个 `d`，`d=ab` 的 ordered coprime factorization 有 `2^omega(d)` 个；再乘
`x>0/x<0` 两符号，总数

\[
2(1+2+2+4)=18.
\]

代码中的模方程编码与正文完全一致：

- `x=aR^2>0` 检查 `aR^2-bS^2=1`；
- `x=-aR^2<0` 检查 `bS^2-aR^2=1`；
- 两者都检查 `a^2R^4-dU^2=9`。

逐行重算所得 15 个阻碍 modulus 正好是正文表：`d=1` 的 `16,8`；`d=2`
除 `(1,2,+)` 外为 `9,8,8`；`d=3` 除 `(3,1,-)` 外为 `9,8,8`；`d=6`
除 `(3,2,+)` 外为 `9,8,8,8,8,8,8`。每个 modulus 都对全部 residue
`R,S,U` 穷举，不是随机样本。

三个剩余分支的恒等式、符号与小值均正确：

1. `(d,a,b,sign)=(2,1,2,+)`：
   `(U-RS)(U+RS)=(R^2-9)/2`；`R` 奇，`R=1` 不可能，`R=3` 给
   `(S,U)=(2,6)`，`R>=5` 时两因子为正且 `U+RS` 大于其乘积。
2. `(3,3,1,-)`：
   `(RS-U)(RS+U)=R^2+3`；`R=0,2` 不可能，`R=1` 给 `(2,0)`，
   `R>=3` 时 `RS>sqrt(3)R^2>R^2+3`。
3. `(6,3,2,+)`：
   `(U-RS)(U+RS)=(R^2-3)/2`；`R` 奇，`R=1` 给 `(1,0)`，
   `R>=3` 使用同样的正因子大小矛盾。

因此

\[
H_{77}(\mathbf Z)={(-6,0),(-3,0),(-2,0),(0,0),(6,\pm72)\}
\]

确由全局分支证明得到。有界 `|t|<=10^6` 清单虽然一致，但代码和稿件均正确标成
conjectural-only，未参与完备性。

### 4. mask 77/89 的 same-parameter 逻辑

反射 `t=-u-6` 的多项式恒等式正确。mask 77 唯一非 branch 整数参数为 `t=6`；
mask 89 因此为 `t=-12`。对仅含一个特殊 mask 的行，程序在同一个 `t` 上重算全部
15 个 character product；含二者的 7 行候选集合 `{6}` 与 `{-12}` 交空。44 行全部
被严格排除，54 行 ID 互异。这里没有“分别在不同 quotient 上选参数”的兼容性漏洞。

### 5. 引用中已核实正确的部分

- González-Jiménez--Xarles 的原论文 Proposition 5 给出七位置四子集的五个禁型，
  Corollary 6 明确给出 `Q(6)=Q(7)=4`；正文的四位置 screen 有实质支持：
  <https://arxiv.org/html/1301.5122>。
- Xarles 的原论文摘要明确说 quadratic fields 的长度上界是 5，足以支持“不存在六项”
  这条输入：<https://arxiv.org/html/0909.1642>。
- LMFDB API 核实 `[0,0,0,-36,0]` 的确是 576.c3；稿件只把标签当 cross-check，
  没有把椭圆模型的 integral points 与所需 S-integral 条件混淆：
  <https://www.lmfdb.org/api/ec_curvedata/?lmfdb_label=576.c3&_format=json>。
- 两篇 2026 原论文确有条件性边界：quadratic-extension 论文涉及 class number 与椭圆
  曲线 base-change/rank 条件；non-primitive quartic 论文也对 `D` 加条件：
  <https://arxiv.org/abs/2602.03251>，<https://arxiv.org/abs/2602.01380>。

## Blocking

### B1. 正文没有交付可定位的计算证明补充材料

正文多次写 “the supplementary generator” 或 “the certificate”，但没有给出文件名、
版本/commit、归档 DOI/URL、数据可得性声明，亦未附 35 survivor、44 same-`t` audit、
19 affected IDs 或 284 行 canonical pattern 表。因而脱离当前工作区后，以下核心主张均
无法由论文独立复核：109/59 screen、186 排除、44 same-`t` 排除、19 排除和最终 35。

投稿前至少需要：

1. 将 exact generators、三个证书和测试打成不可变 supplement 并公开归档；
2. 在正文列出精确文件名、release/commit、SHA256 和一条从 clean checkout 运行的命令；
3. 附录至少列 35 survivor 的 canonical ID/partition，并说明 ID 规范；
4. 对 15 个 congruence branches 给伪代码或 residue-set 摘要，使读者不依赖 Python
   实现细节即可重写验证。

这是投稿阻断，不是发现了数学反例。

## Major

### M1. `R_1(6)=5` 是关键筛条件，但正文未定义 `R_1`、未在使用处引用

它负责排除 affine rank 0/1，并保证后面的三/四块枚举完备。当前只写 “known equality”，
读者不能看出它与 quadratic-field 六平方不存在的等价关系。应定义 `R_s(N)`，给公共
缩放引理的推论，并精确引用 Xarles 的 degree-2 bound；同时给五项下界例子或引用。

### M2. Proposition 1 的 kernel 等式需要一行 Kummer 论证

\[
\ker(\Q^*/\Q^{*2}\to L^*/L^{*2})=\langle[D_1],[D_2]\rangle
\]

是正确的，但目前在 converse 中直接断言。应说明由 biquadratic extension 的三个 quadratic
subfields/Kummer correspondence 得出，并处理 `[L:Q]<4` 的退化情形。这是整篇从
square classes 到低次数域解释的基础。

### M3. 主结果的陈述层级不足

目前没有一个总定理明确说“在所定义的 canonical pattern universe 中，所有可行七项
affine-rank-2 参数只能属于列出的 35 个模式”。Theorem 7 标题 “Finite classification”
容易被读成实际解分类，但只是一层排除。建议把 Proposition 3、Theorem 7、Corollary 9
汇总成一个精确主定理，并在同一句中声明：不证明 35 个模式可实现，也不判定
`R_2(7)`。

### M4. 证书的长期审计绑定仍不够完整

next-gate certificate 绑定了两个上游 JSON，测试也检查 disk certificate 等于当前生成值；
但证书没有绑定生成脚本、测试、Python/SymPy 版本或仓库 release。改变生成器后重新运行可
产生一个同样“自洽”的新证书。公开 supplement 应以 release/commit 或独立 manifest
同时绑定 source、inputs、outputs 和命令。

### M5. prior-art 文件有一个明确书目错误

`PAPER_SQUARE_PRIOR_ART.md` 把 Bremner--Siksek 2015 写成 “over quartic fields”；
arXiv 1505.06424 和正文 bibliography 的正确题名是 **over cubic fields**。应统一修正。

## Minor

1. 题名说 “an elementary integral quartic”，但正文严格求解了 `H_77` 和 `H_102`
   两个 quartic；题名和摘要可改成复数，或说明第二个只是 gate lemma。
2. 摘要的 “After known six-term and four-square restrictions” 应加精确引用，且最好明确
   研究对象是整数参数而非任意有理 `t`。
3. `MassPethoTzanakis` 这个 BibTeX key 与实际作者 Masser--Rickert 不符，虽不影响输出，
   但会误导维护者。
4. README 的 “reproducible” 目前指内容/构建成功而非 bit-for-bit PDF：clean build 成功且
   页数、大小相同，但 PDF SHA 因生成元数据不同而改变。若宣称 bitwise reproducibility，
   需固定 `SOURCE_DATE_EPOCH` 等元数据。
5. PDF 未设置题名/作者 metadata 且不是 tagged PDF；多数数学期刊不阻断，但归档前可补。

## 构建与版面

从只含 `main.tex` 与 `references.bib` 的干净临时目录运行 README 的 `latexmk` 命令成功，
BibTeX 与交叉引用收敛；最终 log 无 undefined citation/reference、Overfull 或 Underfull。
保存的 `main.pdf` 为 A4、5 页，SHA256 与报告一致。

逐页 140 dpi 渲染检查未见文字截断、重叠、黑块或不可读公式。页 3 的 18-branch 表较密，
但仍清晰；标题层级、页码和参考文献换页正常。版面本身可接受，不是阻断项。

## 投稿可行性

当前状态：**not submission-ready; mathematically promising after major revision**。

若完成 B1、M1--M5，这一版本可作为“两个精确 integral quartic + 七项 square-class 模式
严格缩减”的短篇计算数论稿投稿。新颖性措辞必须继续维持 “we did not locate”，因为负面
检索不能证明 first/new；且最终仍余 35 模式，贡献不是解决 `R_2(7)`。以当前数学闭合度，
更适合重视可复现计算或短结果的期刊层级。若后续关闭全部 35 或得到结构性分类，再考虑
更高层级的数论期刊。
