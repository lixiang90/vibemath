# 第九次论文组会：mask 90、四命中聚类与两处局部门

日期：2026-09-04

主持：导师（root）

结论：三线都取得严格但有边界的增量。当前工作树六组共 **218/218**
项回归通过；冻结 commit `85eb55b49f9f80e05a7d890fec7cc289083b802b` 的 Round09
内部 clean-clone 也已成功。外部真人复现和数据库级新颖性核验继续开放。

## 1. 研究生甲：mask 90 将必要模式从 10 降至 7

对

`C_90: y^2=(t+1)(t+3)(t+4)(t+6)`，

令

`A=(t+1)(t+6)`，`B=(t+3)(t+4)`。

则 `B-A=6` 且 `gcd(A,B)|6`。在两个正值外区间，共同平方自由核只可能为
`1,2,3,6`；四个分支分别由模 4、有限因子分解和平方间隔排除。六个中间整数
只产生四个含零分支点。故完整整数点集为

`(-6,0), (-4,0), (-3,0), (-1,0)`。

这严格排除 IDs `43,251,281`，必要筛链成为

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23 -> 15 -> 10 -> 7`。

剩余 IDs 为 `12,31,59,134,214,230,276`。这不证明其中任何模式可实现或
不可实现，也不决定 `R_2(7)`。甲线 supplement 已更新为
`paper-square-supplement-v0.8.0`，manifest SHA-256 为
`29ee9fe4a34a01f4066c017912130f3c02dcd55a031fb9f19dc7046d8854eb54`。

## 2. 研究生乙：29 个四命中模型的精确聚类

乙线从原始 `5*3^4=405` 个部分着色重算 `405 -> 38 -> 31 -> 29`。29 个待处理
模型按颜色重数分为 `4+9+16`；在报告明确限定的坐标置换作用下，它们聚成
`2+9+14=25` 类。不同 key 只表示在这一小作用下未发现同构，不被宣称为任意
`Q`-同构分类。

两条新的 `3+1` 模型复用光滑三次曲线

`2X^3-3Y^3+Z^3=0`

及其到 `v^2=u^3-243` 的已证非挠点，因此再得到两个无穷族。31 个四命中模型
现有 4 个闭合为无穷族，另 27 个仍开；未对其余模型推断秩或有理点。

## 3. 研究生丙：E 侧两处局部分类

对

`F_d=dU^4+aU^2V^2+(b/d)V^4`

及 `Delta=a^2-4b`，恒等式

`4dF_d=(2dU^2+aV^2)^2-Delta*V^4`

结合 `v_p(Delta)=1`，在 `p=59,71699` 给出穷尽的三赋值分支。两个素数处的
可解平方类恰为同一 16 类；再与实位 `d>0` 相交，32 个 `E` 侧支撑候选严格缩至

`1,3,5,7,15,21,35,105`。

这只是 `E` 侧 covering 的必要条件，不是完整 2-Selmer、原 Campbell 纤维的
有理点或全局阻碍。当前机器没有独立 Sage/Magma/PARI 椭圆曲线环境，报告没有
冒充第二 CAS 复现。

## 4. 交叉审稿与修复记录

- 乙审甲：
  `square-progressions/seven-consecutive-squareclasses/reviews/PAPER_SQUARE_ROUND_09_REVIEW_CUBE.md`。
  独立重算 mask-90 的关系空间出现位置、四平方自由分支和 `10 -> 7` 影响，结论
  **PASS**。
- 丙审乙：
  `powers-in-progressions/pure-cubic-five-term/reviews/PAPER_CUBE_ROUND_09_REVIEW_ELLIPTIC.md`。
  数学定理 **PASS**，但首次冻结证书把 `0100` 的 `A1=0`/`A4=0` 变量名写反，
  因而证书被判 **FAIL pending correction**。作者随后修正为
  `A1=0 => Z=-Y => X^3=2Y^3`、`A4=0 => Z^3=2Y^3`，加入直接语义断言并重生
  证书；当前证书 SHA-256 为
  `4217f170ce6cd27d488811119289dd1cccb480b47c536c23bd10be99b1193662`。
- 甲审丙：
  `elliptic-curve-progressions/campbell-two-isogeny-selmer/reviews/PAPER_ELLIPTIC_ROUND_09_REVIEW_SQUARE.md`。
  独立复算恒等式、三赋值分支、16 类和实位交后 8 类，结论 **PASS**。审稿指出
  的 `-1,qquad` 排版笔误已改为 `-1,\qquad`，并由 Round09 测试固定。

三份交叉审稿中的独立复算不能由下述统一回归替代；乙线错误被保留在审稿记录中，
没有因后续修复而抹去。

## 5. 合并验证与 Round09 clean-clone

`python tools/run_all_checks.py` 的六组结果为：

| 组 | tests |
|---|---:|
| squareclasses | 78 |
| number fields | 33 |
| pure cubic | 29 |
| fourth powers | 14 |
| C29 | 8 |
| Campbell Selmer | 56 |
| **合计** | **218** |

全部通过。`tools/cold_reproduce.py` 的期望计数已同步为
`[78,33,29,14,8,56]`。同一组数随后在 clean Round09 commit
`85eb55b49f9f80e05a7d890fec7cc289083b802b` 上实际通过：source clean，PDF 页数依次
为 10、7、10，三份 final-log warning list 均为空。提交版/重建版各自的
`pdftotext` SHA-256 完全一致：

- squareclasses: `f945d398d6169e5e2ad1009d1b6f9ef0f9150f89c72a5fb67a4b37ea6bdfa7a4`;
- pure cubic: `6ca420753b087ed24bbf675c8c5f8069a9dfc54428213b4b455503120fbfbbf4`;
- Campbell Selmer: `b1413392f725f042a3809bb4d7c3f709453a11e7024a2ed0faaa23033b6fac98`.

机器记录为 `INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.json` 与
`INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.log`；combined log SHA-256 为
`6bf7915a75983763fa8a98d096e8fbd2f6a7ee258a57575f0864912b56be0c00`。
第七轮 `559e89364b6e` 和第八轮 `4a8dae3dbc04` 的记录继续作为历史基线保留。
三次都只是内部 clean-clone reproduction，不是工作区外的真人独立复现。

## 6. 开放边界与下一步

1. 甲线只留下 7 个必要模式；继续选影响大的低难度 character mask，遇到真正的
   Mordell--Weil/Thue--Mahler 障碍即 fail-closed。
2. 乙线剩余 27 个四命中模型；25 个置换 cluster 不是完整 `Q`-同构分类。
3. 丙线的 8 类只是 `E` 侧局部必要条件；全局兼容纤维和独立 CAS 复现仍开。
4. 三线都仍需人类完成 MathSciNet/zbMATH/引用图优先权核验，并需要工作区外的
   真人独立复现。当前成果不得以“首次”或“外部复现完成”表述。
