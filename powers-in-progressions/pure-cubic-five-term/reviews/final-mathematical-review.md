# 甲组对 Kummer5 终修的窄复核

日期：2026-09-03  
复核基准：`PAPER_CUBE_KUMMER5_FINAL_REPAIR_06.md`、冻结 TeX/PDF、证书及新版 manifest generator/verifier/tests。  
决定：**前次 blocking 已解除；ACCEPT with minor revisions。** 数学主定理与有限证书没有新缺口，剩余问题均为发布卫生或措辞同步，不阻挡 `R^times_(3,1)(5)=4` 的候选稿冻结。

## 1. 前次 blocking：已严格解除

旧问题是 `build_manifest()` 在比较前调用 `sync_core()`，使被篡改的 submission 副本先被覆盖回正确字节再“通过验证”。新版结构已真正分离：

- `sync_core()` 只由显式写入入口 `generate_manifest()` 调用；
- `build_manifest()` 不写文件，且 source/bundle 核心哈希不同时立即抛出 `ValueError`；
- `verify_manifest()` 只读 stored manifest、磁盘文件和 fresh data model，不调用 `sync_core()`、`generate_manifest()` 或任何写 API；
- 五个核心副本同时受 bundle SHA、source SHA 及 `source_copy_sha256_match=true` 约束；
- 21 个 manifest row 的路径集合必须精确等于允许集合，submission 顶层普通文件集合也必须精确相等。

攻击测试是有效的：隔离副本中的 `PAPER_CUBE_KUMMER5.py` 被追加稳定 sentinel 后，`verify_manifest()` 抛错，随后逐字节断言 sentinel 仍在，证明不是“报错前先修复”；加入顶层 `UNLISTED.txt` 同样抛错且文件保持不变。本人以 `python -B` 复跑这两项及全部 manifest 测试，均通过。故前次唯一工程 blocking 关闭。

当前只读验证输出 schema `paper-cube-kummer5-supplement-manifest-v1`、恰 21 行；冻结 manifest SHA-256 为
`A4E7EFDB0B5BAB23AF841A36EE5089C9A7E1E1B4C7FB1EFF23E998CADD3D6400`。

## 2. Burnside 计数：通过

作用群为颜色仿射群 `AGL(1,3)`（6 元）与位置反转（2 元）的直积，共 12 元。独立逐词计数得到 fixed-point 数多重集

```text
243, 27, 9, 9, 9, 1, 1, 1, 0, 0, 0, 0,
```

总和 300，Burnside 给 `300/12=25`。这与直接覆盖全部 `3^5=243` 词的 25 轨道及 `9+1+15` 分割一致。正文现在既有 Burnside 核验，也保留 15 个局部代表，已消除原来的“只信代表选取”问题。

## 3. good-prime Jacobian 与光滑性：通过

正文取 `u_i=D^{c_i}x_i^2` 后的 `3x5` Jacobian 正确。对 `p>=7,p∤D`，两个 `u_i` 为零会令对应 AP 两项为零；因指标差在 1 至 4 之间且模 `p` 可逆，首项与公差都为零，进而全部射影坐标为零，矛盾。因此几何点至多一个 `u_i=0`。

无零时列 `012` 的 minor 为 `u0*u1*u2`。唯一零依次位于 `u0,...,u4` 时，列
`124,024,014,014,013` 的 minors 独立重算为

```text
3*u1*u2*u4,
-2*u0*u2*u4,
u0*u1*u4,
u0*u1*u4,
-2*u0*u1*u3.
```

在这些特征中均非零，故 Jacobian rank 为 3，射影特殊纤维几何光滑。表中素数全满足条件，因而 “good prime” 已有实质证明，不再只是 `gcd(p,3D)=1` 的标签。新增符号测试覆盖六种情形。

## 4. 证书定位：通过

正文现在明确给出：

- `PAPER_CUBE_KUMMER5_CERTIFICATE.json`；
- schema `paper-cube-pure-cubic-kummer-n5-v2`；
- 证书 SHA-256 `7C5FF0BD36EBFC3BACE0CA5898625B2FD7F03D318C754C6650D3A2483DD83977`；
- 根 locator `PAPER_CUBE_KUMMER5_SUPPLEMENT_MANIFEST.json`；
- 60 格各枚举 `p^2-1` 个非零参数对、合计 23520 对；
- 当前不是公开归档，投稿时必须回填不可变 DOI/URL。

根与 submission 内的 certificate、TeX、PDF 哈希一致；只读 verifier 也重新构造完整 data model 并逐项比较。此前的证书可定位性 major 已解除。

## 5. 测试与 PDF

复跑：

```text
python -B -m unittest -v \
  PAPER_CUBE_KUMMER5_test.py \
  PAPER_CUBE_KUMMER5_SUPPLEMENT_MANIFEST_test.py
```

结果：**Ran 16 tests in 0.423s — OK**。其中 9 项数学/证书测试与 7 项 manifest 测试，覆盖 Burnside、六个 minors、60 个局部阻碍、stored/live 一致、篡改不修复及未列顶层文件攻击。

冻结 PDF SHA-256 为
`BA140E67DE083B00721DFF00E81B89B4C1B4D0433EB7EC3ABA1989E5C303B771`，`pdfinfo` 确认为 4 页。本人在隔离目录双编译，最终 log 无 undefined citation/reference、LaTeX/Package warning、overfull 或 underfull；将冻结 PDF 与隔离重建 PDF 各自渲染为 130 dpi PNG，四页逐页像素哈希完全一致。目检标题、Burnside 段、Jacobian/minors、局部表、长 SHA、主定理及参考文献，无裁切、重叠、越界、坏字形或不可读内容。

## 6. 剩余 minor

1. `PAPER_CUBE_KUMMER5_SUBMISSION/USER_INPUT_CHECKLIST.md` 仍写 “current three-page research note”，应同步为 four-page；这只是投稿清单的过期页数。
2. `output/pdf/PAPER_CUBE_KUMMER5_TEX.pdf` 仍是旧三页版本，SHA 为 `8E43AA...`，而根与 submission 的正式冻结稿是四页 `BA140E...`。它不在 21 行 manifest payload 中，故不损害闭包，但容易被人工误选；建议同步、删除或显式标为 stale。
3. verifier 精确拒绝 submission 顶层未列普通文件，但有意忽略 `__pycache__`，同时也会忽略任意其他未列子目录。若最终归档严格按 manifest 的 21 个显式路径打包，则无风险；若操作方式是直接压缩整个 submission 树，建议只允许 `__pycache__` 或递归拒绝其他目录/文件，并在归档前清除 runtime debris。
4. manifest 内容在先前 `1.0.0-rc1` 冻结点后发生变化但 release ID/semantic version 未递增。因尚未公开归档且外部 SHA 已更新，这不是完整性失败；为避免两个不同哈希都被称为同一 rc1，建议最终归档前升为 `rc2` 或最终 `1.0.0`。

## 7. 最终判断

前次 B1、M1、M2 均已解除。当前可以接受的定理边界仍是：纯三次域 Kummer kernel、25 颜色轨道、`{2,3}` 素数支撑、60 个局部排除及
`R^times_(3,1)(5)=4`。31 个四命中模型的有理点分类仍明确不在本文结论内。

建议：**ACCEPT with minor revisions**。修正页数/旧输出副本，并在最终 archive release 时收紧目录规则与版本号；无需重开数学证明或等待 31 模型分类。
