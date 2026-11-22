"""F3: agreement of the model with real chess, Wilson 95% intervals computed here.  Run from repo root:
    .venv/bin/python research/figures_2026_11/f3_model_vs_chess.py
Sources: research/flat_xtarget_census/REPORT.md table 2 (e.p.-aware passer test, 2049 decisive positions):
  count 1896, mover 1701, opponent 1714.   research/agreement_census/REPORT.md headline table (Q, cap 2):
  cyl:6x6 13/26, flat:5x6 23/26, cyl:5x5 (compact layout) 49/71."""
import sys, os
from math import sqrt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import build

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * p, 100 * (c - h), 100 * (c + h)

rows = [  # (label, k, n, fill)
    (r"count rule", 1896, 2049, "dark"),
    (r"mover rule", 1701, 2049, "blue2"),
    (r"opponent rule", 1714, 2049, "blue2"),
    (r"cylinder $6{\times}6$", 13, 26, "white"),
    (r"flat $5{\times}6$", 23, 26, "white"),
    (r"cylinder $5{\times}5$", 49, 71, "white"),
]
ys = [7, 6, 5, 3, 2, 1]
bars, errs, ylab, pct = [], [], [], []
for (lab, k, n, fill), y in zip(rows, ys):
    p, lo, hi = wilson(k, n)
    print("%-22s %d/%d  %.1f%% [%.1f, %.1f]" % (lab, k, n, p, lo, hi))
    bars.append(r"\fill[%s, draw=edge, line width=0.5pt] (axis cs:0,%.2f) rectangle (axis cs:%.2f,%.2f);" % (fill, y - 0.3, p, y + 0.3))
    errs.append(r"\draw[edge, line width=0.8pt] (axis cs:%.2f,%d) -- (axis cs:%.2f,%d) (axis cs:%.2f,%.2f) -- (axis cs:%.2f,%.2f) (axis cs:%.2f,%.2f) -- (axis cs:%.2f,%.2f);\fill[black] (axis cs:%.2f,%d) circle (1.6pt);" % (lo, y, hi, y, lo, y - 0.18, lo, y + 0.18, hi, y - 0.18, hi, y + 0.18, p, y))
    ylab.append(r"\node[anchor=east, align=right, font=\fontsize{8}{8.6}\selectfont] at (axis cs:-3,%d) {%s\\{\color{black!70}%d/%d}};" % (y, lab, k, n))
    pct.append(r"\node[anchor=west, font=\fontsize{8}{8}\selectfont] at (axis cs:101,%d) {%.1f\%%};" % (y, p))
barlines = "\n".join(bars)
body = r"""
\begin{tikzpicture}\begin{axis}[scale only axis, width=3.6cm, height=5.4cm, xmin=0, xmax=100, ymin=0.3, ymax=8.4,
  xtick={0,25,50,75,100}, ytick=\empty, xlabel={agreement with real chess (\%%)}, xmajorgrids, grid style={gray!25},
  axis line style={edge}, tick style={edge}, major tick length=2pt, clip=false,
  every axis label/.append style={font=\fontsize{8}{9.6}\selectfont}]
%s
%s
%s
%s
\node[anchor=west, fill=white, inner sep=1pt, font=\itshape\fontsize{8}{8}\selectfont] at (axis cs:2,7.85) {flat $8{\times}8$ with trébuchet};
\node[anchor=west, fill=white, inner sep=1pt, font=\itshape\fontsize{8}{8}\selectfont] at (axis cs:2,3.85) {small boards (exact solver)};
\end{axis}\end{tikzpicture}
""" % (barlines, "\n".join(errs), "\n".join(ylab), "\n".join(pct))
build("f3_model_vs_chess", body)
