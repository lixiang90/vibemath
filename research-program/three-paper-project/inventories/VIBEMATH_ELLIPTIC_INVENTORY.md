# vibemath Campbell two-isogeny Selmer：最终数学材料清单

目标根目录：`vibemath/elliptic-curve-progressions/campbell-two-isogeny-selmer/`

资格标记：`PROVED` 可支撑其自身 claim boundary 内的正面定理；`NEGATIVE`
只支撑错误路线的否定；`DOC` 是说明材料；`REVIEW` 是独立审查记录；
`INELIGIBLE` 不得作为数学证据。这里只列映射，不复制文件。

## paper

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `PAPER_ELLIPTIC_TEX.tex` | `paper/main.tex` | 当前数学正文：Campbell 重建、same-m、512 格、`Q x K/[35]`、CT 纠错、全局极小模型、Round09/10 局部门及 Round11 两侧精确二同源 Selmer 群与 `rank<=3` | `PROVED`，受正文边界约束 |
| `PAPER_ELLIPTIC_TEX.pdf` | `paper/main.pdf` | 当前 TeX 的最终参考渲染 | `DOC`；证明权威仍是源文件与证书 |

## code

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `STUDENT_ELLIPTIC_ROUND_03_local.py` | `code/same_m_local.py` | 生成同一参数的实位、2-adic、奇素数证书及有界搜索审计 | `PROVED` 仅限局部证书；有界搜索非证明 |
| `STUDENT_ELLIPTIC_ROUND_03_test.py` | `code/test_same_m_local.py` | 复核 common-m 六元组、非零根、四次不变量和边界 | `PROVED`；其中 Magma 静态检查不等于执行 |
| `PAPER_ELLIPTIC_MOODY_JUYAL.py` | `code/PAPER_ELLIPTIC_MOODY_JUYAL.py` | `NEXT` 测试的符号依赖 | `DOC/DEPENDENCY`，不单独支撑 Campbell 主定理 |
| `PAPER_ELLIPTIC_NEXT_analysis.py` | `code/PAPER_ELLIPTIC_NEXT_analysis.py` | 32+32 初始局部矩阵与符号基础 | `PROVED` 仅限脚本明确恒等式/正见证；旧未决不作结论 |
| `PAPER_ELLIPTIC_NEXT_test.py` | `code/PAPER_ELLIPTIC_NEXT_test.py` | `NEXT` 层回归测试 | `PROVED`，按测试断言范围 |
| `PAPER_ELLIPTIC_CAMPBELL_analysis.py` | `code/PAPER_ELLIPTIC_CAMPBELL_analysis.py` | 完成 64 行、512 格局部矩阵及 `[35]` 投影 | `PROVED`，局部矩阵不自动给全局点 |
| `PAPER_ELLIPTIC_CAMPBELL_test.py` | `code/PAPER_ELLIPTIC_CAMPBELL_test.py` | 逐格、幸存类、缩放与 torsor 投影回归 | `PROVED` |
| `PAPER_ELLIPTIC_ROUND_04_analysis.py` | `code/PAPER_ELLIPTIC_ROUND_04_analysis.py` | clean v2：支撑引理、好素数桥、两侧精确 Selmer、`Q x K` | `PROVED` |
| `PAPER_ELLIPTIC_ROUND_04_test.py` | `code/PAPER_ELLIPTIC_ROUND_04_test.py` | clean 证书、Selmer 集、范数、缩放与 MW 像回归 | `PROVED` |
| `PAPER_ELLIPTIC_ROUND_05_analysis.py` | `code/PAPER_ELLIPTIC_ROUND_05_analysis.py` | 构造并否定旧跨侧 Hilbert/CT 表达式 | `NEGATIVE` |
| `PAPER_ELLIPTIC_ROUND_05_test.py` | `code/PAPER_ELLIPTIC_ROUND_05_test.py` | 强制撤回跨侧 pairing、复核分支依赖 | `NEGATIVE` |
| `PAPER_ELLIPTIC_ROUND_06_analysis.py` | `code/PAPER_ELLIPTIC_ROUND_06_analysis.py` | Campbell 原文公式、索引、退化边界、same-m 摘要与 provenance | `PROVED` |
| `PAPER_ELLIPTIC_ROUND_06_test.py` | `code/PAPER_ELLIPTIC_ROUND_06_test.py` | 源重建、退化边界、same-m 哈希和 fail-closed 回归 | `PROVED` |

