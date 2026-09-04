# `seven-consecutive-squareclasses` 最终数学材料清单

目标根目录：`vibemath/square-progressions/seven-consecutive-squareclasses/`。下表是最小权威闭包；“数学证据”仅表示该文件可直接支撑冻结稿中的数学断言，不表示脱离论文、代码和测试后可以单独充当证明。

## paper (source + final PDF)

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `PAPER_SQUARE_TEX/main.tex` | `paper/main.tex` | 当前论文源；自足陈述 Kummer 归约、`651→343→284→98→54→35→23→15→10→7→4→2` 及截至 mask 85 的全部整数点门 | 是（主要证明文本） |
| `PAPER_SQUARE_TEX/references.bib` | `paper/references.bib` | 论文引用的可定位书目；与 prior-art 核查配套 | 否（书目元数据） |
| `PAPER_SQUARE_TEX/main.pdf` | `paper/main.pdf` | 唯一保留的最终渲染 PDF；便于 GitHub 直接阅读 | 是（`main.tex` 的冻结渲染，不是独立证据） |

## code

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `STUDENT_SQUARE_ROUND_02_patterns.py` | `code/STUDENT_SQUARE_ROUND_02_patterns.py` | 从受限增长词枚举 651 个三/四块模式，并生成反射轨道、字符商和 284 个幸存模式 | 是（精确有限枚举生成器） |
| `STUDENT_SQUARE_ROUND_03_isomorphisms.py` | `code/STUDENT_SQUARE_ROUND_03_isomorphisms.py` | 计算 63 个字符商、仿射/PGL2 同构类及逐 occurrence 的同一参数兼容数据 | 是（精确符号计算） |
| `STUDENT_SQUARE_ROUND_04_pipeline.py` | `code/STUDENT_SQUARE_ROUND_04_pipeline.py` | 生成最终 SAFE/门脚本所依赖的 284 模式与 occurrence lookup；只采信真实几何/映射字段 | 有条件：真实几何与 lookup 是；模拟解析路径不是 |
| `PAPER_SQUARE_SAFE_inventory.py` | `code/PAPER_SQUARE_SAFE_inventory.py` | 重算 `651→343→284`，并用四连续因子恒等式得到 `284→98` | 是（精确有限枚举与恒等式检查） |
| `PAPER_SQUARE_MASK77_analysis.py` | `code/PAPER_SQUARE_MASK77_analysis.py` | mask 77/89：18 个平方自由分支、15 个有限模阻碍及整数点门，推出 `98→54` | 是（穷尽分支与严格有限证书生成器） |
| `PAPER_SQUARE_NEXT_GATE.py` | `code/PAPER_SQUARE_NEXT_GATE.py` | mask 102 的整数点门及受影响模式重算，推出 `54→35` | 是（精确门分析） |
| `PAPER_SQUARE_MASK108.py` | `code/PAPER_SQUARE_MASK108.py` | mask 108、`d∈{1,3}` 的整数点门及受影响模式重算，推出 `35→23` | 是（精确门分析） |

## certificates

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `STUDENT_SQUARE_ROUND_02_certificate.json` | `certificates/STUDENT_SQUARE_ROUND_02_certificate.json` | 651、343、284、63 个字符支持及零项分离的机器可审计证书 | 是 |
| `STUDENT_SQUARE_ROUND_03_CERTIFICATE.json` | `certificates/STUDENT_SQUARE_ROUND_03_CERTIFICATE.json` | 63 商分层、16 个 PGL2 类及同一参数兼容映射证书 | 是 |
| `STUDENT_SQUARE_ROUND_04_CERTIFICATE.json` | `certificates/STUDENT_SQUARE_ROUND_04_CERTIFICATE.json` | 284 模式的 occurrence/变换冻结数据，是下游证书的权威输入 | 有条件：真实几何与 occurrence 字段是；任何 simulation 字段不是 |
| `PAPER_SQUARE_SAFE_CERTIFICATE.json` | `certificates/PAPER_SQUARE_SAFE_CERTIFICATE.json` | SAFE 分类与 `284→98` 的端到端证书 | 是 |
| `PAPER_SQUARE_MASK77_CERTIFICATE.json` | `certificates/PAPER_SQUARE_MASK77_CERTIFICATE.json` | mask 77/89 的完整分支、模阻碍、整数解和被排除 44 模式 | 是 |
| `PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json` | `certificates/PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json` | mask 102 的整数点清单、19 个新增排除及 35 个剩余模式 | 是 |
| `PAPER_SQUARE_MASK108_CERTIFICATE.json` | `certificates/PAPER_SQUARE_MASK108_CERTIFICATE.json` | mask 108 的整数点清单、12 个新增排除及最终 23 个模式 | 是 |

