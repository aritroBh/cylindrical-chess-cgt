"""Shared TikZ preamble and build step for the 2026-11 candidate figures.
Same fonts and colours as paper/ieee/make_figures.py (TeX Gyre Termes/Heros, Apple Symbols chess glyphs,
blue and white squares).  Builds with tectonic, then makes a 300 dpi PNG preview with pdftoppm."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIGHT, DARK, LINE = "EDEDED", "7389B8", "4A4A4A"

PREAMBLE = r"""\documentclass[border=1pt]{standalone}
\usepackage{fontspec}
\usepackage{unicode-math}
\setmainfont{texgyretermes}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold,
  ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
\setsansfont{texgyreheros}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold]
\setmathfont{texgyretermes-math.otf}
\newfontfamily\chessfont{Apple Symbols}
\usepackage{tikz}
\usepackage{pgfplots}
\usetikzlibrary{arrows.meta}
\pgfplotsset{compat=1.17}
\definecolor{light}{HTML}{%s}
\definecolor{dark}{HTML}{%s}
\definecolor{edge}{HTML}{%s}
\definecolor{blue2}{HTML}{B9C6E0}
\definecolor{seam}{HTML}{D55E00}
\begin{document}
\fontsize{8}{9.6}\selectfont
""" % (LIGHT, DARK, LINE)


def build(name, body):
    tex = os.path.join(HERE, name + ".tex")
    with open(tex, "w") as fh:
        fh.write(PREAMBLE + body + "\n\\end{document}\n")
    r = subprocess.run(["tectonic", "-X", "compile", "--outdir", HERE, tex], capture_output=True, text=True)
    if r.returncode:
        sys.exit(name + ": tectonic failed\n" + r.stderr[-2500:])
    os.remove(tex) if os.environ.get("KEEP_TEX") is None else None
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile",
                    os.path.join(HERE, name + ".pdf"), os.path.join(HERE, name)], check=True)
    out = subprocess.run(["pdfinfo", os.path.join(HERE, name + ".pdf")], capture_output=True, text=True).stdout
    print(name, [l for l in out.splitlines() if l.startswith("Page size")])
