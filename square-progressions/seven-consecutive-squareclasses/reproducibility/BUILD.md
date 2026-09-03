# Build instructions

The paper uses standard LaTeX packages. From this directory run:

    D:\texlive\2022\bin\win32\latexmk.exe -pdf -interaction=nonstopmode -halt-on-error main.tex

The generated artifacts are main.pdf and build.log. Rebuild the certificate
from the repository root with:

    python PAPER_SQUARE_SAFE_inventory.py
    python PAPER_SQUARE_MASK77_analysis.py --bound 1000000
    python PAPER_SQUARE_NEXT_GATE.py
    python PAPER_SQUARE_MASK108.py
    python PAPER_SQUARE_MASK99.py
    python PAPER_SQUARE_MASK51.py
    python PAPER_SQUARE_MASK90.py
    python PAPER_SQUARE_SUPPLEMENT_MANIFEST.py
    python -m unittest -v STUDENT_SQUARE_ROUND_02_test_patterns.py STUDENT_SQUARE_ROUND_03_test.py STUDENT_SQUARE_ROUND_04_test.py PAPER_SQUARE_SAFE_test.py PAPER_SQUARE_MASK77_test.py PAPER_SQUARE_NEXT_GATE_test.py PAPER_SQUARE_MASK108_test.py PAPER_SQUARE_MASK99_test.py PAPER_SQUARE_MASK51_test.py PAPER_SQUARE_MASK90_test.py PAPER_SQUARE_SUPPLEMENT_MANIFEST_test.py

The bounded search emitted by the first command is labelled conjectural and
is not used in the proof.