## mathematical-notes

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `PAPER_SQUARE_SAFE_CLASSIFICATION.md` | `mathematical-notes/PAPER_SQUARE_SAFE_CLASSIFICATION.md` | 自足记录公共有理缩放、非零项、Kummer 核、651/343/284/98 计数与中心商 | 是 |
| `PAPER_SQUARE_MASK77_REPORT.md` | `mathematical-notes/PAPER_SQUARE_MASK77_REPORT.md` | 第一整数点门的完整人读证明：mask 77/89，`98→54` | 是 |
| `PAPER_SQUARE_NEXT_GATE_REPORT.md` | `mathematical-notes/PAPER_SQUARE_NEXT_GATE_REPORT.md` | 第二整数点门的人读证明：mask 102，`54→35` | 是 |
| `PAPER_SQUARE_MASK108_REPORT.md` | `mathematical-notes/PAPER_SQUARE_MASK108_REPORT.md` | 第三整数点门的人读证明：mask 108，`35→23` | 是 |
| `PAPER_SQUARE_ROUND_05_REPORT.md` | `mathematical-notes/PAPER_SQUARE_ROUND_05_REPORT.md` | 汇总主定理、Kummer kernel 修补、严格模式链及“23 仍未决”的 claim boundary | 是（汇总；以各门报告/证书为底层依据） |
| `PAPER_SQUARE_PRIOR_ART.md` | `mathematical-notes/PAPER_SQUARE_PRIOR_ART.md` | 对精确方程、S-integral、simultaneous Pell、Cremona/LMFDB 与低次数域平方列的可定位查重记录 | 否（新颖性与背景证据，不证明主定理） |

## reviews

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `PAPER_SQUARE_CROSS_REVIEW_ELLIPTIC_02.md` | `reviews/PAPER_SQUARE_CROSS_REVIEW_ELLIPTIC_02.md` | 丙线对 SAFE 分类、计数与中心商的早期独立攻击性审阅 | 否（独立质量保证） |
| `PAPER_SQUARE_CROSS_REVIEW_CUBE_03.md` | `reviews/PAPER_SQUARE_CROSS_REVIEW_CUBE_03.md` | 乙线对 mask 77/89、有限模证书及 44 模式排除的独立审阅 | 否（独立质量保证） |
| `PAPER_SQUARE_MANUSCRIPT_REVIEW_CUBE_04.md` | `reviews/PAPER_SQUARE_MANUSCRIPT_REVIEW_CUBE_04.md` | 乙线对汇总定理、Kummer kernel、引用和 mask 108 前稿的独立稿件审阅 | 否（独立质量保证） |
| `PAPER_SQUARE_MANUSCRIPT_REVIEW_ELLIPTIC_05.md` | `reviews/PAPER_SQUARE_MANUSCRIPT_REVIEW_ELLIPTIC_05.md` | 丙线对修订稿及 `651→23` 证据链的独立稿件审阅 | 否（独立质量保证） |
| `PAPER_SQUARE_FINAL_REVIEW_ELLIPTIC_06.md` | `reviews/PAPER_SQUARE_FINAL_REVIEW_ELLIPTIC_06.md` | 冻结稿的独立终审结论及剩余 minor 清单 | 否（独立质量保证） |
| `PAPER_SQUARE_FINAL_REREVIEW_ELLIPTIC_06.md` | `reviews/PAPER_SQUARE_FINAL_REREVIEW_ELLIPTIC_06.md` | minor 修复后的窄复核，确认主张边界与终稿一致 | 否（独立质量保证） |

