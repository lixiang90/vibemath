import hashlib
import json
import unittest
from pathlib import Path

import PAPER_ELLIPTIC_ROUND_05_analysis as a


ROOT = Path(__file__).resolve().parent
CERT = ROOT / "PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json"


class Round05CorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CERT.read_text(encoding="utf-8"))

    def test_conic_point_and_tangent(self):
        R, S, N = a.CONIC_POINT
        self.assertEqual(a.conic_value(R, S, N), 0)
        self.assertEqual(a.tangent_value(R, S, N), 0)
        self.assertEqual(a.TANGENT, (60677401, -697502396215296, -8012928))

    def test_padic_branch_residues_are_exact(self):
        audit = self.data["rejected_opposite_side_formula_audit"]
        for p_text, cell in audit["local_data"].items():
            p = int(p_text)
            U, V, rhs = cell["U"], cell["V"], cell["rhs"]
            self.assertEqual(rhs, a.quartic_rhs(U, V))
            for branch in cell["branches"]:
                modulus = branch["modulus"]
                N = branch["N_mod"]
                self.assertEqual((N*N-rhs) % modulus, 0)
                self.assertEqual(
                    a.tangent_value(U*U, V*V, N) % modulus,
                    branch["L_mod"],
                )
                self.assertEqual(
                    a.hilbert_symbol(branch["L_mod"], a.e, p),
                    branch["hilbert_symbol"],
                )

    def test_rejected_formula_fails_branch_independence(self):
        audit = self.data["rejected_opposite_side_formula_audit"]
        self.assertEqual(audit["branch_symbols"]["59"], [-1, 1])
        self.assertEqual(audit["branch_symbols"]["71699"], [-1, 1])
        self.assertEqual(
            audit["possible_products_from_independent_local_branches"], [-1, 1]
        )
        self.assertEqual(audit["well_definedness_test"], "FAIL_BRANCH_INDEPENDENCE")

    def test_claim_boundary_withdraws_opposite_side_pairing(self):
        joined = " ".join(self.data["claim_boundary"]["withdrawn"])
        self.assertIn("opposite isogeny Selmer groups", joined)
        self.assertIn("C_H(Q) is empty", joined)
        self.assertIn(
            "full 2-Selmer group or a basis",
            " ".join(self.data["claim_boundary"]["not_proved"]),
        )

    def test_source_hashes(self):
        for name, expected in self.data["source_sha256"].items():
            actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)

    def test_magma_input_uses_full_coverings_only(self):
        text = (ROOT / "PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m").read_text(
            encoding="utf-8"
        )
        self.assertIn("TwoDescent(EH", text)
        self.assertIn("CasselsTatePairing(CH, covers[i])", text)
        self.assertIn("FourDescent(CH)", text)
        self.assertNotIn("CasselsTatePairing(35", text)
        self.assertNotIn("CasselsTatePairing(4230241", text)

    def test_clean_round04_and_finite_matrix_are_preserved(self):
        round04 = json.loads(
            (ROOT / "PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("d35_cassels_tate_setup", round04)
        self.assertEqual(
            round04["schema"], "paper-elliptic-campbell-round-04-clean-v2"
        )
        self.assertIn("FAIL_BRANCH_INDEPENDENCE", json.dumps(self.data))
        matrix = json.loads(
            (ROOT / "PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(matrix["summary"]["status_counts"]["YES"], 384)
        self.assertEqual(matrix["summary"]["status_counts"]["NO"], 128)


if __name__ == "__main__":
    unittest.main()
