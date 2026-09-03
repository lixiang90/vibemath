# 甲组对丙线第四轮稿件的交叉审稿

审稿对象：`PAPER_ELLIPTIC_CAMPBELL_ROUND_04_REPORT.md`、
`PAPER_ELLIPTIC_ROUND_04_analysis.py`、JSON 证书、测试、Magma 输入及
`PAPER_ELLIPTIC_TEX.tex/pdf`。日期：2026-09-03。

## 总评

代码层面的主要算术结论可以接受：在采用报告所述标准二同源下降模型的
前提下，支撑枚举与好素数桥把旧的 8+4 ambient survivors 升级成了两侧
**精确 isogeny Selmer 群**；维数为 3、2，故 `rank E(Q) <= 3`。`Q x K`
分解、范数、64 缩放和 `d=35` 投影也均通过独立重算。

但是五页 TeX 目前只是 extended abstract，不是可投稿的证明稿；且
Cassels--Tate 闸门把“足以证明排除的非零结果”写得近似“做完一次即可
判定”，并把局部可解见证误称为已经准备好的配对局部点。以下 blocking
项修复前，不宜把 PDF 当作完成论文。

## Blocking

### B1. TeX 中没有精确 Selmer 定理的证明或可审计证书入口

`PAPER_ELLIPTIC_TEX.tex:66--86` 依次标记 `[proved]`，但没有 proof
环境，也没有给出：

- 带符号的 32+32 支撑类为何完备；
- 两侧的确切集合
  `S={infinity,2,3,5,7,59,71699,339106321}`；
- 512 格局部表、正见证、负证书或其稳定哈希；
- 24 个三进正见证与 32 个 `p=59,71699` 估值阻碍的统一证明；
- 从两 Kummer 商维数到 rank 的精确序列及 `-2` 项来源。

报告中有上述材料，代码也重算它们，但 PDF 既不包含也不引用这些附件。
因此 PDF 内的主定理当前是无证明断言。最低修复是把支撑引理和
Hasse--Hensel 引理完整证明写入正文，将 64 行表压缩为“每类首次阻碍/每个
survivor 的全部正见证”附录并绑定证书 SHA-256，最后写出标准二同源精确
序列。仅写 “the JSON certificate accompanies this draft” 不足以成为论文
证明。

### B2. Cassels--Tate 输入尚不是可执行的局部点证书

Round04 JSON 对 `d=35` 保存的是 `(U,V,rhs)` 加“`rhs` 是
`Q_p` 平方”的判据；它没有保存实际的 `N in Q_p`、所需精度、关联 conic
的坐标、全局 conic 点或切线 `L_35`。这些数据足以证明局部可解，从而用于
Selmer 成员资格，却不足以直接计算
`HilbertSymbol(L_35(P_v),e)_v`。报告第 6 节所称“全部局部点输入已从 JSON
逐格嵌入”应改成“全部局部可解见证已保存；配对坐标仍待构造”。

此外，`PAPER_ELLIPTIC_ROUND_04_two_cover_descent.m` 只打印
`TwoCoverDescent(CH)` 和两个目标整数；它不计算所列 pairing bits，也没有
把 Magma 返回类与结构化 `Q x K` 元素比较。故该文件目前只是候选输入，
不能作为配对审计脚本。

## Major

### M1. 好素数桥数学上成立，但正文陈述缺少必要限定

正确版本应先固定 `d` 为由 `b` 的素因子及 `-1` 支撑的平方自由代表，并令
`p` 为满足 `p not dividing 2b(a^2-4b)` 的有限素数。此时二元四次的判别式
为 `16b(a^2-4b)^2`，其**光滑射影模型**是几何连通 genus-one 曲线；Hasse
保证一个 `F_p` 点，光滑性/适当模型再由 Hensel 提升。TeX 的“all primes
outside ... are automatically locally soluble”省略了 `d`、有限素数及光滑
射影模型条件。报告版本基本完整，建议把该版本移入正文并说明这里给的是
充分的坏支撑集合，不是声称集合内每个素数都必有阻碍。

### M2. rank 公式正确，但须显示商群方向与 torsion 修正

当前命名方向是自洽的：E 上的 `x`-Kummer 类对应
`Sel^(dual phi)(E'/Q)`，E' 上的类对应 `Sel^phi(E/Q)`。应在正文明确

`rank E(Q) = dim E(Q)/dual_phi E'(Q)
             + dim E'(Q)/phi E(Q) - 2`,

