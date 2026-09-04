# vibemath 乙线最终数学材料映射清单

目标根：`vibemath/powers-in-progressions/pure-cubic-five-term/`  
规则：仅迁移下列数学证据；本清单不复制文件。

## 主论文：paper

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5_TEX.tex` | `vibemath/powers-in-progressions/pure-cubic-five-term/paper/main.tex` | 权威论文源；包含 Kummer kernel、25 轨道、60 个好素数模障碍、下界见证、六个正秩四命中模型及精确 claim boundary。 |
| `PAPER_CUBE_KUMMER5_TEX.pdf` | `vibemath/powers-in-progressions/pure-cubic-five-term/paper/main.pdf` | 与上述 TeX 对应的当前八页可读快照；供数学内容和版面复核，不作为源码替代。 |

## 代码：code

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5.py` | `vibemath/powers-in-progressions/pure-cubic-five-term/code/PAPER_CUBE_KUMMER5.py` | 唯一权威生成器：符号核验 Kummer kernel，枚举 `3^5` 个词及 25 轨道，构造 60 个模型并逐格计算模障碍。 |
| `PAPER_CUBE_KUMMER5_test.py` | `vibemath/powers-in-progressions/pure-cubic-five-term/code/PAPER_CUBE_KUMMER5_test.py` | 九项数学回归：kernel resultant、radicand 规范化、Burnside、轨道分割、60 模障碍、Jacobian minors、下界和 stored/live 一致。 |

## 证书：certificate

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5_CERTIFICATE.json` | `vibemath/powers-in-progressions/pure-cubic-five-term/code/PAPER_CUBE_KUMMER5_CERTIFICATE.json` | schema `paper-cube-pure-cubic-kummer-n5-v2` 的冻结精确证书；含 kernel、25 轨道分割、60 个 `(word,D,p)` 完整计数和四命中 fail-closed 状态。因生成器和测试按同目录解析，目标处须与两份 Python 文件共置。 |

## 数学说明：notes

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5_ROUND_06_REPORT.md` | `vibemath/powers-in-progressions/pure-cubic-five-term/notes/proof-audit-and-scope.md` | 最完整的纸面推导与边界说明：公共缩放的仿射颜色、kernel、25=`9+1+15`、素数支持引理、60 曲线和 `R^times_(3,1)(5)=4`；明确不声称分类 31 个四命中模型。 |
| `PAPER_CUBE_KUMMER5_SUBMISSION/prior_art_search.md` | `vibemath/powers-in-progressions/pure-cubic-five-term/notes/prior-art-search.md` | 创新性风险记录：精确定义、三方程与关键词查询、最近相关工作及 `not found != novelty proof` 边界。 |
| `PAPER_CUBE_KUMMER5_SUBMISSION/references_metadata.md` | `vibemath/powers-in-progressions/pure-cubic-five-term/notes/reference-metadata.md` | Darmon--Merel 与 Hajdu--Tengely 两个实际定理依赖的题录、DOI 和使用范围。 |

## 独立审稿：reviews

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5_FINAL_REVIEW_SQUARE_06.md` | `vibemath/powers-in-progressions/pure-cubic-five-term/reviews/final-mathematical-review.md` | 权威独立终审：复核 kernel、Burnside 25 轨道、good-prime Jacobian、60 证书定位和精确最大值；接受数学结论并隔离 31 模型。文中的旧发布哈希仅是历史信息。 |

## 可复现性：reproducibility

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_KUMMER5_SUBMISSION/data_dictionary.md` | `vibemath/powers-in-progressions/pure-cubic-five-term/reproducibility/CERTIFICATE_SCHEMA.md` | 逐字段解释证书顶层、60 条局部记录、`p^2-1` 扫描恒等式和 good-prime 布尔量。 |
| `PAPER_CUBE_KUMMER5_ROUND_06_REPORT.md` 的第 8 节 + `PAPER_CUBE_KUMMER5_test.py` | `vibemath/powers-in-progressions/pure-cubic-five-term/reproducibility/REPRODUCE.md` | 形成 GitHub 布局下的最小复现入口：运行同目录九项测试、重生成证书、双编译 TeX；只抽取数学命令，不继承旧投稿 ZIP/manifest 拓扑。 |