## reproducibility

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `PAPER_SQUARE_TEX/README.md` | `reproducibility/BUILD.md` | 论文的本地 LaTeX 构建命令与工具说明 | 否（构建说明） |
| `PAPER_SQUARE_SUBMISSION/data_dictionary.md` | `reproducibility/DATA_DICTIONARY.md` | 逐 JSON 字段说明类型、单位、claim eligibility 和 supersession；从投稿目录抽取但内容属于数学数据语义 | 否（解释层） |
| `PAPER_SQUARE_SUPPLEMENT_MANIFEST.json` | `reproducibility/SUPPLEMENT_MANIFEST.json` | Round11 数学 supplement v0.10.1 的 38 个文件哈希、角色和 claim boundary；已收入 Round11 冻结源提交 | 否（完整性锚点） |
| `PAPER_SQUARE_SUPPLEMENT_MANIFEST.py` | `reproducibility/SUPPLEMENT_MANIFEST.py` | 重生成/校验 supplement manifest 的实现 | 否（完整性工具） |
| `PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py` | `reproducibility/tests/PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py` | 对 supplement 闭包和篡改拒绝的回归测试 | 否（验证层） |
| `STUDENT_SQUARE_ROUND_02_test_patterns.py` | `reproducibility/tests/STUDENT_SQUARE_ROUND_02_test_patterns.py` | 651/343/284 与字符商生成器回归测试 | 否（验证证据文件，不单独证明定理） |
| `STUDENT_SQUARE_ROUND_03_test.py` | `reproducibility/tests/STUDENT_SQUARE_ROUND_03_test.py` | 同构类、变换和兼容映射回归测试 | 否（验证层） |
| `STUDENT_SQUARE_ROUND_04_test.py` | `reproducibility/tests/STUDENT_SQUARE_ROUND_04_test.py` | occurrence lookup、解析器边界和证书重算测试；其中 synthetic fixture 测试仅测试软件路径 | 否（验证层） |
| `PAPER_SQUARE_SAFE_test.py` | `reproducibility/tests/PAPER_SQUARE_SAFE_test.py` | SAFE 计数、哈希和 `284→98` 端到端重算 | 否（验证层） |
| `PAPER_SQUARE_MASK77_test.py` | `reproducibility/tests/PAPER_SQUARE_MASK77_test.py` | mask 77/89 分支完备性、模证书和模式排除测试 | 否（验证层） |
| `PAPER_SQUARE_NEXT_GATE_test.py` | `reproducibility/tests/PAPER_SQUARE_NEXT_GATE_test.py` | mask 102 整数点门与 `54→35` 重算测试 | 否（验证层） |
| `PAPER_SQUARE_MASK108_test.py` | `reproducibility/tests/PAPER_SQUARE_MASK108_test.py` | mask 108 整数点门与 `35→23` 重算测试 | 否（验证层） |

## Round07--Round11 严格增量

下列文件把上述初始冻结点从 23 个必要模式继续推进到 2 个；它们是当前权威闭包
的一部分，而不是有界搜索记录。

| 轮次 | 生成器 / 证书 / 测试 | 人读报告与审稿 | 严格增量 |
|---|---|---|---|
| Round07 | `code/PAPER_SQUARE_MASK99.py`; `certificates/PAPER_SQUARE_MASK99_CERTIFICATE.json`; `reproducibility/tests/PAPER_SQUARE_MASK99_test.py` | `mathematical-notes/PAPER_SQUARE_MASK99_REPORT.md` | mask 99：`23→15` |
| Round08 | `code/PAPER_SQUARE_MASK51.py`; `certificates/PAPER_SQUARE_MASK51_CERTIFICATE.json`; `reproducibility/tests/PAPER_SQUARE_MASK51_test.py` | `mathematical-notes/PAPER_SQUARE_MASK51_REPORT.md`; `reviews/PAPER_SQUARE_ROUND_08_REVIEW_ELLIPTIC.md` | mask 51 与 mask 102 整数平移：`15→10` |
| Round09 | `code/PAPER_SQUARE_MASK90.py`; `certificates/PAPER_SQUARE_MASK90_CERTIFICATE.json`; `reproducibility/tests/PAPER_SQUARE_MASK90_test.py` | `mathematical-notes/PAPER_SQUARE_MASK90_ROUND_09_REPORT.md`; `reviews/PAPER_SQUARE_ROUND_09_REVIEW_CUBE.md` | mask 90：`10→7` |
| Round10 | `code/PAPER_SQUARE_MASK54.py`; `certificates/PAPER_SQUARE_MASK54_CERTIFICATE.json`; `reproducibility/tests/PAPER_SQUARE_MASK54_test.py` | `mathematical-notes/PAPER_SQUARE_MASK54_ROUND_10_REPORT.md`; `reviews/ROUND_10_CROSS_REVIEW.md` | mask 54：`7→4`；终审 PASS |
| Round11 | `code/PAPER_SQUARE_MASK85.py`; `certificates/PAPER_SQUARE_MASK85_CERTIFICATE.json`; `reproducibility/tests/PAPER_SQUARE_MASK85_test.py` | `mathematical-notes/PAPER_SQUARE_MASK85_ROUND_11_REPORT.md`; `reviews/ROUND_11_CROSS_REVIEW.md` | mask 85：完整整数点集且全部退化，`4→2`；交叉审稿 FINAL PASS |
| Round12 | 数学代码、证书和 96-test 数量不变 | `mathematical-notes/PAPER_SQUARE_ROUND_12_NOVELTY_AUDIT.md`; `mathematical-notes/PAPER_SQUARE_PRIOR_ART.md`; `reviews/ROUND_12_NOVELTY_CROSS_REVIEW.md` | 最近先例、等价边界与检索缺口整合；novelty cross-review FINAL PASS，不声称 priority |

