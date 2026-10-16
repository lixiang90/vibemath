"""Reproduce Sun90 certificates without changing tracked project files.

Run ``python verify.py`` to check the proof's exact computational components.
Use ``python verify.py --report reproducibility/full_verification.json``
to retain the aggregate report after temporary files have been cleaned.
Relative report paths are resolved from this project directory.
Requires Python >=3.9 and SymPy 1.14.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CODE = (
    'sun90_modparam_verify.py',
    'verify_sun90.py',
    'prize90_geometry_mod7_sturm.py',
    'prize90_geometry_cm_verify.py',
    'verify_sun90_full.py',
)
DATA = (
    'prize_congruence_curve90_jet_certificate.json',
    'prize90_geometry_mod7_result.json',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_stage_directory(folder):
    """Validate the absolute deletion target immediately before cleanup."""
    stage = Path(folder).resolve()
    if stage.parent != ROOT.resolve() or not stage.name.startswith('.sun90-stage-'):
        raise RuntimeError('Refusing to clean a temporary directory outside the project')
    return stage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, help='save JSON report; relative to project root')
    args = parser.parse_args()
    if sys.version_info < (3, 9):
        parser.error('Python >=3.9 is required')
    try:
        import sympy
    except ImportError as exc:
        raise SystemExit('Install dependencies with: python -m pip install -r requirements.txt') from exc

    sources = {name: ROOT / 'code' / name for name in CODE}
    sources.update({name: ROOT / 'certificates' / name for name in DATA})
    expected = {name: digest(path) for name, path in sources.items()}
    source_hashes = {
        path.relative_to(ROOT).as_posix(): expected[name]
        for name, path in sources.items()
    }
    source_hashes['verify.py'] = digest(ROOT / 'verify.py')
    source_hashes['requirements.txt'] = digest(ROOT / 'requirements.txt')

    temporary = tempfile.TemporaryDirectory(prefix='.sun90-stage-', dir=ROOT)
    try:
        stage = checked_stage_directory(temporary.name)
        for name, source in sources.items():
            shutil.copyfile(source, stage / name)
            if digest(stage / name) != expected[name]:
                raise RuntimeError('Staged input hash mismatch: ' + name)
        subprocess.run([sys.executable, str(stage / 'verify_sun90_full.py')],
                       cwd=stage, check=True)
        report = json.loads((stage / 'sun90_full_verification.json').read_text(encoding='utf-8'))
        if report['program_and_data_sha256'] != expected:
            raise RuntimeError('Executed program/data hashes do not match the public source files')
        if any(digest(path) != expected[name] for name, path in sources.items()):
            raise RuntimeError('A public source file changed during verification')
        report['reproduction_environment'] = {
            'python': platform.python_version(),
            'sympy': sympy.__version__,
        }
        report['public_source_sha256'] = source_hashes
        report['staged_hashes_match_public_sources'] = True
    finally:
        checked_stage_directory(temporary.name)
        temporary.cleanup()

    # Persist only after both temporary staging levels have been removed.
    if args.report is not None:
        target = args.report.expanduser()
        if not target.is_absolute():
            target = ROOT / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print('Saved report: ' + str(target.relative_to(ROOT) if target.is_relative_to(ROOT) else target))
    print('PASS: public code/data hashes match; temporary files cleaned.', flush=True)


if __name__ == '__main__':
    main()
