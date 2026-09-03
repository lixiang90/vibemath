import json
import unittest

import sympy as sp

import PAPER_ELLIPTIC_CAMPBELL_analysis as C
import PAPER_ELLIPTIC_NEXT_analysis as N


class CampbellLocalMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = C.build_certificate()

    def test_next_y_slice_inverse_boundaries_and_nonzero_gates(self):
        identities = N.y_slice_identities()
        self.assertTrue(all(value == 0 for value in identities.values()))
        self.assertEqual(
            N.y_slice_boundary_map(),
            {
                "rho=0,eta=+1": "O",
                "rho=0,eta=-1": (0, 0),
                "infinity_+": (-4, 0),
                "infinity_-": (-8, 0),
            },
        )

    def test_certificate_disk_and_script_hashes(self):
        stored = json.loads(C.CERTIFICATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(stored, self.certificate)
        for name, digest in stored["source_sha256"].items():
            self.assertEqual(C.sha256(C.ROOT / name), digest)

    def test_every_one_of_512_cells_is_explicitly_resolved(self):
        rows = self.certificate["rows"]
        self.assertEqual(len(rows), 64)
        self.assertEqual(len({(row["side"], row["d"]) for row in rows}), 64)
        expected_places = {"infinity", *(str(p) for p in N.BAD_PRIMES)}
        for row in rows:
            self.assertEqual(set(row["places"]), expected_places)
            for cell in row["places"].values():
                self.assertIn(cell["status"], {"YES", "NO", "UNRESOLVED"})
                self.assertNotEqual(cell["status"], "UNRESOLVED")
                self.assertIn("depth", cell)

    def test_every_finite_yes_cell_has_an_exact_qp_square(self):
        for row in self.certificate["rows"]:
            for place, cell in row["places"].items():
                if place == "infinity" or cell["status"] != "YES":
                    continue
                prime = int(place)
                witness = cell["witness"]
                U, V = int(witness["U"]), int(witness["V"])
                rhs = C.quartic_rhs(row["side"], row["d"], U, V)
                self.assertEqual(rhs, witness["rhs"])
                if prime == 2:
                    self.assertTrue(N.q2_square(rhs))
                else:
                    self.assertTrue(N.odd_p_square(rhs, prime))

    def test_every_no_cell_has_the_claimed_exact_proof(self):
        for row in self.certificate["rows"]:
            side, d = row["side"], row["d"]
            for place, cell in row["places"].items():
                if cell["status"] != "NO":
                    continue
                method = cell["method"]
                if place == "infinity":
                    self.assertEqual(side, "E")
                    self.assertLess(d, 0)
                    self.assertEqual(method, "REAL_NO_SIGN")
                elif method == "exhaustive_weighted_projective_mod_prime_power":
                    depth = cell["depth"]
                    self.assertFalse(
                        N.has_projective_solution_mod_prime_power(
                            d,
                            N.SIDES[side]["a"],
                            N.SIDES[side]["b"],
                            int(place),
                            depth["exponent"],
                        )
                    )
                elif method == "valuation_normalized_double_root_obstruction":
                    self.assertEqual(
                        cell,
                        {**C.multiplicative_prime_obstruction(d, int(place)),
                         "previous_status": cell["previous_status"]},
                    )
                else:
                    self.fail((side, d, place, method))

    def test_the_former_56_unresolved_cells_are_24_yes_and_32_no(self):
        summary = self.certificate["summary"]
        self.assertEqual(
            summary["previous_56_unresolved_resolved_as"],
            {"YES": 24, "NO": 32, "UNRESOLVED": 0},
        )
        self.assertEqual(summary["status_counts"], {"YES": 384, "NO": 128, "UNRESOLVED": 0})
        self.assertEqual(summary["cells"], 512)

    def test_exact_final_ambient_survivors(self):
        survivors = self.certificate["summary"]["surviving_ambient_classes"]
        self.assertEqual(survivors["E"], [1, 3, 5, 7, 15, 21, 35, 105])
        self.assertEqual(
            survivors["E_dual"],
            [1, 4230241, 339106321, 1434501462453361],
        )
        initial = self.certificate["initial_stage_survivors_16_plus_4"]
        self.assertEqual(len(initial["E"]), 16)
        self.assertEqual(len(initial["E_dual"]), 4)

    def test_C_H_reconstruction_resolvent_and_projected_class(self):
        data = self.certificate["torsor_projection"]
        self.assertTrue(data["H_equals_Campbell_g_at_x_8"])
        I, J = C.binary_quartic_invariants()
        self.assertEqual((I, J), (data["I"], data["J"]))
        phi = data["rational_resolvent_root_phi"]
        self.assertEqual(phi**3 - 3*I*phi + J, 0)
        a, b, c, _, _ = C.H_COEFFS
        self.assertEqual(data["g4_at_1_0"], 3*b*b - 8*a*c)
        self.assertEqual(3*data["z_rational_component"], 4*a*phi + data["g4_at_1_0"])
        self.assertEqual(C.squarefree_part(data["z_rational_component"]), 35)
        self.assertEqual(data["projection_to_isogeny_ambient_class"], {
            "side": "E",
            "d": 35,
            "identity": "x_big+3*phi=64^2*(x_small+197298357)=64^2*X",
            "meaning": (
                "This is the rational-2-torsion component of the H^1(Q,J_H[2]) "
                "class of C_H, not a claim that C_H is isomorphic to the displayed C_d quartic."
            ),
        })
        self.assertIn(35, self.certificate["summary"]["surviving_ambient_classes"]["E"])

    def test_large_small_jacobian_scaling(self):
        data = self.certificate["torsor_projection"]
        I, J = data["I"], data["J"]
        u = data["large_to_small_weierstrass_scaling_u"]
        self.assertEqual((-27*I)//u**4, -58243635870855147)
        self.assertEqual((-27*J)//u**6, -3811211217040595260188186)
        self.assertEqual(-3*data["rational_resolvent_root_phi"], u**2*data["small_rational_2_torsion_x"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
