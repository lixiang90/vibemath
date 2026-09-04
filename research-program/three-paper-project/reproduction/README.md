# Cold reproduction records

This directory stores durable evidence from clean-clone reproduction runs.
The runner clones one committed Git tree into an operating-system temporary
directory, checks out the exact commit, runs every archived mathematical test,
rebuilds all three papers, scans each final LaTeX log, and compares the text
extracted from each rebuilt PDF with the committed PDF.

Run from the repository root:

```text
python tools/cold_reproduce.py --commit HEAD --output-dir research-program/three-paper-project/reproduction
```

Each run produces a compact JSON report plus the complete combined command
log.  Build intermediates are deleted with the temporary clone.

## Recorded successful runs

| round | commit | tests | PDF pages | record |
|---|---|---:|---|---|
| 07 | `559e89364b6e5c5e38e60d7b55b43ebb56e40409` | 183 | 9 / 6 / 8 | `INTERNAL_COLD_REPRODUCTION_559e89364b6e.json` |
| 08 | `4a8dae3dbc04712991783053e97b14b2d073964a` | 198 | 10 / 7 / 9 | `INTERNAL_COLD_REPRODUCTION_4a8dae3dbc04.json` |
| 09 | `85eb55b49f9f80e05a7d890fec7cc289083b802b` | 218 | 10 / 7 / 10 | `INTERNAL_COLD_REPRODUCTION_85eb55b49f9f.json` |
| 10 | `ccc4c4be6562534f25b18817c6c4773bb0cf0cc4` | 243 | 11 / 8 / 11 | `INTERNAL_COLD_REPRODUCTION_ccc4c4be6562.json` |
| 11 | `20bb94753801907b46d41db611ab18c4cd9f9a10` | 266 | 11 / 9 / 11 | `INTERNAL_COLD_REPRODUCTION_20bb94753801.json` |
| 12 | `29019a1b844d3db570029eab315477c5f6c46fe3` | 266 | 12 / 10 / 11 | `INTERNAL_COLD_REPRODUCTION_29019a1b844d.json` |

For Round10, all three committed/rebuilt text hashes are equal, every final-log
warning list is empty, and the combined log SHA-256 is
`72486507e0ebfafe8ba4b4a2415bcb19056a4e23d392d223548629bab6e59645`.

For Round11, all six groups `96/33/42/14/8/73` pass, all three
committed/rebuilt text hashes are equal, and every final-log warning list is
empty. The text hashes for squareclasses, pure cubic and Campbell Selmer are
`5aca3c9cc84f52121a501a3f08640d1aa806a0154e2bb1429cd0e977e6659f9d`,
`59cdb61632ddc7273a3733f562206a23e6bec2ddca0dbfd2ffc3e200effb9fbe`, and
`7616879662139ea87f2fc1d992aa5e7fafff45ea7057dc79d6ad4181a9752b23`.
The JSON SHA-256 is
`ab12184073c6c53d90d306caa701eb1476dbf1e02c944eb7c84bfa42fdf6c1c4`;
the combined log SHA-256 is
`584cb911399d45d666b8cc7a1123d30650f478feefe1fbd810bd13723e9dfe46`.

For Round12, the same six groups `96/33/42/14/8/73` pass in a clean clone of
source commit `29019a1b844d3db570029eab315477c5f6c46fe3`. The PDFs rebuild to
12 / 10 / 11 pages, every final-log warning-pattern list is empty, and the
committed/rebuilt text hashes agree. The squareclasses, pure-cubic and Campbell
Selmer text hashes are
`aa31abfe701256176428bf7dae2353f21bee7d5ca588f5e2c9393449e7e5175b`,
`7c6663afe703196f5c16d2e71e327f999704a4fbca74227e5e8008f142d57f1e`, and
`5988c0aa3947a6cbe9cac0925c1e0394c3bf9555512979e1670d01014152c883`.
The JSON SHA-256 is
`e49cb775dc43991611acc746b69c3cb862f9181d59c739c744cbcd440e4b9848`;
the combined log SHA-256 is
`9fbcecb02c8ce7b0187fcb3c36027e18ea90cb78b546a4c77e21b82b47f25e66`.

These records prove an **internal clean-clone reproduction** on the recorded
machine.  They do not prove that a human outside the project independently
understood or reproduced the mathematics.  External reproduction remains a
separate completion gate and must record the reviewer, environment, commit,
commands and outcome without overwriting the internal record.
