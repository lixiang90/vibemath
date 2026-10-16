"""Run the four exact Sun90 certificate components in a flat directory.

Python >=3.9 and SymPy 1.14.0 are required. Put the four component scripts
and two certificate JSON inputs beside this program. The project-level
verify.py stages this layout automatically without changing tracked files.

CCY table entries suggested discovery candidates, rather than supplying
theorems to the complete proof. The programs check explicit arithmetic
identities; the paper supplies the modularity hypotheses, Fricke argument,
holomorphy, continuation, signs, and analytic convergence arguments.
No prize priority, acceptance, or eligibility is verified by these programs.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
STEPS = [
    ('sun90_modparam_verify.py', 'sun90_modparam_result.json'),
    ('verify_sun90.py', 'verify_sun90_result.json'),
    ('prize90_geometry_mod7_sturm.py', 'prize90_geometry_mod7_sturm_result.json'),
    ('prize90_geometry_cm_verify.py', 'prize90_geometry_cm_verify_result.json'),
]
INPUTS = [name for name, _ in STEPS] + [
    'prize_congruence_curve90_jet_certificate.json',
    'prize90_geometry_mod7_result.json',
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_run_directory(folder):
    """Require the temporary directory to be a direct child of this layout."""
    run_dir = Path(folder).resolve()
    if run_dir.parent != BASE.resolve() or not run_dir.name.startswith('.sun90-certificates-'):
        raise RuntimeError('Refusing to clean a temporary directory outside the flat layout')
    return run_dir


def main():
    if sys.version_info < (3, 9):
        raise SystemExit('Python >=3.9 is required')

    # Component programs write beside themselves or in their current working
    # directory. Isolate all of those reports before creating the aggregate.
    results = {}
    temporary = tempfile.TemporaryDirectory(prefix='.sun90-certificates-', dir=BASE)
    try:
        run_dir = checked_run_directory(temporary.name)
        for name in INPUTS:
            shutil.copyfile(BASE / name, run_dir / name)
        for script, result in STEPS:
            print('\nRUN ' + script, flush=True)
            subprocess.run([sys.executable, str(run_dir / script)], cwd=run_dir, check=True)
            results[script] = json.loads((run_dir / result).read_text(encoding='utf-8'))
    finally:
        checked_run_directory(temporary.name)
        temporary.cleanup()

    param = results['sun90_modparam_verify.py']
    bridge = results['verify_sun90.py']
    mod7 = results['prize90_geometry_mod7_sturm.py']
    cm = results['prize90_geometry_cm_verify.py']
    assert param['literature_table_data_used_as_theorems'] is False
    assert (param['weight4_sturm_bound'], param['weight8_sturm_bound']) == (48, 96)
    assert bridge['all_exact_checks_passed'] is True and bridge['value'] == '90/pi'
    assert bridge['particular_literature_table_values_assumed'] is False
    assert bridge['Fricke_argument_verified_by_this_program'] is False
    assert mod7['coefficients_verified_zero_through'] == mod7['sturm_bound'] == 6144
    assert cm['proved_X60_CM_value'] == '5/4 - sqrt(21)/4'
    assert cm['proved_lambda60_CM_value'] == '3/2 - 11*sqrt(21)/42'
    assert cm['Fricke_argument_verified_by_this_program'] is False

    out = {
        'status': 'all four exact certificate components passed',
        'identity': 'Sun equation (5.9), value 90/pi',
        'particular_literature_table_values_assumed': False,
        'discovery_reference': 'Campbell--Cooper--Ye, arXiv:2602.09352v1, Tables 2-4 and 50',
        'standard_mathematical_inputs': [
            'eta-quotient modularity, character and cusp-order criteria',
            'Dedekind eta transformation law',
            'logarithmic derivative of eta and derivative covariance',
            'Sturm theorem for modular forms',
        ],
        'arguments_supplied_by_paper': [
            'The modularity and holomorphy hypotheses for the exact Sturm checks',
            'The eta/Fricke differentiation of the weighted CM period',
            'Analytic continuation, signs, and convergence arguments',
        ],
        'scope_note': 'The suite checks explicit exact computational identities. The paper supplies the standard-theorem applications and analytic arguments; running the suite alone is not a complete proof review.',
        'Fricke_argument_verified_by_programs': False,
        'component_results': results,
        'program_and_data_sha256': {
            name: digest(BASE / name) for name in INPUTS + ['verify_sun90_full.py']
        },
        'first_proof_priority_confirmed_by_sponsor': False,
        'prize_eligibility_confirmed_by_sponsor': False,
    }
    # All component temporary files have been cleaned before persistence.
    (BASE / 'sun90_full_verification.json').write_text(
        json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print('\nPASS: all exact certificate components agree.', flush=True)


if __name__ == '__main__':
    main()
