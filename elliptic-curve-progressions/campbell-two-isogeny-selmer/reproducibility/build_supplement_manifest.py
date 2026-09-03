"""Build the finite Campbell theorem supplement manifest."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.json"
RELEASE_ID = "paper-elliptic-campbell-supplement-v0.6.1"

ARTIFACTS = [
    ("STUDENT_ELLIPTIC_ROUND_03_certificate.json", "same_m_input_certificate", True),
    ("PAPER_ELLIPTIC_MOODY_JUYAL.py", "next_stage_dependency", True),
    ("PAPER_ELLIPTIC_NEXT_analysis.py", "local_matrix_base_generator", True),
    ("PAPER_ELLIPTIC_NEXT_test.py", "regression_test", True),
    ("PAPER_ELLIPTIC_CAMPBELL_analysis.py", "local_matrix_completion_generator", True),
    ("PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json", "512_cell_certificate", True),
    ("PAPER_ELLIPTIC_CAMPBELL_test.py", "regression_test", True),
    ("PAPER_ELLIPTIC_ROUND_04_analysis.py", "exact_selmer_generator", True),
    ("PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json", "clean_exact_selmer_certificate", True),
    ("PAPER_ELLIPTIC_ROUND_04_test.py", "regression_test", True),
    ("PAPER_ELLIPTIC_ROUND_05_analysis.py", "rejected_formula_audit_generator", True),
    ("PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json", "rejected_formula_certificate", True),
    ("PAPER_ELLIPTIC_ROUND_05_test.py", "regression_test", True),
    ("PAPER_ELLIPTIC_ROUND_06_analysis.py", "campbell_source_and_provenance_generator", True),
    ("PAPER_ELLIPTIC_ROUND_06_CERTIFICATE.json", "campbell_source_and_provenance_certificate", True),
    ("PAPER_ELLIPTIC_ROUND_06_test.py", "regression_test", True),
    ("PAPER_ELLIPTIC_PRIOR_ART.md", "prior_art_not_found_report", False),
    ("PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m", "unexecuted_candidate_input", False),
    ("PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.py", "manifest_generator", True),
    ("PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST_test.py", "manifest_and_isolation_test", True),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest() -> dict[str, object]:
    rows = []
    for name, role, eligible in ARTIFACTS:
        path = ROOT / name
        assert path.is_file(), name
        rows.append({
            "path": name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "role": role,
            "mathematical_evidence_eligible": eligible,
        })
    return {
        "schema": "paper-elliptic-supplement-manifest-v1",
        "semantic_version": "0.6.1",
        "release_id": RELEASE_ID,
        "release_status": "LOCAL_RELEASE_CANDIDATE_NOT_PUBLICLY_ARCHIVED",
        "archival_url": None,
        "runtime": {"python": platform.python_version(), "sympy": sympy.__version__},
        "files": rows,
        "reproduction_commands": [
            "python PAPER_ELLIPTIC_CAMPBELL_analysis.py",
            "python PAPER_ELLIPTIC_ROUND_04_analysis.py",
            "python PAPER_ELLIPTIC_ROUND_05_analysis.py",
            "python PAPER_ELLIPTIC_ROUND_06_analysis.py",
            "python PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST.py",
            "python -m unittest -v PAPER_ELLIPTIC_NEXT_test.py PAPER_ELLIPTIC_CAMPBELL_test.py PAPER_ELLIPTIC_ROUND_04_test.py PAPER_ELLIPTIC_ROUND_05_test.py PAPER_ELLIPTIC_ROUND_06_test.py PAPER_ELLIPTIC_SUPPLEMENT_MANIFEST_test.py",
        ],
        "claim_boundary": {
            "proved": "Campbell source identities, same-m local solubility, the 512-cell local matrix, both exact 2-isogeny Selmer groups, rank at most 3, and the Q x K invariant",
            "not_proved": "a ninth rational point or its nonexistence, the full 2-Selmer group, a Cassels-Tate value, or Mordell-Weil rank equality",
        },
        "ineligible_input_policy": {
            "PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m": "No transcript and no trusted Magma binary hash; never consumed by the proved pipeline."
        },
        "supersession_policy": {
            "clean_certificate": "PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json",
            "forbidden_clean_certificate_fields": [
                "d35_cassels_tate_setup",
                "pairing_bits_to_compute",
                "decisive_outcome",
            ],
            "negative_audit": "PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json",
            "rule": "Round-05 proves only that the superseded opposite-side expression is invalid; it supplies no pairing value.",
        },
        "test_accounting": {
            "core_tests_run_inside_isolated_supplement": 39,
            "supplement_manifest_tests": 3,
            "release_manifest_tests": 3,
            "full_release_total": 45,
        },
    }


def main() -> None:
    OUTPUT.write_text(json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