## Round07--Round10 四命中严格增量

| 轮次 | 当前文件 | 严格结论与边界 |
|---|---|---|
| Round07 | `PAPER_CUBE_FOURHIT_0001_ROUND_07.md`; `code/PAPER_CUBE_FOURHIT_0001.py`; 对应 test/certificate | 第一正秩四命中模型给出无穷族 |
| Round08 | `PAPER_CUBE_FOURHIT_0010_ROUND_08.md`; `code/PAPER_CUBE_FOURHIT_0010.py`; 对应 test/certificate | 第二模型闭合，并经显式对称得到后续可复用分支 |
| Round09 | `PAPER_CUBE_FOURHIT_CLUSTER_ROUND_09.md`; `code/PAPER_CUBE_FOURHIT_CLUSTER_ROUND09.py`; 对应 test/certificate | 29 个待处理模型在明确置换作用下聚成 25 类；这不是任意 `Q`-同构分类 |
| Round10 | `PAPER_CUBE_FOURHIT_3PLUS1_ROUND_10.md`; `code/PAPER_CUBE_FOURHIT_3PLUS1_ROUND10.py`; 对应 test/certificate；`reviews/ROUND_10_CROSS_REVIEW.md` | `3X^3-4Y^3+Z^3=0` 正秩，闭合两个新模型；交叉审稿 PASS |

当前结论为原 31 个四命中模型中 6 个具有正秩无穷族，25 个仍开；不声称精确
秩、完整 Mordell--Weil 基或完整极值分类。pure-cubic 组当前 36 项测试通过。

## 长期线建议一：P6 四次幂问题（独立 paper 目录）

