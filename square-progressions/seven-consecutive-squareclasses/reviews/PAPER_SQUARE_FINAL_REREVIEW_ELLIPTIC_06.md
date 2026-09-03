# 甲线终修 v0.6.1 窄复核（丙组）

日期：2026-09-03  
范围：`PAPER_SQUARE_FINAL_REPAIR_06.md`、cover letter、submission root manifest/生成器/测试、完整 63 项联合测试及冻结 PDF。未修改任何甲线文件。

## 决定

**ACCEPT。** 终审指定的两项 minor 已实质修复；没有发现 mathematical、manifest-closure 或版面 blocking。当前包可作为本地 journal candidate 冻结，但仍不能对外投稿，直至文末列出的作者输入、人工复核和公开归档步骤完成。

有一个不影响本次 ACCEPT 的 patch-version 注记：冻结 manuscript-v0.6.0 的第 6 页仍把当时的 root release 写成 `paper-square-submission-v0.6.0`，而当前外层 root package 已补丁升级到 v0.6.1。root manifest 明确把稿件/PDF 标成 v0.6.0、submission prose 标成 v0.6.1，因此哈希和组件版本没有歧义；不过在最终公开归档时，作者最好把正文这句改成“稿件组件 v0.6.0、当前 root package v0.6.1”，或明确保留其历史含义。若改 PDF，必须发行新的 root version 并重算哈希。此项是归档元数据同步，不影响数学结论或当前闭包验证。

## 1. Cover letter 的 651 入口

修订后的 `PAPER_SQUARE_SUBMISSION/cover_letter.md` 明确写道：先排除 affine rank at most one，才把 651 个 three-/four-block patterns 缩为 23 个显式必要候选。量词顺序与正文摘要和 Theorem 12 一致，也紧接着声明不决定 `R_2(7)`、不证明 surviving patterns 可实现。上一轮 m1 已闭合。

## 2. Root verifier 的四个语义字段

`PAPER_SQUARE_SUBMISSION_MANIFEST.py` 以常量固定并逐项验证：

1. `release_status`；
2. `author_metadata_status`；
3. `manifest_trust_anchor`；
4. 完整 `claim_boundary` 字典。

测试把四种篡改加入 fail-closed attacks。我另行逐项执行后，分别且精确得到：

```text
release_status         -> release status mismatch
author_metadata_status -> author metadata status mismatch
manifest_trust_anchor  -> manifest trust anchor mismatch
claim_boundary         -> claim boundary mismatch
```

磁盘 JSON 等于生成器输出，`verify_manifest` 返回空错误列表。13 个 payload 的顺序、角色、组件版本、字节数和 SHA-256，以及九文件 submission-directory closure、nested supplement 元数据和 PDF policy 均受验证。上一轮 m2 已闭合。

## 3. 独立 SHA-256 复算

```text
PAPER_SQUARE_SUBMISSION_MANIFEST.json
3D168CA3E55F9BFF368ECF6FCD22A581FB7BD14F60D690B448596A1FE392D8EC

PAPER_SQUARE_SUBMISSION/cover_letter.md
7BD0A8CE92BD91F2C90B58A8713CB33DB82D178A22F3FF496285ACE4180B339A

PAPER_SQUARE_TEX/main.pdf
5AEA6AD40D4E76007BF6D6DDB4A973AE8677DCF478A7429B7A89F30F2FAB1535

PAPER_SQUARE_SUPPLEMENT_MANIFEST.json
6004AFC5334BBEA62969640079CAD80764D2938D73B6FD62A85ABC2249794588
```

四值均与 `PAPER_SQUARE_FINAL_REPAIR_06.md` 一致。

## 4. 63 项联合测试

按 root manifest 所存完整命令运行九个测试模块，结果：

```text
Ran 63 tests in 6.020s
OK
```

其中包含 57 项数学/补充材料测试及 6 项 submission-root 测试；逐 payload 字节篡改、缺失/额外 submission 文件、schema/role/version/self-reference、四个顶层语义字段及 PDF policy 的负测均通过。

## 5. 冻结 PDF 哈希与版面

`PAPER_SQUARE_TEX/main.pdf` 为 7 页 A4、267512 bytes、PDF 1.5；其 SHA-256 与 root manifest 一致。现存 LaTeX log 未检出 undefined citation/reference、LaTeX/Package warning、overfull 或 underfull。逐页以 130 dpi 渲染检查标题与摘要、长公式、18 分支表、mask 102/108、23 模式表、manifest 长文件名及参考文献，未见裁切、重叠、坏字形、黑块、表格越界或页码问题。

本次窄复核没有原地重编译，以免改变受 root manifest 绑定的冻结 PDF；其独立重建策略已由 manifest 明确规定为内容/诊断/版面一致，而非时间戳敏感的 bitwise identity。

## 6. 剩余外部占位与提交闸门

ACCEPT 不等于已经授权投稿。仍须由用户/作者完成：

- 选定目标期刊并复核其当前模板、数据与 AI 披露政策；
- 填入作者顺序、姓名、单位、通信作者、邮箱、邮址及可选 ORCID；
- 人工确认 funding、conflict of interest、原创性/非一稿多投和 AI-assisted disclosure；
- 独立复核全部证明、表格、参考文献和新颖性，尤其完成 MathSciNet/zbMATH 人工查重；
- 将精确的 v0.6.1 root manifest 与全部绑定 payload（含 nested v0.5.0 supplement）存入公开档案，填入真实 DOI/URL，并由档案/期刊记录锚定 root-manifest SHA-256；
- 若为处理上面的正文 patch-version 注记而改动稿件或 PDF，发行新 root version、重建 root manifest、重跑 63 测试并复核 PDF；
- 由全体作者明确批准最终题名、摘要、cover letter 和实际投稿。

结论：本轮指定修复可接受，数学内容继续冻结；除明确的外部投稿闸门及上述非阻断版本注记外，无剩余内部审稿问题。
