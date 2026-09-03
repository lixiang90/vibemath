import hashlib
import json
from pathlib import Path
import unittest

from STUDENT_ELLIPTIC_ROUND_03_local import (
    BRANCH_MODEL_BAD_PRIMES,
    D_COEFFS,
    H_COEFFS,
    ODD_LOCAL_CERTIFICATES,
    build_certificate,
    evaluate,
    quartic_and_jacobian_audit,
    root_isolation_certificate,
    search_ch_height,
    verify_odd_local_certificate,
)


HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "STUDENT_ELLIPTIC_ROUND_03_certificate.json"
MAGMA_PATH = HERE / "STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m"
WRAPPER_PATH = HERE / "STUDENT_ELLIPTIC_ROUND_03_run_magma_audit.ps1"
EXPECTED_CERTIFICATE_HASH = "74843e4e53c7d09793fa857a2ce57d37a21be855ce135fec9f22b5b00aab5e08"
EXPECTED_MAGMA_HASH = "ae6a61f417f82e29d6e496229399a05ce88a0f085d5e6f29869e9c03acdf00e8"


class RoundThreeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = CERTIFICATE_PATH.read_bytes()
        cls.certificate = json.loads(cls.payload)

    def test_certificate_hash_and_classification(self):
        self.assertEqual(hashlib.sha256(self.payload).hexdigest(), EXPECTED_CERTIFICATE_HASH)
        self.assertFalse(self.certificate["global_status"]["fake_two_selmer_computed"])
        self.assertEqual(self.certificate["bounded_CH_search"]["logical_status"], "bounded evidence only")

    def test_all_same_m_local_rows(self):
        self.assertTrue(all(verify_odd_local_certificate(row) for row in ODD_LOCAL_CERTIFICATES))
        rows = self.certificate["same_m_local_certificates"]["odd"]
        self.assertEqual(rows, [[r.p, r.m, r.d_value, r.d_root, r.h_value, r.h_root] for r in ODD_LOCAL_CERTIFICATES])
        for p, m, dv, dy, hv, hz in rows:
            self.assertEqual(evaluate(D_COEFFS, m, p), dv % p)
            self.assertEqual(evaluate(H_COEFFS, m, p), hv % p)
            self.assertNotEqual(dy % p, 0)
            self.assertNotEqual(hz % p, 0)
            self.assertEqual(dy*dy % p, dv % p)
            self.assertEqual(hz*hz % p, hv % p)
        self.assertEqual(tuple(self.certificate["branch_model_bad_primes"]), BRANCH_MODEL_BAD_PRIMES)

    def test_root_isolation_and_small_exact_search(self):
        self.assertEqual(len(root_isolation_certificate()), 4)
        small = search_ch_height(1000)
        self.assertEqual(small["CH_points"], [])
        self.assertEqual(small["logical_status"], "bounded evidence only")
        recorded = self.certificate["bounded_CH_search"]
        self.assertEqual(recorded["bound_B"], 50000)
        self.assertEqual(recorded["CH_point_count"], 0)
        self.assertEqual(recorded["full_fibre_product_point_count"], 0)

    def test_binary_quartic_jacobian_models(self):
        d = quartic_and_jacobian_audit(D_COEFFS, 32)
        h = quartic_and_jacobian_audit(H_COEFFS, 64)
        self.assertEqual(d["integral_scaled_model"], [0, 0, 0, -137904664808967867, -4890817235485401208238826])
        self.assertEqual(h["integral_scaled_model"], [0, 0, 0, -58243635870855147, -3811211217040595260188186])
        self.assertFalse(d["minimality_claimed"])
        self.assertFalse(h["minimality_claimed"])
        self.assertEqual(self.certificate["binary_quartic_audits"]["D"], d)
        self.assertEqual(self.certificate["binary_quartic_audits"]["H"], h)

    def test_magma_call_is_unbounded_and_wrapper_is_fail_closed(self):
        magma = MAGMA_PATH.read_text(encoding="utf-8")
        active_lines = [line.strip() for line in magma.splitlines() if line.strip() and not line.strip().startswith(("/*", "*", "*/", "//"))]
        descent_lines = [line for line in active_lines if "TwoCoverDescent" in line]
        self.assertEqual(descent_lines, ["time SelH, AtoSelH := TwoCoverDescent(CH);"])
        self.assertIn("SAME_M_FIBRE_PRODUCT_LOCAL_CERTIFICATES_OK", magma)
        self.assertEqual(hashlib.sha256(MAGMA_PATH.read_bytes()).hexdigest(), EXPECTED_MAGMA_HASH)
        for row in self.certificate["same_m_local_certificates"]["odd"]:
            self.assertIn("[" + ",".join(str(value) for value in row) + "]", magma)
        wrapper = WRAPPER_PATH.read_text(encoding="utf-8")
        self.assertIn(EXPECTED_CERTIFICATE_HASH, wrapper)
        self.assertIn(EXPECTED_MAGMA_HASH, wrapper)
        self.assertIn("$FailurePattern", wrapper)
        self.assertIn("FAKE_TWO_SELMER_DESCENT_COMPLETED", wrapper)
        self.assertIn("AUDIT_COMPLETED", wrapper)


if __name__ == "__main__":
    unittest.main()
