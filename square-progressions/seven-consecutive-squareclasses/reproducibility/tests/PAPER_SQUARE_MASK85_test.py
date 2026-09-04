import json
from collections import Counter, defaultdict
from math import isqrt
from pathlib import Path
import unittest

import PAPER_SQUARE_MASK85 as gate
import sympy as sp


ROOT = Path(__file__).resolve().parent
SOURCE_CERTIFICATES = (
    "PAPER_SQUARE_MASK54_CERTIFICATE.json",
    "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json",
    "STUDENT_SQUARE_ROUND_02_certificate.json",
)


def source_certificate(name):
    """Load a predecessor certificate in either flat staging or the source tree."""
    path = ROOT / name
    if not path.is_file():
        path = ROOT.parent.parent / "certificates" / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def predecessor_data():
    return tuple(source_certificate(name) for name in SOURCE_CERTIFICATES)


def source_rows():
    mask54, round4, _ = predecessor_data()
    pattern_ids = mask54["pattern_impact"]["remaining_pattern_ids"]
    wanted = set(pattern_ids)
    rows = [
        row for row in round4["pattern_occurrences"]
        if row["pattern_id"] in wanted
    ]
    return pattern_ids, rows


def mask_support(mask):
    return [position for position in range(7) if (mask >> position) & 1]


def constant_pairing(mask):
    roots = mask_support(mask)
    if len(roots) != 4:
        return None
    first = roots[0]
    for mate in roots[1:]:
        left = [first, mate]
        right = [root for root in roots if root not in left]
        if sum(left) == sum(right):
            return {
                "left": left,
                "right": right,
                "difference_right_minus_left": (
                    right[0] * right[1] - left[0] * left[1]
                ),
            }
    return None


