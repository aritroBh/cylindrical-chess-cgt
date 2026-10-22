"""Board pictures and graphs for the paper, in the style of the 2025 paper's diagrams
(blue and white squares, rank numbers on the left, file letters underneath).

Each figure is written as a standalone TikZ/pgfplots file in figures/src/ and compiled with tectonic into
figures/<name>.pdf, which main.tex includes. Pieces use the chess glyphs of the macOS font Apple Symbols,
so regenerate on a Mac; Overleaf only needs the PDFs.

    .venv/bin/python paper/figures/make_figures.py            # all figures
    .venv/bin/python paper/figures/make_figures.py eighth kpk  # only these
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(HERE, "src")
sys.path.insert(0, ROOT)

LIGHT, DARK, LINE = "EDEDED", "7389B8", "4A4A4A"
GLYPH = {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "N": "♞", "P": "♟"}
OUTLINE = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙"}
TREB = "Kf5 Pg4 kh4 pg5"  # the trebuchet king group

PREAMBLE = r"""\documentclass[border=3pt]{standalone}
\usepackage{fontspec}
\newfontfamily\chessfont{Apple Symbols}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.17}
\definecolor{light}{HTML}{%s}
\definecolor{dark}{HTML}{%s}
\definecolor{edge}{HTML}{%s}
\definecolor{blue2}{HTML}{B9C6E0}
\begin{document}
""" % (LIGHT, DARK, LINE)


def board(pieces, marks=(), arrows=()):
    """pieces: 'Kf5 pg5 ...' (upper case = white). marks: squares to ring. arrows: ('a2','a4') pairs."""
    s = 0.62  # square size in cm
    out = [r"\begin{tikzpicture}[x=%.2fcm,y=%.2fcm]" % (s, s)]
    for f in range(8):
        for r in range(8):
            col = "light" if (f + r) % 2 else "dark"
            out.append(rf"\fill[{col}] ({f},{r}) rectangle ({f + 1},{r + 1});")
    out.append(r"\draw[edge, line width=0.8pt] (0,0) rectangle (8,8);")
    for r in range(8):
        out.append(rf"\node[anchor=east, text=gray, font=\sffamily\scriptsize] at (-0.05,{r + 0.5}) {{{r + 1}}};")
    for f in range(8):
        out.append(rf"\node[anchor=north, text=gray, font=\sffamily\scriptsize] at ({f + 0.5},-0.05) {{{'abcdefgh'[f]}}};")
    for sq in marks:
        f, r = "abcdefgh".index(sq[0]), int(sq[1]) - 1
        out.append(rf"\draw[red!70!black, line width=1.1pt] ({f + 0.5},{r + 0.5}) circle (0.47);")
    for tok in pieces.split():
        p, f, r = tok[0], "abcdefgh".index(tok[1]), int(tok[2]) - 1
        size = r"\fontsize{17}{17}\selectfont"
        at = f"({f + 0.5},{r + 0.47})"
        if p.isupper():  # white piece: white body, black outline
            out.append(rf"\node[text=white] at {at} {{\chessfont{size}{GLYPH[p]}}};")
            out.append(rf"\node[text=black] at {at} {{\chessfont{size}{OUTLINE[p]}}};")
        else:
            out.append(rf"\node[text=black] at {at} {{\chessfont{size}{GLYPH[p.upper()]}}};")
    for a, b in arrows:
        fa, ra = "abcdefgh".index(a[0]) + 0.5, int(a[1]) - 0.5
        fb, rb = "abcdefgh".index(b[0]) + 0.5, int(b[1]) - 0.5
        out.append(rf"\draw[-latex, line width=2pt, green!45!black, opacity=0.75] ({fa},{ra}) -- ({fb},{rb});")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def bars(ylabel, symbolic, series, ymax=100, width="12cm", legend_cols=3, nodes=False):
    """Grouped bar chart. series: [(legend, colour, [values])]."""
    out = [r"\begin{tikzpicture}\begin{axis}[ybar, bar width=7pt, width=%s, height=5.2cm," % width,
           r"  ymin=0, ymax=%s, ylabel={%s}, symbolic x coords={%s}, xtick=data," % (ymax, ylabel, ",".join(symbolic)),
           r"  x tick label style={font=\small}, ymajorgrids, grid style={gray!25}, enlarge x limits=0.08,",
           r"  legend style={at={(0.5,1.03)}, anchor=south, legend columns=%d, draw=none, font=\small}," % legend_cols,
           r"  axis line style={edge}" + (r", nodes near coords, nodes near coords style={font=\tiny}" if nodes else "") + "]"]
    for name, colour, vals in series:
        coords = " ".join(f"({x},{v})" for x, v in zip(symbolic, vals))
        out.append(rf"\addplot[fill={colour}, draw=edge] coordinates {{{coords}}};")
        out.append(rf"\addlegendentry{{{name}}}")
    out.append(r"\end{axis}\end{tikzpicture}")
    return "\n".join(out)


def dawson_grundy():
    from dawson.octal import grundy
    g = grundy("0.137", 120)
    pts = " ".join(f"({n},{g[n]})" for n in range(len(g)))
    ring = " ".join(f"({m},0)" for m in range(len(g)) if g[m] == 0)
    return "\n".join([
        r"\begin{tikzpicture}\begin{axis}[width=13cm, height=4.6cm, xmin=-1, xmax=121, ymin=-0.5, ymax=9.5,",
        r"  xlabel={strip length $n$}, ylabel={Grundy value $g(n)$}, ytick={0,2,...,8}, ymajorgrids,",
        r"  grid style={gray!25}, axis line style={edge},",
        r"  legend style={at={(0.5,1.03)}, anchor=south, legend columns=2, draw=none, font=\small}]",
        rf"\addplot[ycomb, dark, line width=1.6pt] coordinates {{{pts}}};",
        r"\addlegendentry{$g(n)$ for the flat $3\times n$ board}",
        rf"\addplot[only marks, mark=*, mark size=1.6pt, red!70!black] coordinates {{{ring}}};",
        r"\addlegendentry{$g(m)=0$: the $3\times(m+3)$ cylinder is a first-player win}",
        r"\end{axis}\end{tikzpicture}"])


def star2_by_pawns():
    # *2 positions under the count rule with the e.p.-aware passed test, flat boards of width <= 4
    # (atlas/flat8/rerun census for <= 6 pawns; research/star2_frontier scope (b) for 7 and 8 pawns,
    # each hit re-checked with cylcgt in delegate/checks/star2_caware_check.out)
    counts = {4: 0, 5: 0, 6: 0, 7: 2, 8: 4}
    coords = " ".join(f"({k},{v})" for k, v in counts.items())
    return "\n".join([
        r"\begin{tikzpicture}\begin{axis}[ybar, bar width=16pt, width=8cm, height=4.6cm, ymin=0, ymax=5,",
        r"  xtick={4,5,6,7,8}, xlabel={number of pawns}, ylabel={positions of value $\ast2$},",
        r"  ymajorgrids, grid style={gray!25}, axis line style={edge}, nodes near coords,",
        r"  nodes near coords style={font=\small}]",
        rf"\addplot[fill=dark, draw=edge] coordinates {{{coords}}};",
        r"\end{axis}\end{tikzpicture}"])


T = TREB
FIGURES = {
    # boards
    "trebuchet": lambda: board(T),
    "elkies_dup": lambda: board("Pa2 pa6"),
    "star2_textbook": lambda: board("Pa2 Pc2 pb7 pd7 " + T, arrows=[("c2", "c4")]),
    "eighth": lambda: board("Pa2 Pb2 Pb3 pa5 pa6 pb6 " + T),
    "upsecstar": lambda: board("Pa2 Pb2 Pb6 pa6 pb7 pc5 " + T),
    "tiny1": lambda: board("Pa2 Pb2 Pb6 pa6 pb7 pc6 " + T),
    "star2_seven_a": lambda: board("Pa4 Pb3 Pd2 Pd3 pa7 pb7 pc5 " + T),
    "star2_seven_b": lambda: board("Pb4 Pc2 Pd2 pa6 pa7 pc6 pd5 " + T),
    "star2_eight_five": lambda: board("Pa3 Pb3 Pc2 Pe2 pa6 pc5 pd5 pe3 " + T),
    "kpk_rookpawn": lambda: board("Ka6 Pa5 ka8"),
    "eighth_open": lambda: board("Pb2 Pb5 pa5 pb4 " + T),
    # graphs
    "tb_bars": lambda: bars(r"positions won (\%)", ["KQK", "KRK", "KBBK", "KBNK", "KNNK", "KRBK", "KRRK", "KQRK"],
                            [("plane", "edge!55", [100, 100, 99.98, 99.51, 0.0107, 100, 100, 100]),
                             ("cylinder", "dark", [100, 2.80, 100, 0.0245, 0.0077, 99.74, 100, 100]),
                             ("torus", "blue2", [0, 0, 0, 0, 0, 0.0218, 100, 100])]),
    "kpk_bars": lambda: bars(r"White wins (\%)", ["White to move", "Black to move"],
                             [("plane", "edge!55", [76.51, 58.09]), ("cylinder", "dark", [78.89, 55.88])],
                             width="7cm", legend_cols=2, nodes=True),
    "star2_by_pawns": star2_by_pawns,
    "dawson_grundy": dawson_grundy,
}


def build(name):
    os.makedirs(SRC, exist_ok=True)
    path = os.path.join(SRC, f"{name}.tex")
    with open(path, "w") as fh:
        fh.write(PREAMBLE + FIGURES[name]() + "\n\\end{document}\n")
    r = subprocess.run(["tectonic", "-X", "compile", "--outdir", HERE, path], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"{name}: tectonic failed\n{r.stderr[-1500:]}")
    print(f"figures/{name}.pdf")


if __name__ == "__main__":
    for name in sys.argv[1:] or FIGURES:
        build(name)
