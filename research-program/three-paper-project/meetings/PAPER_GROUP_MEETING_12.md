# 第十二次论文组会：新颖性边界、投稿材料与冻结前逐项验收

日期：2026-09-04

主持：导师（root）

总状态：**ACTIVE / ROUND12 FREEZE AND COLD REPRODUCTION PENDING**。

Round12 没有改写三篇主定理，而是把可访问文献中的最近先例、等价关系和检索缺口
纳入正文、参考文献、投稿说明与独立交叉审稿。三份 novelty cross-review 均为
**PASS**（甲为 FINAL PASS）。权威根入口本轮实测
`96/33/42/14/8/73=266/266`，三份当前 PDF 直接读取为 `12/10/11` 页。
以上是当前工作树证据；Round12 源冻结与 clean-clone 冷复现仍待执行，不得沿用
Round11 冷复现来宣称 Round12 已冻结。

## 1. 三篇主定理与证明边界

| 论文线 | 当前主定理 | 完整证明状态 | 明确未证明 |
|---|---|---|---|
| 甲：seven consecutive squareclasses | 对整数 `t` 的七个连续非零项，affine squareclass rank 至多 2 时只剩 `0012202`、`0012131` 两个必要反转轨道 | PASS：Kummer 归约、15 个字符、各整数点门及 mask 85 的 `4->2` 完整链均在正文、报告、证书和测试中 | 不证明两模式可实现/不可实现，不决定 `R_2(7)`，不覆盖任意有理首项 |
| 乙：pure cubic five-term | 非常数五项有理 AP 在一次公共有理缩放及一个非平凡纯三次域下，非零立方命中数精确最大为 4 | PASS：上界的 25 颜色轨道与 60 个好素数阻碍完整，下界显式；另有 6 个无穷族模型和第 7 个严格存在性模型 | 不完整分类 31 个四命中模型；正秩商不推出第 7 个亏格 4 源曲线有无穷点 |
| 丙：Campbell target descent | index-8 九项条件目标 Jacobian 的两侧二同源 Selmer 群精确为 8 元与 4 元，故 `rank E(Q)<=3` | PASS：支撑引理、全部坏素数局部 iff、正见证、同源方向与核阶闭合 | 不给精确秩、full 2-Selmer、Cassels--Tate 配对、MW 基或第九点存在/不存在 |

## 2. Round12 新颖性与等价边界

- 甲线 `reviews/ROUND_12_NOVELTY_CROSS_REVIEW.md` 为 **FINAL PASS**。它核对
  BLT2010、Xarles2012、González-Jiménez--Xarles 2013/2014 与两篇 2026 工作；
  明确区分整数 `t` 与一般有理 AP、公共平方缩放与未缩放项、反转/平移/伸缩及
  单曲线同构和十五字符同参数兼容。检索无命中不构成优先权证明。
- 乙线对应审稿为 **PASS with HIGH-CAUTION boundary**。González-Jiménez--Xarles
  的二元 squareclass/type、公共缩放、反转和曲线方法被列为明确先例；本文差异是
  三次幂、纯三次域、三颜色及部分非零命中最大值，而不是“新方法”。
- 丙线对应审稿为 **PASS**。Campbell 2003 的 rank-2 参数曲线 `D` 控制第八条件，
  与本文第九条件四次曲线的目标 Jacobian 不同；Campbell thesis 已含二同源下降
  方法，所以贡献只写目标特定的精确 Selmer 集和秩上界。

三篇均使用 `we determine`、`we did not locate an equivalent statement in the
sources inspected` 一类受限措辞，不使用 `first/new` 证明优先权。等价变换、退化、
参数域和公共缩放边界均已显式写入。

## 3. 用户 Goal 逐项完成审计

