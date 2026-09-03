/*
  Audited decisive computation for the Campbell ninth-point curve.

  The local rows are copied from STUDENT_ELLIPTIC_ROUND_03_certificate.json,
  SHA-256 74843e4e53c7d09793fa857a2ce57d37a21be855ce135fec9f22b5b00aab5e08.
  The PowerShell wrapper checks that hash before launching Magma.

  The descent call below has no optional bound parameter.  It is intended to
  compute the complete fake 2-Selmer set.
*/

print "AUDIT_BEGIN";
print "MAGMA_GET_VERSION", GetVersion();

Q := Rationals();
Qm<m> := PolynomialRing(Q);
D := -264815*m^4 - 19343520*m^3 + 62846856064*m^2
     - 2906312951808*m - 495507443511296;
H := -850079*m^4 - 11210976*m^3 + 138714149248*m^2
     - 5501355374592*m - 1679721044504576;

/* Real fibre-product certificate: the same m works for D and H. */
mReal := -400;
assert Evaluate(D,mReal) eq 5181235987451904;
assert Evaluate(H,mReal) eq 1670565049012224;
assert Evaluate(D,mReal) gt 0 and Evaluate(H,mReal) gt 0;

/* Q_2 fibre-product certificate: the same odd m gives two square units. */
mTwo := 1;
dTwo := Integers()!Evaluate(D,mTwo);
hTwo := Integers()!Evaluate(H,mTwo);
assert dTwo eq -498350929215375;
assert hTwo eq -1685083697790975;
assert dTwo mod 8 eq 1 and hTwo mod 8 eq 1;

/* Rows are [p,m,D(m),sqrt(D),H(m),sqrt(H)] modulo p. */
localRows := [
    [3,0,1,1,1,1],
    [5,0,4,2,4,2],
    [7,0,1,1,4,2],
    [11,0,4,2,4,2],
    [13,3,3,4,1,1],
    [17,0,16,4,16,4],
    [19,3,11,7,11,7],
    [23,1,16,4,9,3],
    [29,5,28,12,25,5],
    [31,1,18,7,14,13],
    [37,1,1,1,25,5],
    [41,2,18,10,1,1],
    [43,3,1,1,35,11],
    [47,6,37,15,27,11],
    [53,1,10,13,1,1],
    [59,12,3,11,35,25],
    [61,4,36,6,46,30],
    [67,3,35,13,56,18],
    [71,17,58,22,38,31],
    [73,0,9,3,37,16],
    [79,8,2,9,19,16],
    [83,2,7,16,25,5],
    [89,1,55,12,34,37],
    [97,1,65,29,93,44],
    [8599,5,4872,521,3474,1968],
    [71699,1,13080,12817,43856,30327],
    [898543,12,593875,198084,686233,420590],
    [23037169,1,7173562,1999717,70894,4416133],
    [339106321,1,59232546,46825223,41459015,138493612],
    [1153266911,0,604401320,115415469,678697814,139525893]
];

expectedCertificatePrimes := [
    3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,
    83,89,97,8599,71699,898543,23037169,339106321,1153266911
];
assert [row[1] : row in localRows] eq expectedCertificatePrimes;

for row in localRows do
    p := row[1];
    m0 := row[2];
    dv := row[3];
    dy := row[4];
    hv := row[5];
    hz := row[6];
    assert (Integers()!Evaluate(D,m0)) mod p eq dv mod p;
    assert (Integers()!Evaluate(H,m0)) mod p eq hv mod p;
    assert dy mod p ne 0 and hz mod p ne 0;
    assert (dy^2-dv) mod p eq 0;
    assert (hz^2-hv) mod p eq 0;
end for;

discD := Integers()!Discriminant(D);
discH := Integers()!Discriminant(H);
resDH := Integers()!Resultant(D,H);
bad := Sort(Setseq({2} join Seqset(PrimeDivisors(Abs(discD)))
                      join Seqset(PrimeDivisors(Abs(discH)))
                      join Seqset(PrimeDivisors(Abs(resDH)))));
assert bad eq [2,3,5,7,17,19,31,59,8599,71699,898543,23037169,
               339106321,1153266911];
assert GCD(D,H) eq 1;
assert 499918929737821954398975452824771913318400^2 eq resDH;

print "SAME_M_FIBRE_PRODUCT_LOCAL_CERTIFICATES_OK";
print "LOCAL_COVERAGE_OK: real, Q2, odd p<101, branch-model bad odd primes";
print "LOCAL_COVERAGE_REMAINDER: good p>=101 follows from genus-5 Weil bound and Hensel";

CH := HyperellipticCurve(H);
print "FAKE_TWO_SELMER_DESCENT_BEGIN_UNBOUNDED_OPTIONALS_OMITTED";
time SelH, AtoSelH := TwoCoverDescent(CH);
print "FAKE_TWO_SELMER_DESCENT_COMPLETED";
print "FAKE_TWO_SELMER_CARDINALITY", #SelH;
print "FAKE_TWO_SELMER_SET", SelH;

if #SelH eq 0 then
    print "PROVED_FROM_EMPTY_FAKE_TWO_SELMER: CH(Q) IS EMPTY";
    print "PROVED_FROM_EMPTY_FAKE_TWO_SELMER: CAMPBELL_FIBRE_PRODUCT(Q) IS EMPTY";
else
    print "NONEMPTY_FAKE_TWO_SELMER_ONLY: NO RATIONAL POINT CONCLUSION";
end if;

print "AUDIT_COMPLETED";
quit;
