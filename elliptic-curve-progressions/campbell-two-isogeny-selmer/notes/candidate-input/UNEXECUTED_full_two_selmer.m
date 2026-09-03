// Frozen, unexecuted input for the corrected full 2-descent problem.
// It deliberately never pairs the opposite isogeny classes 35 and 4230241.
// Expected semantics (Magma handbook, current at 2026-09-03):
//   TwoDescent(E) returns locally soluble 2-coverings of E;
//   CasselsTatePairing(C,D) is defined only for locally soluble 2-coverings
//   admitting maps to the same elliptic curve;
//   FourDescent(CH)=[] implies that the class of CH does not lift to Sel^4.

Q := Rationals();
Qm<m> := PolynomialRing(Q);
H := -850079*m^4-11210976*m^3+138714149248*m^2
     -5501355374592*m-1679721044504576;
CH := HyperellipticCurve(H);
EH, mapH := AssociatedEllipticCurve(CH);

print "PAPER_ELLIPTIC_ROUND_05_BEGIN";
print "MAGMA_VERSION", GetVersion();
print "H", H;
print "ASSOCIATED_ELLIPTIC_CURVE", EH;
print "EXPECTED_CUBIC_ALGEBRA_D", 1434501462453361;
print "EXPECTED_Z_Q", 9250179026780160;
print "EXPECTED_Z_K_BASIS_1_SQRTD", [467235380575281152,-6963847168];

SetVerbose("TwoDescent", 1);
time covers := TwoDescent(EH : WithMaps := false);
print "FULL_TWO_DESCENT_COVER_COUNT", #covers;
for i in [1..#covers] do
    print "FULL_TWO_COVER", i, covers[i];
end for;

SetVerbose("CasselsTate", 2);
for i in [1..#covers] do
    time bit := CasselsTatePairing(CH, covers[i]);
    print "FULL_CT_PAIRING_WITH_CH", i, bit;
end for;

// This independently tests whether the CH class lifts from Sel^2 to Sel^4.
// Empty output is a rigorous obstruction; nonempty output is not a point.
SetVerbose("FourDescent", 1);
time four_covers := FourDescent(CH);
print "CH_FOUR_DESCENT_COVER_COUNT", #four_covers;
for i in [1..#four_covers] do
    print "CH_FOUR_COVER", i, four_covers[i];
end for;
print "PAPER_ELLIPTIC_ROUND_05_END";
