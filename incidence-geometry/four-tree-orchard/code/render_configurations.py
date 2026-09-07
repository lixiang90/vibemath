"""Render the record-setting n=59 and n=60 configurations as exact SVGs."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from verify_construction import admissible_pairs, intervals, rational_points


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "docs" / "assets"
WIDTH, HEIGHT = 760, 620
LEFT, RIGHT, TOP, BOTTOM = 64, 724, 42, 568
PROJECTIVE_OFFSETS = {
    # These half-integral offsets spread the point families without sending a
    # selected point to infinity.  They are presentation choices only.
    59: (Fraction(-11, 2), Fraction(-18)),
    60: (Fraction(-11, 2), Fraction(-41, 2)),
}


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def clip_line(
    first: tuple[float, float], second: tuple[float, float]
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Clip the infinite line through two points to the plotting rectangle."""

    x1, y1 = first
    dx, dy = second[0] - x1, second[1] - y1
    candidates: list[tuple[float, float]] = []
    if dx:
        for x in (LEFT, RIGHT):
            t = (x - x1) / dx
            y = y1 + t * dy
            if TOP - 1e-7 <= y <= BOTTOM + 1e-7:
                candidates.append((x, y))
    if dy:
        for y in (TOP, BOTTOM):
            t = (y - y1) / dy
            x = x1 + t * dx
            if LEFT - 1e-7 <= x <= RIGHT + 1e-7:
                candidates.append((x, y))
    unique = []
    for point in candidates:
        if not any(abs(point[0] - old[0]) < 1e-6 and abs(point[1] - old[1]) < 1e-6 for old in unique):
            unique.append(point)
    if len(unique) != 2:
        raise ValueError(f"expected two boundary intersections, got {unique}")
    return unique[0], unique[1]


def render(n: int) -> str:
    families = rational_points(n)
    pairs = list(admissible_pairs(n))
    a_set, b_set, c_set, d_set = intervals(n)
    p_offset, q_offset = PROJECTIVE_OFFSETS[n]
    alpha = 3 * n - p_offset
    beta = n - q_offset

    def transform(point: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        """Apply [x:y:1] -> [x:y:1-alpha*x-beta*y]."""

        x, y = point
        denominator = 1 - alpha * x - beta * y
        if not denominator:
            raise ValueError("a selected point was sent to infinity")
        return x / denominator, y / denominator

    transformed_families = [[transform(point) for point in family] for family in families]
    transformed_points = [point for family in transformed_families for point in family]
    x_values = [point[0] for point in transformed_points] + [Fraction(0)]
    y_values = [point[1] for point in transformed_points] + [Fraction(0)]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    x_padding = (x_max - x_min) * Fraction(7, 100)
    y_padding = (y_max - y_min) * Fraction(8, 100)
    x_min, x_max = x_min - x_padding, x_max + x_padding
    y_min, y_max = y_min - y_padding, y_max + y_padding

    def canvas(point: tuple[Fraction, Fraction]) -> tuple[float, float]:
        x, y = point
        px = LEFT + float((x - x_min) / (x_max - x_min)) * (RIGHT - LEFT)
        py = TOP + float((y_max - y) / (y_max - y_min)) * (BOTTOM - TOP)
        return px, py

    line_rows = []
    highlighted = pairs[len(pairs) // 2]
    for x, y in pairs:
        w = x - y
        q = (Fraction(0), Fraction(1, n + y))
        s = (Fraction(1, 2 * n + w), -Fraction(1, 2 * n + w))
        first, second = clip_line(canvas(transform(q)), canvas(transform(s)))
        css_class = "four-line highlighted" if (x, y) == highlighted else "four-line"
        line_rows.append(
            f'    <path class="{css_class}" d="M{fmt(first[0])} {fmt(first[1])}L{fmt(second[0])} {fmt(second[1])}" />'
        )

    point_rows = []
    for family_name, points in zip(("A", "B", "C", "D"), transformed_families):
        for point in points:
            px, py = canvas(point)
            point_rows.append(
                f'    <circle class="point family-{family_name.lower()}" cx="{fmt(px)}" cy="{fmt(py)}" r="3.4" />'
            )

    support_rows = []
    origin = canvas((Fraction(0), Fraction(0)))
    for direction in ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1))):
        first, second = clip_line(origin, canvas(direction))
        support_rows.append(
            f'    <path d="M{fmt(first[0])} {fmt(first[1])}L{fmt(second[0])} {fmt(second[1])}" />'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">The n={n} four-supporting-line configuration</title>
  <desc id="desc">All {n} points and all {len(pairs)} certified four-point lines, spread out by an exact projective transformation followed by an affine rescaling. The four point families have sizes {len(a_set)}, {len(b_set)}, {len(c_set)}, and {len(d_set)}.</desc>
  <style>
    .frame {{ fill: #081523; stroke: #31475b; stroke-width: 1; }}
    .support {{ fill: none; stroke: #7e94a8; stroke-width: 1.25; stroke-dasharray: 7 7; stroke-opacity: .82; }}
    .four-line {{ fill: none; stroke: #ffcb66; stroke-width: 2.0; stroke-opacity: .195; }}
    .four-line.highlighted {{ stroke-width: 2.2; stroke-opacity: .92; }}
    .point {{ stroke: #07111f; stroke-width: 1.15; }}
    .family-a {{ fill: #79c8ff; }} .family-b {{ fill: #73e0b0; }}
    .family-c {{ fill: #ffcb66; }} .family-d {{ fill: #f49aaf; }}
  </style>
  <rect class="frame" x="1" y="1" width="758" height="618" rx="16" />
  <g class="support">{chr(10).join(support_rows)}
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
