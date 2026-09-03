"""Create the immutable-file manifest for the square-pattern supplement."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "PAPER_SQUARE_SUPPLEMENT_MANIFEST.json"
RELEASE_ID = "paper-square-supplement-v0.7.0"

ARTIFACTS = [
    "STUDENT_SQUARE_ROUND_02_patterns.py",
    "STUDENT_SQUARE_ROUND_02_certificate.json",
    "STUDENT_SQUARE_ROUND_02_test_patterns.py",
    "STUDENT_SQUARE_ROUND_03_isomorphisms.py",
    "STUDENT_SQUARE_ROUND_03_CERTIFICATE.json",
    "STUDENT_SQUARE_ROUND_03_test.py",
    "STUDENT_SQUARE_ROUND_04_pipeline.py",
    "STUDENT_SQUARE_ROUND_04_CERTIFICATE.json",
    "STUDENT_SQUARE_ROUND_04_test.py",
    "PAPER_SQUARE_SAFE_inventory.py",
    "PAPER_SQUARE_SAFE_CERTIFICATE.json",
    "PAPER_SQUARE_SAFE_test.py",
    "PAPER_SQUARE_MASK77_analysis.py",
    "PAPER_SQUARE_MASK77_CERTIFICATE.json",
    "PAPER_SQUARE_MASK77_test.py",
    "PAPER_SQUARE_NEXT_GATE.py",
    "PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json",
    "PAPER_SQUARE_NEXT_GATE_test.py",
    "PAPER_SQUARE_MASK108.py",
    "PAPER_SQUARE_MASK108_CERTIFICATE.json",
    "PAPER_SQUARE_MASK108_test.py",
    "PAPER_SQUARE_MASK99.py",
    "PAPER_SQUARE_MASK99_CERTIFICATE.json",
    "PAPER_SQUARE_MASK99_test.py",
    "PAPER_SQUARE_MASK51.py",
    "PAPER_SQUARE_MASK51_CERTIFICATE.json",
    "PAPER_SQUARE_MASK51_test.py",
    "PAPER_SQUARE_SUPPLEMENT_MANIFEST.py",
    "PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role(name: str) -> str:
    if name.endswith(".json"):
        return "exact_certificate"
    if "test" in name.lower():
        return "regression_test"
    return "generator_or_analysis_source"


def build_manifest() -> dict[str, object]:
    files = []
    for name in ARTIFACTS:
        path = ROOT / name
        assert path.is_file(), name
        files.append({
            "path": name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "role": role(name),
            "mathematical_evidence_eligible": True,
        })
    return {
        "schema": "paper-square-supplement-manifest-v1",
        "semantic_version": "0.7.0",
        "release_id": RELEASE_ID,
        "release_status": "LOCAL_RELEASE_CANDIDATE_NOT_PUBLICLY_ARCHIVED",
        "archival_url": None,
        "source_control_commit": None,
        "source_control_note": "workspace is not a Git repository; SHA-256 entries are the locator",
        "runtime": {
            "python": platform.python_version(),
            "sympy": sympy.__version__,
        },
        "files": files,
        "reproduction_commands": [
            "python PAPER_SQUARE_SAFE_inventory.py",
            "python PAPER_SQUARE_MASK77_analysis.py --bound 1000000",
            "python PAPER_SQUARE_NEXT_GATE.py",
            "python PAPER_SQUARE_MASK108.py",
            "python PAPER_SQUARE_MASK99.py",
            "python PAPER_SQUARE_MASK51.py",
            "python PAPER_SQUARE_SUPPLEMENT_MANIFEST.py",
            "python -m unittest -v STUDENT_SQUARE_ROUND_02_test_patterns.py STUDENT_SQUARE_ROUND_03_test.py STUDENT_SQUARE_ROUND_04_test.py PAPER_SQUARE_SAFE_test.py PAPER_SQUARE_MASK77_test.py PAPER_SQUARE_NEXT_GATE_test.py PAPER_SQUARE_MASK108_test.py PAPER_SQUARE_MASK99_test.py PAPER_SQUARE_MASK51_test.py PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py",
        ],
        "claim_boundary": {
            "proved": "exact finite pattern counts and the mask 77, 89, 102, 108, 99, 51 exclusions documented in the paper",
            "not_proved": "realizability or impossibility of the 10 remaining patterns; R_2(7) is not decided",
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