## certificates

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `STUDENT_ELLIPTIC_ROUND_03_certificate.json` | `certificates/same_m_local.json` | common-m 实位、`Q_2`、30 个奇素数见证及严格 bounded/global 状态 | `PROVED` 仅限处处局部非空；全局点未知 |
| `PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json` | `certificates/local_matrix_512.json` | 64×8=512 格，384 YES、128 NO、0 unresolved；`d=35` 投影 | `PROVED` 仅限局部矩阵/投影 |
| `PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json` | `certificates/selmer_clean_v2.json` | 唯一权威 clean 正面证书：8+4 精确二同源 Selmer、秩上界、`Q x K` | `PROVED`；不含 full 2-Selmer/CT/rank equality |
| `PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json` | `certificates/ct_formula_rejection.json` | 记录 59、71699 分支依赖及撤回字段 | `NEGATIVE`；绝非 CT pairing 值 |
| `PAPER_ELLIPTIC_ROUND_06_CERTIFICATE.json` | `certificates/campbell_source_provenance.json` | Campbell 系数/索引/退化边界、same-m 哈希摘要、未执行 Magma 禁止升级 | `PROVED` 仅限重建与 provenance |

## notes

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `PAPER_ELLIPTIC_ROUND_06_REPORT.md` | `notes/campbell-source-and-boundaries.md` | 最终 Campbell 原文重建、索引与退化边界说明 | `DOC`，结论由 Round-06 证书/测试支撑 |
| `STUDENT_ELLIPTIC_ROUND_03_REPORT.md` | `notes/same-m-local-solubility.md` | same-m 局部证明、Weil–Hensel 桥和 bounded-search 边界 | `DOC`；Magma/有界搜索段不升级 |
| `PAPER_ELLIPTIC_CAMPBELL_REPORT.md` | `notes/local-matrix-512.md` | 512 格及 `d=35` 投影的详细推导 | `DOC` |
| `PAPER_ELLIPTIC_CAMPBELL_ROUND_04_REPORT.md` | `notes/clean-two-isogeny-descent.md` | `Q x K`、精确 Selmer 群与 rank≤3 的完整说明 | `DOC` |
| `PAPER_ELLIPTIC_ROUND_05_REPORT.md` | `notes/ct-pairing-correction.md` | 正式撤回 `<35,4230241>` 跨侧伪 pairing，说明下一步所需对象 | `NEGATIVE/DOC` |
| `PAPER_ELLIPTIC_PRIOR_ART.md` | `notes/prior-art-search.md` | 精确式检索记录与 not-found 边界 | `DOC`；不是新颖性证明 |

## reviews

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `PAPER_ELLIPTIC_CROSS_REVIEW_SQUARE_03.md` | `reviews/01-local-matrix-cross-review.md` | 独立复核 512 格与 ambient/global 边界 | `REVIEW` |
| `PAPER_ELLIPTIC_MANUSCRIPT_REVIEW_SQUARE_04.md` | `reviews/02-selmer-and-pairing-gate-review.md` | 独立确认 Selmer 算术并指出旧 CT 闸门缺口 | `REVIEW` |
| `PAPER_ELLIPTIC_MANUSCRIPT_REVIEW_SQUARE_05.md` | `reviews/03-ct-correction-review.md` | 独立确认跨侧 pairing 撤回、`Q x K/[35]` 与 rank 上界 | `REVIEW` |
| `PAPER_ELLIPTIC_FINAL_REVIEW_CUBE_06.md` | `reviews/04-independent-final-review.md` | 独立终审：数学核心通过并列出 release/clean-certificate 修复项 | `REVIEW` |
| `PAPER_ELLIPTIC_FINAL_REVIEW_CUBE_06_audit.py` | `reviews/04-independent-final-audit.py` | 不导入丙线模块的独立算术/哈希复核脚本 | `REVIEW`；不是主生成器 |
| `PAPER_ELLIPTIC_FINAL_REREVIEW_CUBE_06.md` | `reviews/05-independent-final-rereview.md` | 修复后窄复核，结论 ACCEPT | `REVIEW` |

## reproducibility

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `PAPER_ELLIPTIC_SUBMISSION/data_dictionary.md` | `reproducibility/DATA_DICTIONARY.md` | 解释 same-m、512 格、clean v2、Round05/06、字段类型、eligibility 与 supersession | `DOC` |
| `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json` | `reproducibility/supplement-manifest-v0.6.1.json` | 冻结数学文件 SHA、角色、资格、claim boundary 和 45-test accounting | `DOC/PROVENANCE` |
| `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.py` | `reproducibility/build_supplement_manifest.py` | manifest 生成器 | `PROVED` 仅限发布完整性 |
| `PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST_test.py` | `reproducibility/test_supplement_manifest.py` | 哈希、隔离重建和 ineligible-Magma 负测 | `PROVED` 仅限发布完整性 |

## Round08--Round11 严格增量

