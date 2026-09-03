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

These records prove an **internal clean-clone reproduction** on the recorded
machine.  They do not prove that a human outside the project independently
understood or reproduced the mathematics.  External reproduction remains a
separate completion gate and must record the reviewer, environment, commit,
commands and outcome without overwriting the internal record.