| Goal 项 | 甲 | 乙 | 丙 | Round12 判定 |
|---|---|---|---|---|
| 至少一个闭合主定理 | PASS | PASS | PASS | 数学内容稳定 |
| 完整证明与退化/回提升边界 | PASS | PASS | PASS | 正文、数学笔记与证书互相支撑 |
| 新颖性核查及最近先例比较 | PASS，高谨慎 | PASS，高谨慎 | PASS，中等残余风险 | 三份 Round12 交叉审稿通过；不是绝对 priority certificate |
| 同构、平移、反转、幂缩放/参数边界 | PASS | PASS | PASS | 未把单项等价误写成同参数全局等价 |
| 代码、结构化证书、测试、数据字典 | PASS，96 | PASS，42 | PASS，73 | 根入口同时通过其余 `33/14/8`，总计 266/266 |
| 独立审稿与复现 | Round12 FINAL PASS | Round12 PASS | Round12 PASS | 交叉审稿完成；Round12 clean-clone 仍 PENDING |
| LaTeX/PDF | PASS，12 页 | PASS，10 页 | PASS，11 页 | 当前工作树可读；冻结重建仍 PENDING |
| 摘要、投稿信、期刊建议 | PASS | PASS | PASS | 均已存在；只作数学适配建议，不代表选择/联系/投稿 |
| 作者贡献、代码/数据声明 | PASS | PASS | PASS | 唯一署名 `Codex (GPT-5.6-sol)`；不虚构单位、邮箱、ORCID、资助 |
| 未证声明与 limitation | PASS | PASS | PASS | 开放问题和未运行 CAS 均 fail-closed |
| 实际投稿 | OUT OF SCOPE | OUT OF SCOPE | OUT OF SCOPE | 用户只要求 submission-ready 研究 |

## 4. 残余风险及是否阻断 submission-ready

1. **MathSciNet 订阅检索：不阻断当前内容级 submission-ready，但阻断任何绝对
   优先权措辞。** 证据是三份审稿已用原论文、作者/arXiv/期刊页、DOI 和可访问
   zbMATH/LMFDB 元数据完成定理级比较，同时正文和投稿材料明确披露订阅级引用图
   未覆盖。无命中从未被写成新颖性证明。
2. **Tho 2024 全文与 González-Jiménez--Xarles 前向引用链：不阻断当前受限主张，
   但属于甲/乙线的高谨慎 bibliographic risk。** 当前论文只陈述“所检资料未找到
   等价表述”，并把 2024 全文和完整前向链列入实际投稿前建议；若以后使用
   `first/new` 或扩张到一般数域/AP，这一缺口立即变为阻断。
3. **独立第二 CAS：不阻断丙线现有自足证明和 `rank<=3` 上界，但阻断“第二 CAS 已
   复现”及任何精确秩升级。** 现有结论由精确 Python/符号恒等式、73 项测试和跨线
   审稿支撑；Sage/PARI/GP/Magma 计划明确未运行，无 transcript 或输出被当作证据。
4. **Round12 freeze/cold：阻断本轮项目冻结完成。** 当前 266 项与 12/10/11 页只
   属工作树；必须在树稳定后生成 manifest、提交冻结点并对该提交 clean-clone 重跑，
   才能把总状态从 ACTIVE/PENDING 提升为 Round12 frozen/reproduced。

## 5. 冻结前结论与下一步

- 保留三篇当前主定理和严格未证边界，不因文献无命中增加 priority 语言。
- 冻结前同步根 manifest，并核对只含 Round12 文献整合、三份交叉审稿、组会和项目
  状态文档；清理构建缓存。
- 冻结后在无 hardlink 临时 clone 中运行权威根入口、重建三 PDF、比对文本哈希并
  扫描最终 LaTeX 日志；结果未产生前总状态保持 **ACTIVE/PENDING**。
- MathSciNet 订阅检索、Tho 2024 全文、GJX 前向引用链和第二 CAS 继续列为建议性
  外部风险闭合项。它们不授权实际投稿，也不允许虚构作者或行政信息。

本轮唯一作者口径为 `Codex (GPT-5.6-sol)`。没有选择或联系期刊，没有传送稿件，
没有生成 DOI，也没有虚构单位、邮箱、邮寄地址、ORCID、资助或利益冲突声明。