Round11 squareclasses 组在冻结源提交
`20bb94753801907b46d41db611ab18c4cd9f9a10` 的 clean clone 中 96/96 通过。剩余两个模式
`12:0012202`、`134:0012131` 只具必要性；可实现性与 `R_2(7)` 均未决。
supplement v0.10.1 的当前本地候选 SHA-256 为
`deb3eade7c9f25c6e0c8da019f21f7a0943bdd50fcf263f7add6ed8b3ed0309e`；
这是已同步并随源提交冷复现的 nested manifest。全项目 Round11 证据见
`reproduction/INTERNAL_COLD_REPRODUCTION_20bb94753801.json`：六组 266 项通过，
三份 PDF 为 11/9/11，文本哈希逐项一致。

Round12 当前工作树的 squareclasses 组仍为 96/96，论文增至 12 页；Round12
freeze/cold 尚未完成。MathSciNet 订阅结果、Tho 2024 权威全文及相关前向引用链
仍是高谨慎残余风险，但原始来源比较和 FINAL PASS 审稿足以支撑当前受限的
“所检资料未找到等价表述”，不支撑 `first/new`。

唯一署名为 `Codex (GPT-5.6-sol)`。项目只要求达到
submission-ready 水准，不实际投稿；不得虚构其他作者、单位、联系方式、ORCID、
资助、利益冲突、期刊、DOI 或投稿事件。

## 明确不纳入

| 源路径 | 目标相对路径 | 理由 | 数学证据 |
|---|---|---|---|
| `PAPER_SQUARE_TEX/{main.aux,main.bbl,main.blg,main.log,main.fls,main.fdb_latexmk,main.out,build.log,tmp/**}` | — | LaTeX 中间物、日志和临时目录 | 否 |
| `PAPER_SQUARE_ARCHIVE_CANDIDATE.zip`、`PAPER_SQUARE_ARCHIVE_CANDIDATE*.py` | — | 外部投稿归档及其机械包装测试；GitHub 数学树直接由本清单构建 | 否 |
| 除 `PAPER_SQUARE_TEX/main.pdf` 外的全部 `PAPER_SQUARE*.pdf` 副本 | — | 旧版或重复 PDF，避免多个权威版本 | 否 |
| `STUDENT_SQUARE_ROUND_04_SIMULATED_*`、`STUDENT_SQUARE_ROUND_05_SYNTHETIC_*` | — | synthetic/模拟结果，不得进入数学证据树 | 否 |
| `STUDENT_SQUARE_ROUND_05_*` | — | 以模拟输出检验解析/可信 manifest 的旧管线；不属于冻结主定理链 | 否 |
| `PAPER_SQUARE_rank_gate.m`、`STUDENT_SQUARE_ROUND_03_selmer.m`、`STUDENT_SQUARE_ROUND_05_rank_points_exporter.m` | — | 未执行/未由可信 transcript 封闭的 CAS 候选，不可作为证明 | 否 |
| `PAPER_SQUARE_SUBMISSION/**`（仅 `data_dictionary.md` 例外）、`PAPER_SQUARE_SUBMISSION_MANIFEST*` | — | 作者、期刊、归档和政策层；纯投稿占位或机械闭包，不属于 GitHub 数学材料 | 否 |
| `PAPER_SQUARE_RELEASE_*`、`PAPER_SQUARE_EXTERNAL_READINESS_*`、`PAPER_SQUARE_FINAL_REPAIR_06.md`、`PAPER_SQUARE_ROUND_06_REPORT.md` | — | 发布/期刊政策与包装修订记录；不改变数学 | 否 |
| `PAPER_SQUARE_FEASIBILITY.md`、`PAPER_SQUARE_reconstruct.py`、`PAPER_SQUARE_CERTIFICATE.json`、`PAPER_SQUARE_test.py` | — | 已转向的早期曲线可行性包，不是七项平方类最终定理链 | 否 |
| `PAPER_SQUARE_SAFE_REPORT.md`、`PAPER_SQUARE_ROUND_04_REPORT.md`、`STUDENT_SQUARE_ROUND_0*_REPORT.md` | — | 已被最终分类、三个门报告和 Round 05 汇总报告取代的过程报告 | 否 |
| `GROUP_MEETING_*`、`RELATED_RESEARCH_DIRECTIONS.md`、毕业备选题与跨线审稿文件 | — | 研究管理、选题或其他课题材料，不属于本仓库子项目的最终证据闭包 | 否 |
