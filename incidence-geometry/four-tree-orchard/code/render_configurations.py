"""Render the record-setting n=59 and n=60 configurations as exact SVGs."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from verify_construction import admissible_pairs, intervals, rational_points


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "docs" / "assets"
WIDTH, HEIGHT = 760, 620
LEFT, RIGHT, TOP, BOTTOM = 64, 724, 42, 568


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def render(n: int) -> str:
    families = rational_points(n)
    pairs = list(admissible_pairs(n))
    a_set, b_set, c_set, d_set = intervals(n)
    x_max = max(point[0] for family in families for point in family) * Fraction(11, 10)
    y_values = [point[1] for family in families for point in family]
    y_min = min(y_values) * Fraction(11, 10)
    y_max = max(y_values) * Fraction(11, 10)

    def project(point: tuple[Fraction, Fraction]) -> tuple[float, float]:
        x, y = point
        px = LEFT + float(x / x_max) * (RIGHT - LEFT)
        py = TOP + float((y_max - y) / (y_max - y_min)) * (BOTTOM - TOP)
        return px, py

    p_points, q_points, r_points, s_points = families
    x0, y0 = project((Fraction(0), Fraction(0)))
    x_diag, y_diag = project((min(x_max, y_max), min(x_max, y_max)))
    x_anti, y_anti = project((min(x_max, -y_min), -min(x_max, -y_min)))

    line_rows = []
    highlighted = pairs[len(pairs) // 2]
    for x, y in pairs:
        w = x - y
        q = (Fraction(0), Fraction(1, n + y))
        s = (Fraction(1, 2 * n + w), -Fraction(1, 2 * n + w))
        qx, qy = project(q)
        sx, sy = project(s)
        css_class = "four-line highlighted" if (x, y) == highlighted else "four-line"
        line_rows.append(
            f'    <path class="{css_class}" d="M{fmt(qx)} {fmt(qy)}L{fmt(sx)} {fmt(sy)}" />'
        )

    point_rows = []
    for family_name, points in zip(("A", "B", "C", "D"), families):
        for point in points:
            px, py = project(point)
            point_rows.append(
                f'    <circle class="point family-{family_name.lower()}" cx="{fmt(px)}" cy="{fmt(py)}" r="3" />'
            )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">The n={n} four-supporting-line configuration</title>
  <desc id="desc">All {n} points and all {len(pairs)} certified four-point lines, shown after an affine rescaling. The four point families have sizes {len(a_set)}, {len(b_set)}, {len(c_set)}, and {len(d_set)}.</desc>
  <style>
    .frame {{ fill: #081523; stroke: #31475b; stroke-width: 1; }}
    .grid {{ fill: none; stroke: #193044; stroke-width: 1; }}
    .support {{ fill: none; stroke: #7e94a8; stroke-width: 1.4; stroke-dasharray: 6 6; }}
    .four-line {{ fill: none; stroke: #ffcb66; stroke-width: .85; stroke-opacity: .17; }}
    .four-line.highlighted {{ stroke-width: 2.3; stroke-opacity: .95; }}
    .point {{ stroke: #07111f; stroke-width: 1; }}
    .family-a {{ fill: #79c8ff; }} .family-b {{ fill: #73e0b0; }}
    .family-c {{ fill: #ffcb66; }} .family-d {{ fill: #f49aaf; }}
  </style>
  <rect class="frame" x="1" y="1" width="758" height="618" rx="16" />
  <g class="grid">
    <path d="M{LEFT} 174H{RIGHT}M{LEFT} 305H{RIGHT}M{LEFT} 437H{RIGHT}" />
    <path d="M229 {TOP}V{BOTTOM}M394 {TOP}V{BOTTOM}M559 {TOP}V{BOTTOM}" />
  </g>
  <g class="support">
    <path d="M{LEFT} {fmt(y0)}H{RIGHT}" />
    <path d="M{fmt(x0)} {TOP}V{BOTTOM}" />
    <path d="M{fmt(x0)} {fmt(y0)}L{fmt(x_diag)} {fmt(y_diag)}" />
    <path d="M{fmt(x0)} {fmt(y0)}L{fmt(x_anti)} {fmt(y_anti)}" />
  </g>
  <g>{chr(10).join(line_rows)}
  </g>
  <g>{chr(10).join(point_rows)}
  </g>
</svg>
'''


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for n in (59, 60):
        destination = OUTPUT / f"four-tree-orchard-{n}.svg"
        destination.write_text(render(n), encoding="utf-8", newline="\n")
        print(f"wrote {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
