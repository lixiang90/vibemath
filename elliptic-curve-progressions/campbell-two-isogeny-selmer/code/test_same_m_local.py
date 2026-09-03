import hashlib
import json
from pathlib import Path
import unittest

from same_m_local import (
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
CERTIFICATE_PATH = HERE.parent / "certificates" / "same_m_local.json"


class RoundThreeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = CERTIFICATE_PATH.read_bytes()
        cls.certificate = json.loads(cls.payload)

    def test_certificate_hash_and_classification(self):
        self.assertEqual(self.payload, (json.dumps(self.certificate, indent=2, sort_keys=True) + "\n").encode("utf-8"))
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

    def test_no_unexecuted_descent_is_promoted(self):
        self.assertFalse(self.certificate["global_status"]["fake_two_selmer_computed"])
        self.assertIn("awaiting_magma", self.certificate["classification"])
        self.assertNotIn("Cassels", json.dumps(self.certificate))


if __name__ == "__main__":
    unittest.main()
