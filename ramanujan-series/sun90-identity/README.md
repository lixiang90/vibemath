# Sun's ninety-dollar series for $1/\pi$ / 孙智伟的 90 美元级数

**Author / 作者：李想 (Li Xiang).** Public preprint with exact computational
certificates / 公开预印本及精确计算证书。

The identity is Sun's Conjecture 5, equation (5.9):

$$
\sum_{n=0}^{\infty}\frac{357n+103}{2160^n}\binom{2n}{n}
\sum_{k=0}^{n}\binom{n}{k}\binom{n+2k}{2k}\binom{2k}{k}
(-324)^{n-k}=\frac{90}{\pi}.
$$

Source / 原始出处：
[Z.-W. Sun, arXiv:1102.5649v47](https://arxiv.org/html/1102.5649v47).
The equivalent normalized formula appears as (4.3) in
[van Hoeij–Tsai–Ye, arXiv:2410.19289v2](https://arxiv.org/html/2410.19289v2).

## English

The [paper](paper/main.pdf) gives a proof using a bivariate generating
function, a restriction and gradient identity, an algebraic transformation
to a level-60 modular form, and a CM evaluation obtained by differentiating
the Fricke transformation. Independent eta-product and Sturm certificates
establish the required modular parametrization and degree-seven modular
equation.

The exact programs check coefficient identities, differential operators,
jet multipliers, modular-form Fourier coefficients through the complete
Sturm bounds, rational CM root isolation, algebraic constants, and a
convergence majorant. The paper supplies the standard eta-quotient,
Sturm, and Fricke theory and the arguments for holomorphy, branches,
analytic continuation, and convergence.

OpenAI Codex assisted with symbolic exploration, proof organization,
verification programs, and manuscript preparation; 李想 is the named
author. The original manuscript was emailed to Professor Sun on
16 October 2026. This public revision has not been separately sent to him.
The preprint has not undergone external peer review. Priority, eligibility
for the prize, and payment have not been confirmed.

## 中文

[论文](paper/main.pdf)通过二元生成函数、限制曲线与梯度恒等式，
把原级数转化为 60 级模形式，再由 Fricke 变换微分求出所需 CM 值。
独立的 η 乘积与 Sturm 证书验证一般模参数化和七次模方程。

程序精确检查系数恒等式、微分算子、jet 乘子、完整 Sturm 界内的
模形式 Fourier 系数、有理区间中的 CM 根、代数常数和收敛上界。
标准 η 商、Sturm、Fricke 理论，以及全纯性、分支、解析延拓和
收敛论证，由论文正文给出。

OpenAI Codex 协助了符号探索、证明组织、验证程序及文稿准备，
署名作者为李想。原稿已于 **2026 年 10 月 16 日**邮件提交孙教授；
当前公开修订稿没有另行发送给他。本文尚未经过外部同行审查，
首次性、领奖资格及奖金支付均未获确认。

## Reproduce / 复现

Requirements / 全部计算依赖：**Python >= 3.9 and SymPy 1.14.0**.
Run from the repository root / 在仓库根目录运行：

```powershell
python -m pip install sympy==1.14.0
python ramanujan-series/sun90-identity/verify.py
```

The entry point runs all exact certificate components without changing
tracked files. A successful run is recorded in
`reproducibility/full_verification.json`. To regenerate that record, add
`--report reproducibility/full_verification.json` to the verification command.
The mathematical text remains part of the proof / 默认核验不改变仓库文件；
已保存的完整记录可用上述 `--report` 参数更新。论文中的理论论证也是证明的一部分。

| Path / 路径 | Contents / 内容 |
|---|---|
| [paper/main.pdf](paper/main.pdf) | Public preprint / 公开论文 |
| [paper/main.tex](paper/main.tex) | LaTeX source / 论文源码 |
| [code/](code/) | Exact verification programs / 精确验证程序 |
| [certificates/](certificates/) | Jet and modular-equation data / jet 与模方程数据 |
| [reproducibility/full_verification.json](reproducibility/full_verification.json) | Recorded complete verification / 完整验证记录 |

XeLaTeX build instructions are in the repository's
[reproducibility guide](../../REPRODUCIBILITY.md) /
XeLaTeX 构建方法见仓库[复现说明](../../REPRODUCIBILITY.md)。