| 轮次 | 代码 / 证书 / 报告 / 审稿 | 证据资格与严格边界 |
|---|---|---|
| Round08 | `code/NEXT_ELLIPTIC_ISOMORPHISM_AUDIT.py`; `code/NEXT_ELLIPTIC_ISOMORPHISM_AUDIT_test.py`; `certificates/minimal_model_identity.json` | `PROVED`：显式 `Q`-同构、全局极小模型、判别式与导子；仍无独立第二 CAS |
| Round09 | `code/NEXT_ELLIPTIC_ROUND_09.py`; `code/NEXT_ELLIPTIC_ROUND_09_test.py`; `certificates/round09_two_place_gate.json`; `NEXT_ELLIPTIC_ROUND_09_REPORT.md`; `reviews/PAPER_ELLIPTIC_ROUND_09_REVIEW_SQUARE.md` | `PROVED`：`E` 侧两个素数的完整局部分类，与实位相交剩 8 类；只是不充分的局部必要条件 |
| Round10 | `code/NEXT_ELLIPTIC_ROUND_10.py`; `code/NEXT_ELLIPTIC_ROUND_10_test.py`; `certificates/round10_eprime_two_three_gate.json`; `NEXT_ELLIPTIC_ROUND_10_REPORT.md`; `reviews/ROUND_10_CROSS_REVIEW.md` | `PROVED`：`E'` 侧 `Q_2/Q_3` 两个 iff 及四类交集；最小性只相对于已存七列有限素数矩阵；交叉审稿 PASS |
| Round11 | `code/NEXT_ELLIPTIC_ROUND_11.py`; `code/NEXT_ELLIPTIC_ROUND_11_test.py`; `certificates/round11_isogeny_selmer_audit.json`; `NEXT_ELLIPTIC_ROUND_11_REPORT.md`; `reviews/ROUND_11_CROSS_REVIEW.md` | `PROVED`：完整支撑与正见证把两侧候选升级为阶 8、4 的精确同源 Selmer 群，严格推出 `rank E(Q)<=3`；不计算精确秩、完整 2-Selmer、CT 或第九点；交叉审稿 PASS |

Round11 Campbell Selmer 组在当前工作树 73/73 通过。冻结提交与 cold reproduction
为 PENDING。当前论文 11 页，唯一署名为 `Codex (GPT-5.6-sol)`；项目只要求达到
submission-ready 水准，不实际投稿，不虚构其他作者、单位、联系方式、ORCID、
资助、利益冲突、期刊、DOI 或投稿行为。这些增量不产生或排除第九点，不给出
Cassels--Tate 值、完整 2-Selmer、秩等式或数据库级优先权。

## candidate-input（仅保留历史输入时）

| 源文件 | 目标文件 | 理由 | 证据资格 |
|---|---|---|---|
| `PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m` | `notes/candidate-input/UNEXECUTED_full_two_selmer.m` | 正文所述未来 full 2-descent 输入；保留便于后续人工运行 | `INELIGIBLE`：无 transcript、无可信 binary hash、不得支撑任何结论 |
| `STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m` | `notes/candidate-input/UNEXECUTED_old_fake_selmer.m` | 仅为 Round-03 测试的历史静态输入 | `INELIGIBLE`：不得作为 fake Selmer 计算证据 |
| `STUDENT_ELLIPTIC_ROUND_03_run_magma_audit.ps1` | `notes/candidate-input/old_magma_audit_wrapper.ps1` | 解释旧输入的 fail-closed 意图；未产生认可 transcript | `INELIGIBLE` |

## 明确排除

| 源模式/文件 | 目标 | 理由 | 证据资格 |
|---|---|---|---|
| `*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`, `*.out`, `__pycache__/`, `tmp/`, `$outDir/` | 排除 | 构建缓存或临时审计产物 | `INELIGIBLE` |
| `PAPER_ELLIPTIC_ARCHIVE_CANDIDATE.zip`、allowlist/audit、archive builder/tests | 排除 | 投稿/本地归档工程，不是 GitHub 数学权威源 | `INELIGIBLE` |
| `PAPER_ELLIPTIC_RELEASE_MANIFEST.*`, `PAPER_ELLIPTIC_EXTERNAL_READINESS_07.md` | 排除 | 含投稿包版本与外部准备逻辑；GitHub 应另生仓库级 manifest | `INELIGIBLE` |
| `PAPER_ELLIPTIC_SUBMISSION/*`（唯独 `data_dictionary.md` 例外） | 排除 | 作者、期刊、DOI、cover letter、声明等纯投稿占位文案 | `INELIGIBLE` |
| `output/pdf/*`, `$outDir/*`, `tmp/**/*pdf`, `PAPER_ELLIPTIC_TEX` 的旧副本 | 排除 | 旧/重复 PDF；只保留当前根 `PAPER_ELLIPTIC_TEX.pdf` | `INELIGIBLE` |
| `PAPER_ELLIPTIC_ROUND_04_two_cover_descent.m`、其他 `STUDENT_ELLIPTIC_ROUND_0[2-5]*.m` | 排除 | 已被 clean v2/CT 纠错取代或未执行，易与证明混淆 | `INELIGIBLE` |
| 早期 feasibility/NEXT 报告、组会记录、旧 Round02/03/04/05 审计包装与旧证书 | 排除 | 历史探索已由上列最终报告、clean 证书和终审取代 | `INELIGIBLE` |
