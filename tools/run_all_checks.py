"""Run the archived mathematical checks without creating repository artifacts.

Several historical generators expect a flat supplement directory.  The public
tree is organized for reading, so this script reconstructs that flat layout in
an operating-system temporary directory and removes it automatically.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def copy_files(stage: Path, mappings: list[tuple[Path, str]]) -> None:
    for source, target_name in mappings:
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, stage / target_name)


def all_files(directory: Path, pattern: str) -> list[tuple[Path, str]]:
    return [(path, path.name) for path in sorted(directory.glob(pattern))]


def run_group(name: str, mappings: list[tuple[Path, str]], modules: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix=f"vibemath-{name}-") as temporary:
        stage = Path(temporary)
        copy_files(stage, mappings)
        command = [sys.executable, "-m", "unittest", "-v", *modules]
        print(f"\n=== {name}: {' '.join(modules)} ===", flush=True)
        subprocess.run(command, cwd=stage, env=test_environment(), check=True)


def run_direct(name: str, working_directory: Path, modules: list[str]) -> None:
    """Run checks that already understand the organized public layout."""
    command = [sys.executable, "-m", "unittest", "-v", *modules]
    print(f"\n=== {name}: {' '.join(modules)} ===", flush=True)
    subprocess.run(
        command, cwd=working_directory, env=test_environment(), check=True
    )


def square_group() -> tuple[list[tuple[Path, str]], list[str]]:
    base = ROOT / "square-progressions" / "seven-consecutive-squareclasses"
    mappings = []
    mappings += all_files(base / "code", "*.py")
    mappings += all_files(base / "certificates", "*.json")
    mappings += all_files(base / "reproducibility" / "tests", "*.py")
    mappings += [
        (base / "reproducibility" / "SUPPLEMENT_MANIFEST.py", "PAPER_SQUARE_SUPPLEMENT_MANIFEST.py"),
        (base / "reproducibility" / "SUPPLEMENT_MANIFEST.json", "PAPER_SQUARE_SUPPLEMENT_MANIFEST.json"),
    ]
    modules = [
        "STUDENT_SQUARE_ROUND_02_test_patterns",
        "STUDENT_SQUARE_ROUND_03_test",
        "STUDENT_SQUARE_ROUND_04_test",
        "PAPER_SQUARE_SAFE_test",
        "PAPER_SQUARE_MASK77_test",
        "PAPER_SQUARE_NEXT_GATE_test",
        "PAPER_SQUARE_MASK108_test",
        "PAPER_SQUARE_SUPPLEMENT_MANIFEST_test",
    ]
    return mappings, modules


def number_field_group() -> tuple[list[tuple[Path, str]], list[str]]:
    base = ROOT / "square-progressions" / "magic-squares-over-number-fields"
    mappings = all_files(base / "code", "*.py") + all_files(base / "tests", "*.py")
    modules = [
        "test_magic_square_search",
        "test_quadratic_elliptic_search",
        "test_number_field_magic",
        "test_bremner_j1728",
        "test_campbell_j1728",
        "test_spearman_kummer",
        "test_spearman_parameters",
        "test_bst_number_field",
    ]
    return mappings, modules


def cube_group() -> tuple[list[tuple[Path, str]], list[str]]:
    base = ROOT / "powers-in-progressions" / "pure-cubic-five-term" / "code"
    return all_files(base, "*.py") + all_files(base, "*.json"), ["PAPER_CUBE_KUMMER5_test"]


def fourth_power_group() -> tuple[list[tuple[Path, str]], list[str]]:
    base = ROOT / "powers-in-progressions" / "fourth-powers-six-term" / "code"
    return all_files(base, "*.py"), ["PAPER_CUBE_P6_test_gate", "PAPER_CUBE_P6_test_maps"]


def c29_group() -> tuple[list[tuple[Path, str]], list[str]]:
    base = ROOT / "powers-in-progressions" / "elliptic-simultaneous-torsion-c29" / "code"
    return all_files(base, "*.py") + all_files(base, "*.json"), ["PAPER_CUBE_C29_test_model"]


def elliptic_group() -> tuple[Path, list[str]]:
    base = ROOT / "elliptic-curve-progressions" / "campbell-two-isogeny-selmer"
    modules = [
        "PAPER_ELLIPTIC_NEXT_test",
        "PAPER_ELLIPTIC_CAMPBELL_test",
        "PAPER_ELLIPTIC_ROUND_04_test",
        "PAPER_ELLIPTIC_ROUND_05_test",
        "PAPER_ELLIPTIC_ROUND_06_test",
        "test_same_m_local",
    ]
    return base / "code", modules


def main() -> None:
    groups = [
        ("squareclasses", *square_group()),
        ("number-fields", *number_field_group()),
        ("pure-cubic", *cube_group()),
        ("fourth-powers", *fourth_power_group()),
        ("c29", *c29_group()),
    ]
    for name, mappings, modules in groups:
        run_group(name, mappings, modules)
    elliptic_directory, elliptic_modules = elliptic_group()
    run_direct("campbell-selmer", elliptic_directory, elliptic_modules)
    print("\nAll archived mathematical checks passed.")


if __name__ == "__main__":
    main()
