"""Generate rational parameters on Spearman's quartic by exact chord closure."""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction

from magic_square_search import certified_center_progressions, search_curve
from spearman_kummer import spearman_specialization, squarefree_model


QuarticPoint = tuple[Fraction, Fraction]


def on_spearman_quartic(point: QuarticPoint) -> bool:
    t, w = point
    return w * w == 9 * t**4 + 4 * t**2 + 36


def fourth_intersection(points: tuple[QuarticPoint, QuarticPoint, QuarticPoint]) -> QuarticPoint | None:
    """Fourth intersection with the quadratic through three distinct t-values."""
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    if len(set(xs)) != 3:
        raise ValueError("This chord helper requires three distinct t-values")

    a = b = c = Fraction(0)
    for index in range(3):
        others = [item for item in range(3) if item != index]
        j, k = others
        denominator = (xs[index] - xs[j]) * (xs[index] - xs[k])
        a += ys[index] / denominator
        b -= ys[index] * (xs[j] + xs[k]) / denominator
        c += ys[index] * xs[j] * xs[k] / denominator

    leading = a * a - 9
    if leading == 0:
        # The fourth intersection is at infinity.
        return None
    x4 = -2 * a * b / leading - sum(xs, Fraction(0))
    y4 = a * x4 * x4 + b * x4 + c
    result = x4, y4
    if not on_spearman_quartic(result):
        raise ArithmeticError("Fourth-intersection formula left the quartic")
    return result


def generate_quartic_points(rounds: int = 3, max_component: int = 10**12) -> set[QuarticPoint]:
    """Close small seed points under distinct-point quadratic intersections."""
    points: set[QuarticPoint] = {
        (Fraction(0), Fraction(6)),
        (Fraction(0), Fraction(-6)),
        (Fraction(1), Fraction(7)),
        (Fraction(1), Fraction(-7)),
        (Fraction(2), Fraction(14)),
        (Fraction(2), Fraction(-14)),
    }
    processed: set[tuple[QuarticPoint, QuarticPoint, QuarticPoint]] = set()
    for _ in range(rounds):
        new_points: set[QuarticPoint] = set()
        for triple in itertools.combinations(sorted(points), 3):
            if len({point[0] for point in triple}) != 3 or triple in processed:
                continue
            processed.add(triple)
            result = fourth_intersection(triple)
            if result is None:
                continue
            components = (
                abs(result[0].numerator),
                result[0].denominator,
                abs(result[1].numerator),
                result[1].denominator,
            )
            if max(components) > max_component:
                continue
            new_points.add(result)
            new_points.add((result[0], -result[1]))
        points.update(new_points)
    return points


def canonical_parameter(point: QuarticPoint) -> QuarticPoint | None:
    """Quotient by t -> -t, w -> -w, and (t,w) -> (2/t,2w/t^2)."""
    t, w = abs(point[0]), abs(point[1])
    if t == 0:
        return None
    partner = (2 / t, 2 * w / (t * t))
    return min((t, w), partner, key=lambda item: item[0])


def parameter_orbits(points: set[QuarticPoint]) -> list[QuarticPoint]:
    representatives = {
        representative
        for point in points
        if (representative := canonical_parameter(point)) is not None
    }
    return sorted(representatives)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--max-component", type=int, default=10**12)
    parser.add_argument("--search-box", type=int, default=0)
    args = parser.parse_args()
    points = generate_quartic_points(args.rounds, args.max_component)
    orbits = parameter_orbits(points)
    print(f"quartic points={len(points)}, essential nonzero orbits={len(orbits)}")
    for t, w in orbits:
        data = spearman_specialization(t.numerator, t.denominator, w)
        model = squarefree_model(data)
        print(
            f"t={t}, w={w}, D={model.d}, scale={model.scale_root}, "
            f"digits(n)={len(str(data.n))}"
        )
        if args.search_box:
            centers, candidates = search_curve(
                model.d, model.points, box=args.search_box, minimum_squares=7
            )
            progressions = certified_center_progressions(centers)
            print(
                f"  box={args.search_box}: centers={len(centers)}, "
                f"center_APs={len(progressions)}, seven_square={len(candidates)}"
            )


if __name__ == "__main__":
    main()
