# 甲组对丙线第五轮稿件的交叉审稿

审稿对象：`PAPER_ELLIPTIC_ROUND_05_REPORT.md`、
`PAPER_ELLIPTIC_ROUND_05_analysis.py`、Round 03--05 JSON 证书与测试、
冻结的 `PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m`，以及
`PAPER_ELLIPTIC_TEX.tex/pdf`。日期：2026-09-03。

## 总评

第五轮完成了最重要的数学纠错：原来的
`<35,4230241>_CT` 把两个相反方向的 isogeny Selmer 类当成同一配对的
两个输入，因而没有定义。报告、JSON、测试、TeX 和冻结 Magma 输入中均已
撤回该结论；现在只把 `35` 保留为完整 `2`-覆盖类的一个有理 `2`-挠投影，
没有再把它等同于整个 torsor。这个修复是正确且彻底的。

独立复核也确认：支撑引理、全部坏位的有限局部证书和好素数桥合在一起，
确实给出两个**精确** isogeny Selmer 群，而不再只是 ambient survivor；群名
方向和 rank 公式也正确。`Q x K` 分解、`z(H)`、范数和 `[35]` 投影均通过
整数重算。故这些有限算术结论可以接受。

不过，五页 TeX 尚不能作为独立可审计的投稿稿件：中心的 512 格证书只写
哈希而不写文件名、版本、归档位置或复现命令；更关键的 same-`m` 局部可解
证书连哈希也没有出现在正文。Campbell 构造本身没有参考文献，`g_m` 也未
定义。因此“finite theorem 是 independently reproducible / minimum
publication unit”的稿件级措辞目前过强。以下 blocking 项是**投稿阻断**，
不是对已复跑有限计算的反例。

## Blocking

### B1. 核心计算证书在 TeX 中不可定位，same-`m` 局部可解前提尤其悬空

正文第 4 节给出两个裸 SHA-256，但没有说明它们分别对应
`PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json` 与
`PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json`，也没有 supplement 版本、
公开归档 URL/DOI、脚本哈希、Python 版本或复现命令。第三方拿到 PDF 后
无法取得 512 个单元，更不能核验每个 YES 的精确平方见证和每个 NO 的有限
穷尽/估值证书。因此 Theorem 4 在当前 PDF 中仍依赖不可定位的外部对象。

同样，正文第 1 节与 Proposition 6 的证明都用到“`C_H` 处处局部可解”。
真正的数据在 `STUDENT_ELLIPTIC_ROUND_03_certificate.json` 的
`same_m_local_certificates`，但 TeX 只写 “a separate same-m local
certificate”，没有文件名、哈希、坏素数表或好素数 Weil--Hensel 论证。
这不仅影响“relevant fibre product everywhere locally soluble”的叙述，也
影响 `[C_H] in Sel^2(E/Q)` 以及“其投影 35 位于 lifting pairing 的 radical”
这一纠错论证的明示前提。

最低修复：建立一个随稿 supplement manifest，列出上述三个 JSON、生成
脚本、测试及其 SHA-256 和语义版本；正文给精确文件名、归档定位和一条完整
复现命令。另把 same-`m` 证书的有限坏位清单及好素数桥至少摘要成一个引理。
仅给 64 位哈希不能替代可取得的证书。

### B2. Campbell 输入与论文语境没有文献链，也没有自足定义

正文把 `H(m)=g_m(8)`、八个已知平方和第九候选视为既有事实，却没有定义
`g_m(x)` 的四个系数，也没有引用 Campbell。独立检查表明该等式确实来自
Campbell Theorem 2.5：把文中 `g_3,g_2,g_1,g_0` 代入
`g_m(x)=g_3x^3+g_2x^2+g_1x+g_0` 并令 `x=8`，恰得到本文的 `H`。应引用
[Campbell, JIS 6 (2003), Article 03.1.3](https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html)，
并在正文或补充材料列出这一恒等式的可复核推导。

