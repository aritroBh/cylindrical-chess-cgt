"""Board pictures and graphs for the IEEE version of the paper, in the style of the 2025 paper's
diagrams (blue and white squares, rank numbers on the left, file letters underneath).

Each figure is written as a standalone TikZ/pgfplots file in figures/src/ and compiled with tectonic
into figures/<name>.pdf, which main.tex includes. Pieces use the chess glyphs of the macOS font
Apple Symbols, so regenerate on a Mac; Overleaf and arXiv only need the PDFs.

Sizes: "small" boards are about 1.6 in wide (two per column with subfig), "column" boards about
2.5 in. Graphs are \\columnwidth (about 8.5 cm) with 8 pt text; dawson_grundy is full width (figure*).

    .venv/bin/python paper/ieee/make_figures.py              # build every figure
    .venv/bin/python paper/ieee/make_figures.py zero eighth  # only these
    PYTHONPATH=. .venv/bin/python paper/ieee/make_figures.py --check
        # re-verify every board: pawn value with cylcgt (count rule, e.p.-aware test, e.p. on)
        # and chess legality (no pawn on rank 1 or 8, kings apart across the seam, no check)
"""
import os
import shutil
import subprocess
import sys

IEEE = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(IEEE, "figures")          # output directory: paper/ieee/figures
SRC = os.path.join(HERE, "src")
ROOT = os.path.dirname(os.path.dirname(IEEE))
sys.path.insert(0, ROOT)

LIGHT, DARK, LINE = "EDEDED", "7389B8", "4A4A4A"
GLYPH = {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "N": "♞", "P": "♟"}
OUTLINE = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙"}
FILES = "abcdefgh"
TREB = "Kf5 Pg4 kh4 pg5"  # the trébuchet king group on the f, g and h files (ordinary board)

