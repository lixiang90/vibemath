# Data and code availability

All code and finite certificate data needed for the theorem are in the public
working archive at
<https://github.com/lixiang90/vibemath/tree/main/powers-in-progressions/pure-cubic-five-term>.
The existing repository-root `MANIFEST.sha256` describes the last frozen
payload.  The Round-09 extension and this synchronized submission prose still
require a newly generated root manifest before release.  No preservation
service DOI or frozen GitHub release has yet been assigned.

The current Round-09 extension is reproduced by 29 tests and includes the
29-model reconstruction, the 25 explicit coordinate-permutation clusters,
and four closed positive-rank orbits, leaving 27 models open.  Its corrected
certificate
`code/PAPER_CUBE_FOURHIT_CLUSTER_ROUND09_CERTIFICATE.json` has SHA-256
`4217f170ce6cd27d488811119289dd1cccb480b47c536c23bd10be99b1193662`.
Cross-review found and repaired a metadata-only variable interchange in the
`0100` zero-boundary record; the generator and test now check the underlying
polynomial identities rather than comparing descriptive strings alone.

Persistent archive DOI: `<<ARCHIVE DOI — USER INPUT>>`

Persistent archive URL: `<<IMMUTABLE RELEASE URL — USER INPUT>>`

The historical supplement manifest describes its original local release and
must not be silently rewritten.  Before submission, freeze the current public
payload under an immutable release URL or DOI and verify the download against
the root hash manifest.  If any file changes, issue a new semantic release and
regenerate all hashes rather than reusing the old locator.

Suggested final wording after deposit: “The exact source, tests, certificate,
manifest and manuscript for this release are archived at <<DOI/URL>>.”
