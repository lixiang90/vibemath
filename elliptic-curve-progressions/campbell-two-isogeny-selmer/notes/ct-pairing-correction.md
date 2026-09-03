# 丙线第五轮：Campbell 稿件修复与 Cassels--Tate 配对定义域纠错

日期：2026-09-03  
证据边界：本轮只使用 Python/SymPy 的精确整数与模素数幂计算，并查核原始论文/官方 Magma 文档；本机没有 Magma、Sage、mwrank 或 PARI/GP。本轮没有调用外部在线 CAS，也没有上传任何工作区文件。

## 1. 最重要的结论

原第四轮所谓唯一配对 bit

```text
<35,4230241>_CT
```

必须撤回。`35` 是 E 侧的 `Sel^(dual phi)(E'/Q)` 类，而 `4230241` 是 E' 侧的 `Sel^phi(E/Q)` 类。标准“把 2-同源下降升级为完整 2-下降”的 Cassels--Tate pairing 定义在**同一个** `Sel^(dual phi)` 群与自身之间；其 radical 是完整 `Sel^2(E/Q)` 的像。van Beek--Fisher 在引言式 (2) 明确写出这一同侧定义域：[Acta Arith. 185 (2018), 367--396](https://doi.org/10.4064/aa171108-11-4)。完整二进四次公式也定义在 `Sel^2(E/Q) x Sel^2(E/Q)`：[Fisher, Research in Number Theory 8 (2022), 74](https://doi.org/10.1007/s40993-022-00376-z)。

这里还有一个不依赖记号的强一致性检查：既有同一 `m` 证书已经证明 `C_H` 处处局部可解，所以 `[C_H]` 本身就是完整 `Sel^2(E/Q)` 类；其有理 2-挠投影是 `35`。因此 `35` 已经在

```text
Sel^2(E/Q) -> Sel^(dual phi)(E'/Q)
```

的像里，必然被正确的同侧 lifting pairing 消去。换言之，即使构造出正确同侧 pairing，它也不能通过这一层排除 `35`。

所以：第四轮关于两侧精确 isogeny Selmer 群、`rank <= 3`、`Q x K` 分解与 `d=35` 投影的结果继续成立；“一个对侧 bit 可推出 `C_H(Q)=empty`”不成立。

## 2. 辅助 conic 与 tangent 的精确结果

尽管旧公式无效，本轮确实补出了它要求的算术对象。对标准偶四次

```text
C_35: N^2 = 35 U^4 - 591895071 U^2 V^2
              + 1672465404395520 V^4
```

令 `R=U^2, S=V^2`，辅助 conic 为

```text
N^2 = 35 R^2 - 591895071 R S + 1672465404395520 S^2.
```

它有全局有理整点

```text
(R0,S0,N0) = (16257024,1,36058176).
```

梯度除以公共因子 9 后得到 primitive tangent

```text
L_35 = 60677401 R - 697502396215296 S - 8012928 N.
```

脚本逐项验证 conic residual 与 `L_35(R0,S0,N0)` 均为 0。这只是标准偶四次 `C_35` 的候选局部函数；它不是 `C_H` 的完整 binary-quartic pairing datum。

## 3. 旧公式的分支不变量测试严格失败

把上一节的 `L_35` 强行代入旧式

```text
(L_35(P_v),4230241)_v,  4230241=59*71699,
```

在 `p=59` 和 `p=71699` 的两个 Hensel 分支得到：

| p | modulus | N | L mod p^3 | v_p(L) | symbol |
|---:|---:|---:|---:|---:|---:|
| 59 | 59^3 | 56226 | 127303 | 0 | -1 |
| 59 | 59^3 | 149153 | 145730 | 1 | +1 |
| 71699 | 71699^3 | 152989401412805 | 252464922339130 | 0 | -1 |
| 71699 | 71699^3 | 215596989132294 | 195462237955773 | 1 | +1 |

每个 `N` 都严格满足 `N^2=rhs mod p^3`。两个局部位置可以独立选择分支，故形式乘积既可为 `+1` 也可为 `-1`。证书把此状态标为

```text
FAIL_BRANCH_INDEPENDENCE.
```

这不是 CT 值为零或非零；它证明旧 bare tangent expression 缺少使 pairing 良定义所必需的 cochain/denominator/full-cover 数据。`4230241*339106321=D` 及 `[D]` 是已知 MW 像，也不能修复定义域错误。

## 4. 修订稿现在严格证明什么

`PAPER_ELLIPTIC_TEX.tex/pdf` 已从 extended abstract 扩成五页证明稿，加入：