目标根：`vibemath/powers-in-progressions/fourth-powers-six-term/`

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_P6_GATE.md` | `vibemath/powers-in-progressions/fourth-powers-six-term/notes/initial-reduction-and-local-gate.md` | 已证 `C1,C2` 精确 AP 归约、边界、局部四次幂类、可见 involutions；明确 `P_6(4)` 未决。 |
| `PAPER_CUBE_P6_MAPS.md` | `vibemath/powers-in-progressions/fourth-powers-six-term/notes/quotient-maps-and-coverings.md` | 六个 genus-1 商、统一 quartic--Jacobian 映射、Kani--Rosen 同源与 C1 两 cover 的已证结构；rank/点集保持 fail-closed。 |
| `PAPER_CUBE_ROUND_05_REPORT.md` | `vibemath/powers-in-progressions/fourth-powers-six-term/notes/dplus-genus5-reduction.md` | `D_+` 三个椭圆投影、genus-1 四次与 genus-5 双覆盖的研究记录；只能作为未闭合长期线，不能作为 `P_6(4)` 证明。 |
| `PAPER_CUBE_MANUSCRIPT_REVIEW_SQUARE_05.md` | `vibemath/powers-in-progressions/fourth-powers-six-term/reviews/fail-closed-audit.md` | 独立区分已接受结构结果与未闭合全局点问题，并记录清分母、紧化、测试覆盖和 CAS 饱和要求。 |
| `PAPER_CUBE_P6_gate.py` | `vibemath/powers-in-progressions/fourth-powers-six-term/code/PAPER_CUBE_P6_gate.py` | 初始精确代数/有限域入口。 |
| `PAPER_CUBE_P6_test_gate.py` | `vibemath/powers-in-progressions/fourth-powers-six-term/code/PAPER_CUBE_P6_test_gate.py` | 初始归约和边界回归。 |
| `PAPER_CUBE_P6_maps.py` | `vibemath/powers-in-progressions/fourth-powers-six-term/code/PAPER_CUBE_P6_maps.py` | 商映射、Jacobian、同源及 covering 的精确符号实现；不得把 LMFDB 字段当证明。 |
| `PAPER_CUBE_P6_test_maps.py` | `vibemath/powers-in-progressions/fourth-powers-six-term/code/PAPER_CUBE_P6_test_maps.py` | 对映射、例外纤维、有限域 trace 和 cover 恒等式的回归入口。 |

## 长期线建议二：C29 同时挠点纤维积（独立 paper 目录）

目标根：`vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/`

| 源文件 | 目标文件 | 证据角色 |
|---|---|---|
| `PAPER_CUBE_C29_STAGE_REPORT.md` | `vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/notes/genus2-model.md` | C29 到显式 genus-2 模型的推导、判别式、cusp 与 rank/点集 fail-closed 边界；须与下列修订共同阅读。 |
| `PAPER_CUBE_C29_REVISION.md` | `vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/notes/birational-map-revision.md` | 控制冲突的最终修订：双向复合、主开集分母、六 cusp 局部表、Igusa--Clebsch 指纹和饱和闸门。 |
| `PAPER_CUBE_C29_model.py` | `vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/code/PAPER_CUBE_C29_model.py` | 精确多项式模型、映射、边界和不变量生成器。 |
| `PAPER_CUBE_C29_test_model.py` | `vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/code/PAPER_CUBE_C29_test_model.py` | Kubert 变换、双向映射、cusp、判别式、不变量与 fail-closed 状态回归。 |
| `PAPER_CUBE_C29_FREEZE.json` | `vibemath/powers-in-progressions/elliptic-simultaneous-torsion-c29/code/PAPER_CUBE_C29_FREEZE.json` | 与代码同目录使用的 exact-polynomial 冻结证书；不包含 rank 或完整点集证明。 |

## 明确排除

| 源文件/模式 | 证据角色 |
|---|---|
| `*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`, `*.out`, `tmp/**`, `__pycache__/**`, `output/pdf/**` | 构建副产物、临时文件或重复 PDF，不进入 GitHub 数学材料。 |
| `PAPER_CUBE_KUMMER5_ARCHIVE_CANDIDATE.zip`, `PAPER_CUBE_KUMMER5_ARCHIVE_07*`, `PAPER_CUBE_KUMMER5_EXTERNAL_READINESS_07.md`, `PAPER_CUBE_KUMMER5_SUPPLEMENT_MANIFEST*` | 投稿/归档工程；已知普通解包拓扑曾有阻断，且不属于最终数学证据。 |
| `PAPER_CUBE_KUMMER5_SUBMISSION/{cover_letter.md,journal_shortlist.md,author_contributions.md,ai_disclosure.md,abstract.txt,data_code_availability.md,USER_INPUT_CHECKLIST.md,README.md}` | 纯投稿格式、身份/DOI/声明占位或与 GitHub 数学目录无关的发布文案。 |
| `PAPER_CUBE_TEX.tex`, `PAPER_CUBE_TEX.pdf` | 旧 P6/C29 投稿骨架；长期线仅保留上列已证报告、代码与 fail-closed 审稿。 |
| `PAPER_CUBE_C29_rank_points.m`, `PAPER_CUBE_C29_isomorphism_gate.m`, `PAPER_CUBE_P6_elliptic_quotients.m`, `STUDENT_CUBE_ROUND_0*_rank*.m`, `STUDENT_CUBE_ROUND_05_magma*.m` | 未执行或未获信任的 CAS 输入，无可提升的数学输出。 |
| `STUDENT_CUBE_ROUND_04_SYNTHETIC_*`, `STUDENT_CUBE_ROUND_04_pipeline.py`, `STUDENT_CUBE_ROUND_05_promote.py` 及 fake-Magma fixtures | synthetic/promotion 工程，不是数学证据。 |
| `STUDENT_CUBE_ROUND_02_*` 至 `STUDENT_CUBE_ROUND_05_*` 的 N=20 困难模式流水线 | 早期长期主线实验，未形成本文 Kummer5 定理的必要证据。 |
| `PAPER_CUBE_KUMMER5_MANUSCRIPT_REVIEW_SQUARE_06.md`, `PAPER_CUBE_KUMMER5_FINAL_REPAIR_06.md`, `PAPER_CUBE_KUMMER5_FINAL_RELEASE_HYGIENE_06.md`, `PAPER_CUBE_KUMMER5_EXTERNAL_REVIEW_ELLIPTIC_07.md` | 已被最终数学审稿取代，或主要审计投稿包/归档拓扑；不进入纯数学 GitHub 树。 |
