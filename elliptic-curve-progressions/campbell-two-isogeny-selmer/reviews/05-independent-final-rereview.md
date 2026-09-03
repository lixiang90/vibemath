# 丙线第六轮最终修订窄复核（乙审）

日期：2026-09-03  
审稿范围：`PAPER_ELLIPTIC_FINAL_REPAIR_06.md`、clean Round04 v2、两级
manifest、release/submission 材料、当前 TeX/PDF。未修改任何丙线文件。

## 决定

**ACCEPT（仅余发布时的人工作业，不再是数学或复现阻断）。** 前次报告列出的
major 问题均已解除。稿件仍是本地草稿，作者、归档 DOI/URL、目标期刊当天政策复核
须由人类作者完成；这些是明确标出的投稿闸门，不影响当前有限定理及补充材料验收。

## 逐项核验

1. **clean Round04 v2。** 顶层 schema 为
   `paper-elliptic-campbell-round-04-clean-v2`。旧
   `d35_cassels_tate_setup`、`pairing_bits_to_compute`、
   `decisive_outcome` 不再是证书数据字段，错误的两个 opposite-side pairing 数值也不在
   clean 正文中。三个旧名称仅出现在 `supersession.excluded_fields`，其语义是禁用清单；
   这不是旧断言残留。独立测试还在序列化时排除 `supersession` 后逐一断言禁用字段缺席。
2. **20 项 supplement 闭包。** manifest 精确列出 20 项。逐个检查所有 Python
   `import` 后，本地依赖仅为该清单中的 NEXT、Moody--Juyal、Campbell、Round04/05/06
   与 manifest 模块；标准库和已声明的 SymPy 是唯一外部运行依赖。隔离测试只复制这
   20 项，重建四级证书和 manifest，并成功运行 39 个数学/语义测试。
3. **root 隔离与真实 45 测试。** root 测试只复制两级 manifest 声明的文件到空目录，
   依次运行六个生成器，再执行 release manifest 中同一条七模块命令。环境标记只阻止
   隔离测试递归，不删 test method；子进程明确要求 `Ran 45 tests` 与 `OK`。本次根目录
   独立复跑结果为 `Ran 45 tests in 25.993s — OK`。
4. **support lemma。** 修订后的赋值论证正确：若坏素数不整除方自由代表 `d`，在原
   covering 方程中，`V` 为单位时 `(b/d)V^4` 是唯一最小赋值 `-1` 的项；故 `V` 必须被
   `p` 整除。随后原始性迫使 `U` 为单位，三项赋值分别为 `1, >=2, >=3`，右端赋值
   恰为 `1`，不可能是平方。论证未偷用 `N` 预先整性。
5. **期刊排除与 claim boundary。** shortlist 已明确排除 INTEGERS 与 JIS，首选
   Research in Number Theory、JNT 备选，并要求投稿日重查政策。摘要、正文和 Magma
   输入均一致声明：没有完整 2-Selmer、Cassels--Tate、rank equality 或第九点结论；
   未执行的 Magma 输入为 `mathematical_evidence_eligible=false`。
6. **v0.6.1 哈希与 PDF。** root manifest 的 supplement/TeX/PDF 哈希分别为
   `583ec02b...228fd`、`7480a24b...7fae`、`7a2fb6dd...a6db`，大小记录与磁盘一致；
   root manifest 自身为 `bb5c0679...7e58`（见修订报告）。从当前 TeX 在独立目录重编
   得到 7 页、249658 bytes；由于 PDF 元数据，重编 SHA 与封存快照不同，恰与 manifest
   的非逐比特重现政策一致。第二遍编译无未定义引用、overfull 或 underfull；逐页渲染
   未见裁切、重叠、空白异常或不可读表格。

## 剩余 minor / 人工闸门

- 发布前填入作者、单位、通讯信息和公开归档 DOI/URL，并据目标期刊最新规则定稿
  AI disclosure；当前占位和 `LOCAL_DRAFT_NOT_AUTHORIZED_FOR_SUBMISSION` 状态正确。
- `supersession.excluded_fields` 会使纯字符串搜索命中旧字段名；后续审计应检查 JSON
  结构或排除该否定元数据，避免误报。无需改证书。

结论：前次 major 全部解除；当前有限 two-isogeny 定理、rank 上界、same-parameter
局部可解性及其可复现边界可以按现有 claim boundary 接受。
