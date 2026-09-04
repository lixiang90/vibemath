"""Cold-reproduce a committed vibemath tree in a disposable local clone.

The report deliberately distinguishes an internal clean-clone check from an
independent external reproduction.  All build intermediates remain inside an
operating-system temporary directory and are deleted on exit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "squareclasses": Path("square-progressions/seven-consecutive-squareclasses/paper"),
    "pure_cubic": Path("powers-in-progressions/pure-cubic-five-term/paper"),
    "campbell_selmer": Path(
        "elliptic-curve-progressions/campbell-two-isogeny-selmer/paper"
    ),
}
WARNING_PATTERNS = (
    r"Overfull \\hbox",
    r"Underfull \\hbox",
    r"LaTeX Warning:",
    r"Package .* Warning:",
    r"undefined references",
    r"undefined citations",
)
EXPECTED_TEST_GROUP_COUNTS = [96, 33, 42, 14, 8, 73]
EXPECTED_TEST_TOTAL = 266
EXPECTED_PDF_PAGES = {
    "squareclasses": 11,
    "pure_cubic": 9,
    "campbell_selmer": 11,
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Recorder:
    def __init__(self) -> None:
        self.parts: list[str] = []

    def run(
        self,
        command: Sequence[str],
        cwd: Path,
        *,
        check: bool = True,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        self.parts.append(f"\n$ {' '.join(command)}\n[cwd] {cwd}\n")
        result = subprocess.run(
            list(command),
            cwd=cwd,
            env=environment,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.parts.append(result.stdout)
        self.parts.append(f"\n[exit] {result.returncode}\n")
        if check and result.returncode:
            raise RuntimeError(f"command failed ({result.returncode}): {command}")
        return result


def command_version(
    recorder: Recorder,
    command: Sequence[str],
    cwd: Path,
    pattern: str | None = None,
) -> str:
    result = recorder.run(command, cwd)
    if pattern is not None:
        match = re.search(pattern, result.stdout)
        if not match:
            raise RuntimeError(f"version pattern not found: {pattern}")
        return match.group(0).strip()
    return result.stdout.strip().splitlines()[0]


def pdf_text(path: Path) -> bytes:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout


def pdf_pages(recorder: Recorder, path: Path) -> int:
    result = recorder.run(["pdfinfo", str(path)], path.parent)
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"could not read page count for {path}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args()

    for executable in ("git", "latexmk", "pdfinfo", "pdftotext"):
        if shutil.which(executable) is None:
            raise SystemExit(f"required executable not found: {executable}")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    recorder = Recorder()
    commit = recorder.run(
        ["git", "rev-parse", f"{args.commit}^{{commit}}"], ROOT
    ).stdout.strip()
    source_dirty = bool(
        recorder.run(["git", "status", "--porcelain=v1"], ROOT).stdout.strip()
    )

    report: dict[str, object] = {
        "schema": "vibemath-internal-cold-reproduction-v1",
        "commit": commit,
        "classification": "internal clean-clone reproduction; not external independent review",
        "source_worktree_dirty_during_run": source_dirty,
        "tools": {},
        "tests": {},
        "papers": {},
    }

    failure: str | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="vibemath-cold-") as temporary:
            clone = Path(temporary) / "checkout"
            recorder.run(
                ["git", "clone", "--local", "--no-hardlinks", "--quiet", str(ROOT), str(clone)],
                ROOT,
            )
            recorder.run(["git", "checkout", "--quiet", commit], clone)
            cloned_commit = recorder.run(["git", "rev-parse", "HEAD"], clone).stdout.strip()
            if cloned_commit != commit:
                raise RuntimeError("cloned commit differs from requested commit")

            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            tools = report["tools"]
            assert isinstance(tools, dict)
            tools.update(
                {
                    "python": command_version(recorder, [sys.executable, "--version"], clone),
                    "git": command_version(recorder, ["git", "--version"], clone),
                    "latexmk": command_version(
                        recorder,
                        ["latexmk", "--version"],
                        clone,
                        r"Latexmk[^\r\n]*Version [^\r\n]*",
                    ),
                    "pdfinfo": command_version(recorder, ["pdfinfo", "-v"], clone),
                    "sympy": command_version(
                        recorder,
                        [sys.executable, "-c", "import sympy; print(sympy.__version__)"],
                        clone,
                    ),
                }
            )

            test_result = recorder.run(
                [sys.executable, "tools/run_all_checks.py"],
                clone,
                environment=environment,
            )
            counts = [int(value) for value in re.findall(r"Ran (\d+) tests", test_result.stdout)]
            if counts != EXPECTED_TEST_GROUP_COUNTS:
                raise RuntimeError(f"unexpected test group counts: {counts}")
            total = sum(counts)
            if total != EXPECTED_TEST_TOTAL:
                raise RuntimeError(f"unexpected total test count: {total}")
            report["tests"] = {
                "group_counts": counts,
                "total": total,
                "all_passed": "All archived mathematical checks passed." in test_result.stdout,
            }

            paper_results: dict[str, object] = {}
            for name, relative in PAPERS.items():
                directory = clone / relative
                pdf = directory / "main.pdf"
                committed_text_hash = sha256(pdf_text(pdf))
                recorder.run(
                    ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                    directory,
                    environment=environment,
                )
                log_text = (directory / "main.log").read_text(
                    encoding="utf-8", errors="replace"
                )
                warnings = [
                    pattern
                    for pattern in WARNING_PATTERNS
                    if re.search(pattern, log_text, re.IGNORECASE)
                ]
                rebuilt_text_hash = sha256(pdf_text(pdf))
                if warnings:
                    raise RuntimeError(f"{name} final LaTeX log warnings: {warnings}")
                if rebuilt_text_hash != committed_text_hash:
                    raise RuntimeError(f"{name} rebuilt PDF text differs from committed PDF")
                pages = pdf_pages(recorder, pdf)
                if pages != EXPECTED_PDF_PAGES[name]:
                    raise RuntimeError(
                        f"{name} page count {pages} differs from "
                        f"expected {EXPECTED_PDF_PAGES[name]}"
                    )
                paper_results[name] = {
                    "pages": pages,
                    "committed_pdf_text_sha256": committed_text_hash,
                    "rebuilt_pdf_text_sha256": rebuilt_text_hash,
                    "text_identical": True,
                    "final_log_warning_patterns": warnings,
                }
            report["papers"] = paper_results
    except Exception as exc:  # Preserve all evidence even on a failed run.
        failure = f"{type(exc).__name__}: {exc}"

    report["success"] = failure is None
    report["failure"] = failure
    log_text = "".join(recorder.parts)
    log_name = f"INTERNAL_COLD_REPRODUCTION_{commit[:12]}.log"
    report_name = f"INTERNAL_COLD_REPRODUCTION_{commit[:12]}.json"
    (output_dir / log_name).write_text(log_text, encoding="utf-8", newline="\n")
    report["combined_log"] = log_name
    report["combined_log_sha256"] = sha256(log_text.encode("utf-8"))
    (output_dir / report_name).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