class Mask85Tests(unittest.TestCase):
    def test_authoritative_input_and_fifteen_characters(self):
        pattern_ids, rows = source_rows()
        self.assertEqual(pattern_ids, [12, 31, 134, 276])
        self.assertEqual([row["pattern_id"] for row in rows], pattern_ids)
        self.assertEqual(len(rows), 4)
        for row in rows:
            masks = [item["character_mask_m"] for item in row["occurrences"]]
            self.assertEqual(len(masks), 15)
            self.assertEqual(len(set(masks)), 15)

    def test_independent_occurrence_inventory(self):
        _, rows = source_rows()
        counter = Counter()
        hit_ids = defaultdict(set)
        genus = {}
        for row in rows:
            for occurrence in row["occurrences"]:
                mask = occurrence["character_mask_m"]
                counter[mask] += 1
                hit_ids[mask].add(row["pattern_id"])
                genus[mask] = occurrence["genus"]

        pairable = []
        for mask in sorted(hit_ids):
            pairing = constant_pairing(mask)
            if genus[mask] == 1 and pairing is not None:
                pairable.append((
                    mask,
                    len(hit_ids[mask]),
                    abs(pairing["difference_right_minus_left"]),
                    sorted(hit_ids[mask]),
                ))
        pairable.sort(key=lambda row: (-row[1], row[2], row[0]))

        self.assertEqual(sum(counter.values()), 60)
        self.assertEqual((len(counter), sum(genus[m] == 1 for m in counter)), (37, 19))
        self.assertEqual(
            pairable,
            [(85, 2, 8, [31, 276]), (27, 1, 3, [12]), (45, 1, 6, [134])],
        )

    def test_mask85_geometry_and_occurrences(self):
        _, rows = source_rows()
        occurrences = [
            occurrence
            for row in rows
            for occurrence in row["occurrences"]
            if occurrence["character_mask_m"] == 85
        ]
        self.assertEqual(mask_support(85), [0, 2, 4, 6])
        self.assertEqual(
            constant_pairing(85),
            {"left": [0, 6], "right": [2, 4], "difference_right_minus_left": 8},
        )
        self.assertEqual(
            [row["occurrence_id"] for row in occurrences],
            ["P31:m85", "P276:m85"],
        )
        self.assertTrue(all(row["same_t_map"] == "t=(2*U_m+(0)*Z_m)/(0*U_m+(1)*Z_m)"
                            for row in occurrences))

    def test_centered_pairing_identities_are_polynomial(self):
        t, x = sp.symbols("t x")
        target = t * (t + 2) * (t + 4) * (t + 6)
        A = x ** 2 - 9
        B = x ** 2 - 1
        centered = sp.expand(target.subs(t, x - 3))
        self.assertTrue(sp.Poly(sp.expand(centered - A * B), x).is_zero)
        self.assertTrue(sp.Poly(sp.expand(B - A - 8), x).is_zero)
        self.assertTrue(sp.Poly(sp.expand(A + 9 - x ** 2), x).is_zero)

    def test_complete_middle_interval_and_degeneracy(self):
        data = gate.integral_point_certificate()
        self.assertEqual(
            [(row["t"], row["rhs"], row["ys"])
             for row in data["middle_interval_exact_check"]],
            [(-6, 0, [0]), (-5, -15, []), (-4, 0, [0]),
             (-3, 9, [-3, 3]), (-2, 0, [0]), (-1, -15, []), (0, 0, [0])],
        )
        self.assertEqual(
            data["proved_integral_points"],
            [[-6, 0], [-4, 0], [-3, -3], [-3, 3], [-2, 0], [0, 0]],
        )
        self.assertEqual(data["nondegenerate_integral_points"], [])
        self.assertTrue(all(
            0 <= row["zero_position_in_original_block"] <= 6
            for row in data["degeneracy_in_original_seven_term_block"]
        ))

    def test_both_squarefree_branches_are_exhaustive(self):
        def is_squarefree(value):
            return all(value % (prime * prime) for prime in range(2, isqrt(value) + 1))

        kernels = [d for d in range(1, 9) if 8 % d == 0 and is_squarefree(d)]
        derived = {}
        for d in kernels:
            quotient = 8 // d
            rows = []
            for left in range(1, quotient + 1):
                if quotient % left:
                    continue
                right = quotient // left
                if left > right or (left + right) % 2:
                    continue
                rows.append({
                    "factor_pair": [left, right],
                    "U_V": [(right - left) // 2, (right + left) // 2],
                })
            derived[d] = rows
        self.assertEqual(
            derived,
            {
                1: [{"factor_pair": [2, 4], "U_V": [1, 3]}],
                2: [{"factor_pair": [2, 2], "U_V": [0, 2]}],
            },
        )

        data = gate.integral_point_certificate()
        self.assertEqual(data["common_positive_squarefree_kernels"], kernels)
        branches = {row["d"]: row for row in data["branches"]}
        self.assertEqual(branches[1]["positive_same_parity_factor_pairs"], [[2, 4]])
        self.assertEqual(branches[1]["forced_U_V"], [1, 3])
        self.assertNotIn(10 % 8, branches[1]["squares_mod_8"])
        self.assertEqual(branches[2]["nonnegative_same_parity_factor_pairs"], [[2, 2]])
        self.assertEqual(branches[2]["forced_U_V"], [0, 2])

    def test_no_search_or_mordell_weil_is_promoted(self):
        data = gate.integral_point_certificate()
        self.assertFalse(data["bounded_search_used"])
        self.assertFalse(data["mordell_weil_used"])
        self.assertIn("rational square", data["rational_y_is_integral_note"])

    def test_exact_pattern_impact_and_partitions(self):
        mask54, round4, round2 = predecessor_data()
        pattern_ids = mask54["pattern_impact"]["remaining_pattern_ids"]
        wanted = set(pattern_ids)
        rows = {
            row["pattern_id"]: row
            for row in round4["pattern_occurrences"]
            if row["pattern_id"] in wanted
        }
        partitions = {
            pattern_id: round2["unresolved_patterns_ranked"][pattern_id]["partition"]
            for pattern_id in pattern_ids
        }
        self.assertEqual(
            {pattern_id: rows[pattern_id]["partition"] for pattern_id in pattern_ids},
            partitions,
        )

        occurrence_hits = sorted(
            pattern_id for pattern_id, row in rows.items()
            if any(item["character_mask_m"] == 85 for item in row["occurrences"])
        )
        support = mask_support(85)
        xor_values = {
            pattern_id: self._xor(partition[position] for position in support)
            for pattern_id, partition in partitions.items()
        }
        xor_hits = sorted(pattern_id for pattern_id, value in xor_values.items() if value == 0)
        survivors = sorted(wanted - set(occurrence_hits))
        words = {
            pattern_id: "".join(str(label) for label in partition)
            for pattern_id, partition in partitions.items()
        }

        self.assertEqual(xor_values, {12: 1, 31: 0, 134: 1, 276: 0})
        self.assertEqual(occurrence_hits, xor_hits)
        self.assertEqual(occurrence_hits, [31, 276])
        self.assertEqual([words[i] for i in occurrence_hits], ["0001202", "0010203"])
        self.assertEqual(survivors, [12, 134])
        self.assertEqual([words[i] for i in survivors], ["0012202", "0012131"])

    @staticmethod
    def _xor(values):
        result = 0
        for value in values:
            result ^= value
        return result

    def test_disk_certificate(self):
        with gate.OUTPUT.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), gate.build_certificate())


if __name__ == "__main__":
    unittest.main()