1. 支撑引理及赋值证明；
2. 好素数 Hasse--Hensel 引理及二元四次判别式；
3. 64 行、512 格矩阵的摘要，`384 YES + 128 NO`，以及两个旧证书的 SHA-256；
4. 两个精确 isogeny Selmer 群

   ```text
   Sel^(dual phi)(E'/Q) = <3,5,7>, dimension 3,
   Sel^phi(E/Q)         = <4230241,339106321>, dimension 2;
   ```

5. 二同源 rank 公式及 `rank E(Q)<=3` 中 `-2` 的两个可见核来源；
6. binary quartic `z(g)` 定义、`L=Q x K`、完整 `z_Q,z_K`、范数与 `d=35` 上同调投影；
7. 配对定义域纠错命题、分支失败表、严格的新 full-descent 闸门；
8. Cassels、Silverman、Fisher、van Beek--Fisher 和 Magma 手册引用。

编译日志没有 undefined reference、warning、overfull 或 underfull。PDF 渲染为五页，逐页检查没有裁切、重叠或不可读表格。

## 5. 真正剩余的精确对象

要判定 Campbell 类，下一轮不能再使用两侧的单个 squareclass。必须取得：

1. `Sel^2(E/Q)` 的完整基，以具有同一 `(I,J)` 的处处局部可解 binary quartics `g_i` 表示；
2. 每个 `g_i` 的完整 cubic invariant `z(g_i) in (Q x K)^*/square`，用它识别 `z(H)` 的群坐标；
3. 同域的完整配对 `pair([H],[g_i])`，使用 Fisher 2022 Theorem 3.1 的 `g1,g2,g3,m,gamma_1` 数据；或等价地，直接计算 `FourDescent(C_H)`。

官方 Magma 手册明确要求 `CasselsTatePairing(C,D)` 的两个输入都是映到同一椭圆曲线的处处局部可解 2-coverings，并说明 `FourDescent(C_H)=[]` 意味着没有局部可解 4-cover lift：[Magma descent documentation](https://magma.maths.usyd.edu.au/magma/handbook/text/1570)。本轮新增的 `PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m` 已冻结：

```text
AssociatedEllipticCurve(C_H)
TwoDescent(E_H)
CasselsTatePairing(C_H,covers[i])
FourDescent(C_H)
```

并打印完整模型、版本、所有 covers 和 pairing bits。但它尚未执行；没有 transcript，因此不产生数学结论。若 `FourDescent(C_H)` 为空，可严格推出 `C_H(Q)=empty`；若非空，只说明存在 Sel^4 lift，仍不推出有理点。

## 6. 不依赖 pairing 的低垂主定理备选

可立即整理成独立、有限、可重复的最小单元：

> Campbell 第九候选四次的 Jacobian 两侧 2-同源 Selmer 群分别为 `<3,5,7>` 与 `<4230241,339106321>`，故其有理秩至多 3；同时该处处局部可解 binary quartic 的完整 cubic-algebra 类在 `Q x Q(sqrt D)` 中为显式的 `(z_Q,z_K)`，其有理 2-挠投影为 35。

这个定理完全由支撑、好素数、512 格有限局部证书和整数恒等式组成，不依赖 Magma 或 CT pairing。它不解决九项问题，适合做短 computational note/主论文的严格 arithmetic appendix。投稿前仍需对“该特定 Campbell Jacobian 的 exact Selmer groups 是否已发表”做一次专门查重；当前文献检索只确认了方法来源，没有发现这一具体数值计算。

## 7. 文件与测试

新增：

- `PAPER_ELLIPTIC_ROUND_05_analysis.py`：conic/tangent、p-adic lifting、Hilbert symbol 与 branch audit；
- `PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json`：结构化纠错证书；
- `PAPER_ELLIPTIC_ROUND_05_test.py`：7 个第五轮测试；
- `PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m`：未执行的 full-2-descent / four-descent 输入；
- `PAPER_ELLIPTIC_ROUND_05_REPORT.md`：本报告。

更新：

- `PAPER_ELLIPTIC_TEX.tex`；
- `PAPER_ELLIPTIC_TEX.pdf`。

第五轮证书 SHA-256：

```text
af4f02e4e13f48f8e1ac5de22a0404da36c1a8dac7ec26e6144945f66e50968e
```

联合运行

```text
python -m unittest -v PAPER_ELLIPTIC_ROUND_05_test.py \
  PAPER_ELLIPTIC_ROUND_04_test.py \
  PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_NEXT_test.py
```

结果：**33 tests, OK**。

## 8. 下一轮建议

第一优先级不是继续手算 `L_35`，而是在可信本地 Magma 环境运行冻结的 full 2-descent：先保存版本、二进制 hash、完整 stdout/stderr 和所有 quartic models；再用结构化 `z(H)` 独立识别 `C_H` 类。若真实环境短期不可得，就投稿级收束第 6 节的 finite theorem，并单独查重，而不再承诺一个不存在的“唯一对侧 pairing bit”。