PREAMBLE = r"""\documentclass[border=3pt]{standalone}
\usepackage{fontspec}
\usepackage{unicode-math}
\setmainfont{texgyretermes}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold,
  ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
\setsansfont{texgyreheros}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold]
\setmathfont{texgyretermes-math.otf}
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

# square size (cm), glyph size (pt), label font, frame width (pt)
SIZES = {
    "small": (0.44, 12.0, r"\fontsize{9}{9}\selectfont", 0.6),    # about 1.6 in wide; 9 pt labels print
                                                                   # at 6.5-8 pt after scaling
    "column": (0.74, 20.3, r"\fontsize{7.5}{7.5}\selectfont", 0.8),  # about 2.5 in wide
}


def _sq(name):
    return FILES.index(name[0]), int(name[1:]) - 1


def _piece(out, p, f, r, glyph):
    size = r"\fontsize{%.1f}{%.1f}\selectfont" % (glyph, glyph)
    at = f"({f + 0.5},{r + 0.47})"
    if p.isupper():  # white piece: white body, black outline
        out.append(rf"\node[text=white, inner sep=0] at {at} {{\chessfont{size}{GLYPH[p]}}};")
        out.append(rf"\node[text=black, inner sep=0] at {at} {{\chessfont{size}{OUTLINE[p]}}};")
    else:
        out.append(rf"\node[text=black, inner sep=0] at {at} {{\chessfont{size}{GLYPH[p.upper()]}}};")


def _grid(out, files, ranks, size):
    s, glyph, label, frame = SIZES[size]
    for f in range(files):
        for r in range(ranks):
            col = "light" if (f + r) % 2 else "dark"
            out.append(rf"\fill[{col}] ({f},{r}) rectangle ({f + 1},{r + 1});")
    out.append(r"\draw[edge, line width=%.1fpt] (0,0) rectangle (%d,%d);" % (frame, files, ranks))
    for r in range(ranks):
        out.append(rf"\node[anchor=east, text=black!70, font=\sffamily{label}] at (-0.04,{r + 0.5}) {{{r + 1}}};")
    for f in range(files):
        out.append(rf"\node[anchor=north, text=black!70, text height=1.45ex, text depth=0.2ex, inner sep=1.5pt, font=\sffamily{label}]"
                   rf" at ({f + 0.5},-0.04) {{{FILES[f]}}};")


def board(pieces, size="small", files=8, ranks=8, marks=(), arrows=()):
    """pieces: 'Kf5 pg5 ...' (upper case = white). marks: squares to ring. arrows: ('a2','a4') pairs.
    `files` < 8 draws a narrow board (the 3- and 4-file cylinders)."""
    s, glyph, label, frame = SIZES[size]
    out = [r"\begin{tikzpicture}[x=%.2fcm,y=%.2fcm]" % (s, s)]
    _grid(out, files, ranks, size)
    for sq in marks:
        f, r = _sq(sq)
        out.append(rf"\draw[red!70!black, line width=1.1pt] ({f + 0.5},{r + 0.5}) circle (0.47);")
    for tok in pieces.split():
        f, r = _sq(tok[1:])
        _piece(out, tok[0], f, r, glyph)
    for a, b in arrows:
        (fa, ra), (fb, rb) = _sq(a), _sq(b)
        n = max(abs(fb - fa), abs(rb - ra))  # start the arrow at the edge of the moving piece
        x0, y0 = fa + 0.5 + 0.38 * (fb - fa) / n, ra + 0.5 + 0.38 * (rb - ra) / n
        out.append(r"\draw[-latex, line width=%.1fpt, green!45!black, opacity=0.8] (%.2f,%.2f) -- (%.1f,%.1f);"
                   % (2.0 * s / 0.62, x0, y0, fb + 0.5, rb + 0.5))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def dawson_strip(n=6, ring=False, size="small"):
    """Dawson's chess: 3 rows, n files, white pawns on rank 1 and black pawns on rank 3.
    With `ring`, the last file is adjacent to file a (the cylinder); the two glued edges are dashed."""
    s, glyph, label, frame = SIZES[size]
    out = [r"\begin{tikzpicture}[x=%.2fcm,y=%.2fcm]" % (s, s)]
    _grid(out, n, 3, size)
    for f in range(n):
        _piece(out, "P", f, 0, glyph)
        _piece(out, "p", f, 2, glyph)
    if ring:
        for x in (0, n):  # the seam: the left edge of file a is glued to the right edge of the last file
            out.append(r"\draw[red!70!black, line width=2pt, dash pattern=on 4pt off 3pt] (%d,-0.25) -- (%d,3.25);" % (x, x))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# Graphs: \columnwidth, 8 pt text (set once in build()), area legends for the bar charts.

def bars(ylabel, symbolic, series, ymax=100, bar_width=3.6, nodes=False, enlarge=0.07, height=3.4):
    """Grouped bar chart. series: [(legend, colour, [values])]."""
    out = [r"\begin{tikzpicture}\begin{axis}[ybar, bar width=%.1fpt, scale only axis, width=7.0cm," % bar_width,
           r"  height=%.1fcm, ymin=0, ymax=%s, ylabel={%s}, symbolic x coords={%s}, xtick=data,"
           % (height, ymax, ylabel, ",".join(symbolic)),
           r"  ymajorgrids, grid style={gray!25}, enlarge x limits=%.2f, area legend," % enlarge,
           r"  legend style={at={(0.5,1.02)}, anchor=south, legend columns=-1, draw=none,",
           r"    /tikz/every even column/.append style={column sep=6pt}},",
           r"  axis line style={edge}, tick style={edge}, major tick length=2pt"
           + (r", nodes near coords, nodes near coords style={font=\fontsize{7}{7}\selectfont}" if nodes else "")
           + "]"]
    for name, colour, vals in series:
        coords = " ".join(f"({x},{v})" for x, v in zip(symbolic, vals))
        out.append(rf"\addplot[fill={colour}, draw=edge, line width=0.3pt] coordinates {{{coords}}};")
        out.append(rf"\addlegendentry{{{name}}}")
    out.append(r"\end{axis}\end{tikzpicture}")
    return "\n".join(out)


def tb_bars():
    # 4-man pawnless tables, White to move, % won (RESULTS.md section 2; SPEC fact sheet "Tablebases")
    return bars(r"positions won by White (\%)", ["KQK", "KRK", "KBBK", "KBNK", "KNNK", "KRBK", "KRRK", "KQRK"],
                [("plane", "edge!45", [100, 100, 99.98, 99.51, 0.0107, 100, 100, 100]),
                 ("cylinder", "dark", [100, 2.80, 100, 0.0245, 0.0077, 99.74, 100, 100]),
                 ("torus", "blue2", [0, 0, 0, 0, 0, 0.0218, 100, 100])])


def kpk_bars():
    # KPK, % of legal positions won by White (two solvers; SPEC fact sheet "KPK")
    return bars(r"positions won by White (\%)", ["White to move", "Black to move"],
                [("plane", "edge!45", [76.51, 58.09]), ("cylinder", "dark", [78.89, 55.88])],
                bar_width=22, nodes=True, enlarge=0.4, height=3.0)


def star2_by_pawns():
    # *2 positions under the count rule with the e.p.-aware passed test, flat boards of width <= 4
    # (atlas/flat8/rerun census for <= 6 pawns; research/star2_frontier scope (b) for 7 and 8 pawns,
    # each hit re-checked with cylcgt in delegate/checks/star2_caware_check.out)
    counts = {4: 0, 5: 0, 6: 0, 7: 2, 8: 4}
    coords = " ".join(f"({k},{v})" for k, v in counts.items())
    return "\n".join([
        r"\begin{tikzpicture}\begin{axis}[ybar, bar width=14pt, scale only axis, width=7.0cm, height=2.8cm,",
        r"  ymin=0, ymax=5, xtick={4,5,6,7,8}, ytick={0,1,...,5}, xlabel={number of pawns},",
        r"  ylabel={positions of value $\star2$}, ymajorgrids, grid style={gray!25}, axis line style={edge},",
        r"  tick style={edge}, major tick length=2pt, nodes near coords,",
        r"  nodes near coords style={font=\fontsize{7}{7}\selectfont}]",
        rf"\addplot[fill=dark, draw=edge, line width=0.3pt] coordinates {{{coords}}};",
        r"\end{axis}\end{tikzpicture}"])


def dawson_grundy():
    from dawson.octal import grundy
    g = grundy("0.137", 120)
    pts = " ".join(f"({n},{g[n]})" for n in range(len(g)))
    ring = " ".join(f"({m},0)" for m in range(len(g)) if g[m] == 0)
    return "\n".join([
        r"\begin{tikzpicture}\begin{axis}[scale only axis, width=16.0cm, height=2.0cm, xmin=-1, xmax=121,",
        r"  ymin=-0.5, ymax=9.5, xlabel={strip length $n$}, ylabel={Grundy value $g(n)$}, ytick={0,2,...,8},",
        r"  xtick={0,10,...,120}, ymajorgrids, grid style={gray!25}, axis line style={edge}, tick style={edge},",
        r"  major tick length=2pt,",
        r"  legend style={at={(0.5,1.03)}, anchor=south, legend columns=-1, draw=none,",
        r"    /tikz/every even column/.append style={column sep=10pt}}]",
        rf"\addplot[ycomb, dark, line width=1.3pt] coordinates {{{pts}}};",
        r"\addlegendentry{$g(n)$ for the ordinary $3\times n$ board}",
        rf"\addplot[only marks, mark=*, mark size=1.3pt, red!70!black] coordinates {{{ring}}};",
        r"\addlegendentry{$g(m)=0$: the $3\times(m+3)$ cylinder is a first-player win}",
        r"\end{axis}\end{tikzpicture}"])


# ---------------------------------------------------------------------------------------------
# Boards. Each entry: pieces, geometry, size, the pawn part valued by cylcgt and its expected value
# (count rule, e.p.-aware passed test, e.p. on; cgt.show notation, "+W" = a passed pawn), or None
# when the board is not a single pawn value (kings, sums, Dawson's chess).
#   geometry: "cyl" = 8x8 cylinder (a and h adjacent), "flat" = ordinary 8x8 board,
#             "cyl3"/"cyl4" = 3- or 4-file cylinder with 8 ranks.
T = TREB
BOARDS = {
    # Section III: the basic positions of the 2025 study (cylinder)
    "zero":           ("Pe4 pe5", "cyl", "small", "W: e4 / B: e5", "0"),                  # 2025 Pos. 2.1
    "zero_seam":      ("Pa4 Ph3 pa5 ph6", "cyl", "small", "W: a4 h3 / B: a5 h6", "0"),  # legal 2.2
    "one":            ("Pa4 Ph2 pa5 ph6", "cyl", "small", "W: a4 h2 / B: a5 h6", "1"),  # legal 3.1
    "two":            ("Pa5 Ph2 pa6 ph7", "cyl", "small", "W: a5 h2 / B: a6 h7", "2"),  # legal 3.2
    "star":           ("Pe4 pe6", "cyl", "small", "W: e4 / B: e6", "*"),
    "up":             ("Pe2 pe5", "cyl", "small", "W: e2 / B: e5", "↑"),              # 4.2 corrected
    "tiny1_2025":     ("Pa4 Ph2 Ph4 pa5 pa6 pa7 ph3", "cyl", "small", "W: a4 h2 h4 / B: a5 a6 a7 h3", "tiny(1)"),
    # Section IV: kings
    "trebuchet_2025": ("Kh5 Pa4 kb4 pa5", "cyl", "small", None, None),
    "trebuchet":      (T, "flat", "small", None, None),
    "kinggroup72":    ("Ke6 Pd7 kd8 pe7", "cyl", "small", None, None),
    # Section V: the 2025 puzzles (cylinder)
    "puzzle71":       ("Pa4 Pa5 Pc2 Pc3 Pf3 Pf4 Ph2 Ph3 pa7 pc5 pc6 pf7 ph6", "cyl", "small", None, None),
    "puzzle72":       ("Ke6 Pa2 Pb2 Pd7 Ph3 kd8 pa6 pb7 pe7 ph7", "cyl", "small", None, None),
    "puzzle73":       ("Kg8 Pa1 Pa5 Pc1 Pc3 Pd3 Pf7 Pg1 Ph1 kf6 pc2 pd4 pd5 pd6 pg3 pg7 ph4", "cyl", "small",
                       "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4", "+W"),
    "sum_counter":    ("Pb2 Pd4 Pg3 Ph5 pa7 pc7 pf7 pg4", "cyl", "small", None, None),
    # Section II: the e.p.-aware passed test
    "ep_test":        ("Pa2 pb4", "flat", "small", "W: a2 / B: b4", "0"),
    # Section VI: atlases
    "elkies_dup":     ("Pa2 pa6", "flat", "small", "W: a2 / B: a6", "⇑*"),
    "hot3":           ("Pa2 Pb4 pa5 pb7", "flat", "small", "W: a2 b4 / B: a5 b7", "±3"),
    "ring3_threequarters": ("Pa2 Pb4 pb7 pc6", "cyl3", "small", "W: a2 b4 / B: b7 c6", "3/4"),
    "ring3_quarter":  ("Pa2 Pb2 pc5 pc6", "cyl3", "small", "W: a2 b2 / B: c5 c6", "1/4±1/4"),
    "ring4":          ("Pa2 Pc2 pb7 pd7", "cyl4", "small", "W: a2 c2 / B: b7 d7", "{2±1 | -2±1}"),
    # Section VII: Elkies' small values (ordinary board, beside the trébuchet)
    "eighth":         ("Pa2 Pb2 Pb3 pa5 pa6 pb6 " + T, "flat", "small", "W: a2 b2 b3 / B: a5 a6 b6", "1/8"),
    "upsecstar":      ("Pa2 Pb2 Pb6 pa6 pb7 pc5 " + T, "flat", "small", "W: a2 b2 b6 / B: a6 b7 c5", "{0, * | ↓}"),
    "tiny1":          ("Pa2 Pb2 Pb6 pa6 pb7 pc6 " + T, "flat", "small", "W: a2 b2 b6 / B: a6 b7 c6", "tiny(1)"),
    # Section VIII: the *2 question
    "star2_textbook": ("Pa2 Pc2 pb7 pd7 " + T, "flat", "small", "W: a2 c2 / B: b7 d7", "{2±1 | -2±1}"),
    "star2_seven_a":  ("Pa4 Pb3 Pd2 Pd3 pa7 pb7 pc5 " + T, "flat", "small", "W: a4 b3 d2 d3 / B: a7 b7 c5", "*2"),
    "star2_seven_b":  ("Pb4 Pc2 Pd2 pa6 pa7 pc6 pd5 " + T, "flat", "small", "W: b4 c2 d2 / B: a6 a7 c6 d5", "*2"),
    "star2_eight_five": ("Pa3 Pb3 Pc2 Pe2 pa6 pc5 pd5 pe3 " + T, "flat", "small",
                         "W: a3 b3 c2 e2 / B: a6 c5 d5 e3", "*2"),
    # Section IX: the open end position of the 1/8 certification
    "eighth_open":    ("Pb2 Pb5 pa5 pb4 " + T, "flat", "small", "W: b2 b5 / B: a5 b4", "+W"),
    # Section X: the KPK rook pawn, a cylinder win
    "kpk_rookpawn":   ("Ka6 Pa5 ka8", "cyl", "small", None, None),
}
GEOM = {"cyl": (8, True), "flat": (8, False), "cyl3": (3, True), "cyl4": (4, True)}

FIGURES = {name: (lambda e=e: board(e[0], e[2], files=GEOM[e[1]][0])) for name, e in BOARDS.items()}
FIGURES.update({
    "ep_test": lambda: board(BOARDS["ep_test"][0], "small", arrows=[("a2", "a4")]),  # the double step
    "dawson_strip": lambda: dawson_strip(6, ring=False),
    "dawson_ring": lambda: dawson_strip(6, ring=True),
    "tb_bars": tb_bars,
    "kpk_bars": kpk_bars,
    "star2_by_pawns": star2_by_pawns,
    "dawson_grundy": dawson_grundy,
})
GRAPHS = {"tb_bars", "kpk_bars", "star2_by_pawns", "dawson_grundy"}


def build(name):
    os.makedirs(SRC, exist_ok=True)
    if name == "cover":
        shutil.copyfile(os.path.join(ROOT, "prior_work", "Pictures", "CoverPic.png"), os.path.join(HERE, "CoverPic.png"))
        print("figures/CoverPic.png")
        return
    body = FIGURES[name]()
    if name in GRAPHS:
        body = r"\fontsize{8}{9.6}\selectfont" + "\n" + body
    path = os.path.join(SRC, f"{name}.tex")
    with open(path, "w") as fh:
        fh.write(PREAMBLE + body + "\n\\end{document}\n")
    r = subprocess.run(["tectonic", "-X", "compile", "--outdir", HERE, path], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"{name}: tectonic failed\n{r.stderr[-1500:]}")
    print(f"figures/{name}.pdf")


# ---------------------------------------------------------------------------------------------
# --check: re-verify the boards

def legality(pieces, files, wrap):
    """Chess legality of a diagram: no pawn on rank 1 or 8, kings not adjacent (across the seam on a
    cylinder), not both kings in check. Returns (ok, text)."""
    at = {_sq(t[1:]): t[0] for t in pieces.split()}
    bad = [FILES[f] + str(r + 1) for (f, r), p in at.items() if p in "Pp" and r in (0, 7)]
    if bad:
        return False, "pawn on rank 1/8: " + " ".join(sorted(bad))
    kings = {p: fr for fr, p in at.items() if p in "Kk"}
    if not kings:
        return True, "legal pawn placement (no kings)"

    def nb(f, d):
        g = f + d
        return g % files if wrap else (g if 0 <= g < files else None)

    if len(kings) == 2:
        (wf, wr), (bf, br) = kings["K"], kings["k"]
        df = abs(wf - bf)
        df = min(df, files - df) if wrap else df
        if max(df, abs(wr - br)) <= 1:
            return False, "kings adjacent"
    checked = []
    for k, (f, r) in kings.items():
        enemy, dr = ("p", 1) if k == "K" else ("P", -1)
        if any(at.get((nb(f, d), r + dr)) == enemy for d in (-1, 1) if nb(f, d) is not None):
            checked.append("White" if k == "K" else "Black")
    if len(checked) == 2:
        return False, "both kings in check"
    if checked:
        return True, f"legal, {checked[0]} in check (so {checked[0]} to move)"
    return True, "legal, neither king in check (either side to move)"


def check():
    from cylcgt import pawns, cgt
    pawns.RACE_RULE, pawns.PASSED_RESPECTS_EP = "count", True
    pawns._value.cache_clear()
    fails = 0
    for name, (pieces, geom, size, part, expect) in BOARDS.items():
        files, wrap = GEOM[geom]
        ok, text = legality(pieces, files, wrap)
        line = f"{name:20s} {geom:5s} {text}"
        if part:
            got = cgt.show(pawns.value(pawns.Board(files, 8, wrap, True), pawns.Pos.parse(part)))
            line += f" | {part} = {got}" + ("" if got == expect else f"  MISMATCH (expected {expect})")
            fails += got != expect
        print(line)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        check()
    for name in sys.argv[1:] or [*FIGURES, "cover"]:
        build(name)