再以两个 Mordell--Weil 商嵌入对应 Selmer 群得到上界。`-2` 不能只称为
“standard formula”，应解释来自两侧可见有理 2-挠 Kummer 像。否则读者
容易怀疑群名被反置或遗漏 torsion 项。

### M3. `Q x K` 与 `d=35` 算术正确，cohomological map 尚未写出

独立检查确认：

- `D=59*71699*339106321` 平方自由且 `D=1 mod 4`；
- 二次预解因子的判别式是 `12288^2 D`，两根为
  `-134689011712 +/- 6144 sqrt(D)`；
- `z_Q=35*16257024^2`，约化 K 分量的范数为
  `35*15915620907648^2`，总 étale 范数确为所列平方；
- `x_big=64^2 x_small`、`y_big=64^3 y_small` 及平移得到报告中的 E；
- 有理预解分量确投影到 `[X]=35`。

但 TeX 没有定义 binary-quartic `z(H)`、预解代数、从
`H^1(Q,E[2])` 到有理 2-挠 Kummer 分量的映射，也没有证明所用符号约定。
需要给出推导或原始引用；否则 proposition 只是一串可验整数，不能支持
“Campbell class projects to d=35”的上同调结论。报告正确保留了 K 分量，
没有犯“有理投影等于完整 torsor”的错误。

### M4. pairing 决策是单向的，摘要的“一次计算”措辞过强

若任一 `<35,e>_CT` 非零，则 35 不在 Mordell--Weil Kummer 像；结合
投影必要性，可严格推出 `C_H(Q)=empty`。这一**非零分支**是正确的。
反之，两个值为零并不自动证明 35 来自 Mordell--Weil，也不判定 `C_H`；
还可能需要完整 Selmer/二覆盖提升分析。摘要第 21 行“left conditional on
one explicit ... computation”以及报告所称“精确剩余阻断”应改成“下一项
可能给出排除的单向闸门”。

另外 `4230241*339106321` 的平方类是 `D`，而 `[D]` 已在 E' 的已知
torsion Kummer 像中，所以这两个 pairing 值只有一个独立 bit；可以保留两
项作一致性检查，但应断言并测试二者相等，而不是仅说“相关”。

### M5. Selmer 与配对理论完全缺少引用

TeX 无 bibliography。支撑引理、二同源覆盖方程、rank 公式、二同源
Cassels--Tate 配对的 radical/局部 Hilbert-symbol 公式都应给原始或标准
权威来源。尤其 `prod_v (L_35(P_v),e)_v` 依赖具体 conic 与切线归一化，
在该对象未定义前不能作为已建立的“标准显式公式”。

## Minor

1. TeX 第 103 行使用 `proposition [open computation; not a theorem]` 自相
   矛盾；应改成 remark/problem，不放在 theorem 环境。
2. “supported on b”应写成“supported on `-1` and the prime divisors of
   `b`”，以对应实际的 32 个带符号候选。
3. 标题 “Eight-Term Family” 与正文 “ninth term / g_m(8)”容易造成索引
   歧义，应在首段说明八个已知项与第九候选的编号约定。
4. 正文应列出 `E'` 的构造公式
   `a'=-2a, b'=a^2-4b`，而不只给数值。
5. `K` 的计算使用 Q-基 `(1,sqrt D)`，不是整数基；报告已说明
   `O_K=Z[(1+sqrt D)/2]`，TeX 也应保留这句，避免把系数整性误读为整数环
   坐标。
6. PDF 日志无 undefined、overfull 或 underfull；排版层面没有阻断。

## 复跑与可接受结论

执行

```text
python -m unittest -v PAPER_ELLIPTIC_ROUND_04_test.py \
  PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_NEXT_test.py
```

结果 **26/26, OK**。可接受结论限于：

- 512 个所需实/坏位单元已严格分成 YES/NO；
- 好素数 Hasse--Hensel 桥与支撑引理使 8+4 成为精确的两同源 Selmer
  群，而非仅 ambient survivor 集；
- 两群维数 3、2，`rank E(Q)<=3`；
- `Q x K` 算术、范数条件、64 缩放与 `d=35` 有理 2-挠投影；
- 配对状态仍为 `UNKNOWN_FAIL_CLOSED`，`C_H(Q)` 未判定。

建议下一轮只做两件事：先把 B1 的证明与证书摘要写入论文；再为 `d=35`
构造真正的 conic/tangent/local-coordinate 证书，并把“非零即排除、零则仍
未决”写进解析器和测试。