当前参考文献也没有对“这个特定 Campbell Jacobian 的两个精确 Selmer 群
及 `z(H)` 未曾发表”做系统查重。Round05 报告诚实地承认仍需专门检索，
因此 PDF 第 7 节把结果称为 “safe minimum publication unit” 还不能视为
新颖性结论。投稿前必须完成精确方程、同构模型、Campbell 后续文献与曲线
数据库检索；若无新增上下文，单个大系数曲线的 Selmer 计算更稳妥的定位是
主论文的 arithmetic appendix，而非已确立的独立论文。

## Major

### M1. `p=2` 的同侧 pairing 应补直接参考文献

van Beek--Fisher 的引言 Equation (2) 是对素次数同源的一般上同调陈述，
所以用它确认“配对定义在
`Sel^(dual phi)(E'/Q) x Sel^(dual phi)(E'/Q)`，其核为完整 Selmer 像”
在逻辑上没有错；其正文计算对象却是 `3`-isogeny，并明确把 `p=2` 交给其他
文献。建议补引直接处理有理 `2`-挠/二同源高次下降的
[Fisher, *Higher descents on an elliptic curve with a rational 2-torsion point*, Math. Comp. 86 (2017), 2493--2518](https://doi.org/10.1090/mcom/3163)，
同时保留 [Fisher 2022](https://doi.org/10.1007/s40993-022-00376-z)
作为完整 binary-quartic `2`-Selmer 配对公式来源。

### M2. 冻结 Magma 输入方向正确，但还不是投稿级审计输入

`TwoDescent(EH : WithMaps := false)` 返回同一 `EH` 上的处处局部可解
`2`-coverings；`CasselsTatePairing(CH,covers[i])` 的两个输入因而属于同一
椭圆曲线，`FourDescent(CH)` 也正是测试 `[C_H]` 是否有局部可解
`4`-cover lift 的正确调用。官方 [Magma descent handbook](https://magma.maths.usyd.edu.au/magma/handbook/text/1570)
支持这三个语义。脚本不再出现跨侧整数输入，这一点通过测试。

但脚本尚未执行，也没有 transcript；而且运行前未显式断言：

- `H` 非奇异且 `IsLocallySoluble` 为真；
- `EH` 与 TeX 中数值模型 `E` 的显式同构/不变量一致；
- `TwoDescent` 返回模型的数量、哈希和到 `EH` 的关联；
- class-group/unit 计算是否 unconditional，以及随机种子/软件二进制来源。

因此当前脚本只能称为 frozen candidate input。将来即使输出
`CH_FOUR_DESCENT_COVER_COUNT 0`，也应由 fail-closed parser 同时验证
begin/end 标记、版本、模型、local-solubility 断言和完整 stdout/stderr 后
再升级为数学结论。

### M3. branch-independence 证书的结论边界应再收窄一句

对 `p=59` 与 `p=71699`，同一 `(U,V)=(0,1)` 的两个 Hensel 分支分别给
Hilbert symbols `[-1,+1]`；其余已列位的选择均为 `+1`，未列好位对整数
单位不给贡献。因此允许各局部点独立选择时，旧 bare expression 的总乘积
确实可为 `-1` 或 `+1`。这严格证明了**该具体表达式不是 branch-independent
的 pairing 公式**，且报告/TeX 均正确声明这些数不是 CT 值。

不过，“它证明缺少的对象恰是 cochain or denominator data”仍是对失败原因
的合理诊断，不是由四行同余本身唯一推出的定理。建议改为“therefore the
bare expression is insufficient; a valid full-cover construction includes the
additional cochain/denominator data described in the cited formula”。不要暗示
已经证明任何可能的修正公式都必须采用这一特定切线的某个唯一归一化。

### M4. `z(H)` 的上同调含义应把约定写得更完整

整数恒等式均正确：

- `D=59*71699*339106321`，且二次预解因子的判别式为 `12288^2 D`；
- `z_Q=35*16257024^2`；
- 约化 `K` 分量的范数为 `35*15915620907648^2`，总 étale 范数为平方；
- `64` 缩放和平移得到正文的 `E`，有理因子投影为 `[35]`。

正文也已明确说 `[35]` 只是一个 projection，绝不等同于偶四次 `C_35` 或
完整 torsor；这一关键边界正确。为使命题自足，仍建议补一句：固定
binary-quartic 等价/缩放约定后，式 (1) 如何表示
`H^1(Q,E[2])` 中的类，以及换模型时 `z(g)` 的平方类为什么不变。另应显式
记录 `disc(H) != 0`，从而 `C_H` 确为 genus-one `2`-cover。

## Minor

1. rank 公式方向正确，但正文可以直接写出两个商的对应关系：
   `E(Q)/dual_phi E'(Q)` 注入 E-side 的
   `Sel^(dual_phi)(E'/Q)`，`E'(Q)/phi E(Q)` 注入 E'-side 的
   `Sel^phi(E/Q)`。现有等式中两个 order-2 kernel 给出分母 `4`，所以
   `3+2-2=3`，没有反置。
2. “all $56$ cells ... split into 24 YES and 32 NO”是对旧未决单元的增量
   统计，不是 512 格总统计；正文随后给出 `384 YES + 128 NO`，已足以消除
   歧义，建议只加 “formerly unresolved” 的强调。
3. 冻结 Magma 注释称 `FourDescent(CH)=[]` 为 obstruction 是正确的；
   非空只表示存在 Selmer `4`-lift，不自动给有理点。报告与 TeX 都守住了
   这一单向边界。
4. PDF 为五页，重新编译后无 undefined citation/reference、overfull、
   underfull 或 LaTeX warning；逐页渲染未见裁切、重叠或不可读表格。

## 独立复核记录与可接受结论

直接分解得到

```text
B              = 2^18 * 3^12 * 5^2 * 7^5,
A^2 - 4B       = 3^4 * 59 * 71699 * 339106321,
B'             = 3^4 * 59 * 71699 * 339106321,
A'^2 - 4B'     = 2^22 * 3^12 * 5^2 * 7^5.
```

故每侧恰有 `32` 个带符号平方自由支撑类，所需位的并集恰为
`{infinity,2,3,5,7,59,71699,339106321}`。支撑引理排除所有其他 squareclass
支撑；对不除 `2b(a^2-4b)` 的素数，光滑射影 genus-one 约化、Hasse 界与
Hensel 提升覆盖所有未列位。512 格证书于是给出精确 survivor：

```text
Sel^(dual phi)(E'/Q) = <3,5,7>,               dim 3,
Sel^phi(E/Q)         = <4230241,339106321>,   dim 2.
```

联合运行

```text
python -m unittest -v PAPER_ELLIPTIC_ROUND_05_test.py \
  PAPER_ELLIPTIC_ROUND_04_test.py \
  PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_NEXT_test.py
```

结果 **33/33, OK**。Round05 证书 SHA-256 也与报告所列
`af4f02e4e13f48f8e1ac5de22a0404da36c1a8dac7ec26e6144945f66e50968e`
一致。`latexmk -pdf -interaction=nonstopmode -halt-on-error
PAPER_ELLIPTIC_TEX.tex` 成功生成五页 PDF。

因此现在可以接受的数学结论是：两个精确二同源 Selmer 群、
`rank E(Q) <= 3`、完整 `Q x K` 数值坐标及其 `[35]` 投影，以及旧跨侧
pairing 公式无定义且其 bare local expression 不具 branch-independence。
不能接受的升级仍包括：完整 `2`-Selmer 维数、任何 CT pairing 值、rank
等号、`C_H(Q)` 空或非空，以及该有限结果已经满足独立投稿的新颖性/复现性。

最小下一步应先关闭 B1--B2（可定位 supplement、same-`m` 引理、Campbell
公式与精确方程查重），再运行并严格解析冻结 full-descent 输入；在此之前
不应继续构造新的跨侧局部符号。
