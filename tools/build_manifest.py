"""Build a deterministic SHA-256 inventory for the public research tree."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "MANIFEST.sha256"


def files_to_hash() -> list[Path]:
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path != OUTPUT
            and "__pycache__" not in path.parts
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def build() -> str:
    rows = []
    for path in files_to_hash():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    OUTPUT.write_text(build(), encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.name} with {len(files_to_hash())} entries")

