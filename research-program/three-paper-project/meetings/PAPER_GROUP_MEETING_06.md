# 第六次论文组会：三篇论文的内部验收

日期：2026-09-03  
主持：导师（root）  
结论：三篇论文均通过组内数学与复现验收；Goal 因外部投稿信息未齐保持 `ACTIVE`

## 1. 统一验收结果

导师从仓库根目录重新执行三套冻结测试：

| 论文 | 测试 | 结果 | PDF |
|---|---:|---|---|
| 甲：七个连续整数的平方类模式 | 63 | PASS | 7 页 |
| 乙：纯三次域中的五项 AP 立方密度 | 18 | PASS | 4 页 |
| 丙：Campbell 四次的精确二同源下降 | 45 | PASS | 7 页 |
| **合计** | **126** | **全部通过** | **18 页** |

三份 PDF 均由 TeX Live 2022 `latexmk` 成功构建；最终日志没有 undefined
reference/citation、LaTeX warning、overfull 或 underfull。每稿均经另一位研究生独立
重算关键数学、隔离复现、编译和逐页目检。

## 2. 甲线：ACCEPT

论文暂题：*Square-class patterns of seven consecutive integers and an elementary
integral quartic*。

主定理：对非退化整数 `t`，若 `[t],...,[t+6]` 在 `Q*/Q*2` 中的 affine rank
至多 2，则真实平方类等值划分（模重标号与反射）属于显式列出的 23 个必要模式。
严格链为

`651 -> 343 -> 284 -> 98 -> 54 -> 35 -> 23`，

其中 `98` 前的箭头实际为 284 中由四连续因子排除 186；这里的记号只表示必要条件
筛，不宣称 23 个模式可实现，也不决定 `R_2(7)`。mask 77/89、102、108 的完整整数
点定理均已闭合。

终审：丙线 `ACCEPT`，无数学 blocking/major；两项 minor 已修，发布统一为
`paper-square-submission-v0.6.3`。最终 root manifest：

`E984110262B1A6AE0F19AF431826809B2A5870D327123CED93DBF8CF68A0BCBD`。

冻结 PDF：`PAPER_SQUARE_TEX/main.pdf`，SHA-256
`AF959B6B78F052AED2182C64BCD8193DF515A5627968EC76D947DAEEC4E79D68`。

## 3. 乙线：ACCEPT

论文暂题：*Five-Term Arithmetic Progressions and Cubes in a Pure Cubic Field*。

精确定义下的主定理为

\[
R^{\times}_{(3,1)}(5)=4.
\]

这里研究非恒定有理五项 AP；零项不计；允许一次公共有理缩放；所有被计项须在同一
非平凡纯三次域中成为立方。上界证明包括：

- `ker(Q*/Q*3 -> Q(cuberoot D)*/K*3)=<[D]>`；
- 243 个颜色词在平移、取负与反转下给 25 个轨道；
- 9 个轨道由三立方 AP 排除，1 个由 `P_5(3)=3` 排除；
- 余下 15 轨道由素数支撑引理化为 60 个模型，每个模型有表列良素数处无射影点证书。

下界由 `(-3,-1,1,3,5)` 在 `Q(cuberoot 3)` 的前四项给出。论文不声称分类全部
达到四项的 AP；那将涉及另 31 个有理点模型。

甲线独立重算全部 25 轨道、`9+1+15` 分割、四个方向和 60 格共 23520 个有限域参数
对，数学结论 `ACCEPT`。manifest 先覆盖后验证的阻断已修为纯只读 fail-closed，版本为
`1.0.0-rc2`。最终 manifest：

`00A042E39159C92976CE06BC3C54D90D69E70AA219D0D8CFC17B2A74E710AA7C`。

冻结 PDF：`PAPER_CUBE_KUMMER5_TEX.pdf`，SHA-256
`BA140E67DE083B00721DFF00E81B89B4C1B4D0433EB7EC3ABA1989E5C303B771`。

## 4. 丙线：ACCEPT

论文定位：Campbell 八项族某一第九候选四次的有限二同源下降短文。

严格主结果为

```text
Sel^(dual phi)(E'/Q) = <3,5,7>,               dim = 3,
Sel^phi(E/Q)         = <4230241,339106321>,   dim = 2,
rank E(Q) <= 3.
```

同时给出 `Q x Q(sqrt D)` 预解代数、范数、`[35]` 有理二挠投影、512 格局部矩阵及
same-`m` 处处局部证书。论文不声称完整 2-Selmer、Cassels--Tate 值、秩等号或
Campbell 第九项的有理点存在/不存在。

第五轮发现并撤回跨二同源两侧的错误 pairing 表达式。终修把旧字段从可提升的
Round04 clean v2 证书物理移除；未执行 Magma 输入保持
`mathematical_evidence_eligible=false`。乙线终审 `ACCEPT`，45 项在真实空目录隔离
环境中复现。最终 release manifest：

`BB5C06797331036D096A9CFB107771D56BAF35754267F7B999C03E52B9CDAC2F`。

冻结 PDF：`PAPER_ELLIPTIC_TEX.pdf`，SHA-256
`7A2FB6DD5F327F34BD393EE162BAE58B939D5EFCAE4728CA67CA3E522898A6DB`。

## 5. 期刊与声明边界

- 甲：Research in Number Theory 暂列首选，JNT 与条件性 EJC 为备选；INTEGERS
  因当前公开 AI 政策不兼容而排除。
- 乙：Research in Number Theory 暂列首选；INTEGERS 因当前公开 AI 政策不兼容而排除。
- 丙：Research in Number Theory 暂列首选，Journal of Number Theory 备选；INTEGERS
  与 JIS 因当前政策排除。
- 网络和精确方程检索只支持“未检索到相同已发表计算”，不构成 MathSciNet/zbMATH
  级的新颖性证明。提交前仍须作者人工完成数据库和引文链查重。

## 6. Goal 尚未完成的外部条件

三篇已经达到组内的数学、证明、代码、证书、测试、LaTeX/PDF 和投稿文案标准，但以下
条件不能由研究组代填：

1. 每篇真实作者姓名、单位、邮箱、ORCID 与通讯作者；
2. 资金、利益冲突、作者贡献和 AI 使用声明的人工确认；
3. 选择目标期刊并按其最新模板/政策终排；
4. 将各 supplement 精确 payload 存入公开稳定归档并取得 DOI/URL；
5. 作者对最终 PDF、公开数据与实际投稿的明确授权。

因此本次组会记录为 **INTERNAL ACCEPTANCE / EXTERNAL SUBMISSION PENDING**。
Goal 继续 `ACTIVE`，不以内部接受冒充已经公开归档或投稿。
