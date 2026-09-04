# Build instructions

From the repository root, build the paper with standard LaTeX packages:

    latexmk -cd -pdf -interaction=nonstopmode -halt-on-error square-progressions/seven-consecutive-squareclasses/paper/main.tex

Run every repository check, including the squareclasses group, with:

    python tools/run_all_checks.py

To run only the authoritative squareclasses group while retaining its clean
temporary flat staging layout, use:

    python -c "from tools.run_all_checks import square_group,run_group; run_group('squareclasses',*square_group())"

The individual commands below apply inside an exported flat supplement
directory containing the 35 files listed by
`PAPER_SQUARE_SUPPLEMENT_MANIFEST.json`.  They are not repository-root
commands:

    python PAPER_SQUARE_SAFE_inventory.py
    python PAPER_SQUARE_MASK77_analysis.py --bound 1000000
    python PAPER_SQUARE_NEXT_GATE.py
    python PAPER_SQUARE_MASK108.py
    python PAPER_SQUARE_MASK99.py
    python PAPER_SQUARE_MASK51.py
    python PAPER_SQUARE_MASK90.py
    python PAPER_SQUARE_MASK54.py
    python PAPER_SQUARE_MASK85.py
    python PAPER_SQUARE_SUPPLEMENT_MANIFEST.py
    python -m unittest -v STUDENT_SQUARE_ROUND_02_test_patterns.py STUDENT_SQUARE_ROUND_03_test.py STUDENT_SQUARE_ROUND_04_test.py PAPER_SQUARE_SAFE_test.py PAPER_SQUARE_MASK77_test.py PAPER_SQUARE_NEXT_GATE_test.py PAPER_SQUARE_MASK108_test.py PAPER_SQUARE_MASK99_test.py PAPER_SQUARE_MASK51_test.py PAPER_SQUARE_MASK90_test.py PAPER_SQUARE_MASK54_test.py PAPER_SQUARE_MASK85_test.py PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py

The bounded search emitted by `PAPER_SQUARE_MASK77_analysis.py` is labelled
conjectural and is not used in the proof.
