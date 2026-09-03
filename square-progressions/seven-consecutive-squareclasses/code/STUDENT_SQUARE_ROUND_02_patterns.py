"""Finite pattern reduction for the question R_2(7)=6 or 7.

The script performs only exact combinatorics and necessary local screens.  It
does not use a height bound and it does not claim that points on different
character quotients are compatible.  All JSON fields distinguish strict
eliminations from unresolved patterns and heuristic difficulty data.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from itertools import combinations


N = 7


def restricted_growth_strings(n: int, blocks: int):
    """Yield set partitions as canonical restricted-growth strings."""
    word = [0] * n

    def visit(pos: int, current_max: int):
        if pos == n:
            if current_max + 1 == blocks:
                yield tuple(word)
            return
        for value in range(min(current_max + 1, blocks - 1) + 1):
            word[pos] = value
            yield from visit(pos + 1, max(current_max, value))

    yield from visit(1, 0)


def canonical_partition(word: tuple[int, ...]) -> tuple[int, ...]:
    """Forget block names, retaining only the set partition."""
    names: dict[int, int] = {}
    result = []
    for value in word:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def reflection_canonical(word: tuple[int, ...]) -> tuple[int, ...]:
    reflected = canonical_partition(tuple(reversed(word)))
    return min(word, reflected)


def label_value(block: int) -> int:
    # For 3 blocks use 00,01,10; for 4 use all of F_2^2.  Every permutation
    # of three or four points is induced by AGL(2,2) ~= S_4, so an unlabeled
    # set partition is exactly an AGL orbit.
    return block


def endpoint_six_windows_have_rank_two(word: tuple[int, ...]) -> bool:
    # R_1(6)=5 excludes a six-term window supported on <=2 labels.
    return len(set(word[:6])) >= 3 and len(set(word[1:])) >= 3


def strict_pattern_reasons(word: tuple[int, ...]) -> tuple[str, ...]:
    """Known global theorems that rule out a label partition."""
    reasons = []
    if not endpoint_six_windows_have_rank_two(word):
        reasons.append(
            "one endpoint six-term window uses at most two squareclasses, contradicting R_1(6)=5"
        )
    for block in sorted(set(word)):
        positions = tuple(i for i, value in enumerate(word) if value == block)
        if len(positions) > 4:
            reasons.append(
                f"block {block} has {len(positions)} positions, contradicting Q(7)=4"
            )
        elif len(positions) == 4:
            gaps = tuple(positions[i + 1] - positions[i] for i in range(3))
            if gaps[0] == gaps[2]:
                reasons.append(
                    f"block {block} occupies symmetric four-square pattern {positions}, excluded by Gonzalez-Jimenez--Xarles Proposition 5"
                )
    return tuple(reasons)


def relation_space(word: tuple[int, ...]) -> tuple[int, ...]:
    """Return W={e: sum e_i=0 and sum e_i label_i=0} as bit masks."""
    labels = [label_value(block) for block in word]
    relations = []
    for mask in range(1 << N):
        if mask.bit_count() % 2:
            continue
        xor_label = 0
        for i, label in enumerate(labels):
            if mask >> i & 1:
                xor_label ^= label
        if xor_label == 0:
            relations.append(mask)
    return tuple(relations)


def f2_rank(masks: list[int]) -> int:
    basis: dict[int, int] = {}
    for mask in masks:
        x = mask
        while x:
            p = x.bit_length() - 1
            if p not in basis:
                basis[p] = x
                break
            x ^= basis[p]
    return len(basis)


def relation_basis(relations: tuple[int, ...]) -> tuple[int, ...]:
    basis: dict[int, int] = {}
    for relation in relations:
        x = relation
        while x:
            p = x.bit_length() - 1
            if p not in basis:
                basis[p] = x
                break
            x ^= basis[p]
    return tuple(basis[p] for p in sorted(basis, reverse=True))


def discriminant_for_roots(indices: tuple[int, ...]) -> int:
    disc = 1
    for i, j in combinations(indices, 2):
        disc *= (j - i) ** 2
    return disc


def prime_factors(n: int) -> tuple[int, ...]:
    factors = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        factors.append(n)
    return tuple(factors)


def legendre_is_square(value: int, prime: int) -> bool:
    value %= prime
    return value == 0 or pow(value, (prime - 1) // 2, prime) == 1


def nonbranch_affine_residues(relations: tuple[int, ...], prime: int) -> int:
    """Count t mod p passing all character equations away from branch points.

    This is a search heuristic only.  A rational point can be p-adically close
    to the common point at infinity or to a branch point, so count zero is not
    recorded as a strict global obstruction.
    """
    count = 0
    for t in range(prime):
        values = [(t + i) % prime for i in range(N)]
        if any(value == 0 for value in values):
            continue
        good = True
        for mask in relations[1:]:
            rhs = 1
            for i, value in enumerate(values):
                if mask >> i & 1:
                    rhs = rhs * value % prime
            if not legendre_is_square(rhs, prime):
                good = False
                break
        if good:
            count += 1
    return count


def squareclass_mask_integer(value: int, prime_bits: dict[int, int]) -> int:
    if value == 0:
        raise ValueError("zero is handled separately")
    mask = int(value < 0)
    n = abs(value)
    p = 2
    while p * p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            if p not in prime_bits:
                prime_bits[p] = len(prime_bits) + 1
            mask ^= 1 << prime_bits[p]
        p += 1 if p == 2 else 2
    if n > 1:
        if n not in prime_bits:
            prime_bits[n] = len(prime_bits) + 1
        mask ^= 1 << prime_bits[n]
    return mask


def affine_rank_with_zero(values: list[int]) -> int:
    prime_bits: dict[int, int] = {}
    masks = [squareclass_mask_integer(v, prime_bits) for v in values if v]
    anchor = masks[0]
    return f2_rank([mask ^ anchor for mask in masks[1:]])


@dataclass(frozen=True)
class Quotient:
    relation_mask: int
    indices: tuple[int, ...]
    degree: int
    genus: int
    discriminant: int
    candidate_bad_primes: tuple[int, ...]


def quotient_data(mask: int) -> Quotient:
    indices = tuple(i for i in range(N) if mask >> i & 1)
    degree = len(indices)
    genus = (degree - 2) // 2
    disc = discriminant_for_roots(indices)
    return Quotient(
        relation_mask=mask,
        indices=indices,
        degree=degree,
        genus=genus,
        discriminant=disc,
        candidate_bad_primes=prime_factors(2 * disc),
    )


def pattern_record(word: tuple[int, ...], primes: tuple[int, ...]) -> dict[str, object]:
    relations = relation_space(word)
    basis = relation_basis(relations)
    quotients = [quotient_data(mask) for mask in relations if mask]
    genus_counts = Counter(q.genus for q in quotients)
    all_bad = sorted({p for q in quotients for p in q.candidate_bad_primes})
    residue_counts = {str(p): nonbranch_affine_residues(relations, p) for p in primes}
    # A transparent heuristic only: more genus-2 factors and more bad primes
    # usually make 2-Selmer/Jacobian work harder.
    difficulty = 3 * genus_counts[2] + genus_counts[1] + 2 * len(all_bad)
    jacobian_dimension = sum(genus * count for genus, count in genus_counts.items())
    return {
        "partition": word,
        "blocks": len(set(word)),
        "relation_dimension": len(basis),
        "relation_basis_masks": basis,
        "quotients": [asdict(q) for q in quotients],
        "genus_counts": dict(sorted(genus_counts.items())),
        "sum_of_character_jacobian_dimensions": jacobian_dimension,
        "candidate_bad_primes_union": all_bad,
        "real_nonbranch_point": True,
        "real_witness_interval": "t>0 (all linear factors are positive)",
        "nonbranch_affine_residues_mod_p_heuristic": residue_counts,
        "expected_selmer_difficulty_score": difficulty,
        "status": "unresolved: character-quotient points have not been tested for compatible lifting",
    }


def build_certificate(primes: tuple[int, ...]) -> dict[str, object]:
    raw = []
    strict_excluded_raw = []
    survivors_before_reflection = []
    for blocks in (3, 4):
        for word in restricted_growth_strings(N, blocks):
            raw.append(word)
            reasons = strict_pattern_reasons(word)
            if reasons:
                strict_excluded_raw.append({"partition": word, "reasons": reasons})
            else:
                survivors_before_reflection.append(word)

    excluded_orbits: dict[tuple[int, ...], dict[str, object]] = {}
    for row in strict_excluded_raw:
        representative = reflection_canonical(row["partition"])
        if representative not in excluded_orbits:
            excluded_orbits[representative] = {
                "partition": representative,
                "reflection_orbit_size": 0,
                "reasons_across_orbit": set(),
            }
        excluded_orbits[representative]["reflection_orbit_size"] += 1
        excluded_orbits[representative]["reasons_across_orbit"].update(row["reasons"])
    strict_excluded = []
    for row in excluded_orbits.values():
        row["reasons_across_orbit"] = sorted(row["reasons_across_orbit"])
        strict_excluded.append(row)
    strict_excluded.sort(key=lambda row: row["partition"])

    orbit_members: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for word in survivors_before_reflection:
        representative = reflection_canonical(word)
        orbit_members.setdefault(representative, []).append(word)

    patterns = []
    for representative, members in sorted(orbit_members.items()):
        record = pattern_record(representative, primes)
        record["reflection_orbit_size"] = len(members)
        patterns.append(record)
    patterns.sort(key=lambda row: (row["expected_selmer_difficulty_score"], row["partition"]))

    unique_masks = sorted(
        {q["relation_mask"] for pattern in patterns for q in pattern["quotients"]},
        key=lambda mask: (mask.bit_count(), discriminant_for_roots(tuple(i for i in range(N) if mask >> i & 1)), mask),
    )
    unique_quotients = [asdict(quotient_data(mask)) for mask in unique_masks]
    genus_strata = Counter(
        tuple(sorted((int(genus), count) for genus, count in pattern["genus_counts"].items()))
        for pattern in patterns
    )
    exclusion_reason_counts = Counter(
        reason
        for row in strict_excluded_raw
        for reason in row["reasons"]
    )

    zero_cases = []
    for zero_index in range(N):
        values = [i - zero_index for i in range(N)]
        zero_cases.append(
            {
                "zero_index": zero_index,
                "values": values,
                "affine_rank_of_nonzero_squareclasses": affine_rank_with_zero(values),
                "status": "strictly excluded" if affine_rank_with_zero(values) > 2 else "would require separate analysis",
            }
        )

    return {
        "problem": "R_2(7)=6 or 7",
        "definitions": {
            "labels": "unlabeled partitions into 3 or 4 blocks are exactly AGL(2,2)-orbits",
            "reflection": "i maps to 6-i",
            "relation_space": "W={e: sum(e_i)=0 and sum(e_i*label_i)=0}",
            "character_quotient": "y^2=product_{i:e_i=1}(t+i)",
        },
        "counts": {
            "raw_AGL_orbits_with_3_or_4_blocks": len(raw),
            "all_orbits_after_reflection": len(strict_excluded) + len(patterns),
            "strictly_excluded_before_reflection": len(strict_excluded_raw),
            "strictly_excluded_after_reflection": len(strict_excluded),
            "survive_before_reflection": len(survivors_before_reflection),
            "unresolved_after_reflection": len(patterns),
        },
        "strict_excluded_patterns": strict_excluded,
        "strict_exclusion_reason_counts_before_reflection": dict(exclusion_reason_counts),
        "zero_term_cases": zero_cases,
        "unique_character_quotients": unique_quotients,
        "unresolved_genus_strata": [
            {
                "genus_counts": {str(genus): count for genus, count in stratum},
                "number_of_patterns": multiplicity,
            }
            for stratum, multiplicity in sorted(genus_strata.items())
        ],
        "unresolved_patterns_ranked": patterns,
        "strict_local_obstruction_note": (
            "No surviving pattern is declared excluded by the mod-p heuristic. "
            "Every cover has degenerate rational points at infinity (the constant-AP branch), "
            "and separate quotient points need not lift compatibly."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="STUDENT_SQUARE_ROUND_02_certificate.json")
    parser.add_argument("--primes", default="11,13,17,19,23,29,31")
    args = parser.parse_args()
    primes = tuple(int(p) for p in args.primes.split(",") if p)
    certificate = build_certificate(primes)
    with open(args.output, "w", encoding="utf-8") as stream:
        json.dump(certificate, stream, indent=2, sort_keys=True)
    print(json.dumps(certificate["counts"], sort_keys=True))
    print("zero ranks:", [row["affine_rank_of_nonzero_squareclasses"] for row in certificate["zero_term_cases"]])
    print("output:", args.output)


if __name__ == "__main__":
    main()
