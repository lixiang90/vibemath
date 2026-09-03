# 丙线第六轮独立终审（乙）

日期：2026-09-03  
决定：**MAJOR REVISION（数学主定理可接受；当前投稿包不可按所列首选期刊提交）**。

本报告只审阅丙线文件，没有修改它们。独立核验脚本为
`PAPER_ELLIPTIC_FINAL_REVIEW_CUBE_06_audit.py`。

## 1. 已确认的数学结论

### 1.1 Campbell 重建与退化边界：通过

独立展开验证了

- `g_m(j)=q_j(m)^2`，`j=0,...,6`；
- `g_m(7)=D(m)`，`g_m(8)=H(m)`，所以八项与第九候选的索引没有错位；
- `g_3=-18816(m^2-72256)(m^2-36m-29920)`；两个二次因子均无有理根；
- 参数变换分母 `m^2-72256` 无有理零点；Campbell 的 `t=5/2` 例外值对应的二次方程也无有理解；
- `disc_x(g_m)/(-65028096)` 是次数 16 的本原多项式并且模 53 不可约，故无有理奇异特化；
- `D,H` 都可分且 `Res(D,H) != 0`；`m=infinity` 因首项
  `Y^2=-264815 M^4` 没有有理点。

Campbell 原文页面和 PDF 确认了作者、题名、JIS 6 (2003), Article
03.1.3，以及 Theorem 2.5 中的 `D,g_3,g_2,g_1,g_0` 和横坐标
`0,...,7`：
[Campbell 原文](https://cs.uwaterloo.ca/journals/JIS/VOL6/Campbell/campbell4.html)。
因此正文把 `H=g_m(8)`标为本稿直接展开所得，而没有错误归于 Campbell。

### 1.2 same-`m` 处处局部可解：通过

独立重算得到分支坏素数恰为

```text
{2,3,5,7,17,19,31,59,8599,71699,898543,23037169,
 339106321,1153266911}.
```

证书覆盖实位、`Q_2`、全部奇素数 `<101` 以及所有奇分支坏素数。每个奇素
见证的两个平方根都非零模 `p`，故关于平方根变量的导数为单位，Hensel
提升有效。对其余素数，两个可分四次式分支互不相交；双二次纤维积是光滑
几何连通 genus 5 曲线。`p>=101` 时
`p+1-10 sqrt(p)>0`，所以 Weil 界给出有限域点并可提升。局部支撑是完整的，
但只证明处处局部非空，不证明有理点。

### 1.3 两个二同源 Selmer 群与秩：通过

独立检查：

```text
E :  y^2=X^3-591895071 X^2+58536289153843200 X,
E': y^2=X^3+1183790142 X^2+116194618458722241 X.
```

`a'^2-4b'=16b`；两侧坏素数并集（连同 2）恰为
`{2,3,5,7,59,71699,339106321}`。一般覆盖四次式的判别式为
`16 b (a^2-4b)^2`，因此 support lemma 与 good-prime lemma 确实把问题
化为各 32 个带符号平方类及 512 个局部单元。冻结证书给出的幸存集合是

```text
{1,3,5,7,15,21,35,105} = <3,5,7>,
{1,4230241,339106321,1434501462453361}
  = <4230241,339106321>.
```

两者在平方类乘法下分别是维数 3 和 2 的 `F_2` 子群。两条曲线的有理二挠
核各为阶 2；标准二同源秩公式因此给出 `rank E(Q)<=3`。公式及方向与
van Beek--Fisher 文中一般 `p`-同源的准确序列一致；该文还明确指出
`p=2` 由 Fisher 2017 处理：
[van Beek--Fisher 预印本](https://www.dpmms.cam.ac.uk/~taf1000/papers/ctp-3isog.pdf)、
[Fisher 2017](https://arxiv.org/abs/1509.03234)。

### 1.4 `Q x K`、`[35]` 与 claim boundary：通过

独立精确算术验证：

- 三次 resolvent 有有理根 `269378023424`；二次因子判别式为
  `12288^2*1434501462453361`；
- `1434501462453361=59*71699*339106321`；
- `z_Q=35*16257024^2`；约化后的 `z_K` 的范数为
  `35*15915620907648^2`；全范数为所列整数的平方；
- `-3 phi_0=64^2*(-197298357)`，所以有理二挠投影确为 `[35]`。

Fisher 2022 的原始论文确实给出正文采用的二元四次式 `I,J`、Jacobian 与
三次代数框架：[Fisher 2022](https://doi.org/10.1007/s40993-022-00376-z)。
正文正确限制为“完整 `H^1(Q,E[2])` 类的一个有理分量”，没有把 `C_H`
误认为 `C_35`，也没有提升为完整 2-Selmer、Cassels--Tate、秩等号或第九点
结论。

## 2. 阻断/重大问题

### B1. 当前首选期刊 INTEGERS 与已披露工作流不相容（投稿阻断）

投稿包把 **INTEGERS** 列为首选，但其当前作者须知明确写明：不考虑使用
AI 产生数学、计算机代码、书目信息或其他内容的文章。投稿包自己的
`ai_disclosure.md` 则如实列出 AI 用于符号代数脚本、测试设计、文献查询和
文字编辑。两者不能同时满足：
[INTEGERS 作者须知](https://math.colgate.edu/~integers/submit.html)。

必须从 shortlist 删除 INTEGERS，不能靠改写披露规避。Journal of Integer
Sequences 也要求文章英文不得由 LLM 撰写，且任何证明建议必须在正文中明确
归功；现有通用披露不足以满足该规则，并且本稿与“整数序列”范围的契合也弱：
[JIS 投稿须知](https://cs.uwaterloo.ca/journals/JIS/)。因此应先核验 Research
in Number Theory 或其他明确允许所披露 AI 工作流的期刊政策。

### B2. 两级 manifest 没有封存报告宣称的完整 45-test 验证链（发布重大）

实际联合命令复跑为 `Ran 45 tests ... OK`，但 supplement 的 17 个文件没有
包含 `PAPER_ELLIPTIC_NEXT_test.py` 和 `PAPER_ELLIPTIC_ROUND_05_test.py`；
supplement/root manifest 的 `commands.tests` 也省略这两项，实际只运行 29
项。尤其 Round05 是撤回错误 pairing 公式的语义防线，却没有进入归档测试
闭包。当前隔离重建能逐字节重建证书，不能复现报告所称的全部 45 项审计。

修复要求：把这两个测试加入 supplement 文件表和隔离目录，`reproduction_commands`
与 root `commands.tests` 改为实际 45 项命令；隔离测试应在临时目录真正运行
这 45 项，而不仅重生成 JSON。随后重生成两级 manifest、TeX 中哈希和 PDF。

### B3. Round04 中已知错误的 pairing 提案仍整体标为 evidence eligible

`PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json` 仍含错误的跨侧
`<35,4230241>_CT`/`<35,339106321>_CT` 及错误的 `decisive_outcome`；虽然
`pairing_status=UNKNOWN_FAIL_CLOSED`，Round05 和正文已明确撤回，但 supplement
仍把整个 Round04 证书标成 `mathematical_evidence_eligible=true`，且没有字段级
supersession 规则。机器消费者只读 manifest 时仍可能把该错误方案当作可用
数学证据。

修复要求：生成只含已验证 `Q x K`/Selmer 内容的干净 Round04 证书，或在
manifest 中加入机器可判定的字段级 allowlist/denylist 与
`superseded_by=Round05`；不能只靠正文叙述纠正。Round05 的负面证书本身可以
eligible，因为它证明的是“旧公式不良定义”，但角色/claim 必须明确限制。

## 3. 次要问题

### M1. support lemma 的书面证明漏写一个赋值步骤

令 `p∤b` 且 `v_p(d)=1`。正文取 `U,V in Z_p` primitive 后直接约化
`dN^2=...`，但尚未说明 `N in Z_p`。结论正确，只需补一句：若 `V` 为单位，
原方程右侧中 `(b/d)V^4` 是唯一赋值 `-1` 的项，不可能为平方，故 `p|V`；
于是 `U` 为单位，原方程右侧赋值恰为 `1`，仍不可能为平方。这样无需预设
`N` 的整性，也更短。

### M2. prior-art 措辞安全，但不能升级

引号系数检索未发现特定两条曲线或幸存集合的匹配；Campbell 原文也没有本稿
的 `H`-Jacobian 二同源 Selmer 计算。正文与 `PAPER_ELLIPTIC_PRIOR_ART.md`
都明确说这是 not-found report 而非新颖性证明，此处合格。投稿前仍需要人工
MathSciNet/zbMATH、引用链及有理同构模型查重；目前不得写 “first/new”。

## 4. 工程复核

- 按报告给出的 7 文件命令独立复跑：**45/45 tests PASS**，8.186 秒。
- reviewer-owned 独立脚本：**PASS**；它不导入丙线模块，重算 Campbell
  恒等式、判别式/resultant、局部支撑、Selmer 群结构、秩公式、`Q x K`
  恒等式与两级文件哈希。
- 未执行 Magma 文件在 Round06 证书、supplement manifest 与测试中均为
  `mathematical_evidence_eligible=false`；无 transcript、无 binary hash，
  且 proved pipeline 不读取它。fail-closed 边界通过。
- 在临时目录用 TeX Live 2022 `latexmk` 重编译成功，7 页；最终日志无
  undefined citation/reference、overfull/underfull 或 LaTeX warning。重建
  PDF 与冻结 PDF 字节数相同但哈希因生成元数据不同，符合 root manifest 的
  `pdf_policy`。
- 逐页渲染目检 7 页：无裁切、重叠、越界或不可读表格；第 7 页留白较多但
  不是版面错误。

## 5. 最终意见

**数学核心没有 blocking：**有限二同源 Selmer 定理、`rank<=3`、`Q x K/[35]`
与 same-`m` 处处局部可解均可接受。**当前投稿快照仍需 major revision：**
先解决 B1--B3，再补 M1 并重冻 manifest/PDF。修复后可作一次窄范围复核；
不需要重新做 512 格数学计算，也不应运行未审计 Magma 来扩大主张。
